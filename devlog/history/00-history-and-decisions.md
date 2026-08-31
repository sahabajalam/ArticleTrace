---
title: ArticleTrace — Distilled history and decisions
status: archived
snapshot_date: 2026-05-20
purpose: |
  A single-narrative read-once history of how ArticleTrace got to its current
  shape. Distilled from ~30 source files across the original `gdpr context/`
  brainstorm dir and the pre-pivot `docs/archive/`. For verbatim primary
  sources, see `01-research-arc.md` in the same dir.
ai_guidance: |
  This is a historical archive, frozen at snapshot_date. It is NOT a guide to
  the current system. Many specific claims here have been superseded by later
  work captured in design-evolution/. For current state, read
  ../SYSTEM.md. Use this file as a narrative reference; verify any specific
  claim against SYSTEM.md and the code before acting.
---

> **⚠ This is a historical archive, frozen at 2026-05-20.**
> For the current system, see [`../SYSTEM.md`](../SYSTEM.md).
> For active proposals, see [`../design-evolution/`](../design-evolution/).
> Decisions in this file may have been superseded — verify against `SYSTEM.md` before acting on any claim here.

---

# ArticleTrace — distilled history and decisions

This file compresses ~30 source documents (the `gdpr context/` brainstorm trail + the pre-pivot `docs/archive/`) into a single read-once narrative. It is the answer to *"how did we get here?"* for someone reading this repo for the first time.

For the full primary-source archive (every paragraph from every source doc, preserved verbatim), see [`01-research-arc.md`](01-research-arc.md).

---

## Part 1 — Origin (late 2025 to early 2026)

### 1.1 The opportunity

Two large EU regulatory frameworks went live or are going live in roughly the same window:

- **GDPR** — in force since May 2018. 99 articles, 173 recitals. Mature enforcement (Clearview AI fined €90.5M for biometric scraping; Meta fined €1.2B for cross-border transfers). Compliance officers know it but its application to AI systems is contested.
- **EU AI Act** — effective August 2024 with phased rollout. 113 articles, 180 recitals, 13 annexes. New tiered risk model (Prohibited / High-Risk / Limited / Minimal). Penalties reach €35M or 7% of global turnover. No mature compliance tooling existed when the project started.

Together they form an interlocking compliance burden: GDPR governs personal data; AI Act governs AI systems; many obligations stack (e.g., GDPR Art 22 *automated decisions* + AI Act Art 14 *human oversight* both apply to a credit-scoring system).

Industry estimates put the cost of manual AI Act compliance at ~£8,500 per assessment, ~40 hours of work, for organizations doing ~15 assessments per year. That's ~£1.5M annual spend, with high error variance because the rules are dense and the reviewers are scarce.

The thesis: a sufficiently structured regulatory knowledge graph plus deterministic detection could reduce this to ~£1,200 per assessment, ~6.5 hours of work. The portfolio frame was always "compliance automation as a real-money problem with no good tools."

### 1.2 The original three projects

Early planning broke the work into three separate portfolio projects:

1. **Project 2 — AI Model Governance & Compliance Monitoring Pipeline** — continuous runtime monitoring of AI systems. Watches agent decisions, flags drift, bias, Article 14 oversight violations. Stack: PostgreSQL + Prometheus + FastAPI.
2. **Project 3 — GraphRAG Legal Research Engine** — the regulatory knowledge graph itself. Hybrid vector + graph retrieval. Stack: Neo4j + ChromaDB + Gemini.
3. **Project 4 — EU AI Act Compliance Automation Agent** — multi-agent LangGraph workflow that takes a user description of an AI system and produces a compliance assessment. Stack: LangGraph + FastAPI + (calls into Project 3).

A fourth notional "Project 1" — a basic RAG over the same regulations — was envisioned as the simplest didactic version.

### 1.3 The pipeline realization

The four-project breakdown didn't survive contact with reality. Two observations changed it:

1. **The projects formed a pipeline, not a portfolio.** Project 3 (KG) is consumed by Project 4 (compliance agent), which produces decisions monitored by Project 2. You can't sell "I built three half-projects" — you sell "I built one platform whose pieces compose." The naming convention "Project 1" was retroactively absorbed into the merged platform because it was the first project in the chronological series, not because it shipped a separate thing.
2. **The portfolio narrative becomes legible only as one platform.** The £1.3M/year savings claim only makes sense end-to-end; no single sub-project carries the whole value proposition.

