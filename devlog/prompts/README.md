# Prompt Library

A curated, refined, versioned store of reusable prompts. Same discipline as the rest of `devlog/` (frontmatter, status, refinement before save) — different target: prompts that worked, not system state.

This file is a condensed playbook. The canonical source is [`../../DOCS_PLAYBOOK.md`](../../DOCS_PLAYBOOK.md) §13. If anything here disagrees with that, the playbook wins.

## The core rule

**Never save raw prompts. Always refine first.** The refinement IS the value. A raw transcript captures what you said; a refined entry captures *why it worked*. Without refinement, you have a chat archive — not a library.

## When to save

Save when:
- A long prompt produced a notably good result and feels reusable.
- The prompt encodes a non-obvious technique (a structure, a constraint, a framing) that took effort to discover.
- You'll reuse it in this project later, or carry it to other projects.

Don't save:
- One-off questions, trivial prompts.
- Prompts that didn't work (unless explicitly archiving failures with `status: failed`).
- Prompts that are 80% boilerplate, 20% one-line context — save just the technique.

## The save workflow (7 steps)

When the user says "save this prompt" (or similar), an AI agent should:

1. **Locate** the raw prompt in the user's recent turn. Ask if ambiguous.
2. **Identify what made it work** — goal, technique, constraints, what's project-specific vs portable. *This is the load-bearing step.* Skip it and refinement is cosmetic.
3. **Refine** — tighten language, replace project-specific bits with `<UPPER_SNAKE_CASE>` placeholders, preserve the user's voice and sharp framing.
4. **Pick a kebab-case slug** — short, descriptive, action-oriented (e.g., `research-codebase-then-docs`, `audit-system-arch`).
5. **Save to `<slug>.md`** in this directory using [`_TEMPLATE.md`](_TEMPLATE.md). Fill every frontmatter field.
6. **If updating an existing prompt** of the same purpose — edit in place, bump `last_used:`, append to `## History`.
7. **Report back** — one line on what was saved + why this version is better than raw.

## Scope: portable vs project

- **`scope: portable`** — works in any project; all project-specific bits replaced with placeholders. Carry to other repos.
- **`scope: project`** — references project-specific code or conventions. Use as reference when writing the portable version; don't carry verbatim.

## Cross-project portability

When carrying prompts to another project:

1. Copy this `prompts/` directory wholesale.
2. Filter to `scope: portable` entries (delete or quarantine `scope: project`).
3. Drop entries where `tags:` don't match the new project's domain.
4. For each carried prompt, update `origin_session:` with a note about the new project.
5. The `<PLACEHOLDER>` tokens make filling in new-project context obvious.

## Anti-patterns

1. **Saving raw prompts without refinement.** Defeats the point.
2. **Vague slugs.** `good-prompt.md`, `prompt-1.md`. You won't find them in 3 months.
3. **Versioning by filename.** `audit-v1.md`, `audit-v2.md`. The file IS the latest; history lives in `## History`.
4. **Placeholder explosion.** If 80% of the prompt is `<PLACEHOLDERS>`, you've abstracted too far.
5. **Stripping the user's voice.** Sharp framing was probably what made the prompt work.
6. **No `Notes on what works` section.** Without it the prompt is opaque.

## Current entries

| Slug | Scope | Tags | Last used |
|---|---|---|---|
| [`research-codebase-then-docs.md`](research-codebase-then-docs.md) | portable | research, methodology, documentation | 2026-05-20 |

When the library grows past ~15 entries, sub-folder by category (`research/`, `implementation/`, `review/`, `writing/`, `meta/`). Start flat.
