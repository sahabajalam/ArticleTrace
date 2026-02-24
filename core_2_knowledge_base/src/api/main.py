"""FastAPI server for the GraphRAG Legal Research Engine.

Exposes the retrieval and reasoning engines over HTTP so that
Core 3 (Compliance Agent) can call them via the Legal Research Agent.

Endpoints:
  POST /api/v1/vector/search     - Vector similarity search
  POST /api/v1/graph/traverse    - Neo4j graph traversal
  POST /api/v1/hybrid/search     - Combined RRF search
  POST /api/v1/hybrid/reason     - Multi-hop reasoning with LLM synthesis
  GET  /health                   - Health check
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from google import genai

from src.config import settings
from src.stores.graph_store import GraphStore
from src.stores.vector_store import VectorStore
from src.retrieval.engine import RetrievalEngine
from src.retrieval.reasoning_engine import ReasoningEngine
from src.retrieval.query_models import (
    ComplianceQueryRequest,
    ComplianceQueryResponse,
)

logger = logging.getLogger(__name__)

# ── Globals (initialized at startup) ─────────────────────────────────────────

graph_store: GraphStore | None = None
vector_store: VectorStore | None = None
retrieval_engine: RetrievalEngine | None = None
reasoning_engine: ReasoningEngine | None = None


# ── Request / Response models ────────────────────────────────────────────────

class VectorSearchRequest(BaseModel):
    query: str
    top_k: int = 10
    collections: list[str] | None = None
    filter_regulations: list[str] | None = None


class VectorSearchResponse(BaseModel):
    results: list[dict[str, Any]] = Field(default_factory=list)
    count: int = 0


class GraphTraverseRequest(BaseModel):
    start_entities: list[str]
    relationship_types: list[str] | None = None
    max_hops: int = 2
    limit: int = 20


class GraphTraverseResponse(BaseModel):
    paths: list[dict[str, Any]] = Field(default_factory=list)
    count: int = 0


class HybridSearchRequest(BaseModel):
    query: str
    top_k: int = 10
    regulation_filter: str | None = None
    max_hops: int | None = None


class HybridSearchResponse(BaseModel):
    results: list[dict[str, Any]] = Field(default_factory=list)
    count: int = 0


# ── Lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize stores and engines on startup, close on shutdown."""
    global graph_store, vector_store, retrieval_engine, reasoning_engine

    logger.info("Starting GraphRAG API server...")

    # Initialize Google AI client
    genai_client = genai.Client(api_key=settings.google_api_key)

    # Initialize stores
    try:
        graph_store = GraphStore(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
        )
        logger.info("Neo4j connection established")
    except Exception as e:
        logger.warning(f"Neo4j connection failed (will retry on request): {e}")
        graph_store = None

    vector_store = VectorStore(
        persist_dir=str(settings.parsed_data_dir.parent / "chroma_data")
    )
    logger.info("Vector store loaded")

    # Initialize engines
    if graph_store:
        retrieval_engine = RetrievalEngine(
            graph_store=graph_store,
            vector_store=vector_store,
            genai_client=genai_client,
            embedding_model=settings.embedding_model,
            rrf_k=settings.rrf_k,
            default_top_k=settings.default_top_k,
            max_hops=settings.max_hops,
        )

        reasoning_engine = ReasoningEngine(
            retrieval_engine=retrieval_engine,
            genai_client=genai_client,
            model=settings.llm_model,
        )
        logger.info("Retrieval and reasoning engines initialized")
    else:
        logger.warning("Engines not initialized (Neo4j unavailable)")

    yield

    # Shutdown
    if graph_store:
        graph_store.close()
        logger.info("Neo4j connection closed")


# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="GraphRAG Legal Research Engine",
    description="EU AI Act & GDPR knowledge graph with hybrid retrieval and LLM reasoning",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ───────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "GraphRAG Legal Research Engine",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    neo4j_ok = graph_store is not None
    vector_ok = vector_store is not None

    collections_count = {}
    if vector_ok:
        for coll in VectorStore.COLLECTIONS:
            collections_count[coll] = vector_store.count(coll)

    node_counts = {}
    if neo4j_ok:
        try:
            node_counts = graph_store.count_nodes()
        except Exception:
            neo4j_ok = False

    return {
        "status": "healthy" if (neo4j_ok and vector_ok) else "degraded",
        "neo4j": "connected" if neo4j_ok else "disconnected",
        "vector_store": "loaded" if vector_ok else "not loaded",
        "collections": collections_count,
        "graph_nodes": node_counts,
    }