The decision (early Feb 2026): merge the three single-project documents into one integrated portfolio narrative. Result: [`gdpr context/main/01_PROJECT_PORTFOLIO.md`](01-research-arc.md) dated 2026-02-12. This is the moment the project as currently understood begins.

---

## Part 2 — The baseline architecture (early Feb 2026, captured in v01)

The first shipped architecture was the **three-core free-text compliance platform**:

| Core | Service | Port | Stack |
|---|---|---|---|
| `core_1` | AI Model Governance & Monitoring | 8002 | PostgreSQL + Prometheus |
| `core_2` | GraphRAG Legal Research Engine | 8001 | FastAPI + Neo4j + ChromaDB |
| `core_3` | Compliance Automation Agent | 8000 | FastAPI + LangGraph |

User contract: `POST /api/v1/assessments { description: "<free-text prose>" }`. The supervisor agent in `core_3` ran a 5-step LangGraph workflow (risk classify → technical assess → legal research → doc generate → HITL approval on Critical → final report).

### 2.1 Why this baseline was the right starting point

Even though the baseline was later superseded for its input modality, shipping it first was the correct order:

1. **The KG schema had to be proven.** Entity-aligned IDs across Neo4j + ChromaDB, cross-regulation edges, paragraph-level granularity. Free-text Q&A is a forgiving testbed for these.
2. **GraphRAG retrieval had to be proven.** Vector + graph + RRF + LLM synthesis is the whole moat. If hybrid retrieval can't beat plain vector search on legal queries, the project has no differentiation.
3. **LangGraph supervision had to be plumbed.** Multi-agent orchestration with state, HITL pauses, audit logging — all needed end-to-end wiring before input modality could change.

Once those three were proven, the input modality (free text vs. real code) became a free variable. The pivot exploited that freedom.

### 2.2 Architectural decisions documented during the baseline phase

From [`gdpr context/main/02_ARCHITECTURE_AND_INTEGRATION.md`](01-research-arc.md) and [`gdpr context/main/03_KB_DESIGN_AND_CONSTRUCTION.md`](01-research-arc.md):

| Decision | Rationale |
|---|---|
| Neo4j + ChromaDB (not SQL/Elasticsearch) | Vector search alone fails for cross-regulation reasoning. The graph captures legal relationships; vectors add semantic discovery. SQL would require hand-maintaining the join logic. |
| Knowledge graph over document store | Vector similarity will lie on synonyms ("biometric data" GDPR ≠ "remote biometric identification system" AI Act — overlap but not equivalence). Structured edges capture the actual relationships. |
| Paragraph-level granularity (not article-level) | Articles have exceptions, conditions, sub-clauses. Embedding at article level returns the right article but can't pinpoint *which paragraph*. Hallucinations on legal exceptions are the worst failure mode. |
| Dual extraction: rule-based + LLM-assisted | Definitions follow deterministic patterns ("X means Y"); rule-based. Obligations require interpreting modal verbs and exception language ("shall," "must not," "does not apply where"); LLM with mandatory source-quote verification. |
| Standalone KB first, integration later | `core_2` is built and tested standalone before `core_3` consumes it. Clean API boundary; no premature coupling. |
| Entity-aligned IDs across stores | `GDPR_ART_35` is the same ID in Neo4j and the vector store. Removes a known class of GraphRAG bugs. |
| Cross-regulation edges from day one | `ANNEX_III_1 → TRIGGERS → GDPR_ART_35`. The system models legal causality, not just textual similarity. |

---

## Part 3 — The gap analysis crisis (mid-Feb 2026)

In Feb 2026, an honest audit of the KB produced [`gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`](01-research-arc.md). The numbers were uncomfortable:

| Metric | At gap analysis | Required |
|---|---|---|
| GDPR articles loaded | 14 / 99 (14%) | 99 / 99 |
| AI Act articles loaded | 11 / 113 (10%) | 113 / 113 |
| Recitals loaded | 0 / 173 GDPR + 0 / 180 AI Act (0%) | All |
| EDPB guidelines | None loaded | Material amount |
| CJEU case law | None loaded | Key precedents |
| Multi-hop reasoning failure rate | ~88% on test scenarios | <10% |

