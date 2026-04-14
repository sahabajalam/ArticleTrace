"""Phase 3: Extract semantic entities (definitions, actors, data types, etc.)

Runs all rule-based extractors and writes output to parsed_data/entities/.
Also extracts DEFINES relationships linking definitions to their source articles.

Rule-based (deterministic):
  - Definitions from Art 3 / Art 4
  - Actors (18 entities)
  - Data Types (17 entities)
  - Risk Categories (4 entities)
  - AI System Types (20 entities)
  - Penalties (6 entities)

Output files:
  parsed_data/entities/definitions.json
  parsed_data/entities/actors.json
  parsed_data/entities/data_types.json
  parsed_data/entities/risk_categories.json
  parsed_data/entities/ai_system_types.json
  parsed_data/entities/penalties.json
  parsed_data/relationships/defines.json
  parsed_data/relationships/semantic_links.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.extractors.definition_extractor import DefinitionExtractor
from src.extractors.rule_based_extractor import RuleBasedExtractor


def main() -> None:
    parsed_dir = project_root / "parsed_data"
    entities_dir = parsed_dir / "entities"
    rels_dir = parsed_dir / "relationships"
    entities_dir.mkdir(parents=True, exist_ok=True)
    rels_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Phase 3: Semantic Entity Extraction (Rule-Based)")
    print("=" * 60)

    all_entities: dict[str, list] = {}
    all_relationships: list[dict] = []

    # ----------------------------------------------------------------
    # 1. Definitions from Art 4 (GDPR) and Art 3 (AI Act)
    # ----------------------------------------------------------------
    print("\n[1/6] Extracting definitions from Art 4 (GDPR) + Art 3 (AI Act)...")
    defn_extractor = DefinitionExtractor()

    gdpr_articles = _load_json(parsed_dir / "legal" / "gdpr_articles.json")
    ai_articles = _load_json(parsed_dir / "legal" / "eu_ai_act_articles.json")

    definitions: list[dict] = []
    defines_rels: list[dict] = []

    # GDPR Art 4
    gdpr_art4 = [a for a in gdpr_articles if a["id"] == "GDPR_ART_4"]
    if gdpr_art4:
        gdpr_defs = defn_extractor.extract_from_article(gdpr_art4[0], "GDPR")
        definitions.extend(gdpr_defs)
        for d in gdpr_defs:
            defines_rels.append({
                "source_id": "GDPR_ART_4",
                "target_id": d["id"],
                "type": "DEFINES",
                "properties": {"definition_number": d["definition_number"]},
            })
        print(f"  GDPR Art 4: {len(gdpr_defs)} definitions")
    else:
        print("  WARNING: GDPR Art 4 not found in parsed data!")

    # AI Act Art 3
    ai_art3 = [a for a in ai_articles if a["id"] == "AIACT_ART_3"]
    if ai_art3:
        ai_defs = defn_extractor.extract_from_article(ai_art3[0], "EU_AI_ACT")
        definitions.extend(ai_defs)
        for d in ai_defs:
            defines_rels.append({
                "source_id": "AIACT_ART_3",
                "target_id": d["id"],
                "type": "DEFINES",
                "properties": {"definition_number": d["definition_number"]},
            })
        print(f"  AI Act Art 3: {len(ai_defs)} definitions")
    else:
        print("  WARNING: AI Act Art 3 not found in parsed data!")

    print(f"  Total definitions: {len(definitions)}")
    all_entities["definitions"] = definitions
    all_relationships.extend(defines_rels)

    # ----------------------------------------------------------------
    # 2-6. Rule-based entities
    # ----------------------------------------------------------------
    rb = RuleBasedExtractor()

    extractors = [
        ("2/6", "actors", rb.extract_actors),
        ("3/6", "data_types", rb.extract_data_types),
        ("4/6", "risk_categories", rb.extract_risk_categories),
        ("5/6", "ai_system_types", rb.extract_ai_system_types),
        ("6/6", "penalties", rb.extract_penalties),
    ]

    for step, name, fn in extractors:
        print(f"\n[{step}] Extracting {name}...")
        entities = fn()
        all_entities[name] = entities
        print(f"  {name}: {len(entities)} entities")

    # ----------------------------------------------------------------
    # Build semantic relationships from rule-based entities
    # ----------------------------------------------------------------
    print("\n[+] Building semantic relationships...")
    semantic_rels = _build_semantic_relationships(all_entities)
    all_relationships.extend(semantic_rels)
    print(f"  Semantic relationships: {len(semantic_rels)}")

    # ----------------------------------------------------------------
    # Write output files
    # ----------------------------------------------------------------
    print("\n[+] Writing output files...")

    for name, entities in all_entities.items():
        out_path = entities_dir / f"{name}.json"
        out_path.write_text(
            json.dumps(entities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"  {out_path.name}: {len(entities)} entities")

    # Write DEFINES relationships
    defines_path = rels_dir / "defines.json"
    defines_path.write_text(
        json.dumps(defines_rels, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  defines.json: {len(defines_rels)} relationships")

    # Write semantic relationships
    semantic_path = rels_dir / "semantic_links.json"
    semantic_path.write_text(
        json.dumps(semantic_rels, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  semantic_links.json: {len(semantic_rels)} relationships")

    # ----------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------
    total_entities = sum(len(v) for v in all_entities.values())
    total_rels = len(all_relationships)

    print("\n" + "=" * 60)
    print("Phase 3 Summary (Rule-Based)")
    print("=" * 60)
    for name, entities in all_entities.items():
        print(f"  {name:20s}: {len(entities):4d} entities")
    print(f"  {'TOTAL':20s}: {total_entities:4d} entities")
    print(f"  {'relationships':20s}: {total_rels:4d} edges")
    print("=" * 60)

    # Exit gate
    if total_entities < 50:
        print("\n** EXIT GATE FAILED: Expected 50+ entities, got", total_entities)
        sys.exit(1)
    else:
        print("\n** EXIT GATE PASSED **")
        print("  Rule-based extraction complete.")
        print("  Next: Run obligation/exemption extraction (Phase 3b).")


def _build_semantic_relationships(all_entities: dict[str, list]) -> list[dict]:
    """Build relationships between semantic entities and articles.

    Links:
    - Actor -> definition_article (APPLIES_TO)
    - DataType -> regulated_by articles (APPLIES_TO)
    - DataType -> parent DataType (PART_OF)
    - RiskCategory -> source_article (APPLIES_TO)
    - AISystemType -> risk_category (PART_OF)
    - AISystemType -> source_article/annex (APPLIES_TO)
    - Penalty -> source_article (APPLIES_TO)
    - Penalty -> applies_to_articles (ENFORCES)
    """
    rels: list[dict] = []

    # Actor -> article
    for actor in all_entities.get("actors", []):
        art = actor.get("definition_article")
        if art:
            rels.append(_rel(actor["id"], art, "APPLIES_TO"))

    # DataType -> regulated_by articles
    for dt in all_entities.get("data_types", []):
        for art_id in dt.get("regulated_by", []):
            rels.append(_rel(dt["id"], art_id, "APPLIES_TO"))
        # DataType -> parent
        parent = dt.get("parent_type")
        if parent:
            rels.append(_rel(dt["id"], parent, "PART_OF"))
        # Non-regulated data types reference GDPR scope provisions
        if not dt.get("regulated_by") and not parent:
            # Anonymised/Aggregated data: reference GDPR Recital 26 (scope exclusion)
            rels.append(_rel(dt["id"], "GDPR_REC_26", "REFERENCES"))

    # RiskCategory -> source_article
    for rc in all_entities.get("risk_categories", []):
        art = rc.get("source_article")
        if art:
            rels.append(_rel(rc["id"], art, "APPLIES_TO"))
        # RISK_MINIMAL has no source_article but belongs to AI Act
        if rc["id"] == "RISK_MINIMAL":
            rels.append(_rel(rc["id"], "EU_AI_ACT", "PART_OF"))

    # AISystemType -> risk_category, source_article, annex
    for ast in all_entities.get("ai_system_types", []):
        rc = ast.get("risk_category")
        if rc:
            rels.append(_rel(ast["id"], rc, "PART_OF"))
        art = ast.get("source_article")
        if art:
            rels.append(_rel(ast["id"], art, "APPLIES_TO"))
        annex = ast.get("annex_reference")
        if annex:
            rels.append(_rel(ast["id"], annex, "APPLIES_TO"))

    # Penalty -> source_article, applies_to_articles
    for pen in all_entities.get("penalties", []):
        art = pen.get("source_article")
        if art:
            rels.append(_rel(pen["id"], art, "APPLIES_TO"))
        for target in pen.get("applies_to_articles", []):
            rels.append(_rel(pen["id"], target, "ENFORCES"))

    return rels


def _rel(source_id: str, target_id: str, rel_type: str, **props) -> dict:
    return {
        "source_id": source_id,
        "target_id": target_id,
        "type": rel_type,
        "properties": props,
    }


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
