# 07 — Market Fit & Portfolio Audit (June 2026)

> **Status:** living analysis · **Compiled:** 2026-06-16 · **Author:** Claude (research + repo audit session)
> **Intended home:** `D:\60 Days\10Weeks\07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`
> **Companion to:** `04_MARKET_RESEARCH.md` (frozen May-2026 snapshot — this doc re-validates it live), `03_APPLICATION_STRATEGY.md`, `05_VISA_AND_SPONSORSHIP.md`, `project_calibration/`.
>
> **How to read this:** §2–§3 are the live market + JD picture. §4 checks whether `10Weeks` is still pointing at the right target. §5 is the "what it actually takes" synthesis. §6 audits each repo against the requirements with ranked, cheapest-first gap fixes. §7 is the portfolio-level coverage matrix and the priority order. §8 lists sources.

---

## 1. Purpose & method

This document answers five questions, in order:

1. What is the **current UK job market** for AI/ML engineering doing (June 2026)?
2. What do **junior-level AI-engineer (and adjacent) job descriptions** actually require in 2026?
3. Are the assumptions baked into `10Weeks` **still relevant**?
4. What does it **actually take** to land one of these roles?
5. How do the **four portfolio projects** cover those requirements, where are the gaps, and what fills them?

**Method.** Live web research on 2026-06-16 (eight search passes across market-contraction data, JD skill analyses, salary benchmarks, visa thresholds, interview-integrity studies, EU AI Act enforcement, and clinical-NLP hiring), plus a direct code-and-docs audit of all four repositories on the `D:` drive. Repo claims were checked against each project's own `SYSTEM.md` / `PROJECT_OVERVIEW.md` / `README.md` and directory structure — where a project doc disagreed with the code or with `10Weeks`, that is flagged.

A caveat worth stating plainly: job-board counts and salary figures are point-in-time and source-dependent. Where sources disagree (and they do, especially on salary), the range is given rather than a single number.

---

## 2. UK market state — June 2026

### 2.1 The contraction is real and well-documented

The entry-level squeeze that `04_MARKET_RESEARCH.md` described in May is confirmed by multiple independent sources:

| Signal | Figure | Source |
|---|---|---|
| UK tech **graduate** jobs vs 2024 | down **46%**, a further **53%** projected for 2026 | Institute of Student Employers (via TechRadar) |
| UK **entry-level** jobs since ChatGPT (2022) | down **32%**; entry-level now only **25%** of the total UK market | Adzuna (via The Guardian / Notebookcheck) |
| Junior/entry-level roles, last 18 months | down **up to 35%**, tech steepest | Robert Walters Market Intelligence |
| Entry-level **tech postings** 2023→2024 | down **67%** | Stanford Digital Economy Lab |
| 18–24 unemployment | ~**14.5%** | LSE Business Review (ONS-based) |
| Big-4 graduate cohort cuts | KPMG **−29%**, Deloitte **−18%**, EY **−11%**, PwC **−6%** | The Telegraph (via People Management) |
| AI skill demand in tech listings | **+62%** even as entry-level fell | Plant & Works Engineering |

The mechanism is consistent across commentary: routine entry-level tasks (basic research, summarisation, boilerplate coding, first-pass analysis) are the most automatable, so firms are holding experienced staff and cutting the bottom rung. This is the backdrop `10Weeks` is operating against, and it has not eased since May.

### 2.2 …but junior AI roles do exist, and the count is rising

The contraction is in *generic* entry-level work. Demand for *AI-specific* skills is moving the other way:

