---
title: AlloyCode — Change Log
status: living
last_verified: 2026-05-20
companion_doc: devlog/SYSTEM.md
ai_guidance: |
  This is the LIVING change log — entries appended chronologically (newest
  first under the dated divider). Use it to recover the WHY behind any
  change. Each entry pairs with a section update in SYSTEM.md.
---

# AlloyCode — Change Log

## Format

```
## YYYY-MM-DD — <short title>

**What:** <files / tables / modules / pages affected, concrete>
**Why:** <reason in one or two sentences>
**Impact on SYSTEM.md:** <section(s) updated; or "none — internal only">
**Refs:** <commit short hashes / migration numbers / PR refs if any>
```

---

## 2026-05-20 — Adopt living-docs playbook

**What:** Created `CLAUDE.md` (root) + `devlog/` tree (`SYSTEM.md`, this `CHANGELOG.md`, `README.md`, `JOURNEY.md`, `design-evolution/v01-v03`, `history/00-01`, `prompts/`). Moved `DEPLOYMENT_GUIDE.md` → `devlog/DEPLOYMENT.md` and `DEVLOG.md` → `devlog/BUG_LOG.md`. Archived `gdpr context/` and `docs/archive/` into `devlog/history/01-research-arc.md` (preserved full text) + `devlog/history/00-history-and-decisions.md` (distilled narrative).
**Why:** Documentation was in three disconnected piles (root-level ops docs, `docs/` dir, `gdpr context/` brainstorm trail). A fresh AI agent couldn't tell current state from frozen state — `docs/MEMORY.md` said KB was "100% COMPLETE" while `gdpr context/main/04` said "12% complete," neither marked as which epoch. Applying [`../DOCS_PLAYBOOK.md`](../DOCS_PLAYBOOK.md) §11 bootstrap fixes the structural problem.
**Impact on SYSTEM.md:** Created from scratch (was missing); §1–§8 populated from direct code audit.
**Refs:** doc-only; commit pending.

---

## 2026-04-13 — Knowledge base build-out completed

**What:** Neo4j knowledge graph reached final state: 2,301 nodes, 4,423 (or 4,431 — sources disagree) relationships, 17 entity types, 13 relationship types, 2,198 vector documents across 7 collections, 84 cross-regulation `COMPLEMENTS` edges, 0 orphan nodes. Embeddings on `gemini-embedding-001` at 3072 dimensions. Sources: [`docs/MEMORY.md`](history/01-research-arc.md), [`docs/REFERENCE.md`](history/01-research-arc.md) §1.1.
**Why:** The Feb 2026 gap analysis (`gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`) showed the KB was only 12% complete — multi-hop reasoning was failing ~88% of test scenarios. Without a complete corpus, the "rule corpus, not Q&A bot" reframe from the static-scanner pivot doesn't land. Decision: complete in-house at paragraph granularity; no third-party paragraph-level KB exists.
**Impact on SYSTEM.md:** §2.1 Data layer — counts and schema. §3.3 Knowledge Engine — engines now operational against the full corpus.
**Refs:** doc-only (work pre-dates initial git import `2ccaadc`); design rationale captured in [`design-evolution/v03-kb-completion.md`](design-evolution/v03-kb-completion.md).

---

## 2026-04 — HITL approval pause removed from supervisor

**What:** `orchestrator/src/agents/supervisor.py` reduced to a linear graph: `classify_risk → research_legal → generate_narrative → synthesize → END`. The pre-pivot conditional branch that paused on `Critical` severity for human approval was removed. Docstring updated: *"No HITL branch: static scanners produce deterministic, auditable evidence, so there is no classification-uncertainty branch to pause on."*
**Why:** Static scanners produce ground-truth-able findings with `file:line` anchors — every claim is verifiable by opening the file. The HITL pause was inherited from the free-text era (where classification was vibes-based and needed human sanity-check). It became dead weight after the pivot.
**Impact on SYSTEM.md:** §3.2 Supervisor — node table reflects the 4-node linear graph; drift note added pointing at the now-archived `docs/README.md` which still mentioned HITL retention.
**Refs:** doc-only — the pivot landed across multiple unstaged edits; the doc trail is in [`docs/README.md`](history/01-research-arc.md) §5 (claims HITL retained — STALE) vs. [`orchestrator/src/agents/supervisor.py`](../orchestrator/src/agents/supervisor.py) (no HITL — CURRENT).

---

## 2026-Q1 — Migrate vector store to Neo4j; consolidate scripts and docs