The accompanying brainstorm doc [`gdpr context/backup/CRITICAL_GAP_ANALYSIS.md`](01-research-arc.md) called out specific failure modes: queries that should have returned cross-regulation paths returned single-article answers; queries that hit articles with exceptions returned absolute "yes/no" answers because the exception clauses weren't structured.

[`gdpr context/backup/improve_v1.md`](01-research-arc.md) added a constructive critique on top: the system was solid architecturally but had five conceptual gaps —

1. Articles treated as atomic units (no paragraph/clause decomposition).
2. Conditions and exceptions stored as properties, not first-class nodes.
3. Numeric confidence (product of edge weights) too weak for legal reasoning.
4. No temporal versioning (EU AI Act has phased effective dates; no traversal logic uses them).
5. Interpretive hierarchy flat (treaty law / regulation / case law / guidelines / recitals all just "entities").

The gap analysis produced two parallel decisions:

- **Complete the KB in-house at paragraph granularity** (captured in `v03-kb-completion.md`).
- **Reconsider the user-facing input mechanism** (captured in `v02-static-scanner-pivot.md`).

These are technically independent decisions but they were taken in quick succession and they reinforce each other: the static-scanner reframe only lands if the KB is complete (rules need a complete corpus); completing the KB only justifies the cost if the rule-corpus framing produces ground-truth-able findings.

---

## Part 4 — The static-scanner pivot (mid-Feb 2026, captured in v02)

The decision: stop taking free-text descriptions of AI systems; start scanning real code from real GitHub repos.

### 4.1 Why the free-text version was wrong (in retrospect)

Three problems, none of which were fixable by iteration:

1. **Input is vibes.** The user can be vague, wrong, or dishonest. The classifier has no ground truth. No prompt-engineering fixes this.
2. **Every demo looks the same.** Textbox → spinner → markdown. Indistinguishable from any LLM-wrapper portfolio project on the same shelf.
3. **No defensible differentiation.** Credo AI and Holistic AI already do self-reported compliance questionnaires; Guardrails AI does LLM-output validation; Fairlearn/AIF360 do runtime model auditing. The free-text classifier didn't have a niche.

### 4.2 The reframe

Static scan of AI application code against regulatory obligations. **Nobody else does this.** The knowledge graph stops being "the thing the chatbot consults" and becomes "the thing the rules are written against." Detection is deterministic (AST + imports + content patterns); LLMs only write the post-hoc narrative.

### 4.3 The borrowed shape

The pivot adopted patterns that converged across the static-analysis ecosystem:

| Tool | Pattern borrowed |
|---|---|
| Semgrep | Rule catalog as data, not hand-coded if/else |
| SonarQube | Per-rule severity + suppressions via config |
| Snyk | Findings tied to fix suggestions |
| GitGuardian | (Phase 3) pre-commit / on-save delta scanning |
| Trivy | Deterministic scanning first; LLMs post-hoc only |

Core shared principle: **LLMs are kept out of the detection hot path.**

### 4.4 What the pivot threw away

- The free-text input UI.
- The HITL approval pause (no classification uncertainty to pause on — findings are deterministic).
- The monitor module (`core_1` — drift/bias/Prometheus). Decommissioned. Continuous monitoring needs continuous production traffic that no portfolio demo has; the signal-to-effort ratio collapsed.

### 4.5 What survived

- The knowledge graph schema (entity-aligned IDs, paragraph granularity, cross-regulation edges).
- The hybrid retrieval engine (vector + graph + RRF + LLM synthesis).
- The LangGraph supervisor pattern (just with fewer nodes and no HITL).
- The Postgres + Redis backing.

Service renames: `core_3` → `orchestrator` (now on port 8004); `core_2` → `knowledge_engine` (still on port 8001).

---

## Part 5 — KB completion (Feb to April 2026, captured in v03)

The Feb 2026 gap analysis → April 2026 completion arc is documented in detail in `v03-kb-completion.md`. The numbers tell the story:

| Metric | Feb 2026 (gap analysis) | April 2026 (final) |
|---|---|---|
| Nodes | ~290 | 2,301 |
| Relationships | ~600 | 4,423 (or 4,431 — sources disagree slightly) |
| Vector documents | ~280 | 2,198 |
| Vector dimensions | 768 | 3,072 |
| Cross-regulation edges | <10 | 84 (5 interaction types) |
| Orphan nodes | several | 0 |
| Avg relationships per article | <5 | 19.1 |
| Multi-hop reasoning failure rate | ~88% | <10% |

