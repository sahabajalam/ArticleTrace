---
version: "06"
title: Durable knowledge graph + reproducible evaluation
status: proposal
derives_from: v03-kb-completion.md
proposed_date: 2026-08-31
decided_date: null
implemented_in:
  - null
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - knowledge_engine/scripts/10_backup_to_jsonl.py    # the dump that saved the KG twice
  - knowledge_engine/scripts/11_restore_from_jsonl.py # the restore path
  - knowledge_engine/src/config.py                    # env_file=".env", CWD-relative
  - orchestrator/src/config.py                        # same defect
  - devlog/BUG_LOG.md                                 # DL-003, DL-005, DL-019, DL-020, DL-023, DL-025
  - devlog/METRICS.md                                 # the numbers this must keep reproducible
  - devlog/NORTHSTAR.md Part I                        # the gate this passes
ai_guidance: |
  This is a forward-looking proposal. Read SYSTEM.md for what's actually built.
  Only treat this doc as current if status: implemented.
---

# v06 — Durable knowledge graph + reproducible evaluation

## 0. What this document is

`v03-kb-completion` delivered the 2,301-node knowledge graph that every other
part of ArticleTrace depends on. It did not deliver the graph's **durability**.
The graph has now been destroyed twice by the same mechanism — Neo4j Aura
free-tier deletion after 30 days idle — on 2026-06-19 (`652f6242`, recovered
via `DL-025`) and again around 2026-08 (`e8097dda`, DNS no longer resolves,
found dormant on 2026-08-31). The second loss was predicted in writing by
DL-025's own open follow-up, which was never actioned.

Separately, the numbers in `METRICS.md` are no longer reproducible. Every
documented command is Windows-shaped (`./.venv/Scripts/python.exe`), the
project now lives on macOS, and no virtualenv exists on disk. A headline
retrieval metric nobody can re-run is a claim, not a measurement — which is
exactly what NORTHSTAR Part I lever 2 exists to prevent.

This proposal adds no features. It makes the thing v03 built survive being
left alone, and makes the thing `METRICS.md` claims re-runnable by anyone who
clones the repo. Both are preconditions for NORTHSTAR Part I levers 2 and 3;
neither touches the Part IV refuse-list.

## Status

- **State:** `proposal`
- **Decided:** null
- **Implemented in:** null
- **Supersedes:** nothing. Extends `v03-kb-completion.md`.
- **Superseded by:** null

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | Keep the `keep-aura-alive.yml` cron and trust it | Already failed once, silently. DL-025 documents that a `MATCH (n) RETURN count(n)` ping does not reset a policy-based idle timer, and the second deletion confirms it. Keeping it is choosing the option that has a measured 0% success rate. |
| 2 | Pay for a non-free Aura tier | Removes the failure but not the lesson, and spends money on a portfolio project to avoid a problem a 4-minute restore script already solves. Revisit if the project acquires real users. |
| 3 | Self-host Neo4j in `docker-compose.yml` | Contradicts SYSTEM.md §6's deliberate choice to keep Neo4j external, and Cloud Run still needs a hosted instance. Would solve local reproducibility while leaving production exposed. |
| 4 | **Treat deletion as expected; make restore fast, verified and scheduled** ✓ | The backup already exists and has already worked once. Making it routine converts a data-loss incident into a 4-minute chore, and the restore doubles as a portable bootstrap for any new machine or contributor. |

## Consequences

✅ **Unlocks** — a KG that survives dormancy; a one-command bootstrap on any
machine; `METRICS.md` numbers anyone can reproduce; a restore path that is
exercised often enough to be trusted rather than discovered under pressure.

⚠️ **Trade-offs** — the backup is ~102 MB and must stay out of git (already
in `.gitignore`); a scheduled dump costs a workflow run; restore is
CREATE-only, so it needs an empty target or `--force`.

❌ **Rules out** — nothing. No architecture, data model, API contract or
algorithmic change. The KG content is byte-identical to v03's.

## 1. The failure class this is really about

