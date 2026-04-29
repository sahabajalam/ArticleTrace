"""Graph RAG Retrieval Engine.

Fuses two retrieval paths:
  1. Graph traversal (Neo4j): Multi-hop from seed entities
  2. Vector search (embeddings): Semantic similarity across collections

Fusion: Reciprocal Rank Fusion (RRF) with configurable k parameter.

Query flow:
  query -> embed -> vector_search (top-k per collection)
                 -> graph_traverse (seed nodes + N hops)
        -> RRF merge -> ranked results
"""

from __future__ import annotations

import time
from typing import Any

from google import genai
from google.genai import types as genai_types

from src.stores.graph_store import GraphStore


class RetrievalEngine:
    """Hybrid Graph + Vector retrieval with RRF fusion.

    Vectors live on :Entity nodes (`embedding` property, single vector index).
    Both retrieval paths now go through `graph_store`.
    """

    def __init__(
        self,
        graph_store: GraphStore,
        genai_client: genai.Client,
        embedding_model: str = "gemini-embedding-001",
        rrf_k: int = 60,
        default_top_k: int = 10,
        max_hops: int = 3,
    ):
        self.graph = graph_store
        self.genai = genai_client
        self.embedding_model = embedding_model
        self.rrf_k = rrf_k
        self.default_top_k = default_top_k
        self.max_hops = max_hops

    def query(
        self,
        question: str,
        top_k: int | None = None,
        collections: list[str] | None = None,
        regulation_filter: str | None = None,
        max_hops: int | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a hybrid retrieval query.

        Args:
            question: Natural language query
            top_k: Number of results to return
            collections: Vector collections to search (default: all)
            regulation_filter: Filter to "GDPR" or "EU_AI_ACT"
            max_hops: Graph traversal depth

        Returns:
            Ranked list of result dicts with entity data and scores.
        """
        top_k = top_k or self.default_top_k
        max_hops = max_hops or self.max_hops
        collections = collections or GraphStore.VECTOR_COLLECTIONS

        # Step 1: Embed the query
        query_embedding = self._embed_query(question)

        # Step 2: Vector search across collections
        vector_results = self._vector_search(
            query_embedding, collections, top_k * 2, regulation_filter
        )

        # Step 3: Graph traversal from vector seed nodes
        graph_results = self._graph_traverse(
            seed_ids=[r["entity_id"] for r in vector_results[:5]],
            max_hops=max_hops,
        )

        # Step 4: RRF fusion
        fused = self._rrf_fusion(vector_results, graph_results)

        # Step 5: Return top-k
        return fused[:top_k]

    def _embed_query(self, text: str) -> list[float]:
        """Embed query text using Gemini."""
        result = self.genai.models.embed_content(
            model=self.embedding_model,
            contents=[text],
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
            ),
        )
        return result.embeddings[0].values

    def _vector_search(
        self,
        query_embedding: list[float],
        collections: list[str],
        n_results: int,
        regulation_filter: str | None,
    ) -> list[dict[str, Any]]:
        """Search the Neo4j vector index, filtered to the given collections."""
        results = self.graph.vector_search(
            query_embedding=query_embedding,
            n_results=n_results,
            collections=collections,
            regulation_filter=regulation_filter,
        )
        # Tag source for downstream RRF merge.
        for r in results:
            r["source"] = "vector"
        return results

    def _graph_traverse(
        self, seed_ids: list[str], max_hops: int
    ) -> list[dict[str, Any]]:
        """Traverse graph from seed nodes."""
        results: list[dict[str, Any]] = []
        seen: set[str] = set()

        for seed_id in seed_ids:
            try:
                paths = self.graph.traverse(
                    start_id=seed_id,
                    max_hops=max_hops,
                )
            except Exception:
                continue

            # Extract unique nodes from all paths with hop depth
            for path in paths:
                nodes = path.get("nodes", [])
                for depth, node_data in enumerate(nodes):
                    if not isinstance(node_data, dict):
                        continue
                    node_id = node_data.get("id", "")
                    if not node_id or node_id in seen:
                        continue
                    seen.add(node_id)

                    # Score decays with hop distance
                    score = 1.0 / (1 + depth)

                    results.append({
                        "entity_id": node_id,
                        "node_data": node_data,
                        "hop_depth": depth,
                        "graph_score": score,
                        "seed_id": seed_id,
                        "source": "graph",
                    })

        # Sort by graph score
        results.sort(key=lambda x: x["graph_score"], reverse=True)
        return results

    def _rrf_fusion(
        self,
        vector_results: list[dict[str, Any]],
        graph_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Reciprocal Rank Fusion of vector and graph results.

        RRF score = sum(1 / (k + rank_i)) for each result list
        """
        k = self.rrf_k
        scores: dict[str, float] = {}
        result_data: dict[str, dict] = {}

        # Vector rankings
        for rank, r in enumerate(vector_results):
            eid = r["entity_id"]
            scores[eid] = scores.get(eid, 0) + 1.0 / (k + rank + 1)
            if eid not in result_data:
                result_data[eid] = {
                    "entity_id": eid,
                    "sources": [],
                    "metadata": r.get("metadata", {}),
                    "document": r.get("document", ""),
                }
            result_data[eid]["sources"].append("vector")
            result_data[eid]["vector_similarity"] = r.get("similarity", 0)
            result_data[eid]["vector_rank"] = rank + 1

        # Graph rankings
        for rank, r in enumerate(graph_results):
            eid = r["entity_id"]
            scores[eid] = scores.get(eid, 0) + 1.0 / (k + rank + 1)
            if eid not in result_data:
                result_data[eid] = {
                    "entity_id": eid,
                    "sources": [],
                    "metadata": r.get("node_data", {}),
                    "document": "",
                }
            result_data[eid]["sources"].append("graph")
            result_data[eid]["graph_score"] = r.get("graph_score", 0)
            result_data[eid]["hop_depth"] = r.get("hop_depth", 0)
            result_data[eid]["graph_rank"] = rank + 1

        # Build final ranked list
        ranked = []
        for eid, rrf_score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            entry = result_data[eid]
            entry["rrf_score"] = rrf_score
            entry["in_both"] = "vector" in entry["sources"] and "graph" in entry["sources"]
            ranked.append(entry)

        return ranked