**What:** Vector store moved from a custom JSON/ChromaDB hybrid into Neo4j's native vector index. One vector index (`entity_embedding`, 3072-dim, cosine) covers all 7 collections; queries filter by `n.collection`. Scripts in `pipeline.ps1` and `gcp.ps1` consolidated. Various docs reorganized under `docs/`.
**Why:** ChromaDB had Python 3.14 compatibility issues; running two storage backends added operational surface area without buying anything (Neo4j 5.x vector indexes are now first-class). Single backend = simpler health check, single backup story, fewer moving parts in Cloud Run.
**Impact on SYSTEM.md:** §2.1 Data layer — Neo4j-native vector index documented; §6 Deploy — single Neo4j env-var set replaces two storage configs.
**Refs:** commit `661f990` ("Migrate vector store to Neo4j; consolidate scripts and docs").

---

## 2026-Q1 — Restructure modules and update frontend/infrastructure

**What:** Major refactor of orchestrator module layout (introduces `code_analyzer/`, `agents/`, `database/`, `cache/`, `control_plane/` as top-level packages under `orchestrator/src/`). Frontend reorganized under Next.js App Router (`frontend/src/app/{scans,knowledge,page.tsx}`). Infrastructure files (Dockerfile per service, docker-compose.yml) updated.
**Why:** The static-scanner pivot needed a clean home for the new code_analyzer subsystem (scan.py, ingest.py, scanners/, rule_loader.py). Pre-existing layout mixed pre-pivot and post-pivot code; the refactor cleanly separated them.
**Impact on SYSTEM.md:** §3.1 Scan pipeline — newly documented; §5 Frontend — page paths updated.
**Refs:** commit `5210e51` ("Restructure modules and update frontend/infrastructure").

---

## 2026-Q1 — Static-scanner pivot (free-text → code scanner)

**What:** Project pivoted from a free-text "describe your AI system" classifier (5-agent LangGraph workflow over user prose) to a static compliance scanner over GitHub repos (deterministic detection + LLM narrative only). New subsystem: `orchestrator/src/code_analyzer/` (ingest, 6-scanner pipeline, profile builder). Pre-pivot architecture preserved in [`docs/archive/`](history/01-research-arc.md).
**Why:** Three fatal problems with the free-text approach: (1) input was vibes — classifier had no ground truth, (2) every demo looked identical (textbox + spinner + markdown), (3) no differentiator vs. any LLM-wrapper project. The static-scanner reframe ties every finding to `file:line` in real code; the knowledge graph becomes a rule corpus instead of a research Q&A bot. See [`design-evolution/v02-static-scanner-pivot.md`](design-evolution/v02-static-scanner-pivot.md) for the alternatives weighed and the consequences accepted.
**Impact on SYSTEM.md:** §1, §3.1, §3.2 fully rewritten; §3 added the scanner pipeline; §4.1 added `POST /api/v1/scans` and friends.
**Refs:** the orchestrator/code_analyzer/ subtree did not exist pre-pivot — see [`gdpr context/backup/improve_v1.md`](history/01-research-arc.md) (KB-design critique that pre-dated the pivot) and [`docs/README.md`](history/01-research-arc.md) §2 for the reasoning. Commits `5210e51` and `661f990` carry the bulk of the implementation.

---

## 2026-Q1 — Initial commit (project scaffold)

**What:** First git commit of the EU AI Compliance Engine. Includes the three-service Docker Compose layout, FastAPI scaffolding for orchestrator + knowledge engine, Next.js scaffolding for frontend, initial Neo4j schema definitions.
**Why:** Establish the repo as the consolidated home for what had been three notionally-separate projects (P1 Basic RAG / P3 GraphRAG Legal Engine / P4 Compliance Agent) — see [`history/01-research-arc.md`](history/01-research-arc.md) for the multi-project genesis.
**Impact on SYSTEM.md:** baseline.
**Refs:** commit `2ccaadc` ("Initial commit of EU AI Compliance Engine").

---

## Pre-existing operational bug log

The pre-existing `DEVLOG.md` has been moved to [`BUG_LOG.md`](BUG_LOG.md) and reframed as the **incident log** (companion to this CHANGELOG): 23 dated entries `DL-001` through `DL-023` covering operational fixes — uv/PowerShell issues, embedding model deprecations, CORS, Cloud Run port binding, git binary missing, secret corruption, etc. Format and contents are preserved; only the title and path changed.

Use this CHANGELOG for **intentional changes**. Use `BUG_LOG.md` for **incident-and-fix**.

---

## How to append a new entry

1. Add a new `## YYYY-MM-DD — <title>` block above the most recent dated entry (newest first).
2. Fill the four fields strictly: `What:` (concrete files / modules / pages), `Why:` (one or two sentences — this is the only prose field), `Impact on SYSTEM.md:` (sections updated, or `none — internal only`), `Refs:` (commit shorts, migrations, PR refs).
3. Bump `last_verified:` in this file's frontmatter.
4. Also update the section in `SYSTEM.md` that the change touches, and bump `last_verified:` there too.
