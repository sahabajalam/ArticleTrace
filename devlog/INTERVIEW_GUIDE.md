---
title: AlloyCode — Interview Guide
status: living
last_verified: 2026-06-19
companion_docs:
  - devlog/SYSTEM.md
  - devlog/design-evolution/v02-static-scanner-pivot.md
  - devlog/design-evolution/v04-hitl-decision.md
ai_guidance: |
  Line-by-line defence of the non-obvious design choices in AlloyCode. Each
  section is one question a recruiter or interviewer will ask, with a
  three-sentence answer, the follow-up trap, and the citable code/doc
  reference. Pattern modelled on Project 2's `INTERVIEW_GUIDE.md`. This is
  rehearsal material, not architecture reference — for the architecture
  read SYSTEM.md.

  Written 2026-06-16 in response to `../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`
  §3.4 (the defensibility-over-volume thesis): the interview format has
  shifted to line-by-line interrogation, so every non-obvious choice needs
  a pre-rehearsed answer.
---

# AlloyCode — Interview Guide

> The market shifted: 38.5% of technical interviews show some form of AI-assisted cheating, so the format moved to line-by-line interrogation of non-obvious choices. Every section below is one such question — three-sentence answer + the follow-up trap + the citable source.

For elevator-pitch material, see [`JOURNEY.md`](JOURNEY.md). For architecture depth, see [`SYSTEM.md`](SYSTEM.md). This doc is for the *defence* — the answers you can deliver under pressure without reciting the docs.

---

## How to use this

Each Q has the same three pieces:

1. **One-line setup** — the question reframed in interviewer language.
2. **The answer** — three sentences, deliverable in ~30 seconds.
3. **Follow-up trap + citable reference** — the trap is the cheap rebuttal that lands if you stop after the first sentence; the reference is the file or doc you'd open if asked to prove it.

Aim to deliver each answer with variable latency. Per the audit §3.4, a flat 3–5 second pause before every question is the strongest behavioural tell for AI-assisted cheating; human thinking time is uneven. Slow on one, fast on the next — that's the human cadence.

---

## Q1 — Why static code scanning, not free-text self-assessment?

**Setup:** "Most AI-governance tools collect questionnaire answers from the user — Credo AI, Holistic AI, Aporia. You went the other way. Why?"

**Answer:** Free-text input is vibes — every demo looks the same and you can't ground-truth a textbox. The market gap is *code-level* compliance reading: Fairlearn audits runtime models, Guardrails validates LLM outputs, nothing statically reads AI application code against regulatory obligations. AlloyCode took the static-scanner position because deterministic findings with `file:line` anchors are auditable in a way that LLM-generated risk categories from a user description never will be.

**Follow-up trap:** "But couldn't you just give the LLM the code and ask it to classify?" — Yes, and that's what most demos do. The reason we don't: an LLM categorisation has no falsifiable evidence layer. A YAML rule + an AST match + a code anchor is reproducible; an LLM saying "this looks high-risk" is not. The whole moat is the rule corpus, not the LLM.

**Reference:** [`design-evolution/v02-static-scanner-pivot.md`](design-evolution/v02-static-scanner-pivot.md) (§Alternatives considered + §Consequences); the existence of `orchestrator/src/code_analyzer/` is the implementation.

---

## Q2 — Why RRF (Reciprocal Rank Fusion) instead of pure vector search?

**Setup:** "Your retrieval combines vector similarity with graph traversal via RRF. Why not just stick with cosine similarity over embeddings?"

