---
title: ArticleTrace — North Star
status: living
last_verified: 2026-06-19
companion_docs:
  - devlog/SYSTEM.md            # what is now
  - devlog/CHANGELOG.md         # what changed
  - ../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md   # the audit that produced the current punch list
ai_guidance: |
  This is STRATEGY and POSTURE — not architecture. Use it to decide whether a
  proposed piece of work earns time. For "what's actually built today", read
  SYSTEM.md. Before suggesting new features or modules, check Part IV (the
  refuse list) — many ideas are CORRECTLY-DEFERRED, not bad. The single rule
  (Part I) is the gate every suggestion must pass.

  Current source: the gap list comes from the 2026-06-16 portfolio audit
  (`07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md` §6.1 and §7.3). When that audit is
  refreshed, this doc should be revisited.
---

# ArticleTrace — North Star

> **Posture:** ~95% built, 0% shipped, mislabelled as "sparse" in upstream calibration. The gap closes with a live URL + quantified eval + survives-follow-up defensibility — not with new features.

---

## Part I — The single rule

**A suggestion only earns time if it does one of three things:**

1. **Makes ArticleTrace defensible under follow-up.** Per the audit §3.4: the interview format has shifted to line-by-line interrogation. Every non-obvious choice (RRF over pure vector, HITL removed, LLM-out-of-hot-path, why Neo4j over pgvector, why 6 scanners and which one runs first) must have a one-sentence "why this and not the alternative" ready. Surface that in an `INTERVIEW_GUIDE.md` mirroring Project 2.
2. **Surfaces a production metric.** Per audit §3.3 / §5 Lever 2: production numbers (latency, $/scan, recall@k, eval pass-rate) outrank model numbers (AUC, F1). The architectural rigour is already there; the numbers aren't. Until at least one production-shape number is in the README, P1 fails the ATS+screen gate.
3. **Puts the system in front of a real user (or a real recruiter).** Per §5 Lever 4: a live demo URL is the single strongest portfolio signal because it proves deployment, not just authorship. `gcp.ps1` is written; the URL is "pending." Anything that converts pending → live earns time.

Everything else defers. Refuse new scanners, new rules, new agents, new architectural layers until the three tracks above have moved.

---

## Part II — Targets (next pass)

| Target | Why this matters |
|---|---|
| **Live demo URL on Cloud Run** (or a 60-second Loom of a real scan as interim) | ✅ **Done 2026-06-16** — frontend live at https://aegis-frontend-whfa7vg4ea-ew.a.run.app; KE healthy; orchestrator degraded (DL-024). Loom still pending. |
| **Quantified retrieval + citation precision** on the 6 golden test cases | ✅ **Done 2026-06-16** — [`METRICS.md`](METRICS.md): citation recall@15 = **87.5%**, entity recall@15 = 20%, pass rate = 3/6. |
| **`INTERVIEW_GUIDE.md` at devlog root** mirroring Project 2's | ✅ **Done 2026-06-16** — [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md). 10 Q&A covering RRF, no-LLM-in-detection, no-HITL, Neo4j-vs-pgvector, scanner-order, 10-rules-not-100, GT-01 walkthrough, decommissioned monitor, "worst part." |
| **Single canonical external name** chosen and propagated | ✅ **Done 2026-06-16** — **ArticleTrace** is canonical. Aegis deprecated. Repo + scripts + docs updated. Cloud Run URL renames correctly-deferred (Part IV). |
| **HITL decision made and documented** | ✅ **Done 2026-06-16** — [`design-evolution/v04-hitl-decision.md`](design-evolution/v04-hitl-decision.md). `status: implemented`. Includes EU-AI-Act counter-argument response. |
| **Root `README.md` populated** | ✅ **Done 2026-06-16** — [`../README.md`](../README.md). With Mermaid diagram, headline numbers (incl. 87.5% citation recall@15), live URLs, quickstart, where-to-go-next. |

**Next targets** (open):

