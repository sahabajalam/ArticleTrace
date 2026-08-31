---
title: AlloyCode — Quantified Retrieval Metrics
status: living
last_verified: 2026-06-19
source_of_truth: |
  - knowledge_engine/scripts/07_run_golden_tests.py     — deterministic golden runner (citation/entity recall)
  - knowledge_engine/scripts/12_eval_three_mode.py      — vector_only / graph_only / hybrid_rrf comparison
  - knowledge_engine/scripts/13_eval_ragas_equivalent.py — RAGAS-equivalent metrics (Gemini judge, no langchain dep)
  All run against the live Neo4j Aura instance (URI in .env) with the
  25-query golden set at knowledge_engine/golden_tests/test_queries.json.
companion_docs:
  - devlog/SYSTEM.md
  - devlog/INTERVIEW_GUIDE.md
ai_guidance: |
  Headline retrieval numbers for the knowledge engine, produced by the
  scripts above. If you need to quote a number for the README, a CV, or an
  interview — pull it from here, not from prose elsewhere. The numbers are
  audit-able: scripts in repo, golden set in repo, Aura instance live.
  Anyone with `.env` can reproduce.

  This doc was expanded 2026-06-19 from n=6 → n=25 queries; previous results
  on the n=6 set are preserved under §History as Build A / Build B.
---

# AlloyCode — Quantified Retrieval Metrics

## Headline (n=25 golden queries, top-k=15)

| Metric | Value | What it measures |
|---|---|---|
| **Citation recall @15 (hybrid_rrf)** | **81.8% (27/33)** | Of all expected *Article* citations across the 25 queries, what fraction surface in the top-15 retrieved entities under the production RRF path. **This is the headline number for external use.** Unchanged by the v08 P1 arms. |
| Citation recall @15 (vector_only) | 72.7% (24/33) | Same metric, vector-only retrieval. Hybrid beats vector by ~9pp — RRF validates. |
| Citation recall @15 (graph_only) | 21.2% (7/33) | Same metric, vector-seeded graph traversal only. Confirms graph alone is weak; it earns its place by complementing vector. |
| **Entity recall @15 (hybrid_rrf)** | **62.5% (15/24)** | Non-Article entities (Concepts, Risk Categories, Rights, Penalties). Was 25% before the v08 name arm — see §6. |
| **Pass rate @15 (hybrid_rrf)** | **76% (19/25)** | Queries scoring ≥50% combined citation+entity retrieval. Includes negative cases. Was 68% before the v08 name arm. |
| **Context relevance @15 (RAGAS-equivalent)** | **45.9% mean** | Per-query LLM-judge precision: of the 15 retrieved entities, what fraction are "directly relevant" to the query per a Gemini-2.5-flash judge. n=25 queries × 15 entities = 375 judge calls. |

## Reproducibility

macOS / Linux:

```bash
cd knowledge_engine
uv sync   # bootstrap .venv from uv.lock — a fresh clone has no virtualenv

# 1. Deterministic golden tests (citation + entity recall, no LLM judge)
./.venv/bin/python scripts/07_run_golden_tests.py --dry-run

# 2. 3-mode comparison (vector / graph / hybrid)
./.venv/bin/python scripts/12_eval_three_mode.py

# 3. RAGAS-equivalent (context relevance, ~22 min, Gemini judge cost)
./.venv/bin/python scripts/13_eval_ragas_equivalent.py --context-only
```

Windows (PowerShell) — identical, only the interpreter path differs:

```powershell
cd knowledge_engine
uv sync

./.venv/Scripts/python.exe scripts/07_run_golden_tests.py --dry-run
./.venv/Scripts/python.exe scripts/12_eval_three_mode.py
./.venv/Scripts/python.exe scripts/13_eval_ragas_equivalent.py --context-only
```

Backend: live Neo4j Aura (URI in `.env`).
Embeddings: `gemini-embedding-001`, 3072-dim, queries embedded at runtime.
Judge: `gemini-2.5-flash` (RAGAS-equivalent only).
RetrievalEngine config: `rrf_k=60`, `default_top_k=15`, `max_hops=2`, `seed_count=5`.

CI: [`.github/workflows/golden-tests.yml`](../.github/workflows/golden-tests.yml) runs §1 and §2 on every PR touching `knowledge_engine/`; §3 is manual-dispatch only (LLM cost-gated).

