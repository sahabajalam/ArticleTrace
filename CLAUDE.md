# CLAUDE.md — instructions for AI coding agents

The single instruction file. Read this first; everything else flows from it.

## What AlloyCode is

**AlloyCode** (also referenced as *Aegis Compliance Engine* in portfolio docs; directory name `EU_AI_GDPR`) is a **static compliance scanner for AI codebases**. Point it at a public GitHub repo; deterministic scanners detect AI-system patterns (biometric libraries, LLM SDKs, decision-making surfaces, missing model cards), map them to EU AI Act + GDPR obligations from a Neo4j-backed knowledge graph (2,301 nodes), and return a report of likely violations with `file:line` anchors and article citations. The architecture is three FastAPI/Next.js services orchestrated by LangGraph; the moat is the rule corpus, not the LLM.

The project pivoted in early 2026 from a free-text "describe your AI system" classifier to this static scanner. The pivot is the most important piece of context — see [`devlog/design-evolution/v02-static-scanner-pivot.md`](devlog/design-evolution/v02-static-scanner-pivot.md).

---

## Part 1 — Reading the context

Read in this order:

1. **[`devlog/SYSTEM.md`](devlog/SYSTEM.md)** — current architecture, single source of truth. The container diagram, the LangGraph node order, the scanner pipeline, the Neo4j schema all live here.
2. **[`devlog/NORTHSTAR.md`](devlog/NORTHSTAR.md)** — strategy, posture, and the **refuse list**. Read this BEFORE suggesting new work — many ideas are correctly-deferred, not bad. The single rule (Part I) is the gate every suggestion must pass. The current punch list (Part III) and refuse list (Part IV) derive from the 2026-06-16 portfolio audit at [`07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) §6.1 + §7.3.
3. **[`devlog/CHANGELOG.md`](devlog/CHANGELOG.md)** — what changed recently, with reasons.
4. **[`devlog/design-evolution/`](devlog/design-evolution/)** — forward-looking proposals (and shipped ones). Read the highest-numbered `vNN-*.md` first. Check `status:` in frontmatter — only `implemented` reflects built state. Currently: `v01-baseline` (accepted), `v02-static-scanner-pivot` (implemented), `v03-kb-completion` (implemented).
5. **[`devlog/history/`](devlog/history/)** — **frozen archive.** Open only when you need the reasoning trail behind a decision. Two files: `00-history-and-decisions.md` (distilled narrative) and `01-research-arc.md` (preserved primary sources from the original `gdpr context/` brainstorm dir + pre-pivot docs).
6. **[`devlog/JOURNEY.md`](devlog/JOURNEY.md)** — portfolio narrative for external readers. Optional context.

For operational tasks:
- Deploy: [`devlog/DEPLOYMENT.md`](devlog/DEPLOYMENT.md) (`status: accepted`)
- Bug-fix history: [`devlog/BUG_LOG.md`](devlog/BUG_LOG.md) (`status: living`, format `DL-NNN`)

Before acting on any doc, read its frontmatter `status:` and `ai_guidance:` fields.

### Status lifecycle

| Status | Treat as |
|---|---|
| `living` | Authoritative for current state |
| `accepted` | Authoritative for what it describes |
| `proposal` | Not yet built — do NOT cite as current |
| `implemented` | Shipped (check `implemented_in`) |
| `superseded` | Stale — read `superseded_by` instead |
| `archived` / `frozen` | Historical — verify before acting |

### The hard rule

**If a doc and the code disagree, the code wins.** Flag the disagreement; never silently follow the doc. The pre-existing `docs/README.md` (now archived) contained at least one drift point — it claimed HITL approval was retained, but `orchestrator/src/agents/supervisor.py` explicitly removed the HITL branch. The new `SYSTEM.md` is code-audited; trust it over the historical docs.

---

## Part 2 — Updating the docs

After every code change that affects architecture, schema, API, or behavior:

### Step 1 — Update [`devlog/SYSTEM.md`](devlog/SYSTEM.md)
Edit the relevant section. Bump `last_verified:` in frontmatter to today.

### Step 2 — Append to [`devlog/CHANGELOG.md`](devlog/CHANGELOG.md)
```markdown
## YYYY-MM-DD — <short title>

**What:** <files / tables / modules / pages affected, concrete>
**Why:** <reason in one or two sentences>
**Impact on SYSTEM.md:** <section(s) updated; or "none — internal only">
**Refs:** <commit short hashes / migration numbers / PR refs>
```

### Step 3 — If you shipped a `design-evolution/vNN-*.md` proposal
Flip its frontmatter: `status: proposal` → `status: implemented`, fill `decided_date` and `implemented_in` (commit hashes).

### Step 4 — If you superseded an existing doc
Old doc: `status: superseded`, add `superseded_by:`. New doc: note what it supersedes in its `## Status` section.

### Step 5 — If you're proposing a NEW design (no code yet)
Create `devlog/design-evolution/v04-<title>.md` (next available `vNN`). Frontmatter: `status: proposal`, `derives_from: v03-kb-completion.md`, `proposed_date:`. Use the dual RFC+ADR shape (Status / Alternatives considered / Consequences). Add an entry to CHANGELOG.

### Step 6 — If strategy or refuse-list shifted (rare)
Update [`devlog/NORTHSTAR.md`](devlog/NORTHSTAR.md) — but only when:
- A new track is added to (or removed from) the single rule (Part I).
- A target was met or moved.
- A previously-refused idea is being promoted (move from Part IV → Part III punch list).
- A new "correctly-deferred" idea is being added to the refuse list — record *why* it's deferred so future-Claude won't re-litigate it.

**This is NOT a per-code-change activity.** Strategy moves slowly. If you're touching NORTHSTAR every sprint, the line between strategy and tactics has slipped — that content belongs in CHANGELOG or a `vNN` proposal. If `NORTHSTAR.md` doesn't exist yet and you're being asked to refuse a parked feature for the second time, that's the trigger to create it (skeleton in [`DOCS_PLAYBOOK.md`](DOCS_PLAYBOOK.md) §8.4).

### When NOT to touch docs

- Pure research / Q&A sessions: read only.
- Drift discovered: flag to user; don't silently rewrite.
- [`devlog/history/`](devlog/history/): never edit. Frozen.
- [`devlog/BUG_LOG.md`](devlog/BUG_LOG.md): append-only, never re-order or rewrite past entries.
- [`devlog/NORTHSTAR.md`](devlog/NORTHSTAR.md): do NOT edit on routine code changes. Strategy moves slowly — only touch on punch-list movement, refuse-list additions, or after a new audit.

---

## Part 3 — Saving reusable prompts

When the user says **"save this prompt"**, **"save this"**, **"add this to the prompt library"**, or similar, follow the playbook in [`devlog/prompts/README.md`](devlog/prompts/README.md). **Never save raw prompts** — refinement is the point.

Quick reference:

1. Locate the raw prompt in the user's recent turn.
2. Identify what makes it work — goal, technique, constraints, project-specific bits.
3. Refine — tighten, replace project-specific bits with `<UPPER_SNAKE_CASE>` placeholders, preserve voice.
4. Pick a kebab-case slug.
5. Save to `devlog/prompts/<slug>.md` using [`devlog/prompts/_TEMPLATE.md`](devlog/prompts/_TEMPLATE.md). Fill every frontmatter field.
6. If updating — edit in place, bump `last_used:`, add to `## History`.
7. Report back — one line on what was saved and why this version is better than raw.

---

*This file follows the methodology in [`DOCS_PLAYBOOK.md`](DOCS_PLAYBOOK.md) at the project root. That playbook is the canonical reference; this file is its instantiation for AlloyCode.*