The completion was an in-house build (no third-party paragraph-level KB exists). Dual extraction strategy: rule-based for definitions, LLM-assisted for obligations with mandatory source-quote verification. Stored in Neo4j with the native vector index (one index, 7 collections filtered by `n.collection` — eliminates the dual-store sync problem that the earlier Chroma + Neo4j setup had).

---

## Part 6 — Vector store consolidation (Q1 2026)

Two consolidation decisions landed during the post-pivot cleanup:

1. **Vector store: ChromaDB → Neo4j-native vector index.** ChromaDB had Python 3.14 compatibility issues. Neo4j 5.x vector indexes were now first-class. Running two storage backends added operational surface area without benefit. Single backend = simpler health check, single backup story, fewer moving parts in Cloud Run. Captured in commit `661f990`.
2. **Module restructure.** The orchestrator was reorganized to clearly separate pre-pivot (legacy) from post-pivot code. New top-level packages under `orchestrator/src/`: `code_analyzer/`, `agents/`, `database/`, `cache/`, `control_plane/`. Frontend reorganized under Next.js App Router. Captured in commit `5210e51`.

---

## Part 7 — HITL removal (April 2026)

A late but consequential change: the HITL approval pause in the supervisor was removed.

The pre-pivot supervisor had a conditional branch that paused for human review on any `Critical`-severity finding. After the pivot, static findings carry `file:line` anchors — every claim is verifiable by opening the file. The HITL pause was inherited from the free-text era (where classification was vibes-based and needed human sanity-check). It became dead weight.

The current supervisor docstring is explicit:

> No HITL branch: static scanners produce deterministic, auditable evidence, so there is no classification-uncertainty branch to pause on.

This is the kind of change that's easy to miss: `docs/README.md` (dated 2026-04-13) still mentioned HITL retention even after the supervisor code dropped it. That drift was the canonical example used to justify adopting the living-docs playbook.

---

## Part 8 — Major decisions index

A flat table of every decision documented in the source archive:

| # | Decision | Rationale | Documented in |
|---|---|---|---|
| 1 | Merge three projects into one platform | The pipeline P3 → P4 → P2 is the value story | `01_PROJECT_PORTFOLIO.md` |
| 2 | Three-service architecture (orchestrator / KE / monitor) | Map services to concerns; minimum viable split | `02_ARCHITECTURE_AND_INTEGRATION.md` |
| 3 | Neo4j + (initially ChromaDB) as the data layer | Vector alone fails cross-regulation; graph captures structure | `03_KB_DESIGN_AND_CONSTRUCTION.md` |
| 4 | Paragraph-level granularity for articles | Articles have exceptions / conditions / sub-clauses | `03_KB_DESIGN_AND_CONSTRUCTION.md` |
| 5 | Dual rule-based + LLM-assisted extraction | Definitions are deterministic; obligations need interpretation | `03_KB_DESIGN_AND_CONSTRUCTION.md` |
| 6 | Standalone KB first, integration later | Clean API boundary; no premature coupling | `EU_AI_KB_PROJECT_CONTEXT.md` |
| 7 | Entity-aligned IDs across stores | Removes a known class of GraphRAG bugs | (architectural baseline) |
| 8 | Cross-regulation edges from day one | Models legal causality, not just similarity | `KNOWLEDGE_GRAPH_PROJECT_CONTEXT.md` |
| 9 | Complete the KB in-house at paragraph granularity | No third-party KB exists; differentiator preserved | `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md` → `v03` |
| 10 | Pivot to static code scanner | Free-text input is vibes; no differentiation; static scanners produce ground-truth-able findings | `docs/README.md §2` → `v02` |
| 11 | Vector store: ChromaDB → Neo4j-native index | Python 3.14 compat; single backend; one less moving part | commit `661f990` |
| 12 | Module restructure for post-pivot code separation | Clean post-pivot home; deprecate legacy paths | commit `5210e51` |
| 13 | Decommission monitor module | Drift/bias/Prometheus requires production traffic | `v02-static-scanner-pivot.md §Consequences` |
| 14 | Remove HITL approval pause | Static findings are deterministic; no uncertainty to gate on | `v02-static-scanner-pivot.md §Consequences` |
| 15 | Adopt living-docs playbook (this very document) | Documentation was in three disconnected piles; drift was happening silently | `v05-living-docs-bootstrap.md` *(would be v04 if proposed; bootstrap is current session)* |