---

## §1 — 3-mode comparison

Single run, 2026-06-19, against Aura `e8097dda`:

| Mode | Citation recall@15 | Entity recall@15 | Pass rate | Wall clock |
|---|---|---|---|---|
| `vector_only` | 24/33 (**72.7%**) | 10/24 (**41.7%**) | 17/25 (68%) | included below |
| `graph_only` (vector-seeded, 2 hops) | 7/33 (**21.2%**) | 0/24 (**0%**) | 3/25 (12%) | — |
| `hybrid_rrf` (production) | **27/33 (81.8%)** | 6/24 (25%) | 17/25 (68%) | 144 s total (5.8 s/query) |

**Reading:**

- **Hybrid beats vector by 9pp on citation recall.** RRF earns its place — the graph arm adds the Articles that vector misses (verified by inspecting which 3 citations only hybrid catches).
- **Vector beats hybrid by 17pp on entity recall.** Vector-only retrieves more *concept* nodes; the RRF graph signal dilutes them out of top-15. Real signal — the entity recall sub-headline should treat vector-only as the strong arm if abstract-concept navigation is the use case. (For the production "find me the article" path, hybrid is correct.)
- **Graph-only is weak.** Pure graph traversal without strong seeds can't find specific articles; it's a complement to vector, not a substitute.

### By category

| Category | n | vector_only | graph_only | hybrid_rrf |
|---|---|---|---|---|
| single_hop | 7 | 93% | 14% | 86% |
| multi_hop | 11 | 47% | 11% | 46% |
| out_of_scope | 7 | 57% | 14% | 57% |

Single-hop queries (one expected article) are nearly saturated under vector or hybrid. Multi-hop drops to ~47% — the join across 2–3 expected citations is where most of the headroom lives.

---

## §2 — RAGAS-equivalent metrics (Gemini judge)

Rather than installing the `ragas` package (which pulls in LangChain + OpenAI + pandas), we compute the equivalent metrics directly with the project's existing Gemini client. Same conceptual definitions, no framework dep.

### Context relevance @15

For each of the 15 retrieved entities per query, the judge answers: *"Is this entity directly relevant to answering the question? Yes/no."* Fraction yes-per-query, averaged across queries.

| Bucket | Mean | n | Reading |
|---|---|---|---|
| **Overall** | **45.9%** | 25 | ~7 of 15 retrieved entities are judged directly relevant on average |
| single_hop | 43% | 7 | Single-fact queries surface 1–3 directly relevant entities; the other 12+ are "related context" (recitals, cross-references) the judge calls non-relevant |
| multi_hop | 48% | 11 | Multi-citation queries have more relevant top-15 because the legal-mapping needs more than one article |
| out_of_scope | 45% | 7 | High variance — see below |

**The out-of-scope split is the interesting one:**

| Query | Score | Interpretation |
|---|---|---|
| GT_20 (military exclusion) | 73% | System retrieves Article 2 + related scope text — *correctly* relevant |
| GT_21 (academic research) | 80% | System retrieves GDPR Art 89 + research-purposes text — correctly relevant |
| GT_22 (territorial scope) | 47% | Retrieves Article 3, partial |
| GT_23 (nuclear safety — invented) | 47% | Retrieves *something* but it's not actually about nuclear AI |
| **GT_24 (consent form size — invented)** | **7%** | Judge correctly recognises 14/15 retrievals are non-relevant — system "knows" the question is nonsense |
| **GT_25 (HIPAA in EU — invented)** | **7%** | Same as above |

GT_24 and GT_25 are *invented* constraints — questions the regulation doesn't address. **A low context-relevance score on these is the desired outcome**: it shows the system is not fabricating plausible-sounding retrievals to fit a nonsense question. The 7% is feature, not bug.

This is the part of §3.4 defensibility that's hardest to demonstrate without a number — and now we have one.

### Why not faithfulness + answer_relevance too?

The script ([`13_eval_ragas_equivalent.py`](../knowledge_engine/scripts/13_eval_ragas_equivalent.py)) scaffolds both, but they require running `ReasoningEngine.answer()` for each query, which:
- Costs more (~$0.50 in Gemini spend for 25 queries)
- Requires the LLM-generated answer to be non-empty (some queries time out)
- Doubles wall-clock to ~45 min

