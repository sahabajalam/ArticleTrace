# Portfolio Entry Guide

Generic instructions for filling portfolio entries for any technical
project. Use alongside the project-specific entry document.

---

## What a portfolio entry has to do

Reviewers (recruiters, hiring managers, peers) spend 10–30 seconds on
the card view before deciding whether to click into the detail view.
They spend another 30–60 seconds on the detail view before deciding
whether to open the GitHub repo or live demo. Every field you fill is
optimizing one of those moments.

Three jobs the entry has to perform, in order:

1. **Filter** — does this project match what the reviewer is looking
   for? (Title, short description, image, category.)
2. **Convince** — is this project technically substantial and recent?
   (Long description, tech stack, features.)
3. **Verify** — does the work actually exist, and does it run?
   (GitHub URL, Demo URL.)

If your entry fails at filter, the reviewer never reaches convince.
If it fails at convince, they never reach verify. Optimize in that
order.

---

## Field-by-field

### ID / Slug

The URL-safe identifier. Rules:

- Lowercase, hyphenated, ASCII only.
- 3–6 words. `alloycode-compliance-scanner` works;
  `my-cool-graph-rag-thing-2-final` doesn't.
- Describe the **product**, not the technology. `compliance-scanner`
  ages well; `langchain-rag-app` looks dated within a year.