---

## Part 9 — Conventions and naming

Three names refer to the same system:

- **ArticleTrace** — canonical name used in code (FastAPI title, Docker container names like `articletrace-orchestrator`), in the current `docs/README.md`, and in any new doc going forward.
- **Aegis Compliance Engine** — marketing/portfolio name used in `PROJECT_EXTRACTION.md`. Equivalent.
- **EU_AI_GDPR** — repo directory name (with `Project_1_` prefix). Historical artifact of the four-project portfolio scheme; preserved for path stability.

The earlier three-core scheme used `core_1` / `core_2` / `core_3`. These are now `monitor` (decommissioned) / `knowledge_engine` / `orchestrator`. Old commits and pre-pivot docs may still reference the `coreN` names.

---

## Part 10 — Open future work

Captured from `gdpr context/backup/improve_v1.md` and `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`, not yet picked up:

- Promote Conditions and Exceptions to first-class graph nodes (today stored as properties on Obligations).
- Replace numeric path-product confidence with authority weighting (`PRIMARY_LAW > CASE_LAW > GUIDELINE > RECITAL`).
- Add temporal logic for transitional / phased provisions (EU AI Act has article-dependent effective dates).
- Build a refresh pipeline for EDPB guideline updates and new CJEU case law (without one, the corpus will drift).
- Anti-hallucination guardrail: refuse to answer when retrieved graph contains <1 obligation/prohibition source.
- Multi-language scanner support (current AST scanners are Python-only; tree-sitter beyond Python is Phase-2).

When any of these is picked up, write a new `vNN-*.md` proposal under `design-evolution/`. The expected next versions if proposed are `v04` and onward, derived from `v03-kb-completion.md`.

---

## Sources consolidated into this distillation

From `gdpr context/main/` (the polished merged docs, all dated 2026-02-12):
- `01_PROJECT_PORTFOLIO.md` — the portfolio merge moment.
- `02_ARCHITECTURE_AND_INTEGRATION.md` — three-core architecture.
- `03_KB_DESIGN_AND_CONSTRUCTION.md` — KB design rationale + phased construction plan.
- `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md` — the gap analysis that triggered the KB completion + the pivot.

From `gdpr context/backup/` (raw brainstorms, exploration, pre-merge per-project docs):
- `PROJECT_STORY.md`, `PROJECT_ANALYSIS.md` — narrative framings (the "three kingdoms").
- `CRITICAL_GAP_ANALYSIS.md`, `knowledge_graph_gap_analysis.md` — raw gap audits.
- `improve_v1.md` — constructive critique of the KB design (paragraph decomposition, conditions/exceptions, temporal logic).
- `KNOWLEDGE_GRAPH_PROJECT_CONTEXT.md`, `EU_AI_KB_PROJECT_CONTEXT.md` — original standalone project designs for the KG.
- `Project 2/3/4 *.md` — pre-merge per-project docs.
- `Integration Architecture How Projects Actually Connect.md`, `SYSTEM_ARCHITECTURE.md` — early integration sketches.
- `KB_construction_plan.md`, `MERGED_GAP_ANALYSIS.md`, `DATA_ENHANCEMENT_SUMMARY.md` — execution-phase notes.

From `docs/archive/` (pre-pivot final state):
- `README_pre_pivot.md`, `CLAUDE_pre_pivot.md`, `PROJECT_ANALYSIS_pre_pivot.md`, `REFERENCE_pre_pivot.md`, `EU_AI_KB_PROJECT_CONTEXT.md`, `KB_construction_plan.md`, `gdpr_kg_MEMORY.md`, `gdpr_kg_analysis.md`, `compliance_case_studies.txt`, `data_scraper_*.md` — pre-pivot operational and design docs, plus the data-scraper documentation that produced the KB inputs.

All sources are preserved verbatim in `01-research-arc.md`. Browse that file for the raw quotes, the specific failure scenarios, the dated decision moments. This file is for *what* and *why*; that file is for *how it was actually said at the time*.