Both are runnable now via:
```bash
./.venv/bin/python scripts/13_eval_ragas_equivalent.py    # drop --context-only
# Windows: ./.venv/Scripts/python.exe scripts/13_eval_ragas_equivalent.py
```

Not done in this pass. Logged on [`NORTHSTAR.md`](NORTHSTAR.md) as a P2 follow-up.

---

## §3 — Per-query breakdown (n=25, hybrid_rrf)

| # | Query ID | Category | Citations | Entities | Score | Pass? | Context relevance |
|---|---|---|---|---|---|---|---|
| 1 | `GT_01_PROHIBITED_AI` | multi_hop | 1/1 | 0/3 | 25% | FAIL | 33% (5/15) |
| 2 | `GT_02_CROSS_REG_OBLIGATIONS` | multi_hop | 0/2 | 0/2 | 0% | FAIL | 60% (9/15) |
| 3 | `GT_03_DATA_SUBJECT_RIGHTS` | single_hop | 1/1 | 1/1 | 100% | PASS | 60% (9/15) |
| 4 | `GT_04_DPIA_FRIA` | multi_hop | 2/2 | 1/2 | 75% | PASS | 20% (3/15) |
| 5 | `GT_05_TRANSPARENCY` | multi_hop | 1/1 | 0/2 | 33% | FAIL | 27% (4/15) |
| 6 | `GT_06_HOUSEHOLD_EXEMPTION` | out_of_scope | 1/1 | 0/0 | 100% | PASS | 53% (8/15) |
| 7 | `GT_07_DATA_SUBJECT_DEF` | single_hop | 1/1 | n/a | 100% | PASS | 27% (4/15) |
| 8 | `GT_08_RIGHT_TO_ERASURE` | single_hop | 1/1 | 1/1 | 100% | PASS | 60% (9/15) |
| 9 | `GT_09_BREACH_NOTIFICATION` | single_hop | 1/1 | 1/1 | 100% | PASS | 40% (6/15) |
| 10 | `GT_10_FINE_CEILING` | single_hop | 1/1 | 1/1 | 100% | PASS | 33% (5/15) |
| 11 | `GT_11_RECORDS_OF_PROCESSING` | single_hop | 1/1 | 0/1 | 50% | PASS | 27% (4/15) |
| 12 | `GT_12_VALID_CONSENT` | single_hop | 1/1 | 1/1 | 100% | PASS | 53% (8/15) |
| 13 | `GT_13_HIGH_RISK_DOCUMENTATION` | multi_hop | 2/2 | 1/1 | 100% | PASS | 53% (8/15) |
| 14 | `GT_14_BIOMETRIC_PUBLIC_SPACE` | multi_hop | 1/2 | 0/1 | 33% | FAIL | 53% (8/15) |
| 15 | `GT_15_PROVIDER_OBLIGATIONS` | multi_hop | 1/3 | 1/1 | 50% | PASS | 73% (11/15) |
| 16 | `GT_16_DEEPFAKE_LABELLING` | multi_hop | 1/1 | 0/1 | 50% | PASS | 40% (6/15) |
| 17 | `GT_17_INTERNATIONAL_TRANSFERS` | multi_hop | 3/3 | 0/1 | 75% | PASS | 73% (11/15) |
| 18 | `GT_18_AI_DECISION_RIGHTS` | multi_hop | 2/2 | 1/2 | 75% | PASS | 60% (9/15) |
| 19 | `GT_19_RISK_TIERING` | multi_hop | 1/3 | 0/2 | 20% | FAIL | 40% (6/15) |
| 20 | `GT_20_MILITARY_EXCLUSION` | out_of_scope | 1/1 | n/a | 100% | PASS | 73% (11/15) |
| 21 | `GT_21_ACADEMIC_RESEARCH` | out_of_scope | 1/1 | n/a | 100% | PASS | 80% (12/15) |
| 22 | `GT_22_TERRITORIAL_SCOPE` | out_of_scope | 1/1 | n/a | 100% | PASS | 47% (7/15) |
| 23 | `GT_23_NUCLEAR_SAFETY` | out_of_scope | 0/0 | 0/0 | 0% | FAIL | 47% (7/15) |
| 24 | `GT_24_CONSENT_FORM_SIZE` | out_of_scope | 0/0 | 0/0 | 0% | FAIL | **7%** (1/15) |
| 25 | `GT_25_HIPAA_IN_EU` | out_of_scope | 0/0 | 0/0 | 0% | FAIL | **7%** (1/15) |