| Target | Why this matters |
|---|---|
| **Fix orchestrator `database: unavailable`** (BUG_LOG DL-024) | The URL is live but scans can't persist end-to-end. Until Postgres reconnects, the demo is "browse the architecture" not "scan a repo." |
| **Loom walkthrough of the live demo** | Asynchronous review aid — recruiters watch Looms; not all of them click URLs. |
| **Cross-regulation expansion in `RetrievalEngine`** | Closes the GT_02 citation miss → recall@15 goes 7/8 → 8/8. |
| **Entity-name index + RRF third arm** | Closes the entity-recall gap → 2/10 → ~8/10. |
| **Expand golden set 6 → 25 queries** | Makes recall@15 a stable benchmark; current `n` is too small. |

When a target lands, move it under `## Resolved` rather than deleting it.

---

## Part III — Punch list

Ranked cheapest-and-highest-leverage first. Source: audit §6.1 + §7.3.

- [in-progress] **P0 (new, from 2026-06-19 Aura recovery)** — Confirmed 2026-08-31: the live KE holds Aura host `e8097dda`, which no longer DNS-resolves; `.env` holds a live instance. Secret rotation is the fix and is owner-run (credential handling). Original note follows: Push the new Aura URI/password to GCP Secret Manager and restart Cloud Run services. KE on Cloud Run still holds the phantom `652f6242` secret and will silently break when Aura hard-purges that instance. Run `./gcp.ps1 -Action secrets` then `gcloud run services update aegis-knowledge-engine aegis-orchestrator --region europe-west1 --project gdpreuai`. ~5 min.
- [in-progress] **P0 (from 2026-06-16 deploy verification)** — Diagnosed 2026-08-31: **not** Cloud SQL. No instance has ever existed; the secret holds the `.env` localhost default, so the container dials itself (BUG_LOG DL-024, resolved). Fix is a free-tier Neon Postgres URL written to `DATABASE_URL_ORCHESTRATOR`; owner-run (credential handling). Original note follows: Diagnose and fix the live orchestrator's `database: unavailable` degradation. Frontend + KE are healthy; orchestrator can't persist scans until Postgres reconnects. End-to-end demo blocked on this even though the URL is live.
- [todo] **P2 (from 2026-06-19 RAGAS run)** — Run faithfulness + answer_relevance via `13_eval_ragas_equivalent.py` (drop `--context-only` flag). Scaffolded but requires ReasoningEngine and adds ~$0.50 Gemini cost. Manual dispatch on the new `golden-tests.yml` CI workflow when desired.
- [todo] **P2** — ColPali multimodal — designed and scaffolded in [`design-evolution/v05-multimodal-colpali.md`](design-evolution/v05-multimodal-colpali.md) + [`../knowledge_engine/src/multimodal/`](../knowledge_engine/src/multimodal/). Acceptance criteria in v05 §4. Gated on (a) GPU box, (b) PDFs ingested, (c) Aura tier upgrade for ~300 MB of page embeddings, (d) the 10-query multimodal benchmark beating text-only by ≥15pp.
- [todo] **P1** — Record a 60-second Loom walkthrough of the live demo (frontend tour + a sample scan if the orchestrator DB comes back online). The URLs are live; the Loom is the screen-share-equivalent for asynchronous review.

## Resolved

Items moved here as they land. Most recent at the top. Each line: `[YYYY-MM-DD] item — outcome`.

- **[2026-08-31] Entity-name index + RRF third arm; cross-regulation COMPLEMENTS expansion** — Both shipped and measured by ablation ([`METRICS.md`](METRICS.md) §6). Entity recall@15 **25% → 62.5%** (estimate was ~46%), multi-hop **46% → 63%** (estimate ~55%), pass rate **68% → 76%**, citation recall unchanged at 81.8%. The name arm produced the entire gain. COMPLEMENTS did **not** close `GT_02` as predicted — alone it changes nothing — but it repairs the name arm's single citation displacement on `GT_18`, making the pair strictly better than either alone. Kept on that measured interaction, not on its original rationale.

