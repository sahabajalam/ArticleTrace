"""Phase 2a: Extract structural relationships from parsed data.

Runs without Neo4j -- pure data transformation.
Outputs relationship JSON files for later loading.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.extractors.structural_extractor import StructuralExtractor

PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_OUTPUT_DIR = PARSED_DATA_DIR / "relationships"


def write_json(data: list | dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def main():
    print("=" * 60)
    print("PHASE 2a: Extract Structural Relationships")
    print("=" * 60)

    extractor = StructuralExtractor(PARSED_DATA_DIR)
    results = extractor.extract_all()

    # Write each category
    for category, rels in results.items():
        output_path = REL_OUTPUT_DIR / f"{category}.json"
        write_json(rels, output_path)
        print(f"  {category}: {len(rels)} relationships")

    # Summary and validation
    total = sum(len(r) for r in results.values())
    print(f"\n  Total relationships extracted: {total}")

    # Detailed breakdown
    print("\n  Breakdown by relationship type:")
    type_counts: dict[str, int] = {}
    for rels in results.values():
        for rel in rels:
            t = rel["type"]
            type_counts[t] = type_counts.get(t, 0) + 1

    for t, c in sorted(type_counts.items()):
        print(f"    {t:20s}: {c:5d}")

    # Validation checks
    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    # Check containment completeness
    containment = results["containment"]
    contains_count = sum(1 for r in containment if r["type"] == "CONTAINS")
    part_of_count = sum(1 for r in containment if r["type"] == "PART_OF")
    print(f"  CONTAINS edges: {contains_count}")
    print(f"  PART_OF edges:  {part_of_count}")

    # Check reference density
    references = results["references"]
    ref_sources = set(r["source_id"] for r in references)
    print(f"  Articles with cross-references: {len(ref_sources)} / 212")

    # Check interpretive coverage
    interprets = results["interprets"]
    interp_sources = set(r["source_id"] for r in interprets)
    print(f"  Entities with INTERPRETS links: {len(interp_sources)}")

    # Check citation coverage
    cites = results["cites"]
    cite_sources = set(r["source_id"] for r in cites)
    print(f"  Entities with CITES links: {len(cite_sources)}")

    print("\n  Phase 2a complete. Ready for Neo4j loading.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