Reading all 26 BUG_LOG entries, the dominant recurring class is not
infrastructure — it is **silent degradation**: a component reporting success
while doing nothing.

| Entry | What reported success | What was actually true |
|---|---|---|
| DL-003 | ChromaDB "0 collections" | wrong vector store entirely |
| DL-019 | embeddings call returned | model 404 → *silent empty citations* |
| DL-020 | "Validated 0/0 Citations" | regex missed every real citation phrasing |
| DL-023 | secret verification passed | PowerShell scope mismatch, false negative |
| DL-025 | queries returned full data | instance was deleted; a phantom was serving |

The second Aura loss is the same shape one level up: the system was fine
until someone looked. Every item below is therefore specified to **fail
loudly** rather than degrade, and §4 makes that a standing review question.

## 2. Workstreams

### 2.1 Restore the graph (done first, unblocks everything)

Restore `20260619_183622` into the current instance via
`11_restore_from_jsonl.py`. Acceptance: 2,301 nodes, 4,423 relationships,
2,198 embeddings, `entity_embedding` vector index present.

### 2.2 Make config resolution explicit

Both `knowledge_engine/src/config.py` and `orchestrator/src/config.py` use
`env_file=".env"`, which resolves **relative to the process working
directory**. DL-025 step 2 was caused by exactly this — root `.env` updated,
`knowledge_engine/.env` left pointing at a dead instance — and the condition
is live again today (`knowledge_engine/.env` does not exist).

Anchor `env_file` to an absolute path derived from the repo root, so one
`.env` serves both services and cannot drift. Fail loudly on a missing or
empty `NEO4J_PASSWORD` / `GEMINI_API_KEY` rather than defaulting to `""` and
failing later as a confusing connection error.

### 2.3 Replace the keep-alive with a verified backup cycle

Retire `keep-aura-alive.yml`. Replace with a scheduled workflow that runs
`10_backup_to_jsonl.py` and **verifies the dump** (line counts match
`meta.json`) — an unverified backup is another silent success. This is
DL-025's own recommendation, now overdue by one data-loss event.

### 2.4 Make the eval path POSIX-reproducible

`METRICS.md` and the script docstrings invoke `./.venv/Scripts/python.exe`.
Provide a documented POSIX path (`uv sync` + `.venv/bin/python`) and update the
commands so the reproducibility section is true on the machine the project now
lives on.

> **Correction (2026-08-31, on implementing this section).** This section
> originally also named the CI workflow as carrying the Windows path. It does
> not: `.github/workflows/golden-tests.yml` runs on `ubuntu-latest` and invokes
> plain `python scripts/...` against the `setup-python` interpreter. It was
> audited and needed no change. **§2.4 is delivered** — see `CHANGELOG.md`
> 2026-08-31 "documented eval commands made POSIX-first". The rest of this
> proposal (§2.1, §2.5) remains `proposal`, so the document status is unchanged.

### 2.5 Re-run the golden tests as the acceptance test

Run `07_run_golden_tests.py` and `12_eval_three_mode.py` against the restored
instance. This is deliberately the acceptance test for §2.1–2.4: it exercises
config resolution, the POSIX path, and the restored graph in one command.

Expect citation recall@15 near the recorded **81.8% hybrid_rrf**. Per
`METRICS.md` §5, HNSW non-determinism means an identical-data restore can
move the headline by a few points — **a small delta is expected and must not
be silently rewritten into the headline.** If the number moves materially,
that is a finding to investigate, not a number to update.

## 3. Explicitly out of scope

Per NORTHSTAR Part IV: no new scanners, no new rules, no new agents, no
ColPali (v05 stays `proposal`), no rename. DL-024 (Cloud Run orchestrator
Postgres) is real but is a *deployment* problem; it does not block local
reproducibility and is tracked separately.

## 4. Standing review question

Adopted from the failure class in §1, to be asked of any component touched
here:

> When this component finds nothing, can the caller distinguish *"nothing
> exists"* from *"I stopped looking"*?

DL-003, DL-019, DL-020, DL-023 and DL-025 would each have been caught by
asking it.
