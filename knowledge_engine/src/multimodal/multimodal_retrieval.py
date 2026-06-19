"""Multimodal retrieval — MaxSim scoring over ColPali page-image embeddings.

SCAFFOLDING ONLY. Integrates with the existing RRF fusion in
`src/retrieval/engine.py` as a third arm alongside vector + graph.

MaxSim scoring (from the ColPali paper):
    score(q, d) = Σᵢ max_j sim(q_i, d_j)

For each query token q_i, find the best-matching document token d_j by
cosine similarity, then sum those maxima over all query tokens. Captures
late interaction between query and document — significantly stronger than
single-vector cosine for layout-heavy / table-heavy documents.
"""

from __future__ import annotations

from typing import Any

# Multi-vector cosine similarity helpers ------------------------------------


def _cosine(a: list[float], b: list[float]) -> float:
    import math
    num = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return num / (na * nb)


def maxsim(
    query_vectors: list[list[float]],
    doc_vectors: list[list[float]],
) -> float:
    """MaxSim: sum over q_i of max over d_j of cosine(q_i, d_j).

    O(|q| * |d|) — for ColPali typical sizes ~32 * ~1024 = 32k ops per page.
    Acceptable for ~100 candidate pages; if scaling to thousands, swap to
    a GPU matmul or a learned compressor.
    """
    total = 0.0
    for q in query_vectors:
        best = 0.0
        for d in doc_vectors:
            sim = _cosine(q, d)
            if sim > best:
                best = sim
        total += best
    return total


class MultimodalRetriever:
    """Vector-style retrieval against :Page nodes holding ColPali embeddings.

    Expected Neo4j schema (added at index time by ColPaliIndexer):
        (:Page {doc_id, page_number, vectors, image_hash})
        (:Article)-[:HAS_PAGE]->(:Page)

    Query path:
        1. Embed query via ColPali query encoder (caller provides client)
        2. For each candidate page (pre-filtered by doc_id), compute MaxSim
        3. Return top-K pages by score
        4. Caller can join back to articles via :HAS_PAGE for citation
    """

    def __init__(self, graph_store, colpali_query_encoder):
        self.graph = graph_store
        self.encoder = colpali_query_encoder

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        doc_id_filter: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Run multimodal retrieval. Returns hits in the same dict shape as
        the vector path so RRF fusion can treat all three arms uniformly.
        """
        # 1. Query embedding
        q_vectors = self.encoder.encode_query(query)

        # 2. Fetch candidate pages
        candidates = self._fetch_candidates(doc_id_filter)

        # 3. MaxSim scoring
        scored = []
        for page in candidates:
            score = maxsim(q_vectors, page["vectors"])
            scored.append({
                "entity_id": f"PAGE:{page['doc_id']}:{page['page_number']}",
                "score": score,
                "source": "multimodal",
                "doc_id": page["doc_id"],
                "page_number": page["page_number"],
            })

        # 4. Sort and return top-K
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _fetch_candidates(self, doc_id_filter: list[str] | None) -> list[dict]:
        """Cypher: pull all :Page nodes (optionally filtered)."""
        with self.graph._driver.session() as s:
            if doc_id_filter:
                cypher = ("MATCH (p:Page) WHERE p.doc_id IN $ids "
                          "RETURN p.doc_id AS doc_id, p.page_number AS page_number, "
                          "p.vectors AS vectors")
                result = s.run(cypher, ids=doc_id_filter)
            else:
                cypher = ("MATCH (p:Page) "
                          "RETURN p.doc_id AS doc_id, p.page_number AS page_number, "
                          "p.vectors AS vectors")
                result = s.run(cypher)
            return [dict(r) for r in result]