**Answer:** Pure vector retrieval over a legal corpus drops obvious citations — case law that references an article often shares no surface vocabulary with it (e.g., *Schufa* and Article 22 GDPR cite each other but their texts don't embed close). Graph traversal recovers those connections because the KG already encodes the `CITES` / `INTERPRETS` / `COMPLEMENTS` edges. RRF is the merge: it ranks each result list independently, fuses by 1/(k+rank), and gives you a unified ordering without having to tune a weighted average between two different similarity scales.

**Follow-up trap:** "Why not just learn a reranker?" — Because we don't have labelled rerank data at the scale a learned reranker needs, and a reranker over zero labels is worse than RRF (which has a single `k` hyperparameter). The RRF call is a defensible default that the audit can't dispute; a learned reranker without held-out validation is a future-vs-now trade.

**Reference:** [`knowledge_engine/src/retrieval/engine.py`](../knowledge_engine/src/retrieval/engine.py) — the `RetrievalEngine.hybrid_search` method; [`SYSTEM.md`](SYSTEM.md) §3.3 + §7 Glossary entry on RRF.

---

## Q3 — Why is the LLM kept out of the detection hot path?

**Setup:** "You have a 6-scanner pipeline that's all deterministic — imports, AST, regex, file patterns. Why not let the LLM do the detection? It would catch more."

**Answer:** Every detection has to be falsifiable to be defensible — a recruiter, an auditor, or a downstream compliance officer needs to be able to say "show me the line that triggered this." An LLM detection is a black box; a YAML rule + a tree-sitter match is a deterministic, reproducible artefact. The LLM still runs — at the `_filter_decision_surfaces` stage to drop test/mock surfaces, and at `generate_narrative` to write the executive summary — but it never *generates* a finding. If the LLM call fails, the regex verdict wins; the pipeline is fail-open.

**Follow-up trap:** "Doesn't that limit what you can detect?" — Yes, by design. The trade is breadth-for-defensibility. The 10 MVP rules are the deepest 10, not the broadest 10; depth-over-breadth is the whole point per [`NORTHSTAR.md`](NORTHSTAR.md) Part IV. A scanner that flags everything and explains nothing is worse than one that flags ten things and cites the article each one violates.

**Reference:** [`orchestrator/src/code_analyzer/scanners/`](../orchestrator/src/code_analyzer/scanners/) — the 6 scanner modules, all deterministic; the LLM call lives in `_filter_decision_surfaces` (`ast_scanner.py`) and `DocumentationGeneratorAgent` (`agents/documentation_generator.py`) only.

---

## Q4 — Why was the human-in-the-loop approval gate removed?

**Setup:** "EU AI Act Article 14 mandates 'human oversight' for high-risk AI systems. Your supervisor has no HITL pause. Explain."

**Answer:** The pre-pivot system had a HITL pause because the classifier was an LLM with no calibrated confidence — we needed a human to override low-confidence categorisations. When we pivoted to a deterministic rule classifier, the trigger condition disappeared: there's no uncertainty score to gate on, so the branch would fire either always-on or never. We chose to remove it rather than retain a pause that adds latency without adding judgment — the oversight obligation lives one layer up.

**Follow-up trap (the Article 14 trap):** "But Article 14 still applies." — Article 14 imposes the oversight obligation on the *operator* of the high-risk system, not the analysis tool reporting on it. AlloyCode is `mypy`-shaped — it surfaces evidence, a human reads the report and decides. Adding HITL inside `mypy` would be a category error; adding it inside AlloyCode is the same category error one layer up. If AlloyCode were ever a CI-blocking enforcement tool, the gate would live in the wrapping GitHub Action, not in AlloyCode itself.

**Reference:** [`design-evolution/v04-hitl-decision.md`](design-evolution/v04-hitl-decision.md) — the full decision record, including §4 "EU AI Act counter-argument and the response" and §5 "What would change this decision."

---

## Q5 — Why Neo4j instead of pgvector?

**Setup:** "You're already running Postgres for scan state. Why add Neo4j instead of using pgvector?"

**Answer:** pgvector handles vector search but not the multi-hop traversals the legal mapping needs — "find articles that this CJEU case interprets, including the recitals those articles cite." That's two hops minimum, sometimes three. We migrated through ChromaDB → JSON-backed store → Weaviate → Neo4j over six months precisely because every previous choice forced us to either denormalise the graph into the vector store or maintain two separate systems. Neo4j's native HNSW vector index landed in 2024, so a single store now serves both vector and graph — eliminating one external service and one consistency boundary.

**Follow-up trap:** "But pgvector + a graph library like rustworkx would be cheaper to run." — Cheaper to run, not cheaper to maintain — you'd own the graph traversal algorithms, the index invalidation, the query language. The Cypher / graph-native model also makes the rule corpus auditable to a non-engineer: a compliance lawyer can read `MATCH (a:Article {id:'GDPR_ART_22'})-[:CITES]->(r:Recital)`. They can't read SQL with recursive CTEs.

**Reference:** [`knowledge_engine/src/stores/graph_store.py`](../knowledge_engine/src/stores/graph_store.py); [`design-evolution/v03-kb-completion.md`](design-evolution/v03-kb-completion.md) for the migration arc; commit `661f990` ("Migrate vector store to Neo4j; consolidate scripts and docs").

---

## Q6 — Why does the scanner order matter?

**Setup:** "You enforce a strict order — imports first, then AST, then LLM enrichment, then AST rules, then content, file-pattern, co-occurrence. Why not run them in parallel?"

**Answer:** Each scanner reads shared state populated by earlier ones, so the order encodes data dependencies. `ImportScanner` builds the library/module map; `AstScanner` uses that map to collect "decision surfaces" (function defs that look like AI inference call sites); the LLM pass filters those surfaces by reading the import map *and* the AST findings; `AstRulesScanner` applies pattern rules to the cleaned surfaces. Running in parallel would mean either each scanner duplicates the work, or we serialise on the shared state anyway with extra coordination overhead.

**Follow-up trap:** "What if a later scanner gets new data the LLM filter would have used?" — Then we'd re-run the LLM filter, but in practice this hasn't fired in the 10-rule MVP. The pipeline order is documented in [`scan.py`](../orchestrator/src/code_analyzer/scan.py) `_scan_and_profile()`; adding a new scanner requires explicitly deciding where it sits in the order, which is a feature, not a bug.

**Reference:** [`orchestrator/src/code_analyzer/scan.py`](../orchestrator/src/code_analyzer/scan.py) — `_scan_and_profile`; [`SYSTEM.md`](SYSTEM.md) §3.1.

---

## Q7 — Why 10 YAML rules and not 100?

**Setup:** "Semgrep ships hundreds of rules. You have ten. Why so few?"

**Answer:** Depth, not breadth, per the audit §3.4. Each of the 10 rules has a passing test, a regulatory citation, and at least one golden case that exercises it end-to-end. Shipping 100 rules without that scaffolding produces a scanner that flags everything and explains nothing — which is worse than a scanner that catches less but cites the article every finding violates. The 10-rule MVP is the deepest 10, not the broadest 10; the rule-as-data design ([`rule_loader.py`](../orchestrator/src/code_analyzer/rule_loader.py)) means adding rule 11 is a YAML file, not a code change.

**Follow-up trap:** "OK, but for a production tool you'd need broader coverage." — Yes, and the way to get there isn't to hand-write 90 more rules; it's to crowdsource them, the way Semgrep does, with each contribution coming with a test and a citation. That's a community pattern, not a single-developer pattern; it earns time only after AlloyCode has users.

**Reference:** [`orchestrator/src/code_analyzer/rules/`](../orchestrator/src/code_analyzer/rules/) — the 10 YAML files; [`NORTHSTAR.md`](NORTHSTAR.md) Part IV ("More YAML rules beyond the current 10").

---

## Q8 — Walk me through GT-01 (résumé screening) end-to-end.

**Setup:** "Pick one of your golden cases and walk me through what happens when AlloyCode scans it."

**Answer:** GT-01 is a Python repo that imports a CV-ranking library and POSTs ranked candidates to a downstream HR system. (1) `ImportScanner` flags `cv_screening` / ML-classification imports and records them in the library map. (2) `AstScanner` finds the `rank_candidates(candidates)` function as a "decision surface" — it returns a sorted list with no human-review hook. (3) The LLM filter passes on it (real production code, not a test mock). (4) `AstRulesScanner` matches rule `AI-005` (automated decision endpoint affecting employment) and rule `AI-007` (no override mechanism). (5) The deterministic classifier sees rule_id `AI-005` triggering Annex III(4) employment + GDPR Article 22 (automated profiling), assigns `HIGH_RISK`, and the `LegalResearchAgent` queries Neo4j for AIACT_ART_6 + GDPR_ART_22 + the connected Recitals and EDPB guidelines. (6) The narrative generator writes the executive summary and remediation steps; `synthesize` packages everything into a `ScanReport` JSON.

**Follow-up trap:** "How do you know GT-01 is a representative input?" — Because it maps cleanly to Annex III §4 ("employment, workers management"), which is one of the eight high-risk categories named in the regulation itself. The same logic runs for GT-06 (credit scoring → Annex III §5 "access to essential private services" + GDPR Article 22). Both are named categories in the regulation; both are exactly the kind of system the regulation was written to govern.

**Reference:** [`orchestrator/data/golden/test_cases.json`](../orchestrator/data/golden/test_cases.json) — the case definitions; [`orchestrator/src/code_analyzer/rules/`](../orchestrator/src/code_analyzer/rules/) for rules `AI-005` / `AI-007`; [`orchestrator/src/agents/risk_classifier.py`](../orchestrator/src/agents/risk_classifier.py) for the category logic.

---

## Q9 — Why was the `monitor/` module decommissioned?

**Setup:** "Your earlier architecture had a third service for drift detection, bias monitoring, and Prometheus. It's gone. Why?"

**Answer:** Honest audit — it produced no usable signal in a portfolio demo without continuous production traffic. Drift detectors need a baseline distribution; bias monitors need labelled outcomes; Prometheus needs a workload that emits metrics. None of those existed because AlloyCode is a batch-scan tool, not a continuously-served model. We could have kept the module as a "look, observability" prop, but that's exactly the kind of LinkedIn-buzzword exhibit the audit (§3.4) says no longer survives follow-up.

**Follow-up trap:** "But shouldn't a compliance tool have observability?" — Yes — *operational* observability (per-scan cost, p95 latency, eval pass-rate). Not *ML* observability (drift, bias, prediction distributions), which is what the decommissioned module was. Operational observability is in [`cost_tracker.py`](../orchestrator/src/cost_tracker.py) and structured logs; the ML half wasn't useful and didn't survive the cut.

**Reference:** [`SYSTEM.md`](SYSTEM.md) §1 (the architecture diagram with monitor explicitly absent); [`design-evolution/v02-static-scanner-pivot.md`](design-evolution/v02-static-scanner-pivot.md) §Consequences ("Decommissioned: `monitor/`").

---

## Q10 — What's the worst part of this project?

**Setup:** A senior engineer's standard last question. The trap is to dodge it.

**Answer:** Three honest weaknesses. (1) **The orchestrator's Postgres connection is degraded on the live URL** — KE + frontend are healthy on Cloud Run; the orchestrator's `/health` reports `database: unavailable` so end-to-end scans can't yet persist. Fix is investigation-pending (BUG_LOG DL-024); not blocking the architecture demo, but the "click here, scan a repo" story isn't complete. (2) **Multimodal retrieval is designed but not built.** ColPali integration is scaffolded at `knowledge_engine/src/multimodal/` and there's a v05 design record, but no GPU box, no PDFs ingested, no MaxSim benchmark. Layout-heavy content in EU AI Act Annexes is currently invisible to the text-only path. Honest position: "designed and scaffolded, not deployed — production text path already hits 81.8% citation recall@15 hybrid without it." (3) **The headline citation-recall number is 81.8% hybrid on a 25-query golden set, but entity recall is only 25%** — because the abstract Concept/RiskCategory nodes have short labels whose embeddings don't compete with paragraph-length article embeddings. Fix is structural (separate entity-name fuzzy match arm), not a bug. **A complete EU AI Act compliance tool would need 100+ rules and a partnership with an actual law firm** to maintain the rule corpus against amendment cycles. AlloyCode is a sharp 10-rule MVP demonstrating the architecture; productionising it is a different project with different ownership.

**Follow-up trap:** "What about test coverage? Security? Multi-language support?" — Multi-language is correctly deferred (NORTHSTAR Part IV — Python+JS covers the AI ecosystem; polyglot expansion is breadth, not depth). Test coverage exists at the unit level for the agents and classifier ([`orchestrator/tests/unit/`](../orchestrator/tests/unit/)); the gap is integration-level coverage tying golden cases to expected reports, which is the eval work in (2). Security is out-of-scope for a portfolio scanner that only reads code, never writes or executes it.

**Reference:** [`NORTHSTAR.md`](NORTHSTAR.md) Part III (the punch list with the same gaps named); [`07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) §6.1 (the external audit naming the same gaps).

---

## Q11 — How do you measure RAG quality? (added 2026-06-19)

**Setup:** "RAGAS, recall@k, faithfulness — pick a metric and tell me your number."

**Answer:** Three numbers, all reproducible from repo. (1) **Citation recall@15 on a 25-query golden set: 81.8% hybrid RRF, 72.7% vector-only, 21.2% graph-only.** Hybrid beats vector by 9 percentage points, which validates RRF — without that delta, the hybrid path wouldn't be earning its place. (2) **Context relevance@15 (RAGAS-equivalent): 45.9% mean.** Computed with a Gemini 2.5 Flash judge over 375 retrieved-entity rows; we didn't install the `ragas` package because it pulls in LangChain + OpenAI + pandas. (3) **The most interesting datapoint is the invented-constraint cases — GT_24 (consent form file-size) and GT_25 (HIPAA in EU) both score 7% context relevance.** That's the system correctly refusing to fabricate relevant-looking retrievals for nonsense questions; low is the right outcome there.

**Follow-up trap (the "why not RAGAS?" question):** "You should've used the real RAGAS library." — We could have, but RAGAS pulls in LangChain + OpenAI + pandas + 100 other deps for what is conceptually four LLM-judge prompts. We chose to implement the same metrics directly against the project's existing Gemini client. Net: faster install, fewer attack surfaces, same metric definitions. The script is in repo; the judge prompts are inspectable. A skeptic can rerun it.

**Reference:** [`devlog/METRICS.md`](METRICS.md) for the full breakdown; [`../knowledge_engine/scripts/12_eval_three_mode.py`](../knowledge_engine/scripts/12_eval_three_mode.py) for the 3-mode runner; [`../knowledge_engine/scripts/13_eval_ragas_equivalent.py`](../knowledge_engine/scripts/13_eval_ragas_equivalent.py) for the RAGAS-equivalent script.

---

## Cheat sheet — citable numbers

For when a fast-tempo question demands a number rather than a sentence:

| Number | What it is |
|---|---|
| **81.8%** | Citation recall@15 — hybrid RRF on the 25-query golden set |
| **72.7%** | Citation recall@15 — vector_only (the hybrid delta) |
| **45.9%** | Context relevance@15 — RAGAS-equivalent (Gemini-judge precision) |
| **25** | Golden queries (7 single-hop / 11 multi-hop / 7 out-of-scope) |
| **2,301** | Nodes in the Neo4j knowledge graph |
| **4,423** | Relationships in the KG |
| **2,198** | Vector embeddings (3072-dim `gemini-embedding-001`) |
| **7** | Vector collections (articles / obligations / recitals / definitions / concepts / rights / interpretive) |
| **84** | Cross-regulation `COMPLEMENTS` edges (5 interaction types) |
| **10** | YAML detection rules |
| **6** | Stages in the scanner pipeline |
| **4** | Nodes in the LangGraph supervisor |
| **3** | Services (frontend + orchestrator + knowledge engine) |
| **3** | Datastores (Postgres + Redis + Neo4j) |
| **0** | Orphan nodes in the KG (100% connectivity) |

---

## When this doc gets updated

- When a Part III item in [`NORTHSTAR.md`](NORTHSTAR.md) lands — the answer to Q10 ("what's the worst part") changes.
- When a new audit lands and reframes the gaps.
- When an interview surfaces a question this guide doesn't pre-answer — add it.
- When the architecture changes in a way that breaks any answer — update the answer and the citable reference.

This is *living* (per its frontmatter), not frozen. Bump `last_verified:` on every edit.
