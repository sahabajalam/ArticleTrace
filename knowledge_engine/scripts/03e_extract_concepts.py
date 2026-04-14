"""Phase 3e: Extract concept entities from curated lists.

Output:
  parsed_data/entities/concepts.json
  parsed_data/relationships/concept_links.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.extractors.concept_extractor import ConceptExtractor


def main() -> None:
    parsed_dir = project_root / "parsed_data"
    entities_dir = parsed_dir / "entities"
    rels_dir = parsed_dir / "relationships"

    print("=" * 60)
    print("Phase 3e: Concept Extraction")
    print("=" * 60)

    # Load all articles for keyword matching
    gdpr_articles = _load_json(parsed_dir / "legal" / "gdpr_articles.json")
    ai_articles = _load_json(parsed_dir / "legal" / "eu_ai_act_articles.json")
    all_articles = gdpr_articles + ai_articles
    print(f"  Loaded {len(all_articles)} articles for keyword matching")

    # Extract
    extractor = ConceptExtractor()
    concepts, relationships = extractor.extract_all(all_articles)

    # Category breakdown
    print(f"\n  Concepts extracted: {len(concepts)}")
    cat_counts: dict[str, int] = {}
    for c in concepts:
        cat = c.get("category", "unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    for cat, count in sorted(cat_counts.items()):
        print(f"    {cat:25s}: {count:3d}")

    print(f"\n  Relationships: {len(relationships)}")
    rel_type_counts: dict[str, int] = {}
    for r in relationships:
        t = r["type"]
        rel_type_counts[t] = rel_type_counts.get(t, 0) + 1
    for t, count in sorted(rel_type_counts.items()):
        print(f"    {t:25s}: {count:3d}")

    # Write outputs
    print("\n[+] Writing output files...")

    concepts_path = entities_dir / "concepts.json"
    concepts_path.write_text(
        json.dumps(concepts, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  concepts.json: {len(concepts)} entities")

    rels_path = rels_dir / "concept_links.json"
    rels_path.write_text(
        json.dumps(relationships, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  concept_links.json: {len(relationships)} relationships")

    # Exit gate
    print("\n" + "=" * 60)
    if len(concepts) >= 40:
        print("** EXIT GATE PASSED **")
    else:
        print(f"** WARNING: Only {len(concepts)} concepts extracted. Expected >= 40. **")
    print("=" * 60)


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