- **[2026-08-31] Diagnose `keep-aura-alive.yml` and replace it if deletion is policy-based** — It is policy-based: a `MATCH (n) RETURN count(n)` ping resumes a *paused* Aura instance but does not reset the 30-day *deletion* timer, which is why the graph was destroyed a second time (`e8097dda`) with the workflow in place. Deleted it rather than disabling it — 0% measured success rate, and a disabled workflow still reads as protection. Replaced by [`../.github/workflows/backup-knowledge-graph.yml`](../.github/workflows/backup-knowledge-graph.yml): weekly + manual `10_backup_to_jsonl.py`, dump published as a 90-day artifact. The script now self-verifies on every run (line counts vs `meta.json`, no mid-write truncation, last record parses) and exits non-zero otherwise, so a green run means a *readable* dump. Verified against the live instance (2,301 / 4,423, self-check passed) and against a deliberately truncated dump (failed with all three problems named). Implements `design-evolution/v06` §2.3; the next deletion is now a ~4-minute restore.
- **[2026-06-19] Close RAG + eval gaps (expanded golden + 3-mode + RAGAS-equivalent + CI + ColPali scaffolding)** — Expanded golden set 6 → 25 (7 single-hop / 11 multi-hop / 7 out-of-scope). 3-mode runner ([`../knowledge_engine/scripts/12_eval_three_mode.py`](../knowledge_engine/scripts/12_eval_three_mode.py)) gives **hybrid 81.8% / vector 72.7% / graph 21.2% citation recall@15** — RRF validated. RAGAS-equivalent metrics ([`../knowledge_engine/scripts/13_eval_ragas_equivalent.py`](../knowledge_engine/scripts/13_eval_ragas_equivalent.py)) computed bespoke with the existing Gemini judge (no langchain/openai/pandas dep) — context relevance @15 = **45.9% mean** (with invented-constraint negatives scoring 7% — system correctly recognises nonsense). CI workflow ([`../.github/workflows/golden-tests.yml`](../.github/workflows/golden-tests.yml)) runs scripts 07 + 12 on every PR; manual dispatch for the heavy script 13. ColPali multimodal scaffolded ([`../knowledge_engine/src/multimodal/`](../knowledge_engine/src/multimodal/)) with full design doc at `v05-multimodal-colpali.md` (`status: proposal`) — module compiles, gated runtime import, acceptance criteria explicit. Fixed real bug: `gemini-2.0-flash` was deprecated 2026-06-19; updated 4 source refs to `gemini-2.5-flash`. Full breakdown in [`METRICS.md`](METRICS.md). Was the #1 calibration-vs-reality gap; now closed.
- **[2026-06-19] Recover from Aura free-tier 30-day deletion (unplanned infra win)** — Discovered phantom-instance grace period after Neo4j auto-deletion of `652f6242`. Wrote streaming JSONL backup ([`../knowledge_engine/scripts/10_backup_to_jsonl.py`](../knowledge_engine/scripts/10_backup_to_jsonl.py)) + idempotent property-keyed restore ([`../knowledge_engine/scripts/11_restore_from_jsonl.py`](../knowledge_engine/scripts/11_restore_from_jsonl.py)). Recovered full 2,301 / 4,423 / 2,198 KG into new instance `e8097dda`. Project now has a durable backup/restore path it lacked entirely. Citation recall@15 = 75% on the restored instance (was 87.5% pre-restore — HNSW non-determinism, identical data, [`METRICS.md`](METRICS.md) §5). Full story in [`BUG_LOG.md`](BUG_LOG.md) DL-025.
- **[2026-06-16] Deploy via `gcp.ps1` to get a live URL** — Discovered already-deployed under earlier "Aegis" naming: frontend at https://aegis-frontend-whfa7vg4ea-ew.a.run.app (HTTP 200), KE at https://aegis-knowledge-engine-whfa7vg4ea-ew.a.run.app (`healthy`, 2,198 docs across 7 collections, 2,301 KG nodes confirmed live), orchestrator at https://aegis-orchestrator-whfa7vg4ea-ew.a.run.app (`degraded` — Postgres unavailable, see DL-024). Loom still pending. The URL-rename to articletrace-* is correctly deferred (Part IV: "Renaming ArticleTrace again"); existing URLs work and renaming would break inbound links for no architectural gain.
- **[2026-06-16] Write `devlog/INTERVIEW_GUIDE.md`** — 10 line-by-line defence questions with three-sentence answers, follow-up traps, and citable code/doc references. Covers the static-scanner thesis, RRF, LLM-out-of-detection-hot-path, no-HITL, Neo4j vs pgvector, scanner-order rationale, 10-rules-not-100, the GT-01 résumé-screening walkthrough, the decommissioned monitor module, and the "worst part of this project" answer. Cheat-sheet of citable numbers at the bottom.
- **[2026-06-16] Populate root `README.md`** — Tagline + Mermaid architecture diagram + headline numbers table (now including the live retrieval metric: 87.5% citation recall@15) + live demo URLs + Quickstart + where-to-go-next table. ATS-keyword coverage (LangGraph / RAG / hybrid retrieval / Neo4j / FastAPI / Cloud Run / cost) per audit §5 Lever 1.
- **[2026-06-16] Produce quantified retrieval metrics on golden queries** — Created [`METRICS.md`](METRICS.md). Headline: **citation recall@15 = 87.5%** (7/8), entity recall@15 = 20% (2/10), pass rate = 3/6. Real reproducible numbers from `knowledge_engine/scripts/07_run_golden_tests.py --dry-run` against live Aura. Per-query breakdown + reading-the-gap section + follow-up work spawned three new P1 items above.
- **[2026-06-16] Clean the cruft** — Deleted 10 empty path-with-spaces artifact dirs from `orchestrator/` (`srcagents`, `srcapi`, `srccontrol_plane`, `srcstate`, `srctemplates`, `srcutils`, `testsintegration`, `testsunit`, `datagolden`, `.githubworkflows`). Deleted `frontend/ts_errors.txt` + 4 `scan_*.json` debug dumps. Added `legacy_prototypes/` to `.gitignore` (preserves the EU AI Act / CJEU / EDPB raw source corpus on disk for KB-rebuild reproducibility, removes it from repo surface).
- **[2026-06-16] Resolve the tri-naming** — Picked **ArticleTrace** as the canonical external name. Updated DEPLOYMENT.md, BUG_LOG.md, gcp.ps1 (5 strings: docstring, banner, project-create name, Artifact Registry description, cleanup message), SYSTEM.md (naming paragraph + glossary entries). Aegis Compliance Engine marked deprecated; new uses refused. The Cloud Run service URLs minted under the older naming are kept (rename is Part IV — correctly-deferred).
- **[2026-06-16] Decide and document the HITL story** — Created [`design-evolution/v04-hitl-decision.md`](design-evolution/v04-hitl-decision.md): formal `status: implemented` decision record. Includes the three-sentence interview answer, the EU AI Act Article 14 counter-argument and the `mypy`-analogue response, and the three conditions that would change the decision. Cross-referenced from SYSTEM.md §3.2, glossary, and INTERVIEW_GUIDE.md Q4.
- **[2026-06-16] Rewrite the calibration deferral rationale** — Updated `../../10Weeks/project_calibration/01_ArticleTrace.md` banner. The original "sparse, empty README, no PORTFOLIO_ENTRY" reason was factually wrong; replaced with a focus-discipline rationale (Iron Rule #3) and a now-complete inventory of what ArticleTrace actually has. The audit's promote-to-front-line suggestion is named explicitly as the trigger for revisiting the deferral.

---

## Part IV — What to refuse

The list of ideas that are NOT being built — not because they're bad, but because they're correctly-deferred. Each entry has one line on why it's deferred so the next person doesn't have to re-litigate.

- **Fine-tuning capability inside P1** — Project 5 (MedGemma) is the portfolio's fine-tuning exhibit; adding it here duplicates coverage and deepens the build-vs-ship gap. Refuse unless P5 is dropped from the portfolio.
- **MCP server for P1** — Project 2 (Credit Scorer) already carries the MCP keyword with a real 5-tool stdio server. P1 doesn't need it for keyword coverage; building it here is redundant.
- **More YAML rules beyond the current 10** — Audit §3.4 + §6.1: depth (defensibility on existing rules) beats breadth. Adding rules without quantifying the existing ones is anti-pattern.
- **New scanner types beyond the existing 6** — Same reason. The 6-scanner pipeline is the architectural story; piling on weakens it.
- **Multi-language Tree-sitter support** (e.g. extending beyond Python/JS) — Out of scope for the portfolio thesis (compliance scanning, not polyglot tooling). Revisit only after a deployed user asks.
- **A 3D / animated visualisation of the KG** — Demo polish without compliance value. Refuse until the deterministic story is shipped and quantified.
- **Skill-agents / sub-agent architecture inside the orchestrator** — The 4-node linear LangGraph is the whole point (deterministic findings → narrative). Adding agentic complexity inverts the moat (rule corpus, not LLM choreography).
- **Re-adding the decommissioned `monitor/` module** — The honest audit (history) said it produced no usable signal in a portfolio demo. Revisit only if a real production deployment surfaces an actual observability need.
- **Renaming `ArticleTrace` again** — Pick one external name and stop. Each rename is a free credibility hit for no architectural gain. **This rule was overridden once, deliberately, on 2026-08-31** (AlloyCode → ArticleTrace) on evidence rather than taste: the old name collided with an operating company at the exact domain, with a compliance fintech, and with a formal-methods language, and it described 1 of the catalog's 26 regulatory references. The reasoning is recorded in `design-evolution/v08-naming.md` so a fourth rename has to argue against it. **The refusal stands for any further rename.**

---

## Part V — Design rationale (why it's built this way)

Why the *shape* of ArticleTrace is what it is — the principle-level reasoning that any individual code change inherits from. Not the architecture (`SYSTEM.md`); not the change history (`CHANGELOG.md`); the *why behind the why*.

**The moat is the rule corpus, not the LLM.** The 2,301-node Neo4j knowledge graph is the hardest-to-rebuild thing in the project. Every detection rule maps to an Article / Obligation in that graph. LLMs are kept out of the detection hot path and write only the post-hoc narrative. This is deliberate: ground-truth-able findings (a deterministic scanner found `face_recognition` at `app.py:42` → mapped to Art 5(1)(f)) beat "vibes-based" LLM classifications in both compliance reality and interview defensibility. Audit §3.4 validates this — the market has moved to rewarding genuine, line-by-line-defensible work.

**Static code analysis is the differentiator from "RAG over EU AI Act."** Anyone can spin up a chatbot over the Act PDF. Few systems take a real codebase and produce `file:line`-anchored findings against named Annex III categories. The pivot from free-text classifier (`v01-baseline`) to static scanner (`v02-static-scanner-pivot`) is the load-bearing decision; everything since (`v03-kb-completion`, the YAML rule catalog, the 6-scanner pipeline order) inherits from it.

**Defensibility over feature breadth.** Per audit §3.2: junior AI engineers are screened on execution and follow-up survival, not architecture ownership. ArticleTrace is *over*-built for "junior" in scope already — the binding risk is not "too thin" but "claims that can't survive a follow-up question." Every Part III punch-list item is in service of that risk, not in service of more features.

**Regulatory framing is real, not decorative.** EU AI Act Annex III names employment decisions, credit scoring, and biometrics — exactly the categories GT-01 and GT-06 test. The August-2026 high-risk enforcement deadline (or late-2027 via the Digital Omnibus shift; treat as fluid) is a live hiring lane. P1's positioning isn't "AI safety theatre"; it's hitting a deadline-pressured compliance-engineering demand curve.

---

## Part VI — When future-Claude reads this

Treat NORTHSTAR as the **gate**. Before suggesting work, ask:

- Does the suggestion match one of the three tracks in Part I? If no → defer.
- Is it on the refuse list (Part IV)? If yes → refuse the suggestion and cite the line. Don't re-litigate. If the user wants to override the refusal, that's their call — but the default is "no."
- Are the Part II targets already moved? If not, that's what to do.
- If the audit (`07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`) has been refreshed since `last_verified:`, re-read it before trusting Parts II–IV blindly.

**When NOT to touch this doc:** routine code changes, bug fixes, refactors. Strategy moves slowly. Touch this only when:
- A Part III item ships → move it to `## Resolved`.
- A new "correctly-deferred" idea surfaces → add to Part IV with one line on *why*.
- A previously-refused idea is being promoted → move from Part IV to Part III with justification.
- A new audit reframes the targets → revisit Part II.
