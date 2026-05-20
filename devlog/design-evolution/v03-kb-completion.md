---
version: "03"
title: Knowledge base completion — from 12% to fully built
status: implemented
derives_from: v02-static-scanner-pivot.md
proposed_date: 2026-02-12
decided_date: 2026-02-12
implemented_in:
  - 2026-04-13  # docs/REFERENCE.md last-updated date (verification anchor; the work pre-dates initial git import 2ccaadc)
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md
  - gdpr context/main/03_KB_DESIGN_AND_CONSTRUCTION.md
  - gdpr context/backup/CRITICAL_GAP_ANALYSIS.md
  - gdpr context/backup/knowledge_graph_gap_analysis.md
  - gdpr context/backup/improve_v1.md
  - docs/MEMORY.md
  - docs/REFERENCE.md
  - knowledge_engine/src/stores/graph_store.py
ai_guidance: |
  This proposal SHIPPED. It captures the arc from "KB is 12% complete and
  multi-hop reasoning fails 88% of scenarios" (Feb 2026) to "KB is fully built;
  2,301 nodes, 4,423 relationships, 2,198 vector embeddings, 0 orphans"
  (April 2026). Read SYSTEM.md §2 for the current counts; this file is the
  decision record for why the in-house completion was the right call.
---

## 0. What this document is

`v03` records the decision to complete the regulatory knowledge base in-house at paragraph-level granularity, after the Feb 2026 gap analysis showed it was only ~12% loaded and that multi-hop reasoning was failing ~88% of test scenarios. The pivot to a static scanner (`v02`) reframed the KB as a "rule corpus, not Q&A bot" — but that reframe only lands if the corpus is actually complete. This proposal documents what was decided and why.

The story is also a methodology demonstration: a structured gap analysis (the Feb doc) produced a concrete remediation plan that was then executed. The result is captured in [`docs/MEMORY.md`](../history/01-research-arc.md) and [`docs/REFERENCE.md §1`](../history/01-research-arc.md). Both are now archived under `history/01-research-arc.md`.

---

## Status

- **State:** implemented.
- **Decision date:** 2026-02-12 (date on `gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`).
- **Implementation:** 2026-04-13 (`docs/REFERENCE.md` last-updated date used as the verification anchor; the build work pre-dates the initial git import `2ccaadc`).
- **Supersedes:** the data-layer claims in `v01-baseline.md §3` (KB was 12% complete) and the implicit assumption in `v02-static-scanner-pivot.md` that the rule-corpus framing has a complete corpus to back it.
- **Superseded by:** none.

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | **Ship at 12% with a "demo-only" caveat.** | Undermines the entire rule-corpus reframe from `v02`. If half the detection rules can't cite a complete obligation chain, the differentiator collapses. Multi-hop reasoning fails ~88% — the failure rate is too visible. |
| 2 | **Outsource the KB to a third-party corpus.** | No third party has the EU AI Act + GDPR at paragraph granularity with cross-regulation edges. Existing legal-tech vendors target lawyers (full-text search), not compliance engineers (structured obligations). Building the in-house schema was already the differentiator. |
| 3 | **Stay at article-level granularity (not paragraph-level).** | Articles have exceptions, conditions, sub-clauses. Vector search at article level retrieves the right article but can't pinpoint *which paragraph* of GDPR Art 6 a finding maps to. Hallucinations on legal exceptions are the worst failure mode — they produce confidently wrong compliance advice. |
| 4 | **Complete the KB in-house at paragraph granularity, dual rule-based + LLM-assisted extraction.** ✅ | The only option that preserves the differentiator. Rule-based extraction handles definitions (deterministic). LLM-assisted extraction handles obligations (requires interpreting "shall," "must," "must not," "does not apply where"). Source verification is mandatory — every extracted obligation must cite a verbatim quote. |

## Consequences

