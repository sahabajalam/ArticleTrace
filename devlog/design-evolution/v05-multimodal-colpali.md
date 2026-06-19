---
version: "05"
title: Multimodal retrieval via ColPali — design + scaffolding
status: proposal
derives_from: v03-kb-completion.md
proposed_date: 2026-06-19
decided_date: null
implemented_in:
  - null
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - knowledge_engine/src/multimodal/                # scaffolding (compiles, doesn't run)
  - knowledge_engine/src/retrieval/engine.py         # the RRF arm this would plug into
  - 01_AlloyCode.md §4.2                             # original Phase-3 plan
  - 07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md §6.1        # audit-flagged gap
ai_guidance: |
  This is a PROPOSAL with scaffolding in repo. The module imports cleanly
  and the interface is fixed, but `colpali-engine` is not in dependencies,
  no PDFs are in repo, and no MaxSim run has been benchmarked. Treat as
  "design ready, integration not done." Only flip to `implemented` when
  the §Acceptance criteria below are all green.

  If asked about ColPali in an interview, the defensible answer is:
  "designed and scaffolded, not deployed — gated on GPU availability + the
  10-question multimodal benchmark; the production text path already hits
  81.8% citation recall@15 without it." Don't overclaim ColPali as live.
---

## 0. What this document is

A design record for adding **ColPali multimodal retrieval** as a third arm
alongside the existing graph traversal + vector search paths in
`RetrievalEngine`. Targets the layout-heavy / table-heavy content in EU AI
Act + GDPR official PDFs that text-only embedding misses.

Code scaffolding lives in [`knowledge_engine/src/multimodal/`](../../knowledge_engine/src/multimodal/):
- [`colpali_indexer.py`](../../knowledge_engine/src/multimodal/colpali_indexer.py) — PDF → page images → multi-vector embeddings → `:Page` nodes
- [`multimodal_retrieval.py`](../../knowledge_engine/src/multimodal/multimodal_retrieval.py) — query → MaxSim scoring → top-K pages

**This is not yet built.** `colpali-engine` is gated behind a runtime
import; running the indexer raises `RuntimeError("colpali-engine not
installed")` until you do `pip install colpali-engine pdf2image pillow`
plus install poppler.

---

## Status

- **State:** proposal (scaffolded)
- **Decision date:** null
- **Implementation:** scaffolding only — see source_of_truth files
- **Supersedes:** none
- **Superseded by:** none

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | **Stay text-only** (current state) | Already at 81.8% citation recall@15 hybrid (n=25, [METRICS.md](../METRICS.md)). Multimodal is a *known* gap on layout-heavy content (Annex tables, fee schedules, scope diagrams) — not solving it leaves real content un-retrievable. |
| 2 | **Layout-aware OCR + text-RAG** (e.g., LayoutLMv3, Donut) | Two-stage pipeline introduces an OCR error budget that compounds with embedding error. Late-interaction multi-vector models like ColPali skip the OCR step entirely — image patches go straight to embeddings. |
| 3 | **CLIP-style single-vector** image embeddings | CLIP collapses each page to one ~512-dim vector. Loses the per-region structure that lets MaxSim find the *table cell* matching the query rather than the *whole page*. Tested in research literature — ColPali beats CLIP by ~20pp nDCG@5 on document retrieval. |
| 4 | **JinaAI v3 or Cohere Embed Multimodal** (closed-source) | Vendor lock-in + no on-prem inference path. ColPali is Apache 2.0; can run on the same Cloud Run instance long-term. |

## Consequences

What shipping this proposal would do:

- ✅ Unlocks retrieval over the layout-heavy content currently invisible to text-only embedding (Annex III enumeration tables, AI Act Article-by-Article numbering tables, GDPR fee schedules).
- ✅ Adds a defensible interview answer to "how do you handle visual content in regulatory PDFs?" — currently we don't.
- ✅ Closes one of the two open eval gaps the audit named ([NORTHSTAR](../NORTHSTAR.md) Part III + [01_AlloyCode.md §4.2](../../01_AlloyCode.md)).
- ⚠️ Adds ~5 GB of model weights (ColPali v1.3) — needs Cloud Run instance memory tier upgrade or a separate GPU service. Current Cloud Run config is CPU-only.
- ⚠️ Adds poppler as a system dep — Dockerfile change.
- ⚠️ MaxSim is O(|q| × |d|) per page; for ~100 candidate pages × ~32 query tokens × ~1024 page tokens = ~3M cosine ops per query. CPU-bound. On GPU it's a single matmul.
- ❌ Rules out staying on the current minimal-dep `knowledge_engine` `pyproject.toml` (would need `torch`, `transformers`, `pdf2image`, `pillow`, `colpali-engine`). Reverses the "no langchain bloat" stance.

---

## 1. Schema additions

Three new node types and one edge type in Neo4j:

