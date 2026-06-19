# Project Extraction Instructions for Claude Code

> Self-contained instruction file. Open Claude Code inside the target project
> directory, point it at this file, and ask for the extraction. The output is
> ready to paste into AlloyNext's project form
> ([`/profile` → Projects](http://localhost:3000/profile)).
>
> Companion design: [15-rework-pipeline-project-to-resume.md](15-rework-pipeline-project-to-resume.md).
> Storage spec: see "Storage format and profile-UI changes" at the end of that doc.

## What you (Claude) are doing

You are running inside a software project directory. The user wants to
populate one row in their AlloyNext `user_projects` table from this codebase.
The row will later drive resume-bullet generation for job applications, so
**every claim must be defensible against the actual code, commits, README,
tests, or screenshots** — anything in this repo.

Produce **one self-contained markdown document** in the exact template below.
The user will paste it into AlloyNext, which has a parser that splits the
sections into the right database columns.

If you are unsure of any fact, **leave the section thin and mark it
`[QUALITATIVE]`** rather than guess. Vague-but-honest beats specific-but-wrong.

## How the user invokes you

```
cd <target-project-dir>
claude   # or claude code session
> Please extract this project for my AlloyNext profile.
> Follow docs/16-project-extraction-instructions.md from my AlloyNext repo:
> d:/60 Days/Projects/Portfolio_Series/project_4_Job_Tracker/docs/16-project-extraction-instructions.md
```

## Mandatory output template

Produce exactly this structure. Headings are load-bearing — the AlloyNext
parser splits on them. Do not add extra H1s, do not skip H2 sections, do not
re-order.

````markdown
# <Project Name>

<One-line pitch, ≤200 characters. No hype, no "passionate", no "innovative".
State what it is and who it's for.>

## What it does

<1–2 short paragraphs. Functional description in user-facing language. What
problem does it solve? Who uses it? What can they do with it?>

## Why I built it

<1–2 short paragraphs. The actual problem you were facing. Was it for your
own job hunt? A client? Learning a new tech? Be honest about scope —
"personal use, not yet shipped to others" is fine.>

## How it's built

<Architecture and key decisions. Use file paths or directory references
wherever possible. Bullet list is fine. Examples of what to include:

- Stack at each layer (frontend / backend / DB / external APIs)
- One or two architectural decisions and the trade-off behind each
- The single most interesting technical choice in the codebase

Cite a file or directory for any concrete claim, e.g. `src/scanner/runner.py`.>

## Impact / Scope

<Real numbers wherever extractable. If no number is available, write the bullet
without one and prefix `[QUALITATIVE]`. Examples of where to dig for real
metrics:

- LOC by feature (rg --count or git ls-files)
- Commits over a period (git log --oneline | wc -l)
- Number of API endpoints, components, tables, etc.
- Test counts and pass rates
- Production users / stars / downloads — only if defensible

If the project is personal use only and has no users, just say so:

- [QUALITATIVE] Personal use; not shipped to other users
- [QUALITATIVE] Active development; no public release yet

NEVER invent counts, percentages, or revenue figures.>

## Story seeds

<2–3 brief STAR+R-shaped paragraphs. Each one is a story you'd tell in a
behavioural interview: a real decision, trade-off, bug-hunt, or scope cut.
2–4 sentences each. Mine the git log for "fix:" / "revert:" commits and the
README for any "Why this approach" / "We tried X but…" notes.

Each story should answer in spirit:
  - Situation: what was happening
  - Task: what you had to do
  - Action: what you actually did
  - Result: what came out of it (including failures)
  - Reflection: what you'd do differently / learned

Examples that work:
  - "Bug-hunt: traced a £2.56 LLM bill spike to one Google Search grounding
    fee. Replaced with a JD-length gate. Now £0.27 per scan."
  - "Architecture flip: scanner started as watched-companies; pivoted to
    Adzuna-only when half the slugs went stale. Lost the ATS-direct fallback
    but kept the inbox flowing."
  - "Schema-mismatch cascade: three different create-job paths each had
    their own column-translation bug. Consolidated into one entry-point
    translator."

Do NOT invent stories. If you only have one solid story from the codebase,
write one — three weak stories are worse than one strong one.>

## Resume bullets

<6–10 candidate bullets. Each 15–25 words. Each must EITHER cite a source
(file path, commit hash, test name) OR be prefixed `[QUALITATIVE]`. These
become AlloyNext's `bullet_points` array — the resume composer will later
select 3–5 of them per job application.

Style rules:
  - Lead with a strong action verb (Built, Designed, Cut, Wired, Replaced,
    Refactored, Shipped, Migrated). No "Was responsible for". No "Worked on".
  - Concrete tools and frameworks where they're actually used.
  - No more than 2 bullets starting with the same verb across this list.
  - No "leveraged", "synergised", "passionate", "results-driven",
    "detail-oriented", "team player", "thought leader", "proven track record".
  - No em-dash-as-filler. Use a colon, parens, or "→" instead.
  - ATS-safe: no markdown bold inside the bullet, no emoji.

Examples of the right shape:
  - Built scanner sweep across 6 ATS providers with parallelised liveness
    probes — 6 concurrent workers (src/scanner/runner.py:373)
  - Cut LLM eval cost ~90% by gating Block D grounded search on JD length
    and deferring Block A-H to manual trigger (commit e4427d2)
  - [QUALITATIVE] Refactored manual-job-add cascade after consecutive schema
    bugs; collapsed three call paths into one entry-point translator

Output format: one bullet per line, no numbering, no surrounding prose.>

- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4>
- <bullet 5>
- <bullet 6>
- <bullet 7 — optional>
- <bullet 8 — optional>

## Tech

<Comma-separated list of technologies actually used in this repo. Verify
each one against package.json / pyproject.toml / requirements.txt / go.mod /
Cargo.toml / etc. Do NOT pad with "Microservices", "REST APIs", or generic
buzzwords — those are concepts, not technologies.

Example: Next.js, TypeScript, Tailwind, FastAPI, Python 3.13, Supabase
(Postgres + auth), Gemini API, httpx, Pydantic>

## Domain

<1–3 short domain labels. Examples: "LLM evaluation", "Job-search
automation", "Resume tailoring", "DevOps observability", "FinTech
payments", "Education".>
````

That's the entire output. No preamble, no "here is the extraction:"
prefix, no closing summary.

## Hard rules

**Evidence or `[QUALITATIVE]`.** Every numeric / specific claim is either
cited (file path, commit hash, test name, line range) or prefixed
`[QUALITATIVE]`. Never both. Never neither.

**No invention.** If git log shows 47 commits, you may write "47 commits over
3 months". You may NOT write "shipped 12 features" unless you can point at
12 distinct merge commits or PR titles that justify the count. Same for
users, latency, revenue, team size. When in doubt, omit or qualify.

**Banned phrases.** Reject if you write any of:

```
"passionate about", "results-oriented", "results-driven", "detail-oriented",
"proven track record", "team player", "synergy", "synergised",
"thought leader", "self-starter", "go-getter", "value-add", "best of breed",
"world-class", "cutting-edge", "innovative solution", "leveraged",
"orchestrated cross-functional"
```

Rewrite anything that drifts toward this register. Marketing copy is the
enemy.

**Action verbs only at the start of bullets.** Built, Designed, Cut, Wired,
Replaced, Refactored, Shipped, Migrated, Reduced, Eliminated, Consolidated,
Automated, Decomposed. No "Was responsible for…", "Worked on…",
"Helped with…", "Assisted…".

**Length discipline.** Each bullet 15–25 words. Each H2 section paragraph
≤4 sentences. The whole `markdown_content` total ≤1500 words. If you have
more to say, sharpen.

**Tech list honesty.** Only list tech you can find in a manifest file or
import statement. Generic terms like "Microservices", "REST APIs",
"Distributed systems" are not technologies — they're concepts. Move those
to the `Domain` line.

**Voice.** Plain technical English. Short sentences. Active voice. No
adjectives that don't carry information (drop "robust", "scalable",
"powerful").

## Extraction workflow

Recommended order. Use whichever tools you have available — `Read`, `Glob`,
`Grep`, `Bash`. Spend ~15 minutes on a fresh project; less on a familiar
one. Each phase produces signal, not output — only synthesise to the
template at the end.

1. **Surface scan** (~1 min). `ls`, `git status`, `git log --oneline | head
   -50`, read the top of `README.md` if any. Get a 30-second sense of what
   the project is.
2. **Manifests** (~2 min). Read `package.json` / `pyproject.toml` /
   `requirements.txt` / `go.mod` / etc. This is your *only* source of
   truth for the Tech section.
3. **Architecture pass** (~3 min). `ls src/` (or equivalent top-level dir).
   Read the entry point (e.g. `main.py`, `app.tsx`, `index.ts`,
   `cmd/server/main.go`). Identify the 2–3 biggest modules by file count
   or size. Skim each. Note their purpose.
4. **Decision archaeology** (~3 min). `git log --oneline | head -100` to
   find feature commits. `git log --all --grep="fix:" --oneline | head -30`
   for bug-hunts. Anything in the README/docs about "Why we…" or
   "We tried X but…". These become the Story seeds.
5. **Metric mining** (~3 min). Use `Bash` for counts:
   - `git log --oneline | wc -l` for commits
   - `find src -name "*.py" -o -name "*.ts" | xargs wc -l | tail -1` for LOC
   - Endpoint count: `grep -rn "@app\." src/ | wc -l` or similar
   - Test count + pass rate if a tests dir exists
   Save each number AS YOU FIND IT, with the command that produced it.
6. **Synthesis** (~5 min). Now and only now write the template top-to-bottom.
   For each bullet, reference the file/commit/number you collected. If you
   can't, prefix `[QUALITATIVE]`.

If any step turns up nothing (no commits, no README, no tests), that's
useful information — write the section thinly and add a `[QUALITATIVE]`
note explaining the absence. Do not pad.

## Worked example — strong extraction

```markdown
# AlloyNext

Personal job-tracker with Adzuna scanner, Block A-H LLM evaluator, and
resume tailoring grounded in real project work.

## What it does

Tracks job applications end-to-end. Scans Adzuna for new listings matching
hunt-list archetypes; runs an LLM evaluator per role producing eight blocks
of structured scoring (legitimacy, comp grounding, fit, etc.); tailors a
resume against each job description using filter+reskin over
candidate-authored bullets rather than generation from sparse description.

For now it's a one-user app — me — built to validate the architectural
hypothesis that evidence-grounded resumes beat generated-from-scratch ones.

## Why I built it

I was writing tailored resumes by hand for ~50 applications. Most "AI
resume builder" tools generate bullets from a 100-word project description,
which produces fluent but vague output. I wanted to test whether richer
intake — human-written bullets that the LLM only selects and rewords —
fixes the vagueness problem. Building it myself was the cheapest way to
find out.

## How it's built

- Frontend: Next.js 16 + Tailwind, hosted under `frontend/`; Supabase auth
- Backend: FastAPI (`src/api.py`) + Gemini SDK; Block A-H eval pipeline
  at `src/evaluators/block_evaluator.py`
- Scanner: per-suffix Adzuna `title_only` queries at
  `src/scanner/aggregators.py`; parallelised liveness probe doubles as
  full-JD scraper at `src/scanner/liveness.py:probe_listing`
- Cost decisions: JD-length-gated grounded search + manual-only Block A-H
  trigger (commits e4427d2, 1b01d95)

## Impact / Scope

- 113 on-target matches per single scan against the user's 10-archetype
  hunt list (verified at runtime, commit `e4427d2`)
- LLM cost per evaluation cut £0.023 → £0.002 (~90% reduction) — verified
  against `cost_ledger` table after the optimisation pass
- 1,400+ commits over 60 days of development (`git log --oneline | wc -l`)
- [QUALITATIVE] Single-user app; not yet open to others

## Story seeds

1. **Bug-hunt — the £2.56 LLM bill spike.** After auto-saving 110+ jobs from
   one Adzuna scan, the day's Gemini bill jumped from £1.90 to £4.46.
   Traced it to one call: Block D's grounded search via `google_search`
   carries a $0.035 per-request grounding fee on top of the smart-tier
   tokens. 110 × $0.035 = the bill. Fix: gate grounded search on
   `len(jd_text) >= 4000`, so Adzuna's 500-char snippets skip the
   expensive lookup entirely. Cost dropped 90% on the next scan.

2. **Architecture flip — watched-companies to Adzuna-only.** Scanner shipped
   with a watched-companies list backed by per-company ATS API calls.
   Sounded clean — until two of three watched companies returned 404
   because their ATS slugs had moved. Pivoted to Adzuna-only as the primary
   source, kept ATS direct as future opt-in. Lost some precision; gained
   a working inbox.

3. **Schema-mismatch cascade.** `/jobs/new` failed three times in a row:
   first on `company_name` (table has `company_id` instead), then `url`
   (column is `job_url`), then on a `source = 'auto_pipeline'` value not
   in the CHECK constraint allowlist. Rather than keep patching one
   endpoint, consolidated all create-job paths through a single
   translator and dropped the auto-pipeline endpoint entirely.

## Resume bullets

- Built scanner sweep across 6 ATS providers (Greenhouse/Lever/Ashby/Workday/BambooHR/Teamtailor) with parallelised liveness probes — 6 concurrent workers (src/scanner/runner.py:373)
- Cut LLM eval cost ~90% by JD-length-gating Block D grounded search and deferring Block A-H to manual trigger (commit e4427d2)
- Replaced broken AND-keyword Adzuna sweep with per-role-suffix title_only queries — took it from 0 results to 117 on-target matches per scan
- Designed Block A-H evaluator pipeline with concurrent fast-tier Gemini calls and smart-tier gates for legitimacy + grounded comp research
- Refactored archetype tagging from substring match to word-boundary regex, eliminating false positives where single-letter keywords matched any title
- Wired liveness probe to also extract full JD body in the same HTTP call — 51% of matches now arrive with 5-11K char JDs instead of 500-char snippets
- Built dev-journal CLI for local project tracking with description.md import into resume builder; data project-local + gitignored
- [QUALITATIVE] Consolidated manual-job-add cascade after three consecutive schema bugs; collapsed three call paths into one entry-point translator

## Tech

Next.js 16, TypeScript, Tailwind, React, FastAPI, Python 3.13, Supabase (Postgres + auth), Gemini API, httpx, Pydantic, lucide-react, date-fns

## Domain

LLM evaluation, Job-search automation, Resume tailoring
```

## Worked example — weak input handled honestly

Suppose you're extracting a small side project — a 3-week pet tracker app
with no README, no tests, sparse commits. Honest output:

```markdown
# PetTracker

Lightweight web app for logging pet feeding times and vet visits.

## What it does

Single-page form for logging when each pet was fed, last vet visit, and
upcoming reminders. Reads/writes a local SQLite file.

## Why I built it

Built in 3 weekends to learn SvelteKit. Used by my household (2 pets, 3
people). Not intended for public release.

## How it's built

- Frontend + server: SvelteKit (`src/routes/`)
- Storage: SQLite via `better-sqlite3`
- No auth — single-household assumption

## Impact / Scope

- [QUALITATIVE] Household-only use; ~40 entries logged
- [QUALITATIVE] No tests, no CI; learning project

## Story seeds

1. **SvelteKit form actions vs API routes.** Started with API routes out of
   habit. Switched to form actions mid-project once I understood the
   server-action model. Cut roughly half the client-side JS.

## Resume bullets

- Built SvelteKit pet-tracking app (single-page form + SQLite via better-sqlite3) for household use over three weekends
- [QUALITATIVE] Migrated from API routes to SvelteKit form actions mid-project, simplifying the client-server boundary

## Tech

SvelteKit, TypeScript, SQLite, better-sqlite3

## Domain

Personal productivity
```

Two bullets is fine. The project is small. The honest output is more useful
than a padded one — it gives the resume composer real material when this
project is the *right* one to surface (e.g. for a "show me a small thing
you shipped" question) and leaves it on the bench when it isn't.

## Troubleshooting

**No commits / git history.** Skip Story seeds or use only project-source
material (README, docs). Note this in `[QUALITATIVE]`.

**No README.** Read the entry-point file and any `docs/` folder. Skim the
top-level directory structure. The `What it does` section may need to come
from the source code itself rather than from a docs file.

**Project is archived / abandoned.** Still extract honestly. Mark status
in the pitch line ("Archived; built in 2023"). Story seeds become especially
valuable — they capture what was learned before it stopped.

**No tests.** Don't fabricate a coverage number. Either omit any test
mention or note `[QUALITATIVE] no automated tests; manual verification only`.

**Project is a tutorial / clone / fork.** Be honest. State it in the pitch
line. Resume bullets should focus on what was *changed* or *added*, not on
the original work.

**You don't know who uses it.** Don't guess. Say "personal use",
"household use", "team of N", or `[QUALITATIVE] usage not measured`. Resist
the pull to invent users.

**Stack is unfamiliar to you.** Read more files before writing. If you
genuinely can't tell what something does after 5 minutes of reading, ask
the user; don't invent.

## Self-audit before handing over

Before returning the markdown to the user, check each line against this
list. Fix anything that fails.

- [ ] Every numeric claim cites a source or is prefixed `[QUALITATIVE]`
- [ ] No banned phrase appears anywhere
- [ ] Every Tech entry is in a manifest file you actually saw
- [ ] Every bullet is 15–25 words
- [ ] No more than 2 bullets start with the same verb
- [ ] No em-dash-as-filler; no markdown bold inside a bullet; no emoji
- [ ] Story seeds reference real commits or events, not invented anecdotes
- [ ] `Why I built it` is honest about scope ("personal use" if so)
- [ ] No section is padded just to fill the template — thin honest sections
      beat fluent dishonest ones

When all eight boxes pass, output the markdown. Plain markdown, no fences
around the whole document, no preamble, no closing remarks.
