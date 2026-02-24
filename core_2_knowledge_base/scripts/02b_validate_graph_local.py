"""Phase 2b: Validate graph structure locally (no Neo4j required).

Builds an in-memory graph from parsed JSON and validates:
- Node counts per type
- Relationship integrity (no dangling references)
- No orphan nodes
- Connectivity from Regulation roots
- Cross-reference density
- Average relationships per article
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_DIR = PARSED_DATA_DIR / "relationships"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def build_in_memory_graph():
    """Build adjacency lists and node registry from JSON files."""
    nodes: dict[str, dict] = {}  # id -> node data
    node_types: dict[str, str] = {}  # id -> type
    edges: list[dict] = []
    adj: dict[str, set[str]] = defaultdict(set)  # id -> set of neighbor ids

    # ── Load nodes ────────────────────────────────────────────────────
    # Regulations
    for reg in [
        {"id": "GDPR", "type": "Regulation", "name": "GDPR"},
        {"id": "EU_AI_ACT", "type": "Regulation", "name": "EU AI Act"},
    ]:
        nodes[reg["id"]] = reg
        node_types[reg["id"]] = reg["type"]

    # Chapters
    for fname, reg_id, prefix in [
        ("legal/gdpr_chapters.json", "GDPR", "GDPR"),
        ("legal/ai_act_chapters.json", "EU_AI_ACT", "AIACT"),
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

    # ── Load relationships ────────────────────────────────────────────
    for rel_file in sorted(REL_DIR.glob("*.json")):
        for rel in load_json(rel_file):
            edges.append(rel)
            adj[rel["source_id"]].add(rel["target_id"])
            adj[rel["target_id"]].add(rel["source_id"])  # undirected for connectivity

    return nodes, node_types, edges, adj


def validate():
    """Run all Phase 2 validation checks."""
    print("=" * 60)
    print("PHASE 2b: Local Graph Validation (no Neo4j)")
    print("=" * 60)

    # Check relationship files exist
    if not REL_DIR.exists():
        print("\nERROR: No relationship files found. Run 02a first.")
        return 1

    nodes, node_types, edges, adj = build_in_memory_graph()

    # ── Node counts ───────────────────────────────────────────────────
    print("\n[1/6] Node counts per type:")
    type_counts: dict[str, int] = defaultdict(int)
    for ntype in node_types.values():
        type_counts[ntype] += 1

    for t in sorted(type_counts.keys()):
        print(f"    {t:25s}: {type_counts[t]:5d}")
    print(f"    {'TOTAL':25s}: {len(nodes):5d}")

    # ── Relationship counts ───────────────────────────────────────────
    print("\n[2/6] Relationship counts per type:")
    rel_type_counts: dict[str, int] = defaultdict(int)
    for edge in edges:
        rel_type_counts[edge["type"]] += 1

    for t in sorted(rel_type_counts.keys()):
        print(f"    {t:25s}: {rel_type_counts[t]:5d}")
    print(f"    {'TOTAL':25s}: {len(edges):5d}")

    # ── Dangling references ───────────────────────────────────────────
    print("\n[3/6] Checking for dangling references...")
    dangling = 0
    dangling_details: list[str] = []
    for edge in edges:
        if edge["source_id"] not in nodes:
            dangling += 1
            if len(dangling_details) < 5:
                dangling_details.append(f"  Source missing: {edge['source_id']} -[{edge['type']}]-> {edge['target_id']}")
        if edge["target_id"] not in nodes:
            dangling += 1
            if len(dangling_details) < 5:
                dangling_details.append(f"  Target missing: {edge['source_id']} -[{edge['type']}]-> {edge['target_id']}")

    if dangling:
        print(f"  WARNING: {dangling} dangling references found")
        for d in dangling_details:
            print(d)
    else:
        print(f"  No dangling references (all {len(edges)} edges valid)")

    # ── Orphan nodes ──────────────────────────────────────────────────
    print("\n[4/6] Checking for orphan nodes...")
    orphans = [nid for nid in nodes if nid not in adj]
    if orphans:
        print(f"  WARNING: {len(orphans)} orphan nodes (no relationships)")
        for o in orphans[:10]:
            print(f"    {o} ({node_types.get(o, '?')})")
        if len(orphans) > 10:
            print(f"    ... and {len(orphans) - 10} more")
    else:
        print(f"  No orphan nodes -- all {len(nodes)} nodes connected")

    # ── Connectivity from roots ───────────────────────────────────────
    print("\n[5/6] Checking connectivity from Regulation roots...")
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
    print(f"  Reachable from roots: {len(reachable)}/{len(nodes)}")
    if unreachable:
        print(f"  Unreachable: {len(unreachable)} nodes")
        for u in list(unreachable)[:10]:
            print(f"    {u} ({node_types.get(u, '?')})")
        if len(unreachable) > 10:
            print(f"    ... and {len(unreachable) - 10} more")

    # ── Article relationship density ──────────────────────────────────
    print("\n[6/6] Article relationship density...")
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
        # Target: >= 4 avg
        if avg >= 4:
            print(f"  Target (avg >= 4): PASS")
        else:
            print(f"  Target (avg >= 4): BELOW TARGET (Phase 3 will add more)")

    # ── Exit gate ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PHASE 2 EXIT GATE")
    print("=" * 60)

    checks = {
        "Regulation nodes == 2": type_counts["Regulation"] == 2,
        "Chapter nodes == 24": type_counts["Chapter"] == 24,
        "Article nodes == 212": type_counts["Article"] == 212,
        "Recital nodes == 353": type_counts["Recital"] == 353,
        "Annex nodes == 13": type_counts["Annex"] == 13,
        "CaseLaw nodes == 20": type_counts["CaseLaw"] == 20,
        "Guideline nodes == 21": type_counts["Guideline"] == 21,
        "EnforcementAction == 15": type_counts["EnforcementAction"] == 15,
        "Total nodes >= 660": len(nodes) >= 660,
        "Total relationships >= 1500": len(edges) >= 1500,
        "Dangling references == 0": dangling == 0,
        "Orphan nodes <= 5": len(orphans) <= 5,
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
        print("Graph is structurally valid. Load into Neo4j when ready.")
    else:
        print("SOME CHECKS FAILED -- investigate before proceeding.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(validate())
