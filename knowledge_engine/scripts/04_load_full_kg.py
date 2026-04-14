"""Phase 4: Load complete knowledge graph into Neo4j.

Loads ALL entities (Phase 1-3) and ALL relationships into Neo4j.
Total: ~2235 nodes, ~4074 relationships.

Usage:
    python scripts/04_load_full_kg.py            # Load (skip existing)
    python scripts/04_load_full_kg.py --clear     # Wipe and reload
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_DIR = PARSED_DATA_DIR / "relationships"
ENTITIES_DIR = PARSED_DATA_DIR / "entities"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    clear_first = "--clear" in sys.argv

    print("=" * 60)
    print("PHASE 4: Load Complete Knowledge Graph into Neo4j")
    print("=" * 60)

    # ── Connect to Neo4j ──────────────────────────────────────────
    print("\n[1/5] Connecting to Neo4j...")
    try:
        from src.config import settings
        from src.stores.graph_store import GraphStore

        store = GraphStore(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
        )
        print("  Connected.")
    except Exception as e:
        print(f"  ERROR: Cannot connect to Neo4j: {e}")
        print("  Make sure Neo4j is running.")
        return 1

    if clear_first:
        print("  Clearing existing data...")
        store.clear_all()

    # ── Create indexes ────────────────────────────────────────────
    print("\n[2/5] Creating indexes...")
    store.create_indexes()

    # ── Load ALL nodes ────────────────────────────────────────────
    print("\n[3/5] Loading all entity nodes...")

    all_nodes: list[dict] = []

    # Regulation root nodes
    all_nodes.extend([
        {"id": "GDPR", "type": "Regulation", "name": "General Data Protection Regulation",
         "description": "Regulation (EU) 2016/679", "regulation_id": "GDPR", "effective_date": "2018-05-25"},
        {"id": "EU_AI_ACT", "type": "Regulation", "name": "EU AI Act",
         "description": "Regulation (EU) 2024/1689", "regulation_id": "EU_AI_ACT", "effective_date": "2024-08-01"},
    ])

    # Chapter nodes
    for fname, reg_id, prefix in [
        ("legal/gdpr_chapters.json", "GDPR", "GDPR"),
        ("legal/ai_act_chapters.json", "EU_AI_ACT", "AIACT"),
    ]:
        for ch in load_json(PARSED_DATA_DIR / fname):
            if ch.get("number") is None:
                continue
            all_nodes.append({
                "id": f"{prefix}_CH_{ch['number']}", "type": "Chapter",
                "name": f"Chapter {ch['number']}", "description": ch.get("name", ""),
                "regulation_id": reg_id, "chapter_number": ch["number"],
            })

    # Phase 1 parsed entities
    phase1_files = [
        "legal/gdpr_articles.json", "legal/eu_ai_act_articles.json",
        "legal/gdpr_recitals.json", "legal/ai_act_recitals.json",
        "legal/ai_act_annexes.json",
        "interpretive/case_law.json", "interpretive/edpb_guidelines.json",
        "interpretive/enforcement_actions.json",
    ]
    for fname in phase1_files:
        entities = load_json(PARSED_DATA_DIR / fname)
        all_nodes.extend(entities)
        print(f"  {fname}: {len(entities)} nodes")

    # Phase 3 semantic entities
    phase3_files = [
        "entities/definitions.json", "entities/actors.json",
        "entities/data_types.json", "entities/risk_categories.json",
        "entities/ai_system_types.json", "entities/penalties.json",
        "entities/obligations.json", "entities/exemptions.json",
        "entities/concepts.json", "entities/rights.json",
    ]
    for fname in phase3_files:
        entities = load_json(PARSED_DATA_DIR / fname)
        all_nodes.extend(entities)
        print(f"  {fname}: {len(entities)} nodes")

    print(f"\n  Total nodes to load: {len(all_nodes)}")
    loaded = store.create_nodes_batch(all_nodes, batch_size=300)
    print(f"  Loaded: {loaded} nodes")

    # ── Load ALL relationships ────────────────────────────────────
    print("\n[4/5] Loading all relationships...")

    all_rels: list[dict] = []
    for rel_file in sorted(REL_DIR.glob("*.json")):
        rels = load_json(rel_file)
        all_rels.extend(rels)
        print(f"  {rel_file.stem}: {len(rels)} relationships")

    print(f"\n  Total relationships to load: {len(all_rels)}")
    created, skipped = store.create_relationships_batch(all_rels, batch_size=300)
    print(f"  Created: {created}, Skipped: {skipped}")

    # ── Validate ──────────────────────────────────────────────────
    print("\n[5/5] Validating Neo4j graph...")

    node_counts = store.count_nodes()
    rel_counts = store.count_relationships()
    orphans = store.count_orphan_nodes()

    print("\n  Node counts per type:")
    total_nodes = 0
    for label, count in sorted(node_counts.items()):
        if count > 0:
            print(f"    {label:25s}: {count:5d}")
            total_nodes += count
    print(f"    {'TOTAL':25s}: {total_nodes:5d}")

    print("\n  Relationship counts per type:")
    total_rels = 0
    for rel_type, count in sorted(rel_counts.items()):
        print(f"    {rel_type:25s}: {count:5d}")
        total_rels += count
    print(f"    {'TOTAL':25s}: {total_rels:5d}")

    print(f"\n  Orphan nodes: {orphans}")

    # Exit gate
    print("\n" + "=" * 60)
    print("NEO4J LOADING EXIT GATE")
    print("=" * 60)

    checks = {
        "Total nodes >= 2000": total_nodes >= 2000,
        "Total relationships >= 3500": total_rels >= 3500,
        "Orphan nodes == 0": orphans == 0,
        "COMPLEMENTS edges >= 50": rel_counts.get("COMPLEMENTS", 0) >= 50,
    }

    all_pass = True
    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {check_name}")

    print("=" * 60)
    if all_pass:
        print("ALL CHECKS PASS -- Knowledge graph loaded successfully.")
        print(f"Neo4j: {total_nodes} nodes, {total_rels} relationships")
    else:
        print("SOME CHECKS FAILED -- check Neo4j connection and data.")

    store.close()
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
