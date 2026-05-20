---
version: "01"
title: Baseline — three-core free-text compliance platform
status: accepted
derives_from: null
proposed_date: 2026-01-15
decided_date: 2026-01-15
implemented_in:
  - 2ccaadc
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - docs/archive/README_pre_pivot.md
  - docs/archive/CLAUDE_pre_pivot.md
  - docs/archive/PROJECT_ANALYSIS_pre_pivot.md
  - gdpr context/main/02_ARCHITECTURE_AND_INTEGRATION.md
  - gdpr context/backup/Project 2 AI Model Governance & Compliance Monitoring Pipeline.md
  - gdpr context/backup/Project 3 GraphRAG Legal Research Engine.md
  - gdpr context/backup/project_4 EU AI Act Compliance Automation Agent.md
ai_guidance: |
  This is the accepted-and-shipped BASELINE the project started from. Treat it
  as historical context for what shipped initially. The pivot to a static code
  scanner (v02) supersedes the user-facing input mechanism and the monitor
  module described here. The knowledge engine (core_2) and the underlying
  Neo4j+vector data layer survive the pivot largely unchanged. Read SYSTEM.md
  for what's currently built.
---

## 0. What this document is

`v01` anchors the design-evolution stream. It describes the architecture that shipped in the initial commit (`2ccaadc`): a three-core free-text compliance platform where the user describes their AI system in prose and a multi-agent LangGraph workflow classifies it against the EU AI Act and GDPR, with a separate monitoring service watching for drift/bias on agent decisions. This was the starting point; later `vNN` proposals describe the deviations from it.

The thinking that produced this baseline is captured in detail across the pre-pivot `docs/archive/` and the polished `gdpr context/main/` portfolio docs (now consolidated into `history/01-research-arc.md`). This file is the decision-record summary.

---

## Status

- **State:** accepted (and shipped — the entire codebase pre-pivot was this architecture).
- **Decision date:** 2026-01-15 (approximate — the consolidation of the three-project portfolio into one platform happened during early 2026; the dated portfolio doc is `gdpr context/main/01_PROJECT_PORTFOLIO.md`, 2026-02-12).
- **Implementation:** commit `2ccaadc` ("Initial commit of EU AI Compliance Engine").
- **Supersedes:** none (baseline).
- **Superseded by:** partially by `v02-static-scanner-pivot.md` (user input mechanism + monitor module) and `v03-kb-completion.md` (KB built out from 12% to 100%).

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | Ship three separate projects (Project 2 monitoring, Project 3 GraphRAG, Project 4 compliance agent) | Looks like three half-projects on a portfolio. The pipeline P3 → P4 → P2 was the same story; merging it into one platform makes the value proposition legible. |
| 2 | Single monolith with all logic in one FastAPI app | Mixing the regulatory knowledge graph with the compliance reasoning loop with the monitoring backbone produces unbounded complexity and unclear ownership. Three services is the smallest split that maps to the three distinct concerns. |
| 3 | Use SQL + Elasticsearch for the regulatory corpus instead of Neo4j + ChromaDB | Vector search alone can't handle cross-regulation reasoning (e.g., "facial recognition" → "biometric data" → GDPR Art 9 → AI Act Art 10). The graph captures legal relationships; vectors add semantic discovery. SQL would require hand-maintaining the join logic. |

## Consequences

- ✅ Clean three-service split (`core_1` monitoring / `core_2` GraphRAG / `core_3` compliance agent) — each owns one concern, each has its own port, its own Docker container, its own database choice.
- ✅ Entity-aligned IDs across stores (`GDPR_ART_35`, `AIACT_ART_6`) — Neo4j IDs equal vector IDs, removing a known class of GraphRAG bugs.
- ✅ Cross-regulation links modelled from day one (`ANNEX_III_1 → TRIGGERS → GDPR_ART_35`).
- ⚠️ Heavy dependency on the user's prose description — quality of input drives quality of output.
- ⚠️ Three services × three databases × three Docker images = nontrivial deploy story (later resolved by collapsing the monitor and consolidating the vector store into Neo4j).
- ❌ Free-text input means no ground-truth-able findings; the classifier's outputs cannot be verified against any artifact other than the LLM's own confidence.

---

## 1. The three cores

| Core | Service | Port | Stack | Role |
|---|---|---|---|---|
| **core_1** | AI Model Governance & Monitoring | 8002 | PostgreSQL + Prometheus | Watches agent decisions; flags drift, bias, Article 14 violations; emits metrics. |
| **core_2** | GraphRAG Legal Research Engine | 8001 | FastAPI + Neo4j + ChromaDB | Hosts the regulatory knowledge graph; exposes vector / graph / hybrid retrieval; multi-hop reasoning with LLM synthesis. |
| **core_3** | Compliance Automation Agent | 8000 | FastAPI + LangGraph | Five-agent workflow: risk classifier, technical assessor, legal research, doc generator, supervisor. Pauses on `Critical` for human approval. |

## 2. User-facing input contract

```
POST /api/v1/assessments  { description: "<free-text prose>", ... }
```

The user describes their AI system in natural language. The supervisor agent routes the prose through:

1. **RiskClassifier** — classifies against EU AI Act tiers using the description + the KG. Outputs `PROHIBITED | HIGH_RISK | LIMITED_RISK | MINIMAL_RISK`.
2. **TechnicalAssessor** — GDPR gap analysis on the same prose.
3. **LegalResearch** — calls core_2 GraphRAG for relevant Articles + Obligations.
4. **DocGenerator** — produces DPIA / ROPA / conformity assessment scaffolds.
5. **HITL approval** — Critical findings pause for human review before final report.

## 3. Data layer (as of baseline)

- **Neo4j** — regulatory graph. Articles, Recitals, Obligations, Definitions modelled as `:Entity` subtypes; relationships include `REFERENCES`, `TRIGGERS`, `APPLIES_TO`, `COMPLEMENTS`.
- **ChromaDB** — vector store, parallel to Neo4j. IDs match Neo4j entity IDs.
- **PostgreSQL** — agent decision log (core_1 only).
- **Prometheus** — metrics scraping for core_1.

KB completeness at this stage: ~12% (14 of 99 GDPR articles, 11 of 113 AI Act articles loaded). Multi-hop reasoning failed ~88% of test scenarios. This was the gap that `v03-kb-completion.md` addressed.

## 4. Why this baseline was the right starting point

The decision to ship the free-text version first wasn't ignorance of its limits — it was the right portfolio-development order. Three things had to be proved before the static-scanner pivot was even possible:

1. **The KG schema works.** Entity-aligned IDs across Neo4j + ChromaDB, cross-regulation edges, paragraph-level granularity for articles with exceptions — these were unknowns. Free-text Q&A is a forgiving testbed for all of them.
2. **GraphRAG retrieval is real.** Vector + graph + RRF fusion + LLM synthesis is the whole moat. If hybrid retrieval can't beat plain vector search on legal queries, nothing else matters. The free-text demo proved it could.
3. **LangGraph supervision works.** Multi-agent orchestration with state passing, human-in-loop pauses, audit logging — all needed to be plumbed end-to-end before the input modality could change.

Once those three were proven, the input modality (free text vs. code) became a free variable. `v02` exercises that freedom.

---

*Anchors the stream. Subsequent `vNN-*.md` proposals describe deviations from this baseline.*
