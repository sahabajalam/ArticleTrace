"""Phase 2: Load structural knowledge graph into Neo4j.

Loads all parsed entities and structural relationships.
Runs Phase 2a (relationship extraction) first if needed.

Exit gate:
- Node counts match Phase 1 output exactly
- All structural relationships loaded
- No orphan nodes (every node reachable from a Regulation root)
- Graph connectivity verified

Usage:
    python scripts/02_load_structural_kg.py
    python scripts/02_load_structural_kg.py --clear  # Wipe and reload
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.stores.graph_store import GraphStore
from src.extractors.structural_extractor import StructuralExtractor

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_DIR = PARSED_DATA_DIR / "relationships"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def create_regulation_nodes() -> list[dict]:
    """Create the 2 root regulation nodes."""
    return [
        {
            "id": "GDPR",
            "type": "Regulation",
            "name": "General Data Protection Regulation",
            "description": "Regulation (EU) 2016/679",
            "regulation_id": "GDPR",
            "effective_date": "2018-05-25",
        },
        {
            "id": "EU_AI_ACT",
            "type": "Regulation",
            "name": "EU AI Act",
            "description": "Regulation (EU) 2024/1689",
            "regulation_id": "EU_AI_ACT",
            "effective_date": "2024-08-01",
        },
    ]


def create_chapter_nodes(chapters_data: list[dict], regulation_id: str) -> list[dict]:
    """Create Chapter nodes from parsed chapter data."""
    prefix = "GDPR" if regulation_id == "GDPR" else "AIACT"
    nodes = []
    for ch in chapters_data:
        if ch.get("number") is None:
            continue
        nodes.append({
            "id": f"{prefix}_CH_{ch['number']}",
            "type": "Chapter",
            "name": f"Chapter {ch['number']}",
            "description": ch.get("name", ""),
            "regulation_id": regulation_id,
            "chapter_number": ch["number"],
        })
    return nodes


def main():
    clear_first = "--clear" in sys.argv

    print("=" * 60)
    print("PHASE 2: Load Structural Knowledge Graph into Neo4j")
    print("=" * 60)

    # ── Step 0: Extract relationships if not already done ─────────────
    if not REL_DIR.exists() or not (REL_DIR / "containment.json").exists():
        print("\n[0/6] Extracting structural relationships...")
        extractor = StructuralExtractor(PARSED_DATA_DIR)
        results = extractor.extract_all()
        REL_DIR.mkdir(parents=True, exist_ok=True)
        for category, rels in results.items():
            with open(REL_DIR / f"{category}.json", "w", encoding="utf-8") as f:
                json.dump(rels, f, indent=2, ensure_ascii=False, default=str)
            print(f"  {category}: {len(rels)} relationships")
    else:
        print("\n[0/6] Structural relationships already extracted (skipping)")

    # ── Step 1: Connect to Neo4j ──────────────────────────────────────
    print("\n[1/6] Connecting to Neo4j...")
    try:
        # Load settings from .env or environment
        from src.config import settings
        store = GraphStore(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
        )
    except Exception as e:
        print(f"  ERROR: Cannot connect to Neo4j: {e}")
        print("  Make sure Neo4j is running (docker-compose up -d)")
        print("\n  Alternatively, the structural data is ready in:")
        print(f"    Entities: {PARSED_DATA_DIR}/legal/, interpretive/")
        print(f"    Relationships: {REL_DIR}/")
        print("  You can load these later when Neo4j is available.")
        return 1

    if clear_first:
        print("  WARNING: Clearing all existing data...")
        store.clear_all()

    # ── Step 2: Create indexes ────────────────────────────────────────
    print("\n[2/6] Creating indexes...")
    store.create_indexes()

    # ── Step 3: Load all entity nodes ─────────────────────────────────
    print("\n[3/6] Loading entity nodes...")

    all_nodes: list[dict] = []

    # Regulation nodes (2)
    reg_nodes = create_regulation_nodes()
    all_nodes.extend(reg_nodes)
    print(f"  Regulation nodes: {len(reg_nodes)}")

    # Chapter nodes (24)
    gdpr_chapters = load_json(PARSED_DATA_DIR / "legal" / "gdpr_chapters.json")
    ai_chapters = load_json(PARSED_DATA_DIR / "legal" / "ai_act_chapters.json")
    ch_nodes = create_chapter_nodes(gdpr_chapters, "GDPR")
    ch_nodes.extend(create_chapter_nodes(ai_chapters, "EU_AI_ACT"))
    all_nodes.extend(ch_nodes)
    print(f"  Chapter nodes: {len(ch_nodes)}")

    # Article nodes (212)
    gdpr_articles = load_json(PARSED_DATA_DIR / "legal" / "gdpr_articles.json")
    ai_articles = load_json(PARSED_DATA_DIR / "legal" / "eu_ai_act_articles.json")
    all_nodes.extend(gdpr_articles)
    all_nodes.extend(ai_articles)
    print(f"  Article nodes: {len(gdpr_articles) + len(ai_articles)} ({len(gdpr_articles)} GDPR + {len(ai_articles)} AI Act)")

    # Recital nodes (353)
    gdpr_recitals = load_json(PARSED_DATA_DIR / "legal" / "gdpr_recitals.json")
    ai_recitals = load_json(PARSED_DATA_DIR / "legal" / "ai_act_recitals.json")
    all_nodes.extend(gdpr_recitals)
    all_nodes.extend(ai_recitals)
    print(f"  Recital nodes: {len(gdpr_recitals) + len(ai_recitals)} ({len(gdpr_recitals)} GDPR + {len(ai_recitals)} AI Act)")

    # Annex nodes (13)
    annexes = load_json(PARSED_DATA_DIR / "legal" / "ai_act_annexes.json")
    all_nodes.extend(annexes)
    print(f"  Annex nodes: {len(annexes)}")

    # CaseLaw nodes (20)
    cases = load_json(PARSED_DATA_DIR / "interpretive" / "case_law.json")
    all_nodes.extend(cases)
    print(f"  CaseLaw nodes: {len(cases)}")

    # Guideline nodes (21)
    guidelines = load_json(PARSED_DATA_DIR / "interpretive" / "edpb_guidelines.json")
    all_nodes.extend(guidelines)
    print(f"  Guideline nodes: {len(guidelines)}")

    # Enforcement nodes (15)
    enforcement = load_json(PARSED_DATA_DIR / "interpretive" / "enforcement_actions.json")
    all_nodes.extend(enforcement)
    print(f"  Enforcement nodes: {len(enforcement)}")

    print(f"\n  Total nodes to load: {len(all_nodes)}")
    loaded = store.create_nodes_batch(all_nodes, batch_size=200)
    print(f"  Loaded: {loaded} nodes")

    # ── Step 4: Load all relationships ────────────────────────────────
    print("\n[4/6] Loading relationships...")

    all_rels: list[dict] = []
    for rel_file in sorted(REL_DIR.glob("*.json")):
        rels = load_json(rel_file)
        all_rels.extend(rels)
        print(f"  {rel_file.stem}: {len(rels)} relationships")

    print(f"\n  Total relationships to load: {len(all_rels)}")
    created, skipped = store.create_relationships_batch(all_rels, batch_size=200)
    print(f"  Created: {created}, Skipped: {skipped}")

    # ── Step 5: Validate ──────────────────────────────────────────────
    print("\n[5/6] Validating...")

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

    print(f"\n  Orphan nodes (no relationships): {orphans}")

    # ── Step 6: Exit gate checks ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("PHASE 2 EXIT GATE")
    print("=" * 60)

    checks = {
        "Regulation nodes == 2": node_counts.get("Regulation", 0) == 2,
        "Chapter nodes == 24": node_counts.get("Chapter", 0) == 24,
        "Article nodes == 212": node_counts.get("Article", 0) == 212,
        "Recital nodes == 353": node_counts.get("Recital", 0) == 353,
        "Annex nodes == 13": node_counts.get("Annex", 0) == 13,
        "CaseLaw nodes == 20": node_counts.get("CaseLaw", 0) == 20,
        "Guideline nodes == 21": node_counts.get("Guideline", 0) == 21,
        "EnforcementAction nodes == 15": node_counts.get("EnforcementAction", 0) == 15,
        "Total nodes >= 660": total_nodes >= 660,
        "Total relationships >= 1500": total_rels >= 1500,
        "Orphan nodes == 0": orphans == 0,
    }

    all_pass = True
    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {check_name}")

    print("=" * 60)
    if all_pass:
        print("ALL CHECKS PASS -- Phase 2 exit gate satisfied.")
    else:
        print("SOME CHECKS FAILED -- investigate before proceeding to Phase 3.")

    store.close()
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