- Stable. If you rename the project, decide whether to update the
  slug (breaks any inbound links) or keep it (looks slightly off but
  doesn't break links). Inbound traffic on a portfolio is rarely
  enough to justify breaking links — usually keep the old slug.

### Category

Pick one canonical category. Common taxonomy:

- **AI / ML** — anything where the model or retrieval layer is the
  point.
- **Developer Tools** — CLIs, SDKs, IDE plugins, scanners, linters.
- **Web** — frontend-heavy or full-stack web apps without a strong
  AI/data angle.
- **Data Engineering / Pipelines** — ETL, ingestion, analytics.
- **Infrastructure / DevOps** — CI/CD, monitoring, deployment
  tooling.
- **Compliance / Legal Tech / FinTech / HealthTech** — domain-
  specific.

If the project genuinely spans two, pick the one a reviewer would
search by. A "RAG application for legal docs" goes under AI, not
Legal Tech, because the reviewer searching for AI projects is the
intended audience.

### Title

The hook. Two parts: `<Product>: <one-line description of what it
does>`. Examples:

- `AlloyCode: Static Scanner for EU AI Act & GDPR Compliance` ✓
- `MyApp: A Cool Project I Built` ✗ (no information)
- `Smart Graph RAG: Navigating the EU AI Act & GDPR` ⚠ (leads with
  technology, not action)

Rules:

- Under 70 characters so it doesn't truncate.
- Avoid framework names in the title. Frameworks change; problems
  don't.
- Avoid superlatives ("Revolutionary", "Cutting-edge", "Next-gen") —
  they signal the writer is overselling.

### Short description

One sentence. 120–160 characters is the sweet spot for card layouts.
Cover three things:

1. The action (what verb does this project enable?).
2. The input/output (what does it consume; what does it produce?).
3. The differentiator (what does this do that off-the-shelf tools
   don't?).

Example: `Static analysis scanner that maps AI codebases to concrete
EU AI Act and GDPR obligations with file-and-line precision.`

- Action: scan / map.
- Input/output: AI codebase → regulatory obligations.
- Differentiator: file-and-line precision (vs. self-reported answers
  or runtime audits).

### Long description

The detail view's centerpiece. 2–4 paragraphs. Structure:

**Paragraph 1 — what it does, concretely.** Skip the corporate
"transforming the way businesses..." opener. Describe the user-facing
behavior. "Point it at a GitHub repo and it returns a structured
report of likely regulatory violations."

**Paragraph 2 — why it matters or what gap it fills.** This is where
you cite competitors / adjacent tools and explain the gap. Reviewers
notice market awareness; "I built X because nobody else does Y" is
stronger than "I built X to learn Z."

**Paragraph 3 — how it works, technically.** This is where tech depth
goes. Name 3–5 architectural choices and explain *why* you made them.
"Deterministic scanners find facts; LLMs only synthesize narrative"
is a defensible choice. "Used LangChain because it's popular" isn't.

**(Optional) Paragraph 4 — current state and roadmap.** "Phase 1
ships X; Phase 2 adds Y" reads as honest and shows direction. Skip
this if the project is feature-complete.

Rules:

- Don't list features in the long description — features get their
  own field.
- Don't list the tech stack here either — that gets its own field.
- Write in active voice. "The system maps detected patterns to
  obligations" not "Detected patterns are mapped to obligations by
  the system."
- One paragraph = one idea. If a paragraph has more than one idea,
  split it.

### Tech stack

A list of 8–12 items the project actively uses. Hard rules:

- **Be honest.** If you removed a library, remove it from the stack.
  Reviewers cross-check against `package.json` / `pyproject.toml` and
  spot stale lists. Stale stack listings read worse than a shorter
  honest list.
- **Order by importance.** Differentiators first; infrastructure
  last. For an AI project: `Neo4j` and `Gemini` come before
  `Docker` and `Cloud Run`.
- **Prefer specific names.** `Gemini 2.5 Flash` is more useful than
  `LLM`. `Next.js 16` is more useful than `React`.
- **Skip language-level libraries.** `requests`, `pydantic`, `numpy`
  belong in the codebase, not the portfolio. Reviewers assume them.
- **Group versions when relevant.** If you're using a notably-recent
  version (Next.js 16, Python 3.13), call it out. If you're on a
  stable old version, just name the framework.

Bad: `Python, FastAPI, requests, pydantic, numpy, json, asyncio,
typing`.

Good: `Neo4j (graph + native vector index), Gemini 2.5 Flash,
LangGraph, FastAPI, Next.js 16, PostgreSQL, Redis, Docker, Cloud
Run`.

### Key features

3–6 user-visible capabilities. Not implementation details. Format
each as one line, ~80–120 characters.

Rules:

- Lead with a noun describing the user-visible capability.
- Avoid framework names. "LangGraph multi-agent workflow" is
  borderline acceptable because the orchestration *is* the feature;
  "implemented using LangChain abstractions" is not.
- If two features are about the same thing at different abstraction
  levels, drop the lower-level one. "Hybrid retrieval (RRF)" beats
  "Reciprocal rank fusion of two ranked candidate lists".
- Make them measurably true. "97.5% context recall" is better than
  "high accuracy" — reviewers can check.
- Don't pad to hit a number. 4 strong features beats 6 weak ones.

### Image

This is the only visual on the card. It does more work than any
single text field.

**Aspect ratio:** typically 16:9 (1200×675) or 4:3 (1200×900).
Match the portfolio's grid.

**Format:** PNG for screenshots and diagrams, JPG only if the image
is photographic.

**Three composition patterns that work:**

1. **Architecture diagram.** A clean three-tier or four-box drawing
   showing the data flow. Best for backend / infrastructure projects
   where the visual story is the system, not the UI.
2. **Product screenshot.** A real screen of the running app showing
   a real result, not a placeholder. Best for projects with strong
   UX. Crop tightly — the whole window with browser chrome dilutes
   the impact.
3. **Data visualization.** A graph, a chart, a network diagram.
   Best for projects where the *data* is the differentiator.

**Avoid:**

- Stock illustrations (the abstract "AI brain" / "neural network
  glow" graphics).
- Logos of frameworks you used (Python logo, FastAPI logo). Reviewers
  parse this as filler.
- Image filenames with spaces or double extensions (`MyApp.png.png`).
  Stick to `kebab-case-names.png`.

**Filename:** `<slug>.png` — same as your project slug. Easy to find
later, no spaces, no special characters.

### GitHub URL

The URL must be public, must work, and must point to a repo that
opens cleanly. Pre-publication checklist:

- README.md at the repo root (not buried under `docs/`). Should open
  with one paragraph explaining what the project is.
- Live `main` (or `master`) branch — not a feature branch.
- License file present (MIT, Apache 2, or BSD-3 are the safe
  defaults; pick one).
- No leaked secrets in history. Audit `.env`, `.envrc`,
  `credentials.json`, anything matching `secret*`. Use `git log -p
  -- '**/*.env'` to verify nothing got committed.
- A `git log` that shows real iterative work, not 50 "WIP" commits or
  a single "Initial commit" of 5,000 files. Reviewers do look at
  this.

If the repo is private, the entry is broken. Either make it public
(and audit secrets first) or remove the GitHub URL field rather than
linking to a 404.

### Demo URL

A live, reachable URL where the project actually runs. This is the
single highest-leverage field — a working demo turns a portfolio
entry from "interesting on paper" to "they shipped it."

Rules:

- **The URL must work.** Test it from an incognito window in two
  different browsers before publishing. A dead demo URL is worse
  than no demo URL.
- **The demo must show the differentiator.** If your project's pitch
  is "static scanner with file:line citations," the demo must let
  the reviewer see a finding with a file:line citation. Don't gate
  the differentiator behind login or paid tier.
- **Add reviewer-friendly defaults.** Pre-fill an example input. A
  reviewer who lands on a blank input form and doesn't know what to
  type bounces in 5 seconds.
- **Handle cold starts gracefully.** If the demo is on a free tier
  with cold starts (Cloud Run min-instances=0, Vercel free), warm
  it up by pinging a health endpoint on a schedule (GitHub Actions
  cron is free).

**If the demo isn't ready, pick one:**

1. **Hide the field.** Better than a broken URL.
2. **Replace with a video walkthrough.** 60-second Loom or unlisted
   YouTube showing a real run from input to result. Less impressive
   than a live demo, more impressive than nothing.
3. **Link to a deployed stub.** A "demo coming soon" page with
   instructions to clone and run locally. Last resort.

---

## Maintenance

Portfolio entries decay. Schedule reviews:

- **Quarterly:** verify all Demo URLs still resolve. Cloud Run
  services get cleaned up, free tiers get suspended, custom domains
  expire.
- **After every major refactor:** update the tech stack and the long
  description's architecture paragraph. Stale tech listings are the
  most common form of decay.
- **After a pivot:** treat the pivot as a new project. Replace the
  slug, title, image, and descriptions in one pass — don't try to
  edit fields one at a time over weeks. The half-pivoted state reads
  worse than either the old or the new state.

---

## Common anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Title that names the framework instead of the action | Reviewers searching for problems, not technologies |
| Listing every library in the tech stack | Reads as padding; dilutes the actually-important items |
| Stale demo URL | Worse than no demo URL — signals the project is abandoned |
| Stock illustration as the image | Indistinguishable from a hundred other portfolios |
| Long description that opens with "In an era when..." | Boilerplate; reviewers skim past it to the next paragraph |
| Features that are framework names ("Built with LangChain") | Frameworks aren't features; what does it *do* for the user? |
| Superlatives ("Revolutionary AI-powered solution") | Signals overselling; reviewers discount the rest |
| Same wording across multiple project entries | Reads as a template; weakens each entry individually |

---

## Final pass before publish

Read the card view. Then read the detail view. For each field, ask:
*if I had 5 seconds, would this make me click?* If not, rewrite or
remove it. The shortest honest entry beats the most complete padded
one.
