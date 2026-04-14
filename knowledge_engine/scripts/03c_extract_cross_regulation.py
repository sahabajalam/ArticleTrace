"""Phase 3c: Extract cross-regulation COMPLEMENTS edges.

Combines:
  1. Hand-curated mappings (known GDPR <-> AI Act interactions)
  2. Auto-detected cross-references from parsed article text

Output:
  parsed_data/relationships/complements.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.extractors.cross_regulation_extractor import CrossRegulationExtractor


def main() -> None:
    parsed_dir = project_root / "parsed_data"
    rels_dir = parsed_dir / "relationships"

    print("=" * 60)
    print("Phase 3c: Cross-Regulation COMPLEMENTS Extraction")
    print("=" * 60)

    extractor = CrossRegulationExtractor()

    # 1. Hand-curated mappings
    print("\n[1/2] Extracting hand-curated cross-regulation mappings...")
    curated = extractor.extract_cross_regulation_edges()
    print(f"  Curated COMPLEMENTS: {len(curated)} edges (bidirectional)")

    # 2. Auto-detected from parsed articles
    print("\n[2/2] Auto-detecting cross-references from parsed text...")
    gdpr_articles = _load_json(parsed_dir / "legal" / "gdpr_articles.json")
    ai_articles = _load_json(parsed_dir / "legal" / "eu_ai_act_articles.json")
    auto = extractor.extract_auto_cross_references(gdpr_articles, ai_articles)
    print(f"  Auto-detected: {len(auto)} edges")

    # Combine and deduplicate
    all_edges = curated + auto
    deduped = _dedup_edges(all_edges)
    print(f"\n  Total (deduped): {len(deduped)} COMPLEMENTS edges")

    # Write output
    out_path = rels_dir / "complements.json"
    out_path.write_text(
        json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  Written to: {out_path.name}")

    # Breakdown by interaction type
    print("\n" + "=" * 60)
    print("Interaction Type Breakdown")
    print("=" * 60)
    type_counts: dict[str, int] = {}
    for e in deduped:
        it = e["properties"].get("interaction_type", "UNKNOWN")
        type_counts[it] = type_counts.get(it, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t:20s}: {c:4d}")
    print(f"  {'TOTAL':20s}: {len(deduped):4d}")
    print("=" * 60)


def _dedup_edges(edges: list[dict]) -> list[dict]:
    """Deduplicate edges by (source, target, interaction_type)."""
    seen: set[str] = set()
    result = []
    for e in edges:
        key = f"{e['source_id']}|{e['target_id']}|{e['properties'].get('interaction_type', '')}"
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
