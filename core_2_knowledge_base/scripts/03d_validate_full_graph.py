"""Phase 3 Validation: Full graph validation with all entities and relationships.

Extends Phase 2b validator to include Phase 3 semantic entities:
  - Definitions, Actors, DataTypes, RiskCategories, AISystemTypes, Penalties
  - Obligations, Exemptions
  - COMPLEMENTS cross-regulation edges
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_DIR = PARSED_DATA_DIR / "relationships"
ENTITIES_DIR = PARSED_DATA_DIR / "entities"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def build_full_graph():
    """Build in-memory graph with all Phase 1-3 data."""
    nodes: dict[str, dict] = {}
    node_types: dict[str, str] = {}
    edges: list[dict] = []
    adj: dict[str, set[str]] = defaultdict(set)

    # ── Phase 1+2 nodes ─────────────────────────────────────────────
    # Regulations
    for reg in [
        {"id": "GDPR", "type": "Regulation", "name": "GDPR"},
        {"id": "EU_AI_ACT", "type": "Regulation", "name": "EU AI Act"},
    ]:
        nodes[reg["id"]] = reg
        node_types[reg["id"]] = reg["type"]

    # Chapters
    for fname, prefix in [
        ("legal/gdpr_chapters.json", "GDPR"),
        ("legal/ai_act_chapters.json", "AIACT"),
    ]:
        for ch in load_json(PARSED_DATA_DIR / fname):
            if ch.get("number") is None:
                continue
            ch_id = f"{prefix}_CH_{ch['number']}"
            nodes[ch_id] = ch
            node_types[ch_id] = "Chapter"

    # Articles, Recitals, Annexes, CaseLaw, Guidelines, Enforcement
    file_type_map = [
        ("legal/gdpr_articles.json", "Article"),
        ("legal/eu_ai_act_articles.json", "Article"),
        ("legal/gdpr_recitals.json", "Recital"),
        ("legal/ai_act_recitals.json", "Recital"),
        ("legal/ai_act_annexes.json", "Annex"),
        ("interpretive/case_law.json", "CaseLaw"),
        ("interpretive/edpb_guidelines.json", "Guideline"),
        ("interpretive/enforcement_actions.json", "EnforcementAction"),
    ]

    for fname, etype in file_type_map:
        for item in load_json(PARSED_DATA_DIR / fname):
            nodes[item["id"]] = item
            node_types[item["id"]] = etype

    # ── Phase 3 entities ─────────────────────────────────────────────
    entity_files = [
        ("entities/definitions.json", "Definition"),
        ("entities/actors.json", "Actor"),
        ("entities/data_types.json", "DataType"),
        ("entities/risk_categories.json", "RiskCategory"),
        ("entities/ai_system_types.json", "AISystemType"),
        ("entities/penalties.json", "Penalty"),
        ("entities/obligations.json", "Obligation"),
        ("entities/exemptions.json", "Exemption"),
        ("entities/concepts.json", "Concept"),
        ("entities/rights.json", "Right"),
    ]

    for fname, etype in entity_files:
        for item in load_json(PARSED_DATA_DIR / fname):
            nodes[item["id"]] = item
            node_types[item["id"]] = item.get("type", etype)

    # ── All relationships ────────────────────────────────────────────
    for rel_file in sorted(REL_DIR.glob("*.json")):
        for rel in load_json(rel_file):
            edges.append(rel)
            adj[rel["source_id"]].add(rel["target_id"])
            adj[rel["target_id"]].add(rel["source_id"])

    return nodes, node_types, edges, adj


def validate() -> int:
    print("=" * 60)
    print("PHASE 3 VALIDATION: Full Graph (All Entities + Relationships)")
    print("=" * 60)

    nodes, node_types, edges, adj = build_full_graph()

    # ── Node counts ───────────────────────────────────────────────────
    print("\n[1/7] Node counts per type:")
    type_counts: dict[str, int] = defaultdict(int)
    for ntype in node_types.values():
        type_counts[ntype] += 1

    for t in sorted(type_counts.keys()):
        print(f"    {t:25s}: {type_counts[t]:5d}")
    print(f"    {'TOTAL':25s}: {len(nodes):5d}")

    # ── Relationship counts ───────────────────────────────────────────
    print("\n[2/7] Relationship counts per type:")
    rel_type_counts: dict[str, int] = defaultdict(int)
    for edge in edges:
        rel_type_counts[edge["type"]] += 1

    for t in sorted(rel_type_counts.keys()):
        print(f"    {t:25s}: {rel_type_counts[t]:5d}")
    print(f"    {'TOTAL':25s}: {len(edges):5d}")

    # ── Dangling references ───────────────────────────────────────────
    print("\n[3/7] Checking for dangling references...")
    dangling = 0
    dangling_details: list[str] = []
    for edge in edges:
        if edge["source_id"] not in nodes:
            dangling += 1
            if len(dangling_details) < 10:
                dangling_details.append(f"  Source: {edge['source_id']} -[{edge['type']}]-> {edge['target_id']}")
        if edge["target_id"] not in nodes:
            dangling += 1
            if len(dangling_details) < 10:
                dangling_details.append(f"  Target: {edge['source_id']} -[{edge['type']}]-> {edge['target_id']}")

    if dangling:
        print(f"  WARNING: {dangling} dangling references found")
        for d in dangling_details:
            print(d)
    else:
        print(f"  No dangling references (all {len(edges)} edges valid)")

    # ── Orphan nodes ──────────────────────────────────────────────────
    print("\n[4/7] Checking for orphan nodes...")
    orphans = [nid for nid in nodes if nid not in adj]
    if orphans:
        print(f"  WARNING: {len(orphans)} orphan nodes (no relationships)")
        # Show by type
        orphan_by_type: dict[str, list[str]] = defaultdict(list)
        for o in orphans:
            orphan_by_type[node_types.get(o, "?")].append(o)
        for ot, olist in sorted(orphan_by_type.items()):
            print(f"    {ot}: {len(olist)}")
            for oid in olist[:3]:
                print(f"      {oid}")
            if len(olist) > 3:
                print(f"      ... +{len(olist) - 3} more")
    else:
        print(f"  No orphan nodes -- all {len(nodes)} nodes connected")

    # ── Connectivity from roots ───────────────────────────────────────
    print("\n[5/7] Checking connectivity from Regulation roots...")
    reachable = set()
    queue = ["GDPR", "EU_AI_ACT"]
    while queue:
        current = queue.pop()
        if current in reachable:
            continue
        reachable.add(current)
        for neighbor in adj.get(current, set()):
            if neighbor not in reachable:
                queue.append(neighbor)

    unreachable = set(nodes.keys()) - reachable
    pct = 100 * len(reachable) / max(len(nodes), 1)
    print(f"  Reachable from roots: {len(reachable)}/{len(nodes)} ({pct:.1f}%)")
    if unreachable:
        print(f"  Unreachable: {len(unreachable)} nodes")
        unreachable_by_type: dict[str, int] = defaultdict(int)
        for u in unreachable:
            unreachable_by_type[node_types.get(u, "?")] += 1
        for ut, uc in sorted(unreachable_by_type.items()):
            print(f"    {ut}: {uc}")

    # ── Cross-regulation connectivity ─────────────────────────────────
    print("\n[6/7] Cross-regulation COMPLEMENTS edges...")
    complements = [e for e in edges if e["type"] == "COMPLEMENTS"]
    print(f"  COMPLEMENTS edges: {len(complements)}")
    if complements:
        interaction_types: dict[str, int] = defaultdict(int)
        for c in complements:
            it = c.get("properties", {}).get("interaction_type", "UNKNOWN")
            interaction_types[it] += 1
        for it, count in sorted(interaction_types.items()):
            print(f"    {it}: {count}")

    # ── Article relationship density ──────────────────────────────────
    print("\n[7/7] Article relationship density (with Phase 3)...")
    article_ids = [nid for nid, ntype in node_types.items() if ntype == "Article"]
    article_rel_counts = []
    for aid in article_ids:
        count = sum(1 for e in edges if e["source_id"] == aid or e["target_id"] == aid)
        article_rel_counts.append(count)

    if article_rel_counts:
        avg = sum(article_rel_counts) / len(article_rel_counts)
        min_c = min(article_rel_counts)
        max_c = max(article_rel_counts)
        zero_count = article_rel_counts.count(0)
        print(f"  Average relationships per article: {avg:.1f}")
        print(f"  Min: {min_c}, Max: {max_c}")
        print(f"  Articles with 0 relationships: {zero_count}")

    # ── Exit gate ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PHASE 3 EXIT GATE")
    print("=" * 60)

    checks = {
        # Phase 2 entity counts
        "Regulation nodes == 2": type_counts["Regulation"] == 2,
        "Article nodes == 212": type_counts["Article"] == 212,
        "Recital nodes == 353": type_counts["Recital"] == 353,
        # Phase 3 entity counts
        "Definition nodes >= 80": type_counts.get("Definition", 0) >= 80,
        "Actor nodes >= 15": type_counts.get("Actor", 0) >= 15,
        "DataType nodes >= 15": type_counts.get("DataType", 0) >= 15,
        "Obligation nodes >= 500": type_counts.get("Obligation", 0) >= 500,
        "Exemption nodes >= 30": type_counts.get("Exemption", 0) >= 30,
        "Penalty nodes >= 6": type_counts.get("Penalty", 0) >= 6,
        "Concept nodes >= 40": type_counts.get("Concept", 0) >= 40,
        "Right nodes >= 15": type_counts.get("Right", 0) >= 15,
        # Graph health
        "Total nodes >= 1500": len(nodes) >= 1500,
        "Total relationships >= 3000": len(edges) >= 3000,
        "Dangling references == 0": dangling == 0,
        "COMPLEMENTS edges >= 50": len(complements) >= 50,
        "Avg rels per article >= 4": avg >= 4 if article_rel_counts else False,
    }

    all_pass = True
    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {check_name}")

    print("=" * 60)
    if all_pass:
        print("ALL CHECKS PASS -- Phase 3 exit gate satisfied.")
        print("Knowledge graph ready for Neo4j loading + vector store.")
    else:
        print("SOME CHECKS FAILED -- see details above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(validate())
