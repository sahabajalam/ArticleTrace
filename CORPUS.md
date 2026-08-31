# Corpus provenance and reuse terms

AlloyCode's code is Apache-2.0 (see `LICENSE`). **That licence does not and
cannot cover the regulatory content this repository redistributes** — those
texts belong to the European Union. This file records where each dataset came
from, what may be done with it, and what has *not* been verified.

Read this before redistributing the repository, forking it publicly, or
publishing anything derived from `knowledge_engine/parsed_data/`.

---

## 1. What is actually shipped

| Path | Contents | Size | In the public repo? |
|---|---|---|---|
| `knowledge_engine/parsed_data/legal/` | Structured articles, recitals, annexes, definitions from the EU AI Act and GDPR | ~4 MB | yes |
| `knowledge_engine/parsed_data/entities/` | Extracted concepts, rights, penalties, actors, risk categories | ~1 MB | yes |
| `knowledge_engine/parsed_data/relationships/` | Derived edges between the above | small | yes |
| `knowledge_engine/parsed_data/interpretive/` | Derivations of EDPB guidelines, case law, enforcement actions | ~2.5 MB | yes — **see §3** |
| `legacy_prototypes/New_Data/` | Raw source text (AI Act, CJEU, EDPB) used to build the above | 14 MB | **no** — gitignored and untracked |
| `knowledge_engine/backups/` | Neo4j JSONL dumps of the built graph | ~100 MB | **no** — gitignored |

`parsed_data/` is not a verbatim copy of the regulations. It is a structured
derivation: text split into articles and recitals, tagged with identifiers,
and cross-linked. Some fields quote regulatory text directly.

---

## 2. EU AI Act and GDPR (EUR-Lex) — verified

**Source:** [EUR-Lex](https://eur-lex.europa.eu) — Regulation (EU) 2024/1689
(AI Act) and Regulation (EU) 2016/679 (GDPR).

**Terms:** Reuse of Commission documents is governed by
[Commission Decision 2011/833/EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32011D0833)
of 12 December 2011. Documents are made available for reuse without
application, and the Publications Office applies a
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence to editorial
content it owns. Reuse is permitted provided **appropriate credit is given and
changes are indicated** — both of which this file and `NOTICE` do.

**Excluded from that permission:** logos, trademarks, and other industrial
property rights. This project reproduces none of those.

**Authenticity caveat, and it matters for a compliance tool.** Per the
[EUR-Lex legal notice](https://eur-lex.europa.eu/content/legal-notice/legal-notice.html),
only the Official Journal of the European Union in its authenticated form is
legally authentic. `parsed_data/` is a machine-processed derivation and may
contain parsing errors. **Do not cite it as authoritative.** Findings produced
by this scanner point at articles so a human can go read the real text.

---

## 3. EDPB guidelines — NOT VERIFIED, read before publishing

`knowledge_engine/parsed_data/interpretive/edpb_guidelines.json` (~2.2 MB) is
derived from European Data Protection Board guidelines.

**The EDPB's specific reuse terms were not independently verified when this
file was written.** The EDPB is an EU body and most EU institutions publish
under "reproduction authorised provided the source is acknowledged" or CC BY
4.0, but *the EDPB's own legal notice was not successfully retrieved and is not
quoted here.* Assuming the general pattern applies would be a guess, and this
project does not guess about other people's rights.

**Before making this repository public, do one of:**

1. **Verify** the EDPB's terms at <https://www.edpb.europa.eu> and record the
   operative wording in this section; or
2. **Exclude** the file. It powers the `interpretive` vector collection (56 of
   2,198 documents). Removing it degrades interpretive coverage but leaves the
   AI Act / GDPR core intact:

   ```bash
   git rm --cached knowledge_engine/parsed_data/interpretive/edpb_guidelines.json
   echo "knowledge_engine/parsed_data/interpretive/edpb_guidelines.json" >> .gitignore
   ```

   Then rebuild the graph (see README "Build the knowledge graph"); the golden
   tests do not depend on the interpretive collection.

The same question applies to `case_law.json` (CJEU) and
`enforcement_actions.json` (national DPA decisions) in the same directory.
CJEU case law is published by the Court and generally reusable on the same
Commission terms; national DPA decisions vary **by member state** and are the
least certain of the three.

---

## 4. The raw corpus is deliberately not distributed

`legacy_prototypes/New_Data/` holds the raw source text the parser consumed
(208 files, 14 MB: AI Act text, CJEU rulings, EDPB guideline PDFs converted to
text). It is listed in `.gitignore` and untracked as of 2026-08-31.

Two reasons: it is the largest redistribution surface with the least verified
terms, and nothing in the build pipeline needs it. Scripts `02`–`05` build the
knowledge graph from `parsed_data/`; only script `01` (raw → parsed) reads the
raw corpus, and that step has already been run.

If you want to re-derive `parsed_data/` from scratch, fetch the sources
yourself from EUR-Lex and the EDPB and point `raw_data_dir` at them.

---

## 5. If you contribute data

Do not add regulatory or third-party text to this repository without recording
its source and reuse terms in this file, in the same pull request. A compliance
tool that plays loose with other people's licensing terms is not one anyone
should trust with theirs.