Notes on the FAILs:
- `GT_01`: citation found, entity expectations too aggressive (3 expected; 0 retrieved at top-15 — RISK_PROHIBITED has a short label that doesn't embed close to the query)
- `GT_02`: HNSW boundary case — `AIACT_ART_14` slipped past top-15 (see §5 below)
- `GT_19`, `GT_14`: cross-Annex queries — Annex enumeration doesn't surface from semantic embedding of the question
- `GT_23`/`GT_24`/`GT_25`: pure negative cases — `expected_citations=[]`, so pass rate denominator is zero / undefined. The 7% context-relevance is the desired *low* signal here.

---

## §4 — Reading the entity-recall gap

Entity recall@15 is 25% (hybrid) vs citation recall 81.8%. The gap is structural:

- **Articles** have paragraph-length text — their embeddings encode rich semantic content. They land in top-15 reliably.
- **Concepts / Risk Categories / Rights / Penalties** are category nodes with short labels (often <10 tokens). Their embeddings encode a single concept name. Vector similarity over a short label loses to vector similarity over a paragraph article every time.

The likely fix is **a separate entity-name fuzzy match path** (trigram + alias index) merged into RRF — see [`NORTHSTAR.md`](NORTHSTAR.md) Part III. Estimated impact: 5–7 of the 10 currently-missed entity hits would land → entity recall@15 goes 6 → ~11 of 24 (~46%).

---

## §6 — v08 P1 retrieval arms: measured ablation (2026-08-31)

Two changes were proposed in NORTHSTAR Part III: a lexical **entity-name
index** as a third RRF arm, and a one-hop **COMPLEMENTS expansion** for
cross-regulation coverage. Both were implemented and measured independently
via [`scripts/14_eval_p1_arms.py`](../knowledge_engine/scripts/14_eval_p1_arms.py)
(raw data: `golden_tests/p1_ablation_20260831.json`).

| config | citation@15 | entity@15 | pass rate |
|---|---|---|---|
| baseline (both off) | 27/33 (81.8%) | 6/24 (25.0%) | 17/25 (68%) |
| name arm only | 26/33 (78.8%) | 15/24 (62.5%) | 19/25 (76%) |
| COMPLEMENTS only | 27/33 (81.8%) | 6/24 (25.0%) | 17/25 (68%) |
| **both (production)** | **27/33 (81.8%)** | **15/24 (62.5%)** | **19/25 (76%)** |

The baseline row reproduces the committed pre-change numbers exactly, which is
what makes the deltas trustworthy.

**By category:** single_hop 86% → 100%, multi_hop 46% → 63%, out_of_scope 57% →
57% (correctly unchanged — the negative cases must not "improve").

### What the name arm did

Entity recall **25% → 62.5%**, against NORTHSTAR's estimate of ~46%; multi-hop
**46% → 63%** against an estimate of ~55%. Both exceeded. The 9 newly-retrieved
entities are precisely the class §4 predicted would be missed — short-label
category nodes with no body text: `CONCEPT_DPIA`, `CONCEPT_CONSENT`,
`CONCEPT_AUTOMATED_DECISION`, `CONCEPT_TRANSPARENCY_OBLIGATION`, `RISK_HIGH`
(×3), `PEN_GDPR_TIER2`, `AIST_SOCIAL_SCORING_PUBLIC`. One of them,
`PEN_AIACT_PROHIBITED`, carries no embedding at all and was unreachable by
vector search on any budget.

### What COMPLEMENTS did — and did not do

**It did not do what it was proposed for.** NORTHSTAR predicted it would close
`GT_02`'s citation miss (7/8 → 8/8). It did not: `GT_02` still misses both
`GDPR_ART_22` and `AIACT_ART_14` in every configuration. Run alone,
COMPLEMENTS changes nothing — every metric is identical to baseline.

It earns its place for a different, measured reason. The name arm's one
regression is `GT_18_AI_DECISION_RIGHTS`, where the newly-ranked entities push
`GDPR_ART_22` out of the top-15 (citation 27/33 → 26/33). Adding COMPLEMENTS
restores it, because `GDPR_ART_22 —COMPLEMENTS→ AIACT_ART_14` puts it back in
the candidate set. So the pair is strictly better than either alone: **+37.5pp
entity recall at zero citation cost**, where the name arm alone would have
traded 3pp of the headline number for it.

Keeping a component that shows no standalone effect is a deliberate call, and
it rests on this interaction being measured rather than assumed. If the name
arm is ever retuned, re-run the ablation — COMPLEMENTS' justification is
entirely contingent on that displacement.

---

## §5 — HNSW non-determinism (historical context, pre-expansion)

When the golden set was n=6, citation recall was reported as **87.5% on Aura `652f6242`** (Build A) and **75% on Aura `e8097dda`** (Build B, restored from JSONL dump of Build A). The 12.5-percentage-point difference came from a single boundary case (`GT_02`'s `AIACT_ART_14` at rank ~14–16) flipping in or out of top-15.

This is HNSW non-determinism. HNSW (Malkov & Yashunin 2016 §4.2) constructs its search graph using randomised layer assignment + insertion-order-dependent edges. Identical data inserted in a different order produces a topologically different graph and slightly different approximate-nearest-neighbour results at the top-k boundary.

**Why it doesn't matter now:** with n=25 queries, the single-query boundary flip moves the headline by ~3pp, not 12. The current expansion is the structural fix to variance, exactly as recommended in §3 of the prior version of this doc. We can now quote a single number (81.8%) without a parenthetical band.

---

## History

- **2026-06-16 (Build A, n=6)** — Initial run on Aura `652f6242`. Citation recall@15 = 87.5% (7/8), entity recall@15 = 20%, pass rate = 3/6. Source: original 07_run_golden_tests against 6-query set.
- **2026-06-19 (Build B, n=6)** — Rerun on `e8097dda` restored from JSONL dump of Build A. Citation recall@15 = 75% (6/8). Showed HNSW non-determinism on a single boundary case (GT_02's AIACT_ART_14). Triggered the golden-set expansion → moved to current Headline section.
- **2026-08-31 (n=25, restore verification)** — Aura instance `e8097dda` was
  hard-deleted by free-tier idle policy (second occurrence; see BUG_LOG DL-025
  and `design-evolution/v06-durable-kg-and-reproducible-eval.md`). Restored from
  the `20260619_183622` JSONL dump into `dab1e7ea` (2,301 / 4,423 / 2,198,
  0 rels skipped). **Re-ran scripts 07 and 12: every number reproduced exactly** —
  hybrid_rrf 27/33 (81.8%), vector_only 24/33 (72.7%), graph_only 7/33 (21.2%),
  entity recall 6/24 / 10/24 / 0/24, pass rate 17/25 (68%), and the same eight
  queries fail (GT_01, 02, 05, 14, 19, 23, 24, 25). Per-category means identical
  (single_hop 93/14/86, multi_hop 47/11/46, out_of_scope 57/14/57). Wall clock
  135.8 s vs 144 s. **Note for §5:** the HNSW non-determinism that cost 12.5pp on
  the n=6 set moved the headline by **0.0pp** here — the n=25 expansion did the
  structural job §5 predicted it would. Headline numbers unchanged; nothing was
  rewritten.
- **2026-06-19 (n=25, current)** — Golden set expanded to 25 queries (7 single-hop / 11 multi-hop / 7 out-of-scope per the audit's §4.3 plan; see [`../01_AlloyCode.md`](../01_AlloyCode.md) §4.3 — originally specified 12/10/8 split). Headline citation recall@15 = **81.8% hybrid_rrf**. Added 3-mode comparison ([`12_eval_three_mode.py`](../knowledge_engine/scripts/12_eval_three_mode.py)) + RAGAS-equivalent context relevance ([`13_eval_ragas_equivalent.py`](../knowledge_engine/scripts/13_eval_ragas_equivalent.py)) + CI workflow ([`.github/workflows/golden-tests.yml`](../.github/workflows/golden-tests.yml)). RAGAS-equivalent context relevance @15 = 45.9% mean.
