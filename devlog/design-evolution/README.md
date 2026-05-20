# `design-evolution/` — versioned proposals

Forward-looking design proposals that double as decision records (dual RFC+ADR shape).

## How the versioned stream works

Each meaningful design change gets a new file: `vNN-<kebab-title>.md`. `NN` is sortable; the status lives in YAML frontmatter, not the filename. A file's filename never changes once created; its `status:` flips through the lifecycle.

### Status lifecycle

```
proposal ──(decision)──> accepted ──(code lands)──> implemented
                            │
                            └──(replaced later)──> superseded
```

When a status flips, update the matching frontmatter field in the same commit:
- `proposal → accepted` — set `decided_date:`.
- `accepted → implemented` — fill `implemented_in:` with commit hashes / migration numbers.
- `* → superseded` — set `superseded_by:` to the replacement's path.

## Required shape of every `vNN-*.md`

Frontmatter per `DOCS_PLAYBOOK.md §5b`:

```yaml
---
version: "NN"
title: <Short proposal title>
status: proposal              # proposal | accepted | implemented | superseded
derives_from: v<NN-1>-<previous-title>.md
proposed_date: YYYY-MM-DD
decided_date: null
implemented_in:
  - null
superseded_by: null
owner: <author>
source_of_truth:
  - <files / code locations the proposal is grounded in>
ai_guidance: |
  This is a forward-looking proposal. Read SYSTEM.md for what's actually built.
  Only treat this doc as current if status: implemented.
---
```

Body sections, in order:

1. `## 0. What this document is` — 2–3 paragraphs: what's being proposed, why now, what it derives from.
2. `## Status` — bulleted state / decision date / implementation / supersedes / superseded by.
3. `## Alternatives considered` — table of `# | Option | Why rejected`.
4. `## Consequences` — ✅ unlocks / ⚠️ trade-offs / ❌ rules out.
5. `## 1.` and onwards — the substantive body of the proposal.

## Current state

| File | Status | Decided | Implemented in |
|---|---|---|---|
| [`v01-baseline.md`](v01-baseline.md) | `accepted` | pre-2026 | initial commit (`2ccaadc`) |
| [`v02-static-scanner-pivot.md`](v02-static-scanner-pivot.md) | `implemented` | 2026-02-15 (approx, from doc trail) | commits `5210e51`, `661f990`; the entire `orchestrator/src/code_analyzer/` tree |
| [`v03-kb-completion.md`](v03-kb-completion.md) | `implemented` | 2026-02-12 | 2026-04-13 (Neo4j: 2,301 nodes / 4,423 rels / 2,198 vector docs across 7 collections) |

## When to add a new `vNN`

Add a new proposal when you're about to make (or are considering) a change that affects:
- Architecture (a new service, a removed service, a topology change).
- Data model (Neo4j schema, Postgres tables, vector store layout).
- API contracts (new endpoints, breaking changes to existing ones).
- Algorithmic core (scanner pipeline order, retrieval strategy, agent graph nodes).

If the change is purely internal (refactor, bug fix, dependency bump), update `SYSTEM.md` + `CHANGELOG.md` instead — no `vNN` needed.

## Worked example

The static-scanner pivot is the cleanest worked example in this repo. See `v02-static-scanner-pivot.md`:
- `## Alternatives considered` shows three options weighed (free-text RAG kept ✗ / LLM-output guardrails ✗ / static code scanner ✓).
- `## Consequences` shows the trade-offs (need a rule corpus, lose the conversational demo, gain ground-truth-able findings).
- The body sections trace the actual implementation: which scanners exist, what the rule catalog looks like, how the LangGraph workflow consumes the profile.