- ✅ **Multi-hop reasoning becomes viable.** The 88%-failure scenarios from the Feb gap analysis pass after completion. The hybrid `RRF` engine in [`knowledge_engine/src/retrieval/engine.py`](../../knowledge_engine/src/retrieval/engine.py) has enough graph to traverse.
- ✅ **The `v02` "rule corpus" reframe lands.** Detection rules can now reference complete obligation chains (Article → Obligation → Recital → Cross-regulation edge → another Article).
- ✅ **Paragraph-level retrieval reduces hallucination.** Findings map to specific paragraphs, not whole articles. Confidence scores reflect actual semantic match, not article-level approximation.
- ✅ **Cross-regulation edges enable real legal reasoning.** 84 `COMPLEMENTS` edges spanning 5 interaction types let queries traverse from "facial recognition" → "biometric data" (GDPR Art 9) → "remote biometric ID" (AI Act Art 10) without manual join logic.
- ⚠️ **Ongoing maintenance cost.** EDPB guidelines update, CJEU cases land, the EU AI Act has phased effective dates. Without a refresh pipeline, the corpus will drift. (Not solved by this proposal — a candidate `v04` topic.)
- ⚠️ **Schema rigidity is a future constraint.** The current schema (`:Article` → CONTAINS → `:Paragraph` → CONTAINS → `:Clause`) is good for retrieval precision but not for modeling Conditions and Exceptions as first-class nodes (a gap flagged in `gdpr context/backup/improve_v1.md`). Conditions are currently stored as properties on Obligations; promoting them to nodes is open future work.
- ⚠️ **3072-dim embeddings are expensive.** `gemini-embedding-001` at 3072 dim, 2,198 vector documents = ~6.75 MB embedding payload, non-trivial cold-start time on Cloud Run. The choice trades cost for retrieval quality.

---

## 1. Final corpus state (verified)

From [`docs/MEMORY.md`](../history/01-research-arc.md) and [`docs/REFERENCE.md §1.1`](../history/01-research-arc.md), cross-verified against [`knowledge_engine/src/stores/graph_store.py`](../../knowledge_engine/src/stores/graph_store.py):

| Metric | Value | Source |
|---|---|---|
| Total nodes | 2,301 | Cypher: `MATCH (n) RETURN count(n)` |
| Total relationships | 4,423 (one source says 4,431 — discrepancy noted; verify) | Cypher: `MATCH ()-[r]->() RETURN count(r)` |
| Entity types | 17 | `EntityType` enum in `knowledge_engine/src/schema/entities.py` |
| Relationship types | 13 | `RelationshipType` enum in `knowledge_engine/src/schema/relationships.py` |
| Vector documents | 2,198 | `MATCH (n:Entity) WHERE n.embedding IS NOT NULL RETURN count(n)` |
| Vector dimensions | 3,072 | `GraphStore.VECTOR_DIMENSIONS` |
| Vector collections | 7 | `articles`, `recitals`, `interpretive`, `definitions`, `obligations`, `concepts`, `rights` |
| Cross-regulation edges | 84 `COMPLEMENTS` edges (5 interaction types) | gap-analysis-resolution doc |
| Orphan nodes | 0 (100% connectivity) | gap-analysis-resolution doc |
| Avg relationships per article | 19.1 | gap-analysis-resolution doc |

## 2. Decisions documented during the build

From `gdpr context/main/03_KB_DESIGN_AND_CONSTRUCTION.md`:

- **Neo4j-native vector index over a separate vector store.** One index (`entity_embedding`) covers all 7 collections; queries filter by `n.collection`. Eliminates the dual-store sync problem that earlier Chroma+Neo4j setups had.
- **Paragraph-level chunking with article-level rollup.** Embed at paragraph level for precision; preserve `CONTAINS` edges for article-level traversal.
- **Dual extraction: rule-based for definitions, LLM-assisted for obligations.** Definitions follow deterministic patterns ("X means Y"); obligations require interpreting modal verbs and exception language. Every LLM extraction is paired with a source quote for verification.
- **Build standalone first, integrate later.** The knowledge engine is built and tested as a stand-alone service before the orchestrator's `LegalResearchAgent` is wired up to consume it. Clean API boundary; no premature coupling.

## 3. What's left unresolved (candidate v04+ topics)

These are flagged in [`gdpr context/backup/improve_v1.md`](../history/01-research-arc.md) and `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md` but are not part of this `v03`:

- **Conditions and exceptions as first-class nodes.** Today they're properties on Obligations. Promoting them to `:Condition` and `:Exception` nodes would let queries traverse "unless / provided that / except where" relationships.
- **Authority weighting instead of numeric confidence.** Replace path-product confidence with `authority_level` (`PRIMARY_LAW > CASE_LAW > GUIDELINE > RECITAL`); resolve conflicts by higher authority winning.
- **Temporal logic on transitional / phased provisions.** The EU AI Act has article-dependent effective dates; right now `effective_date` exists as a property but isn't used in traversal.
- **Refresh pipeline for EDPB guideline updates and new CJEU case law.** Without one, the corpus will drift.

When one of these is picked up, write a new `vNN-*.md` proposal that `derives_from: v03-kb-completion.md`.

---

*The KB went from a portfolio-risk liability to the project's strongest moat. This proposal is the record of how.*