- Glassdoor listed **325 "junior AI engineer" roles in London in June 2026**, up from **276 in May** — a real month-on-month rise in exactly the target segment. UK-wide "junior AI" sat at **~1,551**.
- Roles mentioning **"LLM" or "RAG" grew ~340% since 2024**, while generic "machine learning" postings **declined ~18%** (MirrorCV's analysis of 387 listings). The label on the door matters.
- **71% of US tech job postings now require some AI fluency** (+181% YoY, Dice) — a leading indicator for the UK.
- Hiring concentrates in London (Kings Cross AI cluster — Anthropic/OpenAI orbit, ARIA, Compare the Market, C3 AI's FDE practice, Citi, Moody's). Forward-Deployed Engineer is a genuine and large category: one aggregator listed **2,600+ FDE roles UK-wide**, clustered in London, Manchester, Belfast, Glasgow.

**Implication for `10Weeks`:** the strategy of targeting AI-labelled roles (Agentic / LLMOps / FDE / AI-ML) rather than generic "data analyst" is correct and is where the few growing pockets are.

### 2.3 Salary vs the visa floor — the constraint is access, not pay

Entry/junior "AI engineer" salary sources vary widely by definition, but they cluster well **above** the £33,400 new-entrant visa floor and the £40,000 target:

| Source | Band | Notes |
|---|---|---|
| CareerMetrics (Hays 2026 data) | **£35,698** | "Trainee AI Engineer" average — the realistic true-entry floor |
| Lorien | **£35k–£50k** entry | mid £60k–£90k |
| Glassdoor (UK, "entry-level AI engineer", n≈3,048) | avg **£72k**, typical **£49.6k–£110.7k** | inflated by senior roles miscategorised as "entry" |
| Knowledge Academy | **£54.8k–£70.7k** junior | |
| Morgan McKinley (London AI/ML specialist) | **£75k–£90k** average | |

**Takeaway:** essentially every genuine AI-engineering role clears the £33,400 floor, and most clear the £40,000 target comfortably. The binding constraint for this hunt is **getting the offer at all** (access through the contraction + the visa filter), not negotiating above the threshold. `05_VISA_AND_SPONSORSHIP.md` already frames this correctly.

### 2.4 The visa filter — validated

Confirmed against current (post-22 July 2025) Immigration Rules:

- **General threshold: £41,700** (or the going rate, whichever is higher).
- **New-entrant rate: £33,400** (70% of standard, or 70% of going rate, whichever higher), capped at **4 years** on the new-entrant rate.
- **Eligibility for new-entrant:** under 26 **OR** switching from a Student/Graduate visa. Sahabaj is 30 but qualifies via the Graduate-route switch — this is the most common path and is explicitly named in the rules.

So the workspace's salary floor and visa logic are accurate. The practical filter remains: **only apply where the employer holds a sponsor licence**, and never accept a base below £33,400 even with bonus/equity sweeteners (bonuses are visa-irrelevant).

---

## 3. What a junior AI-engineer JD actually requires (2026)

### 3.1 The canonical skill stack

Across the JD analyses reviewed (a "real Agentic AI Engineer" posting dissected on Medium; AY Automate's 15-skills list; MirrorCV's 387-listing study; the upGrad RAG-engineer spec; Dice's LangChain listings), the same stack recurs:

- **Orchestration:** LangGraph / LangChain (LlamaIndex secondary); **MCP** (Anthropic donated it to the Linux Foundation in Dec 2025; now the de-facto agent-tool protocol); A2A; function calling; structured outputs.
- **Retrieval:** RAG, **RAGAS** for eval, **hybrid retrieval** (BM25 + vector + reranking), vector DBs (Qdrant / Pinecone / Weaviate / **pgvector**), graph DBs (**Neo4j** / Memgraph), embedding-model versioning, chunking strategy, **reranking by default**.
- **Eval & observability:** evaluation harnesses, judge calibration, **Langfuse / Phoenix / Helicone**, **OpenTelemetry** tracing — "if you can't measure it, you can't ship it."
- **Cost & latency:** caching, tier routing (cheap model first, expensive model only when needed) — quoted as saving 40–70% of production spend; streaming / token-level ops for perceived latency.
- **Fine-tuning:** **QLoRA is the production default** (4-bit base + LoRA adapters); **DPO has displaced RLHF** for alignment in most production settings. Hugging Face (Transformers / PEFT / TRL) is the default toolchain.
- **Safety:** guardrails, **prompt-injection defence** (now framed as a compliance requirement).
- **Foundations assumed, not differentiating:** Python, FastAPI, Docker, a cloud (AWS/GCP/Azure), basic Kubernetes, CI.

### 3.2 What "junior" means in 2026

A widely-cited hiring guide (TekRecruiter, "AI Engineer Job Description 2026") draws the line cleanly: **a junior AI engineer should not own architecture.** The junior brief is **execution** — building against APIs, wiring pipelines, integrating models, writing test coverage, and basic deployment. Architecture ownership, incident command, and retrain/rollback judgement are mid/senior expectations.

This matters for positioning: the portfolio should demonstrate **shipping and maintaining** behaviour (a system that runs, has tests, has a cost ledger, degrades gracefully) rather than over-claiming architectural authorship. All four projects here are *over*-built for "junior" in scope — the risk is not "too thin," it's "claims that can't survive a follow-up question" (see §3.4).

### 3.3 The resume formula and the ATS reality

MirrorCV's 2026 formula, derived from 387 listings, is explicit about the ranking of evidence:

> **production metrics (latency, throughput, cost reduction) > model metrics (accuracy, F1, BLEU) > framework fluency > academic credentials.**

Frontier-lab and scaling-startup screens look for **production-deployment evidence first** — not Kaggle medals, not certificates, not paper counts. And **48% of employers now use AI-powered resume screening (projected 83%)**, so ATS-legible keyword coverage of the §3.1 stack is a gate before a human ever reads the CV.

This is the single most actionable market fact for the portfolio: **every project needs at least one quantified production metric surfaced** (cost-per-call, p95 latency, eval pass-rate, throughput). Three of the four projects have the data but don't surface it prominently (see §6).

### 3.4 The interview-integrity shift — why "defensibility" is the whole game

This is the strongest validation of the `10Weeks` core thesis. The interview format has changed because cheating has become the baseline:

- The **Fabric study** (19,368 live interviews, Jul 2025–Jan 2026): **38.5% cheating overall, 48% in technical roles**, up from <10% in mid-2025.
- **59% of hiring managers** now suspect candidates are faking ability with AI; **71% of job seekers admitted** to some form of it.

The detection methods all reward genuine understanding and punish recited answers:

- **Uniform response latency** — AI tools take a constant 3–5s on every question; human thinking time varies. A flat latency floor is the strongest behavioural tell.
- **Follow-up questions** — "if you can't explain line seven in your own words, you didn't write line seven." This is the layer cheat-tools break on.
- **Gaze / keystroke dynamics**, and most structurally: **novel / custom debugging problems** that aren't in any training set.
- The emerging format is **"pair-programming-with-AI"**: decompose an ambiguous problem (discursive, can't be faked) → implement *with* AI allowed → the interviewer scores *how you prompt, iterate, and discard*.

**This is exactly the bet `10Weeks` makes:** calibrate four projects you can defend line-by-line rather than build many you can't, and rehearse explaining them under follow-up pressure. The market has moved the goalposts to where that bet pays. The interview-prep study surface in Project 4 (§6.3) is the operational expression of this and is the most directly market-aligned piece of the whole system.

---

## 4. Is `10Weeks` still relevant?

Short answer: **the strategy is sound and the frozen May snapshot largely holds. Three things need correcting.**

**What's confirmed.** The contraction (§2.1), the AI-skill demand divergence (§2.2), the salary-clears-floor picture (§2.3), the visa logic (§2.4), and above all the **defensibility-over-volume thesis** (§3.4) are all validated by independent June data. `04_MARKET_RESEARCH.md` can be treated as still-accurate; this doc is the live re-validation it asks for.

**What needs correcting:**

1. **Project 1 is mislabelled as "sparse" and deferred on a false premise.** `project_calibration/01_ArticleTrace.md`'s banner defers EU_AI_GDPR to Phase 3 because it is "sparse (empty README, no PORTFOLIO_ENTRY)." The repo audit (§6.1) shows the opposite: it is one of the **most mature** projects — three services, a 2,301-node Neo4j knowledge graph, a 6-scanner deterministic pipeline, a 4-agent LangGraph workflow, full Cloud Run tooling, a CI cron, *and* a `PORTFOLIO_ENTRY.md` plus a detailed devlog. The deferral may still be defensible on *focus* grounds (don't run three active projects at once), but the stated *reason* is factually wrong and should be rewritten — especially because EU AI Act compliance is a hot 2026 lane (§6.1).

2. **Project 4's calibration plan has drifted from the live product.** `02_AlloyNext.md` plans a "LangGraph rename," "ship one MCP server," and a "DeepEval harness." The live `SYSTEM.md` (verified 2026-06-14) shows: the pipeline is **still a hand-rolled `ThreadPoolExecutor` fan-out, not LangGraph**; **MCP is in "locked negative space"** (explicitly *not* to be built); and there is still no DeepEval harness. The plan and the product's own locked-scope list now contradict each other — reconcile before spending Phase-2 hours on a LangGraph rename the product owner has effectively vetoed.

3. **The migration count is a moving target and the HUNT_LIST figure is already stale.** `HUNT_LIST_FRAMINGS.md` was corrected from "34" to "39" migrations. But Project 4's own `SYSTEM.md` §3.2 now lists **migrations 017→055 (~55 forward migrations)** — and that same doc is *internally* inconsistent (its header/ASCII art still say "35"). The honest, current number is **~55**. Pick one source of truth (the migration directory itself) and quote that; "39" understates real work.

**Net:** keep the strategy; fix the three factual drifts above. None of them changes the plan's direction — they make its claims survive scrutiny, which (per §3.4) is the entire point.

---

## 5. What it actually takes to get one of these jobs

Synthesising §2–§3 into the operative levers, in priority order:

**Lever 1 — Pass the ATS gate (cheap, do first).** 48%→83% of screens are automated. Every CV variant must carry the §3.1 keywords *that are actually true of the projects*: LangGraph, RAG, hybrid retrieval, Neo4j/pgvector, MCP, QLoRA, SHAP, FastAPI, Cloud Run, evaluation/observability, cost optimisation. The projects genuinely contain almost all of these — the gap is surfacing them, not acquiring them.

**Lever 2 — Lead with production metrics, not model metrics.** Reframe every project headline around a *production* number: "p95 latency," "$/call cost ledger," "eval pass-rate in CI," "cold-start handling." Project 4 has a real measured cost ledger; Project 2 has a CI-gated eval pass-rate; Project 1 has a deterministic-vs-LLM cost separation; Project 5 has a 97% cost-reduction story. These should be the first line of each entry, ahead of AUC/ROUGE.

**Lever 3 — Be able to defend it under follow-up.** The interview is now a line-by-line interrogation designed to catch recitation (§3.4). For each project, be ready to answer "why this choice and not the alternative" for every non-obvious decision (why RRF over pure vector; why GaussianCopula over CTGAN; why HITL removed in P1 but kept in P2; why hand-rolled over LangGraph in P4; why QLoRA rank 16). Project 2 already has an `INTERVIEW_GUIDE.md` doing exactly this — **replicate that artifact for the other three.**

**Lever 4 — Show it running.** "Does the code run" is dead as an interview test, but a **live demo URL** is still the strongest single portfolio signal because it proves deployment, not just authorship. Project 2 is live; the others are not (P1 scripted-but-not-deployed, P5 built-but-unconfirmed, P4 deployed-but-no-README). Closing this is the highest-leverage portfolio work available.

**Lever 5 — Volume through the visa filter.** With access as the binding constraint, application volume against *sponsor-licensed* employers matters. The `03_APPLICATION_STRATEGY.md` cadence (≈11–17 apps/week building to conversion focus by week 6) is reasonable; the discipline is filtering to confirmed sponsors before spending a tailoring slot.

**The uncomfortable truth:** in a market down 46% at the graduate level, a 5-year career break plus a visa requirement is a real headwind. The compensating edge is a portfolio of *defensible, deployed, regulation-aware* systems in exactly the sub-segment that's still growing. That edge only works if the demos are live and the claims survive follow-ups — which is why §6's gap fixes are weighted toward "deploy + quantify + document," not "build more."

---

## 6. Project-by-project audit

Each project below: **what it is → how it covers the JD requirements → gaps → how to fill (ranked cheapest/highest-leverage first).** Coverage uses ✓✓ strong / ✓ present / ~ partial / ✗ absent.

### 6.1 Project 1 — `Project_1_EUAI_GDPR` (ArticleTrace / "Aegis")

**What it is.** A static compliance scanner for AI codebases: point it at a GitHub repo, deterministic scanners detect AI-system patterns, and they're mapped to EU AI Act + GDPR obligations with `file:line` anchors and article citations. Three services — Next.js 16 frontend, FastAPI + LangGraph orchestrator, FastAPI knowledge engine over Neo4j. **This is a mature system, not a sparse one** (correcting the `10Weeks` banner).

Verified specifics: 2,301-node / 4,423-rel Neo4j graph; 2,198 embeddings (3072-dim `gemini-embedding-001`) in Neo4j's native HNSW vector index across 7 collections; RRF hybrid retrieval; a strictly-ordered **6-scanner pipeline** (import → AST → LLM-enrich → AST-rules → content → file-pattern → cooccurrence) with **10 YAML rules** and the LLM kept out of the detection hot path; a **4-node LangGraph supervisor** (RiskClassifier [deterministic] → LegalResearch → DocumentationGenerator → synthesize); `cost_tracker`; full `gcp.ps1` Cloud Run tooling; a CI keep-Aura-alive cron; and 6 golden test cases including **GT-06 credit-scoring** and **GT-01 résumé-screening** — both **named EU AI Act Annex III high-risk categories.**

**JD coverage.**

| Requirement | Cover | Evidence |
|---|---|---|
| LLM orchestration (LangGraph) | ✓✓ | 4-agent supervisor graph |
| RAG / hybrid retrieval | ✓✓ | vector + graph + RRF fusion |
| Vector + graph DB (Neo4j) | ✓✓ | native HNSW index over 2,301-node KG |
| Static analysis / AST | ✓✓ | 6-scanner deterministic pipeline, tree-sitter |
| Cost optimisation | ✓ | LLM-out-of-hot-path + `cost_tracker` |
| Safety / governance domain | ✓✓ | the product *is* EU AI Act + GDPR mapping |
| Production deploy | ✓ (scripted) | full Cloud Run tooling, **but not live** |
| Eval | ~ | golden tests exist; no quantified retrieval/RAGAS numbers |
| Fine-tuning / MCP | ✗ | out of scope for this project |

**Market relevance.** Strong and timely. EU AI Act high-risk obligations have an **August 2026 enforcement milestone** (one source notes the high-risk timeline may have shifted to late 2027 via the May-2026 "Digital Omnibus" — treat the exact date as fluid), and Annex III explicitly covers employment decisions, credit scoring, and biometrics. A static scanner that maps code to those obligations sits on a real, intensifying compliance-engineering demand curve.

**Gaps & fills (ranked).**

1. **Deploy the demo (highest leverage, low effort).** The Cloud Run tooling is written; the demo URL is still "pending." Running `./gcp.ps1 -Action deploy` and getting a live URL converts a "scripted" claim into Lever-4 evidence. If deploy is blocked, a 60-second Loom of a real scan (a `face-api` import → AI Act Art 5 finding) is the interim.
2. **Surface quantified eval numbers.** Produce retrieval metrics (recall@k on the golden queries) and a RAGAS-style or precision number for the legal-citation mapping. Currently the rigour is architectural, not numeric — and §3.3 ranks numbers first.
3. **Clean the cruft (cheap credibility).** Empty path-with-spaces artifact dirs (`srcagents`, `.githubworkflows`, `testsunit`, etc.), `frontend/ts_errors.txt`, and the `legacy_prototypes/` tree all read as careless to a reviewer browsing the repo. Delete or `.gitignore`.
4. **Resolve the tri-naming.** ArticleTrace (code/UI) vs Aegis (portfolio docs) vs EU_AI_GDPR (directory) will confuse a reviewer. Pick one external name.
5. **Decide the HITL story.** The supervisor *removed* human-in-the-loop (deterministic findings need no pause), but "human oversight" is an EU AI Act selling point. Either re-add an approval gate for Critical findings or have the explicit rationale ready for the inevitable follow-up.
6. **Root README.** GitHub shows the root README first; copy `devlog/SYSTEM.md`'s top section there.

**Verdict:** the most *underrated* project in the set. The "sparse/deferred" framing is wrong; with a live deploy and quantified eval it is arguably promotable ahead of its current Phase-3 parking — particularly given the regulatory tailwind.

### 6.2 Project 2 — `project_2_Credit_Scorer` (AlloyMLFlow brand)

**What it is.** An explainable agentic UK consumer-credit risk engine, and the **strongest, most complete** project. **It is live:** `https://credit-scorer-f3tstm7bbq-ew.a.run.app/`.

Verified specifics: champion **XGBoost (test AUC 0.766, Brier 0.076)** selected from a 4-model leaderboard (vs LightGBM/CatBoost/LogReg); a **7-node LangGraph workflow** (validate → score → fairness → regulatory → explain → compliance → log) **with real HITL** (`human_queue`), conditional routing, and **SqliteSaver checkpointing** for audit replay; a **Neo4j regulatory knowledge graph** (18 articles: FCA Consumer Duty, UK Equality Act, UK GDPR) with **hybrid GraphRAG** (vector + graph-boost); an **applicant kNN graph** as a model-independent sanity check; an **independent compliance critic** (separate Gemini call + parallel rule-based override, revision loop cap=1); SHAP TreeExplainer; 3-layer fairness; KS/Chi² drift; SDV synthetic cohorts; an **MCP server (5 tools, stdio, Claude Desktop)**; and an **evaluation harness** (5 deterministic metrics + LLM-judge across 4–5 Likert dims, 15 golden cases, **80% pass**, CI exit-code). Docs include an honest `§15 limitations` and an `INTERVIEW_GUIDE.md`.

**JD coverage.**

| Requirement | Cover | Evidence |
|---|---|---|
| LLM orchestration (LangGraph + HITL) | ✓✓ | 7-node graph, conditional routing, checkpointing |
| RAG / hybrid retrieval | ✓✓ | Neo4j GraphRAG, vector + graph-boost |
| Vector + graph DB | ✓✓ | Neo4j native index + sentence-transformers |
| Eval & observability | ✓✓ | harness + LLM-judge + golden set, CI-gated |
| MCP | ✓✓ | 5 tools over stdio |
| Safety / fairness / compliance | ✓✓ | compliance critic + 3-layer fairness + SHAP |
| Classical ML + explainability | ✓✓ | leaderboard + TreeSHAP + calibration |
| Production deploy | ✓✓ | **live on Cloud Run** |
| Cost optimisation | ~ | tiered models, but cost not surfaced as a metric |
| Fine-tuning | ✗ | out of scope |

**Market relevance.** Excellent and double-counted: credit scoring is a **named Annex III high-risk** use case *and* an FCA Consumer Duty obligation, so the regulatory framing is real rather than decorative. Covers the Agentic, Data-Scientist, LLMOps, AI-Solutions-Architect, and Backend archetypes simultaneously.

**Gaps & fills (ranked).** Note: most are self-acknowledged in `PROJECT_OVERVIEW.md §15–16`, which is itself a defensibility asset.

1. **Run the eval with judge + retrieval enabled.** The headline "80% pass" was generated with `--no-judge --no-retrieval` (a Windows pagefile constraint). The full harness is the differentiator — fix the pagefile, run it, and quote the *complete* number. This is the cheapest credibility upgrade in the whole portfolio.
2. **Surface a cost metric.** The system is tiered (Flash-Lite) but doesn't report $/assessment. Add it to the decision packet and the portfolio entry — §3.3 ranks cost first among production metrics.
3. **Record the MCP money-shot.** A 60-second Loom of Claude Desktop calling `assess_credit_application` is, per the project's own notes, the recruiter-facing highlight — and MCP is a 2026 keyword (§3.1).
4. **Name the median-filling limitation proactively.** ~80 of 100+ features are median-filled at inference. It's documented honestly; rehearse the "production fix = bureau/Open Banking API" answer because it *will* be the first follow-up.
5. **Lower-priority, market-aligned:** an observability dashboard (it already has OTel/structlog deps), MLflow versioning, and the SQLite→Postgres move for the fairness window. None block applications; all are good "what I'd do next" interview material.

**Verdict:** the portfolio's anchor. Most of its Phase-1 calibration plan is *already done*. Remaining work is polish-to-quantify, not build.

### 6.3 Project 4 — `project_4_Job_Tracker` (AlloyNext)

**What it is.** A multi-user job-hunt operating system (Next.js 14 + FastAPI + Supabase + Gemini) with a Chrome extension and a dev-journal CLI — the **most actively-developed product** and the daily study surface for the hunt itself. `SYSTEM.md` verified 2026-06-14.

Verified specifics: FastAPI monolith, **21 routers**, `api.py` ≈ 5,378 LOC; **~55 forward migrations (017→055)**; a **Block A–I evaluator** (A–G LLM-scored, H deterministic ATS regex, I catalog-aware concept extraction) running on a **hand-rolled `ThreadPoolExecutor` fan-out** with a **real measured cost ledger** (`eval_cost_usd`, `calls_fast/smart`, `duration_ms`); pgvector embeddings (768-d); a sophisticated **`/interview-prep` study surface** — a 612-row hand-curated concept catalogue (`seed_data.py`, June-2026 refresh), a `pending_concepts` feedback loop, and per-archetype + per-concept tutorial pages with Markdown/KaTeX/Mermaid. Observability is RequestId middleware + structured logs.

**JD coverage.**

| Requirement | Cover | Evidence |
|---|---|---|
| Backend depth (FastAPI) | ✓✓ | 21 routers, 5.4k LOC, RLS, NDJSON streaming |
| Cost optimisation | ✓✓ | **measured** per-eval cost ledger + tier routing |
| Frontend product depth | ✓✓ | large Next.js app, extension, study surface |
| Function calling / grounded search | ✓ | `grounded_search` in Block D + interview prep |
| Vector / embeddings | ✓ | pgvector + concept embeddings + vector-sim feedback |
| LLM orchestration (LangGraph) | ~ | **hand-rolled fan-out, not LangGraph** |
| RAG | ~ | embeddings + concept matching, not a full RAG pipeline |
| Eval & observability | ~ | cost ledger + logs; **no DeepEval, no OTel dashboard** |
| MCP | ✗ | **explicitly locked** (negative space) |
| Graph DB | ✗ | Postgres/pgvector only |

**Market relevance.** Strong as a **Forward-Deployed-Engineer / full-stack-builder** narrative ("build → use → iterate" on a real product with paying-attention-to-cost discipline). Weaker on the *agentic-framework* keywords (LangGraph/MCP) that the Agentic archetype screens for — which is fine if it's positioned for FDE/backend rather than Agentic.

**Gaps & fills (ranked).**

1. **Write the README (cheapest, most embarrassing gap).** `README.md` is **empty** (`---`). It's the first thing a recruiter or `git clone` sees. Port the `SYSTEM.md` summary in. Highest embarrassment-to-effort ratio in the portfolio.
2. **Delete the root cruft.** A dozen `.tmp_*` scratch files and `backend.log` sit in the repo root. Remove/`.gitignore` — same careless-signal problem as P1.
3. **Reconcile the plan vs the product on LangGraph + MCP.** The product owner has put MCP in locked negative space and never did the LangGraph rename. Either (a) accept the product as-is and *drop* those Phase-2 tasks, positioning P4 as the FDE/backend exhibit, or (b) consciously override the lock. Don't spend Phase-2 hours on a rename the product has vetoed without deciding this first. **Recommendation:** drop them — P2 already carries the LangGraph + MCP keywords; P4's edge is product/cost/backend depth.
4. **Fix the internal migration-count inconsistency** (`SYSTEM.md` says both "35" and "55"). Anchor to the migration directory and update `HUNT_LIST_FRAMINGS.md` (currently "39") to the true ~55.
5. **The `/interview-prep` surface is a hidden asset — use it.** It is the operational form of the §3.4 defensibility thesis. It deserves a portfolio line and a demo, not just internal use.

**Verdict:** the best *product* but the messiest *repo presentation*. The fixes are almost entirely janitorial + positioning, not engineering. Position for FDE/backend, not Agentic.

### 6.4 Project 5 — `project_5_Finetune_MeedGeema` (MedGemma)

**What it is.** A QLoRA fine-tune of MedGemma 1.5 4B-IT that converts messy clinical notes into structured SOAP format across 20 specialties. The LoRA adapter is shipped to the HF Hub (`sahabajalam/Med_scribe_V2`), with a local copy at `models/doctor-scribe-lora/`.

Verified specifics: real training config (4-bit NF4 QLoRA, rank 16 / alpha 32, 6 target modules, ~30M trainable params = 0.69%, 500 steps on a T4, ~10h, loss curve 2.00→0.02); train/val/test JSONL splits over 20 specialties; a full `src/` layout (config, data prep, evaluation [ROUGE-L/BERTScore], Pydantic SOAP schema, FastAPI serving + lazy model cache, training, `cost_tracker`); `compare_models.py` + `evaluate_finetuned.py`; a Vite/TS comparison frontend with a **built `dist/`** and a `comparison_results.json`; CI, pre-commit, ruff, unit + integration tests. README headline metrics: **ROUGE-L 0.76, BERTScore F1 0.87, 95% format-compliance, 97% cost reduction vs GPT-4.**

**JD coverage.**

| Requirement | Cover | Evidence |
|---|---|---|
| Fine-tuning (QLoRA) | ✓✓ | the entire project; the 2026 default technique |
| HF ecosystem (PEFT/TRL/Transformers) | ✓✓ | adapter on HF Hub, PEFT 0.18 |
| Eval (task metrics) | ✓ | ROUGE-L + BERTScore + format compliance |
| Structured output | ✓ | Pydantic SOAP schema |
| Cost framing | ✓ | 97% reduction business case |
| Serving / deploy | ~ | FastAPI + Vite `dist/` built; **live deploy unconfirmed** |
| Clinical/PHI domain | ~ | SOAP framing, but data is synthetic/templated |
| LLM orchestration / RAG / MCP | ✗ | out of scope (single fine-tune) |

**Market relevance.** Clinical NLP / medical-LLM is a real niche (PHI/HIPAA, EHR, de-identification, HITL validation; pharma uses QLoRA+RAG). But most listings want a clinical background and 5+ years; true-entry roles are rare. Its best use is as the **fine-tuning evidence** that the other three lack, and as the **AI/ML-Research** framing for pharma-adjacent sponsors — not as a standalone clinical-hire pitch.

**Gaps & fills (ranked).**

1. **Fill the HF model card (highest leverage, ~30 min).** The published card (`models/doctor-scribe-lora/README.md`) is the **default PEFT auto-generated stub** — every field is "[More Information Needed]." For a project whose pitch is "a *verifiable* fine-tuning artifact," a blank public model card actively undermines it. Write a real card: base model, data, hyperparameters, the metrics, intended use, and limitations. This is the single cheapest credibility fix across all four projects.
2. **Commit a reproducible held-out eval.** `comparison_results.json` exists, but the README's headline numbers need a clear, committed, re-runnable provenance (which split, which command, which date). A reviewer who can't trace ROUGE-L 0.76 to a committed artifact will discount it.
3. **Deploy or Loom the demo.** The Vite `dist/` is built but the live URL is unconfirmed. Deploy it (the `gcp.ps1` + nginx Dockerfile are present) or record a comparison walkthrough.
4. **State the synthetic-data limitation up front.** The `raw_dataset/*.jsonl` are templated/synthetic, not de-identified real EHR text. A clinical-NLP reviewer will probe this immediately; own it ("synthetic by design, for a reproducible public demo; production needs real de-identified corpora under DUA").
5. **Fix the small inconsistencies (cheap).** Clone URLs disagree (`doctors-scribe-qlora` vs `medgeema-soap` vs `Med_scribe_V2`); the notebook named in the README (`kaggle_w_notebook.ipynb`) isn't the one on disk (`finetune.ipynb`); the cost-savings table has two different GPT-4 annual figures. Each is a minor "didn't proofread" tell.

**Verdict:** technically real and the portfolio's only fine-tuning exhibit, so it earns its place. But its public face (the HF model card) is currently empty, which is the worst possible state for a "verifiable artifact" — fix that first.

---

## 7. Portfolio-level synthesis

### 7.1 Coverage matrix (projects × JD requirement areas)

| Requirement (from §3.1) | P1 EUAI | P2 Credit | P4 AlloyNext | P5 MedGemma |
|---|:--:|:--:|:--:|:--:|
| LLM orchestration (LangGraph) | ✓✓ | ✓✓ | ~ | ✗ |
| RAG / hybrid retrieval | ✓✓ | ✓✓ | ~ | ✗ |
| Vector DB | ✓✓ | ✓✓ | ✓ | ✗ |
| Graph DB (Neo4j) | ✓✓ | ✓✓ | ✗ | ✗ |
| MCP | ✗ | ✓✓ | ✗ (locked) | ✗ |
| Function calling / tool use | ~ | ✓ | ✓ | ✗ |
| Eval & observability | ~ | ✓✓ | ~ | ✓ |
| Cost optimisation | ✓ | ~ | ✓✓ | ✓ |
| Fine-tuning (QLoRA) | ✗ | ✗ | ✗ | ✓✓ |
| Safety / guardrails / compliance | ✓✓ | ✓✓ | ~ | ~ |
| Classical ML + explainability | ✗ | ✓✓ | ✗ | ~ |
| Backend (FastAPI) | ✓ | ✓ | ✓✓ | ✓ |
| Frontend (Next.js / web) | ✓ | ✓ | ✓✓ | ~ |
| Production deploy | ✓ scripted | ✓✓ **live** | ✓ deployed | ~ built |
| Regulatory-domain fit | ✓✓ EU AI Act | ✓✓ Annex III + FCA | ✗ | ~ Annex I |
| **Live demo URL** | ✗ | ✓ | ~ (no README) | ✗ |
| **Quantified production metric surfaced** | ~ | ~ | ✓ (cost) | ~ |
| **Defensibility doc (INTERVIEW_GUIDE)** | ✗ | ✓ | ✗ | ✗ |

**Reading the matrix:** the *technical* stack is covered well across the four — between P1 and P2 you have LangGraph + RAG + Neo4j + MCP + eval + compliance; P4 adds cost-disciplined product/backend depth; P5 adds the only fine-tuning exhibit. The weak column is not capability — it's **packaging**: only one live demo, inconsistent metric-surfacing, and only one defensibility doc.

### 7.2 The five highest-leverage fills (portfolio-wide)

Ranked by (market impact ÷ effort), cheapest first:

1. **Fill P5's HF model card** — ~30 min, removes an active credibility-killer on a public page.
2. **Write P4's README + delete P4/P1 cruft** — ~1–2 h, fixes the worst "careless repo" signals.
3. **Run P2's full eval (judge + retrieval) and surface a cost metric** — converts the anchor project's headline from partial to complete.
4. **Deploy P1 (and P5) to a live URL, or Loom them** — turns three "scripted/built" claims into Lever-4 live-demo evidence.
5. **Replicate P2's `INTERVIEW_GUIDE.md` for P1, P4, P5** — the §3.4 defensibility layer; arguably the highest *interview*-stage ROI of all.

Note that **none of the top fills is "build a new feature."** This matches the `10Weeks` Iron Rule (calibrate, don't rebuild) and the market reality (§5: deploy + quantify + document beats build-more).

### 7.3 Sequencing recommendation

The current `10Weeks` phasing (P2 in Phase 1; P4 + P5 parallel in Phase 2; P1 deferred to Phase 3) is broadly right, with two adjustments the audit surfaces:

- **P2 (Phase 1)** is nearly done — spend the remaining Phase-1 hours on §6.2 fills #1–#3 (full eval, cost metric, MCP Loom), not on new build.
- **Reconsider P1's deferral.** It is far closer to portfolio-ready than "sparse/deferred" implies, and EU AI Act is a live 2026 hiring lane. A single Phase-2 deploy-and-quantify pass could promote it to a third front-line exhibit cheaply. At minimum, **rewrite the deferral rationale** so it doesn't rest on the false "empty README / no PORTFOLIO_ENTRY" claim.
- **P4 (Phase 2)**: do the janitorial fixes and *drop* the LangGraph-rename / MCP tasks (the product vetoed them); position P4 as the FDE/backend/cost exhibit.
- **P5 (Phase 2 parallel)**: model card → reproducible eval → deploy, in that order.

---

## 8. Sources

Market contraction: Institute of Student Employers via TechRadar (`techradar.com/pro/tech-industry-stalling-as-ai-takes-over`); Adzuna via Notebookcheck / The Guardian; Robert Walters via Plant & Works Engineering (`pwemag.co.uk`); Stanford Digital Economy Lab; LSE Business Review (`blogs.lse.ac.uk/businessreview`, Mar 2026); British Chambers of Commerce (Mar 2026); People Management (Big-4 cohort data).

Junior-AI demand & JD stack: Glassdoor UK junior-AI-engineer listings (Jun 2026); MirrorCV "AI Engineer Resume Guide 2026" (387-listing analysis, `mirrorcv.com`); AY Automate "15 AI Engineer Skills 2026" (`ayautomate.com`); "Agentic AI Engineer Roadmap 2026" (Medium / Data Science Collective); TekRecruiter "AI Engineer Job Description 2026" (`tekrecruiter.com`); upGrad "RAG Engineer Job Description"; Dice (LangChain listings; 71% AI-fluency stat).

Salary: CareerMetrics / Hays 2026 (`careermetrics.co.uk`); Lorien (`lorienglobal.com`); Glassdoor; Morgan McKinley 2026 London guide; Knowledge Academy.

Visa: UK Immigration Rules post-22 July 2025 via Tarve (`tarve.co.uk`), Vanguard Solicitors, i-Migrator salary calculator, UK Sponsor List.

Interview integrity: Fabric study (19,368 interviews) via SpaceComplexity (`spacecomplexity.ai`), We Recruit IT / Connecting People (`werecruit.it`), InterviewMan, ExpertHire; "pair-programming-with-AI" via IEEE-USA (referenced).

EU AI Act: Secure Privacy (`secureprivacy.ai`, Aug-2026 high-risk deadline); Groath (`groath.ai`, Annex III enumeration); Validata (`validata.ai`, May-2026 Digital Omnibus timeline shift).

Clinical NLP / medical LLM: IntuitionLabs (pharma fine-tuning); John Snow Labs (medical LLM / HITL); Norstella & Mass General Brigham listings (PHI/EHR requirements) via Indeed.

Repo audit: direct reads of each project's `SYSTEM.md` / `PROJECT_OVERVIEW.md` / `DEPLOYMENT.md` / `README.md` / `PORTFOLIO_ENTRY.md` and directory structure on `D:\60 Days\Projects\Portfolio_Series\`, 2026-06-16.

---

*End of document. This is analysis, not legal/immigration/financial advice — verify visa thresholds against current gov.uk guidance and confirmed sponsor-licence status before acting.*