# ── Vector Search ────────────────────────────────────────────────────────────

@app.post("/api/v1/vector/search", response_model=VectorSearchResponse)
async def vector_search(request: VectorSearchRequest):
    """Vector similarity search across legal document collections."""
    if not retrieval_engine:
        raise HTTPException(status_code=503, detail="Retrieval engine not available")

    # Embed the query
    query_embedding = retrieval_engine._embed_query(request.query)

    # Determine collections
    collections = request.collections or VectorStore.COLLECTIONS

    # Build regulation filter
    where = None
    if request.filter_regulations and len(request.filter_regulations) == 1:
        where = {"regulation_id": request.filter_regulations[0]}

    all_results: list[dict[str, Any]] = []
    for coll_name in collections:
        result = vector_store.query(
            collection_name=coll_name,
            query_embedding=query_embedding,
            n_results=request.top_k,
            where=where,
        )
        if result["ids"] and result["ids"][0]:
            for i, doc_id in enumerate(result["ids"][0]):
                distance = result["distances"][0][i] if result["distances"][0] else 1.0
                all_results.append({
                    "id": doc_id,
                    "text": result["documents"][0][i] if result["documents"][0] else "",
                    "metadata": result["metadatas"][0][i] if result["metadatas"][0] else {},
                    "score": 1.0 - distance,
                    "collection": coll_name,
                })

    # Sort by score descending, deduplicate, take top_k
    all_results.sort(key=lambda x: x["score"], reverse=True)
    seen = set()
    deduped = []
    for r in all_results:
        if r["id"] not in seen:
            seen.add(r["id"])
            deduped.append(r)

    top_results = deduped[:request.top_k]
    return VectorSearchResponse(results=top_results, count=len(top_results))


# ── Graph Traverse ───────────────────────────────────────────────────────────

@app.post("/api/v1/graph/traverse", response_model=GraphTraverseResponse)
async def graph_traverse(request: GraphTraverseRequest):
    """Multi-hop graph traversal from seed entities.

    Returns paths in the format expected by Core 3's Legal Research Agent:
    {"paths": [{"nodes": [...], "relationship": "TYPE", "weight": score}]}
    """
    if not graph_store:
        raise HTTPException(status_code=503, detail="Graph store not available")

    all_paths: list[dict[str, Any]] = []

    for entity_id in request.start_entities:
        try:
            paths = graph_store.traverse(
                start_id=entity_id,
                relationship_types=request.relationship_types,
                max_hops=request.max_hops,
            )
            # Transform to Core 3 expected format
            for path in paths:
                rels = path.get("relationships", [])
                rel_type = rels[0]["type"] if rels else "RELATED_TO"
                # Weight decays with path length
                weight = 1.0 / max(len(path.get("nodes", [])), 1)
                all_paths.append({
                    "nodes": path.get("nodes", []),
                    "relationship": rel_type,
                    "weight": round(weight, 2),
                })
        except Exception as e:
            logger.warning(f"Traversal failed for {entity_id}: {e}")
            continue

        if len(all_paths) >= request.limit:
            break

    all_paths = all_paths[:request.limit]
    return GraphTraverseResponse(paths=all_paths, count=len(all_paths))


# ── Hybrid Search ────────────────────────────────────────────────────────────

@app.post("/api/v1/hybrid/search", response_model=HybridSearchResponse)
async def hybrid_search(request: HybridSearchRequest):
    """Combined vector + graph retrieval with RRF fusion."""
    if not retrieval_engine:
        raise HTTPException(status_code=503, detail="Retrieval engine not available")

    results = retrieval_engine.query(
        question=request.query,
        top_k=request.top_k,
        regulation_filter=request.regulation_filter,
        max_hops=request.max_hops,
    )

    return HybridSearchResponse(results=results, count=len(results))


# ── Hybrid Reason ────────────────────────────────────────────────────────────

@app.post("/api/v1/hybrid/reason", response_model=ComplianceQueryResponse)
async def hybrid_reason(request: ComplianceQueryRequest):
    """Multi-hop reasoning with LLM synthesis over the knowledge graph."""
    if not reasoning_engine:
        raise HTTPException(status_code=503, detail="Reasoning engine not available")

    response = reasoning_engine.answer(request)
    return response
