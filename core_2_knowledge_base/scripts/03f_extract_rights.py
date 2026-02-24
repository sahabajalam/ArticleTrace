"""Phase 3f: Extract right entities from curated lists.

Output:
  parsed_data/entities/rights.json
  parsed_data/relationships/right_links.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.extractors.right_extractor import RightExtractor


def main() -> None:
    parsed_dir = project_root / "parsed_data"
    entities_dir = parsed_dir / "entities"
    rels_dir = parsed_dir / "relationships"

    print("=" * 60)
    print("Phase 3f: Right Extraction")
    print("=" * 60)

    extractor = RightExtractor()
    rights, relationships = extractor.extract_all()

    # Breakdown
    print(f"\n  Rights extracted: {len(rights)}")
    reg_counts: dict[str, int] = {}
    for r in rights:
        reg = r.get("regulation_id", "unknown")
        reg_counts[reg] = reg_counts.get(reg, 0) + 1
    for reg, count in sorted(reg_counts.items()):
        print(f"    {reg:15s}: {count:3d}")

    print(f"\n  Relationships: {len(relationships)}")
    rel_type_counts: dict[str, int] = {}
    for r in relationships:
        t = r["type"]
        rel_type_counts[t] = rel_type_counts.get(t, 0) + 1
    for t, count in sorted(rel_type_counts.items()):
        print(f"    {t:25s}: {count:3d}")

    # Write outputs
    print("\n[+] Writing output files...")

    rights_path = entities_dir / "rights.json"
    rights_path.write_text(
        json.dumps(rights, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  rights.json: {len(rights)} entities")

    rels_path = rels_dir / "right_links.json"
    rels_path.write_text(
        json.dumps(relationships, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  right_links.json: {len(relationships)} relationships")

    # Exit gate
    print("\n" + "=" * 60)
    if len(rights) >= 15:
        print("** EXIT GATE PASSED **")
    else:
        print(f"** WARNING: Only {len(rights)} rights extracted. Expected >= 15. **")
    print("=" * 60)


if __name__ == "__main__":
    main()
