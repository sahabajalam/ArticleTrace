# AlloyCode — Calibration Plan (Phase 3: Jun 9 – Jun 22)

**Path:** `D:\60 Days\Projects\Portfolio_Series\Project_1_EUAI_GDPR\Project_1_EUAI_GDPR\`
**Current state:** local docker-compose working, Cloud Run-ready, 5+ weeks paused since Apr 29
**Calibration goal:** wake-up + ship public demo + close RAG/multimodal/eval gaps in 2 weeks

---

## 1. Current state — verified

Static compliance scanner. GitHub URL → 10 YAML scanner rules (tree-sitter + content matching) → file:line findings mapped to EU AI Act articles → LangGraph multi-agent enrichment (risk classifier, technical assessor, legal research, doc generator) → JSON / Markdown report with human-in-loop approval on Critical findings.

**Stack:** Python 3.11, FastAPI, LangGraph, Gemini 2.5 Flash, **Neo4j 5** with 2,301-node regulatory graph + native HNSW vector index over 2,198 embeddings, Postgres (asyncpg/SQLAlchemy), Redis, tree-sitter, GitPython, Next.js 16 + React 19 + TypeScript + Tailwind 4 + framer-motion + react-force-graph-2d + react-markdown. Multi-tier: 3 services (Orchestrator :8004 / Knowledge Engine :8001 / Frontend :3000) via docker-compose.

**Scanner rule pack:** 10 YAML files covering biometric libs, LLM SDKs, decision endpoints, transparency, PII handling, training data sources, audit logs, prohibited practices, real-time biometric ID, override gaps. Adding a rule is YAML-only — no code change.

**Knowledge engine:** Neo4j hybrid retrieval (graph traversal + vector via Reciprocal Rank Fusion). API at `knowledge_engine/src/api/main.py` exposes vector search, graph traversal, hybrid reasoning endpoints.

**Multi-agent enrichment:** LangGraph at `orchestrator/src/agents/` — risk classifier → technical assessor → legal research → doc generator. Human-in-loop gate on Critical findings.

**Deployment state:** Local docker-compose works end-to-end. Cloud Run config exists (`gcp.ps1` orchestrator). NOT publicly deployed yet — PORTFOLIO_ENTRY.md notes "pending Cloud Run deploy."

**Recent activity:** 4 commits (squashed history); newest 2026-04-29. **5+ weeks paused.** Wake-up cost is real — first ~2 hours of Phase 3 is just re-orienting.

**Novel patterns:**
1. Rules-as-data YAML pattern (Semgrep-style; 10 rules, runtime-loaded).
2. LLM-out-of-detection-hot-path — deterministic scanners produce findings; Gemini only narrates after.
3. Pivoted from free-text RAG → static scanning after observing failure modes; ships clean not aspirational.
4. Decommissioned monitor module — recognised that Prometheus/drift/bias produced no signal in portfolio demo; removed.
5. Vector-store consolidation journey (ChromaDB → JSON → Weaviate → Neo4j HNSW) — a defensible architectural story.

---

## 2. JD coverage today

This project carries: Python (82.5%), RAG (35.9%), Vector DBs (10.8% — Neo4j HNSW), Agents (14.4% — LangGraph), Prompt Engineering (29.1%), LLM Integration (25.4%), TypeScript/React (23.4%), FastAPI (10.7%), PostgreSQL (9.3%), Docker (31%), Cloud Run (cloud signal), Responsible AI / regulatory compliance (rising). Domain specificity is strong — compliance is a regulated-industry signal.

**Holes:** No public demo URL (highest-leverage fix). No multimodal handling — reg PDFs have charts and tables this project can't parse. No evaluation harness (RAGAS would be the natural fit over the knowledge engine). No cost ledger per scan. CI/CD is minimal (one keep-alive workflow).

---

## 3. Gaps this project will fill

1. **Multimodal RAG (rising 2026 differentiator)** — regulatory PDFs have embedded charts, tables, and forms. ColPali fits the Neo4j knowledge engine cleanly without breaking the existing text retrieval path.
2. **RAGAS evaluation framework** — the knowledge engine is the most natural RAGAS target across all three projects.
3. **Live public demo URL** — Cloud Run is config-ready; just needs the deploy + a path that a recruiter can hit in 5 seconds.
4. **Cost ledger per scan** — recruiters love cost numbers; current scans don't track per-scan Gemini spend.
5. **Domain specificity** — pick **ONE regulatory domain** to ship demo over (recommended: 10 public UK fintech repos against FCA + GDPR; demonstrate UK-overlay for visa-relevant applications).

---

## 4. Recommended additions (priority order)

### 4.1 Deploy to public Cloud Run URL with a 10-repo demo gallery
- **Goal:** one URL a recruiter can open; sees AlloyCode scan results across 10 well-known repos, with file:line links and regulatory article citations.
- **What:**
  - Deploy via `gcp.ps1` (existing). Target `europe-west2` for visa-relevant latency.
  - Pre-scan 10 public repos (mix: 5 UK fintech, 3 healthcare, 2 generic AI) into `data/precomputed_scans/<org>_<repo>.json`. Show as a gallery on landing page.
  - Add a "Scan a public GitHub repo" form on the landing page — rate-limited (1/min/IP) to control Gemini cost.
  - README front-loads the demo URL + 30-second Loom + the comparison table from §5 below.
- **Differentiator phrasing:** "Pre-scanned gallery: 10 production repos against the EU AI Act + GDPR. Average 4.7 findings per repo; 23% of findings link to Article 14 (transparency) — the most-commonly-missed obligation in fintech."
- **Effort:** 4–6 hr (deploy + gallery + rate limiter + README)
- **Defensibility check:** can you whiteboard the 3-service architecture (Orchestrator / Knowledge Engine / Frontend) in 5 min? Can you defend why detection is LLM-free?

### 4.2 Multimodal extension: parse regulatory PDFs via ColPali
- **Goal:** handle the 30%+ of regulatory documents that have content in charts, tables, and forms that text-only RAG misses.
- **What:**
  - Add `knowledge_engine/src/multimodal/` with `colpali_indexer.py` (document-native PDF page → image embeddings via ColPali) and `multimodal_retrieval.py` (MaxSim scoring `score = Σᵢ max_j sim(qᵢ, dⱼ)`).
  - Ingest 5 EU AI Act + GDPR official PDFs (Annex III, Article texts with embedded tables/diagrams).
  - Wire into existing hybrid retrieval as a third path alongside graph traversal + vector similarity — return type stays the same.
  - Comparison table: 10 questions that require visual understanding (e.g., "what's the maximum fine for prohibited practices?") answered by (a) text-only RAG, (b) ColPali, (c) hybrid. Target: ColPali beats text-only by ≥15% on the 10-question multimodal slice.
- **Differentiator phrasing:** "ColPali multimodal retrieval reads tables and charts in EU AI Act PDFs that text-only embedding misses; +20% accuracy on the 10-question multimodal benchmark vs text-only baseline."
- **Effort:** 8–10 hr (largest add in Phase 3)
- **Defensibility check:** can you explain MaxSim scoring vs single-vector cosine in 90 seconds? Can you defend ColPali over a layout-aware OCR + text-RAG baseline?

### 4.3 RAGAS evaluation harness over the knowledge engine
- **Goal:** measure retrieval quality with numbers, not assertion.
- **What:**
  - Create `knowledge_engine/tests/eval/` with 30-question golden set: 12 single-hop (find one article), 10 multi-hop (apply Article X under regime Y), 8 out-of-scope (refuse).
  - Wire RAGAS metrics: faithfulness, answer relevance, context precision, context recall. Run via `python -m knowledge_engine.eval.ragas_run`.
  - Compare three retrieval modes side-by-side: vector-only, graph-only, hybrid RRF. Each across the 30 questions.
  - Add to CI: GitHub Action runs the eval on every PR to `knowledge_engine/`; fails if any metric drops >5% from baseline.
- **Differentiator phrasing:** "30-question golden set with RAGAS metrics; hybrid retrieval beats vector-only by 18% on context precision for multi-hop legal questions. Eval runs in CI on every PR."
- **Effort:** 4–5 hr
- **Defensibility check:** can you explain RAGAS faithfulness vs answer-relevance in 60 seconds? Can you defend the 30-question split (12 single-hop / 10 multi-hop / 8 out-of-scope)?

### 4.4 Cost ledger per scan
- **Goal:** answer the cost-optimisation interview question with real numbers, not estimates.
- **What:**
  - Add `orchestrator/src/cost_tracker.py`: wrap every Gemini call to record (model, input tokens, output tokens, calculated cost from current pricing) → write to scan-result JSON under `cost` field.
  - Render in the frontend findings report as a footer: "This scan cost £0.012 (Gemini 2.5 Flash: 4 calls, 12,800 tokens)."
  - Aggregate in the gallery: "Average scan cost across 10 repos: £0.018."
- **Differentiator phrasing:** "Per-scan Gemini cost ledger surfaces to the user. Average scan: £0.018 across 10 production repos; max: £0.041 (large monorepo)."
- **Effort:** 2–3 hr
- **Defensibility check:** can you defend why per-scan cost tracking matters more than per-month rate? Can you sketch the cost-vs-quality tradeoff for Gemini 2.5 Flash-Lite vs Flash on this workload?

### 4.5 Two-rule precision/recall study (optional, time-permitting)
- **Goal:** demonstrate scanner-rule quality with a number.
- **What:**
  - Pick 2 of the 10 YAML rules (e.g., "PII handling" and "training data sources").
  - Manually label 30 known-positive + 30 known-negative repo files per rule (60 per rule, 120 total).
  - Run scanner; compute precision/recall per rule.
  - Add to README: "Rule X precision 0.91 / recall 0.84 on 60 labeled samples; false-positives concentrated in test fixtures (acknowledged limitation)."
- **Differentiator phrasing:** "Rule-by-rule precision/recall on 60 labeled samples each. Demonstrates scanner quality without overclaiming the full 10-rule pack."
- **Effort:** 3–4 hr (mostly manual labeling)
- **Defensibility check:** can you defend the choice of 60 samples? What confounds are baked in?

---

## 5. Differentiator artifact

**A single README section titled "False-positive / false-negative analysis across 10 production repos"** with three columns: repo, findings count, FP rate (from 4.5 above on 2 rules), with a one-line failure-analysis takeaway per rule. Combined with:

- The 10-repo demo gallery (interactive)
- The 10-question multimodal benchmark table (text-only vs ColPali vs hybrid)
- The RAGAS dashboard screenshot
- The per-scan cost ledger averages

This combination answers four interview questions: "How do you measure RAG quality?", "How do you handle multimodal docs?", "How do you know your rules aren't noisy?", and "What does this cost?"

---

## 6. What NOT to add

- ❌ More YAML scanner rules — 10 rules is enough to demo. Going to 30 is 1 week of legal research with diminishing recruiter signal.
- ❌ Private repo support — adds OAuth + GitHub App overhead, low recruiter signal.
- ❌ Multi-language scanners — Python AST coverage is enough; adding TS/Java AST is weeks of work.
- ❌ PDF export of reports — Markdown export is already there.
- ❌ VS Code extension — fun but 1+ week of work, low recruiter signal vs hosted demo.
- ❌ Re-introducing the monitor module — was decommissioned for good reasons (no signal in portfolio demo). Don't re-add.
- ❌ AWS overlay — defended verbally; same as other projects.
- ❌ Real-time scanning on file save — batch scanning is the right pattern for compliance auditing.
- ❌ Switching off Neo4j to something simpler — Neo4j is the differentiator (Graph DBs at 10.8% in JDs); keep it.

---

## 7. Defensibility checklist

- [ ] **Whiteboard the 3-service architecture** in 5 min: Orchestrator / Knowledge Engine / Frontend, their ports, the data flow on a scan request.
- [ ] **Defend rules-as-data** against the obvious alternative (rules as Python code) — extensibility, testability, non-engineer contributors.
- [ ] **Defend the pivot story** — free-text RAG → static scanning, the three failure modes that drove it.
- [ ] **Defend ColPali vs OCR+text-RAG** for regulatory PDFs.
- [ ] **Defend the vector-store consolidation journey** (ChromaDB → JSON → Weaviate → Neo4j HNSW) — what each step learned.
- [ ] **Defend RAGAS metric choice** — faithfulness vs answer-relevance vs context-precision; when each fails.
- [ ] **Explain the Reciprocal Rank Fusion math** — how scores combine across graph + vector + BM25.
- [ ] **Defend why detection stays LLM-free** — auditability, cost, regulator-acceptability.

**Top 10 likely interview questions:**
1. Walk me through a scan end-to-end (URL submit → findings JSON).
2. Why Neo4j over PostgreSQL with pgvector?
3. How does ColPali differ from CLIP for document retrieval?
4. RAGAS faithfulness — what does it actually compute?
5. Tree-sitter vs LSP — when does each fail?
6. How do you handle EU AI Act updates? (Hint: YAML rules are versioned.)
7. Defend a deterministic-first design — when is LLM-first actually better?
8. Multi-agent enrichment — what does each of the 4 agents add that a single GPT-4 call wouldn't?
9. The 2,301-node regulatory graph — how was it constructed? Is it auditable?
10. The 10-repo demo — pick one finding, walk me through why the scanner flagged it.

---

## 8. Time budget

| Track | Weekly hours | Total project hours | Calendar weeks |
|---|---|---|---|
| Low (15) | ~12 | ~22 hr | 2 weeks tight (drop 4.5 precision/recall study) |
| Mid (20) | ~15 | ~28 hr | 2 weeks (default) |
| High (27–30) | ~20 | ~35 hr | 2 weeks comfortable; add the FP/FN study + UK-overlay swap |

---

## 9. Order of operations within Phase 3 (Jun 9 – Jun 22)

### Week 4 (Jun 9 – Jun 15)
| Day | Block A (project) | Block B (apply) |
|---|---|---|
| Mon Jun 9 | Re-read README + ARCHITECTURE + recent commits — 5-week wake-up | 4 apps + 1 mock |
| Tue Jun 10 | Whiteboard 3-service arch cold (defensibility test) | 4 apps |
| Wed Jun 11 | Deploy to Cloud Run + 10-repo gallery scaffold (Add 4.1, part 1) | 4 apps |
| Thu Jun 12 | Pre-scan 10 repos; landing page polish + Loom (4.1, part 2) | 4 apps |
| Fri Jun 13 | Public demo URL live; README front-load | 4 apps + 1 mock |
| Sat Jun 14 | Buffer / Sunday prep | rest |
| Sun Jun 15 | Sunday review in `_log.md` | rest |

### Week 5 (Jun 16 – Jun 22)
| Day | Block A (project) | Block B (apply) |
|---|---|---|
| Mon Jun 16 | ColPali setup + 5 PDFs ingested (Add 4.2, part 1) | 4 apps |
| Tue Jun 17 | MaxSim retrieval wired into hybrid; 10-question benchmark drafted (4.2, part 2) | 4 apps |
| Wed Jun 18 | Multimodal benchmark run; comparison table in README (4.2, part 3) | 4 apps |
| Thu Jun 19 | RAGAS golden set drafted (30 questions); first eval run (Add 4.3) | 4 apps + 1 mock |
| Fri Jun 20 | RAGAS in CI + cost ledger (Add 4.4) | 4 apps |
| Sat Jun 21 | (Optional) FP/FN study on 2 rules (Add 4.5) OR blog post on the multimodal benchmark | rest |
| Sun Jun 22 | Phase 3 retro + start Phase 4 prep | rest |

---

## 10. Apply-to-jobs hook

| Resume variant | Companies (Tier 1) | Pitch one-liner using this project |
|---|---|---|
| A Agentic / Solutions | Anthropic, Cohere, Mistral, EY UK | "Built AlloyCode — static EU AI Act + GDPR scanner with multi-agent LangGraph enrichment. Live demo scans 10 public repos with regulatory citations at file:line precision." |
| C FDE / Customer Eng | EY UK FDE practice, Isidor, OpenAI London FDE, Anthropic Customer Eng, Google Cloud London | "Compliance audit as a service. Pivoted from free-text RAG to static analysis after recognising 3 failure modes; shipped clean, not aspirational. Live demo + RAGAS eval on 30-question golden set." |
| Solutions Architect | Accenture, Deloitte, BJSS, GSK, AstraZeneca | "Hybrid retrieval over a 2,301-node regulatory knowledge graph + ColPali multimodal for tables/charts in EU AI Act PDFs. Reciprocal Rank Fusion across graph traversal + vector + BM25." |

**Specific JD keywords this project provides:** RAG, hybrid retrieval, GraphRAG, Neo4j, ColPali, multimodal, RAGAS, Reciprocal Rank Fusion, LangGraph, multi-agent, EU AI Act, GDPR, compliance, static analysis, tree-sitter, AST, knowledge graph, Cypher, vector embeddings, HNSW, cost optimization.

---

## Cross-references

- Verified inventory and JD frequency table → [`README.md`](README.md)
- Phase 3 schedule and weekly milestones → [`../00_PLAN.md`](../00_PLAN.md) §9
- Visa-relevant Tier-1 companies (especially EY UK FDE) → [`../03_APPLICATION_STRATEGY.md`](../03_APPLICATION_STRATEGY.md) §1
- The "ColPali multimodal" reference in original 10Weeks plan — superseded; that scope now lands here.
