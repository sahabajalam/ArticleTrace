"""Phase 3b: Extract obligations and exemptions from all articles.

Uses hybrid approach:
  - Rule-based: pattern matching for shall/must/may + actor detection
  - LLM (optional): Gemini refinement for calibration set

Output:
  parsed_data/entities/obligations.json
  parsed_data/entities/exemptions.json
  parsed_data/relationships/obligation_links.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.extractors.obligation_extractor import ObligationExtractor


def main() -> None:
    parsed_dir = project_root / "parsed_data"
    entities_dir = parsed_dir / "entities"
    rels_dir = parsed_dir / "relationships"

    print("=" * 60)
    print("Phase 3b: Obligation & Exemption Extraction")
    print("=" * 60)

    # Load articles
    gdpr_articles = _load_json(parsed_dir / "legal" / "gdpr_articles.json")
    ai_articles = _load_json(parsed_dir / "legal" / "eu_ai_act_articles.json")

    print(f"  GDPR articles: {len(gdpr_articles)}")
    print(f"  AI Act articles: {len(ai_articles)}")

    # Extract (rule-based only for now, LLM refinement is optional)
    extractor = ObligationExtractor(use_llm=False)

    print("\n[1/2] Extracting from GDPR articles...")
    gdpr_obls, gdpr_exs = extractor.extract_from_articles(gdpr_articles, "GDPR")
    print(f"  GDPR obligations: {len(gdpr_obls)}")
    print(f"  GDPR exemptions: {len(gdpr_exs)}")

    print("\n[2/2] Extracting from AI Act articles...")
    ai_obls, ai_exs = extractor.extract_from_articles(ai_articles, "EU_AI_ACT")
    print(f"  AI Act obligations: {len(ai_obls)}")
    print(f"  AI Act exemptions: {len(ai_exs)}")

    # Deduplicate by ID
    obligations = _dedup(gdpr_obls + ai_obls)
    exemptions = _dedup(gdpr_exs + ai_exs)

    # Build relationships: Obligation -> Article (REQUIRES / PROHIBITS / PERMITS)
    obl_rels: list[dict] = []
    for obl in obligations:
        art_ref = obl.get("article_reference")
        if art_ref:
            rel_type = {
                "MUST": "REQUIRES",
                "SHALL": "REQUIRES",
                "MUST_NOT": "PROHIBITS",
                "MAY": "PERMITS",
                "RIGHT": "PERMITS",
            }.get(obl["obligation_type"], "REQUIRES")

            obl_rels.append({
                "source_id": obl["id"],
                "target_id": art_ref,
                "type": rel_type,
                "properties": {
                    "obligation_type": obl["obligation_type"],
                    "paragraph": obl.get("paragraph_number"),
                },
            })

        # Link to duty_bearer actor if known
        bearer = obl.get("duty_bearer")
        if bearer and bearer.startswith("ACTOR_"):
            obl_rels.append({
                "source_id": obl["id"],
                "target_id": bearer,
                "type": "APPLIES_TO",
                "properties": {"role": "duty_bearer"},
            })

    for ex in exemptions:
        art_ref = ex.get("article_reference")
        if art_ref:
            obl_rels.append({
                "source_id": ex["id"],
                "target_id": art_ref,
                "type": "EXEMPTS",
                "properties": {
                    "paragraph": ex.get("paragraph_number"),
                },
            })

    # Write outputs
    print("\n[+] Writing output files...")

    obl_path = entities_dir / "obligations.json"
    obl_path.write_text(
        json.dumps(obligations, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  obligations.json: {len(obligations)} entities")

    ex_path = entities_dir / "exemptions.json"
    ex_path.write_text(
        json.dumps(exemptions, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  exemptions.json: {len(exemptions)} entities")

    rel_path = rels_dir / "obligation_links.json"
    rel_path.write_text(
        json.dumps(obl_rels, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  obligation_links.json: {len(obl_rels)} relationships")

    # Summary stats
    print("\n" + "=" * 60)
    print("Phase 3b Summary")
    print("=" * 60)

    # Obligation type breakdown
    type_counts: dict[str, int] = {}
    for o in obligations:
        t = o["obligation_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t:15s}: {c:4d}")
    print(f"  {'exemptions':15s}: {len(exemptions):4d}")
    print(f"  {'TOTAL':15s}: {len(obligations) + len(exemptions):4d} entities")
    print(f"  {'relationships':15s}: {len(obl_rels):4d} edges")

    # Actor coverage
    bearer_count = sum(1 for o in obligations if o.get("duty_bearer"))
    cond_count = sum(1 for o in obligations if o.get("condition"))
    print(f"\n  Duty bearer detected: {bearer_count}/{len(obligations)} ({100*bearer_count//max(len(obligations),1)}%)")
    print(f"  Condition detected:   {cond_count}/{len(obligations)} ({100*cond_count//max(len(obligations),1)}%)")

    # Exit gate
    total = len(obligations) + len(exemptions)
    if total < 50:
        print(f"\n** WARNING: Only {total} obligations+exemptions extracted. May need LLM refinement. **")
    else:
        print("\n** EXIT GATE PASSED **")

    print("=" * 60)


def _dedup(items: list[dict]) -> list[dict]:
    """Deduplicate by ID, keeping first occurrence."""
    seen: set[str] = set()
    result = []
    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            result.append(item)
    return result


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