```cypher
// PDF document
(:Document {id, regulation, source_url, sha1, ingested_at})

// One image per PDF page
(:Page {
  id: "PAGE:<doc_id>:<page_number>",
  doc_id,
  page_number,
  vectors: [[float; 128]; ~1024],   // multi-vector ColPali embedding
  image_hash: sha1 of rendered image
})

// Link pages back to existing :Article so retrieval can return article citations
(:Article)-[:HAS_PAGE]->(:Page)
(:Document)-[:HAS_PAGE]->(:Page)
```

The multi-vector `vectors` property is the only big-storage item: ~1024 tokens × 128 dims × 4 bytes = ~500 KB per page. For ~600 pages across both regulations that's ~300 MB — fits in Aura Pro tier, exceeds Aura Free's 200 MB.

**Note on storage:** Aura Free (current tier) doesn't have headroom for the multi-vector embeddings. ColPali deployment is gated on a tier upgrade or a sidecar Postgres+pgvector instance for the page embeddings.

---

## 2. Indexing pipeline

```
EU_AI_ACT_OFFICIAL.pdf
    ↓ pdf2image (needs poppler)
[PIL.Image for each page]
    ↓ ColPaliProcessor.process_images()
[token-patch tensors]
    ↓ ColPali forward pass (GPU/CPU)
[multi-vector embeddings]
    ↓ ColPaliIndexer.index_pdf() → neo4j_writer
:Page nodes in Neo4j
```

Estimated indexing wall-clock:
- GPU (T4): ~2 sec per page → ~10 min for 600 pages
- CPU (Cloud Run): ~30 sec per page → ~5 hours for 600 pages

Run as one-time batch job on a GPU box; persist to Neo4j; subsequent queries are inference-only on the *query* side.

---

## 3. Query-time integration

`RetrievalEngine.query()` currently has two arms: vector + graph. Adding multimodal as a third arm changes the signature:

```python
def query(self, question: str, top_k=15, include_multimodal=False, ...):
    q_embedding = self._embed_query(question)
    vector_results = self._vector_search(q_embedding, ...)
    graph_results = self._graph_traverse(seed_ids=vector_results[:5], ...)

    if include_multimodal and self.multimodal is not None:
        mm_results = self.multimodal.retrieve(question, top_k=top_k)
        return self._rrf_fusion_3way(vector_results, graph_results, mm_results)
    return self._rrf_fusion(vector_results, graph_results)
```

The flag-guarded path means multimodal can be enabled per-deployment without affecting the text-only path.

---

## 4. Acceptance criteria (flip to `implemented` when ALL green)

- [ ] `colpali-engine` in `pyproject.toml` dependencies; venv installs cleanly on Python 3.13
- [ ] 5 official PDFs ingested (EU AI Act + GDPR + at least one Annex-heavy doc)
- [ ] `:Page` nodes present in Neo4j; HAS_PAGE edges to relevant articles
- [ ] **10-question multimodal benchmark** authored — queries that text-only retrieval fails on:
  - "What's the fine ceiling for Tier 2 GDPR breaches according to the table in Article 83?"
  - "Which Annex III categories require a fundamental rights impact assessment?"
  - "What's the conformity assessment route for high-risk AI not covered by Annex I?"
  - …7 more in similar style
- [ ] Comparison table in [METRICS.md](../METRICS.md) §6: text-only vs ColPali vs hybrid on the 10-question multimodal slice
- [ ] **Target: ColPali beats text-only by ≥15pp** on the multimodal slice. If it doesn't, the proposal stays `proposal` and the design needs a rethink (the existing scaffolding still serves as documentation of the attempt).

---

## 5. Why this is scaffolding-only and not built

Per [NORTHSTAR](../NORTHSTAR.md) Part I:

> A suggestion only earns time if it does one of three things: (1) defensibility, (2) production metric, (3) live demo.

ColPali doesn't move any of the three tracks. The current 81.8% citation recall@15 ([METRICS.md](../METRICS.md)) already passes the production-metric gate, and the live demo is up. Adding ColPali is a **breadth** move (new capability) rather than a **depth** move (better defence of what exists) — and the audit explicitly puts depth above breadth.

The scaffolding earns its place because:
- It documents the design without committing to the build (defensibility — "I know what ColPali is, here's the wiring, here's why I haven't built it").
- It survives interview challenges on "have you considered multimodal?" without overclaiming a shipped feature.
- It gives the next session a concrete starting point if a user surfaces a real multimodal need.

When to actually build:
- A deployed user reports they're losing content to layout-heavy PDFs (real signal), OR
- A target employer specifically requires multimodal RAG in JDs and the keyword is screen-blocking (market signal), OR
- The text-only path's recall stalls and the failure modes are dominated by layout-heavy retrieval misses (eval signal).

Until one of those fires, the design is correctly-deferred.
