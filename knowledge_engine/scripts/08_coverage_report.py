"""Coverage report: identify gaps in the knowledge graph.

Checks:
  1. Articles with 0 obligations (extraction gaps)
  2. Articles below average relationship count
  3. Entity type distribution
  4. Cross-regulation mapping coverage
  5. Orphan node check
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"
REL_DIR = PARSED_DATA_DIR / "relationships"
ENTITIES_DIR = PARSED_DATA_DIR / "entities"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("=" * 60)
    print("KNOWLEDGE GRAPH COVERAGE REPORT")
    print("=" * 60)

    # ── Load all data ─────────────────────────────────────────────────
    all_nodes: dict[str, dict] = {}
    node_types: dict[str, str] = {}
    all_edges: list[dict] = []
    adj: dict[str, set[str]] = defaultdict(set)

    # Regulations
    for reg in [
        {"id": "GDPR", "type": "Regulation"},
        {"id": "EU_AI_ACT", "type": "Regulation"},
    ]:
        all_nodes[reg["id"]] = reg
        node_types[reg["id"]] = "Regulation"

    # All entity files
    entity_sources = [
        ("legal/gdpr_articles.json", "Article"),
        ("legal/eu_ai_act_articles.json", "Article"),
        ("legal/gdpr_recitals.json", "Recital"),
        ("legal/ai_act_recitals.json", "Recital"),
        ("legal/ai_act_annexes.json", "Annex"),
        ("interpretive/case_law.json", "CaseLaw"),
        ("interpretive/edpb_guidelines.json", "Guideline"),
        ("interpretive/enforcement_actions.json", "EnforcementAction"),
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

    for fname, etype in entity_sources:
        for item in load_json(PARSED_DATA_DIR / fname):
            all_nodes[item["id"]] = item
            node_types[item["id"]] = item.get("type", etype)

    # All relationships
    for rel_file in sorted(REL_DIR.glob("*.json")):
        for rel in load_json(rel_file):
            all_edges.append(rel)
            adj[rel["source_id"]].add(rel["target_id"])
            adj[rel["target_id"]].add(rel["source_id"])

    # ── 1. Entity type distribution ───────────────────────────────────
    print("\n[1/5] Entity Type Distribution")
    print("-" * 40)
    type_counts: dict[str, int] = defaultdict(int)
    for ntype in node_types.values():
        type_counts[ntype] += 1
    for t in sorted(type_counts.keys()):
        print(f"  {t:25s}: {type_counts[t]:5d}")
    print(f"  {'TOTAL':25s}: {len(all_nodes):5d}")

    # ── 2. Articles with 0 obligations ────────────────────────────────
    print("\n[2/5] Articles With Zero Obligations")
    print("-" * 40)

    # Build article -> obligation count map
    article_ids = [nid for nid, nt in node_types.items() if nt == "Article"]
    obl_links = {e["target_id"] for e in all_edges
                 if e["type"] in ("REQUIRES", "PROHIBITS", "PERMITS")}

    zero_obl_articles = [a for a in article_ids if a not in obl_links]
    print(f"  Articles with obligations: {len(article_ids) - len(zero_obl_articles)}/{len(article_ids)}")
    print(f"  Articles with 0 obligations: {len(zero_obl_articles)}")
    if zero_obl_articles:
        # Group by regulation
        gdpr_zero = [a for a in zero_obl_articles if a.startswith("GDPR")]
        ai_zero = [a for a in zero_obl_articles if a.startswith("AIACT")]
        print(f"    GDPR: {len(gdpr_zero)} articles")
        for a in gdpr_zero[:10]:
            name = all_nodes.get(a, {}).get("name", a)
            print(f"      {a}: {name}")
        if len(gdpr_zero) > 10:
            print(f"      ... +{len(gdpr_zero) - 10} more")
        print(f"    AI Act: {len(ai_zero)} articles")
        for a in ai_zero[:10]:
            name = all_nodes.get(a, {}).get("name", a)
            print(f"      {a}: {name}")
        if len(ai_zero) > 10:
            print(f"      ... +{len(ai_zero) - 10} more")

    # ── 3. Articles below average relationship count ──────────────────
    print("\n[3/5] Articles Below Average Relationship Count")
    print("-" * 40)

    article_rel_counts: dict[str, int] = {}
    for aid in article_ids:
        count = sum(1 for e in all_edges if e["source_id"] == aid or e["target_id"] == aid)
        article_rel_counts[aid] = count

    if article_rel_counts:
        avg_rels = sum(article_rel_counts.values()) / len(article_rel_counts)
        below_avg = {a: c for a, c in article_rel_counts.items() if c < avg_rels}
        zero_rels = {a: c for a, c in article_rel_counts.items() if c == 0}

        print(f"  Average relationships per article: {avg_rels:.1f}")
        print(f"  Articles below average: {len(below_avg)}/{len(article_ids)}")
        print(f"  Articles with 0 relationships: {len(zero_rels)}")

        # Show lowest
        sorted_articles = sorted(article_rel_counts.items(), key=lambda x: x[1])
        print("\n  Bottom 10 articles by relationship count:")
        for aid, count in sorted_articles[:10]:
            name = all_nodes.get(aid, {}).get("name", aid)
            print(f"    {aid:20s} ({count:2d} rels): {name}")

    # ── 4. Cross-regulation mapping coverage ──────────────────────────
    print("\n[4/5] Cross-Regulation Mapping Coverage")
    print("-" * 40)

    complements = [e for e in all_edges if e["type"] == "COMPLEMENTS"]
    concept_refs = [e for e in all_edges
                    if e["type"] == "REFERENCES"
                    and e.get("properties", {}).get("link_type") in ("concept_cross_ref", "cross_regulation_right")]
    print(f"  COMPLEMENTS edges: {len(complements)}")
    print(f"  Cross-regulation concept/right REFERENCES: {len(concept_refs)}")

    # Interaction type breakdown
    if complements:
        interaction_types: dict[str, int] = defaultdict(int)
        for c in complements:
            it = c.get("properties", {}).get("interaction_type", "UNKNOWN")
            interaction_types[it] += 1
        for it, count in sorted(interaction_types.items()):
            print(f"    {it}: {count}")

    # Count articles with cross-reg links
    cross_reg_articles = set()
    for c in complements:
        cross_reg_articles.add(c["source_id"])
        cross_reg_articles.add(c["target_id"])
    gdpr_cross = [a for a in cross_reg_articles if a.startswith("GDPR")]
    ai_cross = [a for a in cross_reg_articles if a.startswith("AIACT")]
    print(f"  GDPR articles with cross-reg links: {len(gdpr_cross)}")
    print(f"  AI Act articles with cross-reg links: {len(ai_cross)}")

    # ── 5. Orphan node check ──────────────────────────────────────────
    print("\n[5/5] Orphan Node Check")
    print("-" * 40)

    orphans = [nid for nid in all_nodes if nid not in adj]
    print(f"  Orphan nodes: {len(orphans)}")
    if orphans:
        orphan_types: dict[str, list[str]] = defaultdict(list)
        for o in orphans:
            orphan_types[node_types.get(o, "?")].append(o)
        for ot, ids in sorted(orphan_types.items()):
            print(f"    {ot}: {len(ids)}")
            for oid in ids[:3]:
                print(f"      {oid}")

    # ── Summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("COVERAGE SUMMARY")
    print("=" * 60)
    print(f"  Total nodes:          {len(all_nodes)}")
    print(f"  Total relationships:  {len(all_edges)}")
    print(f"  Entity types:         {len(type_counts)}")
    print(f"  Orphan nodes:         {len(orphans)}")
    print(f"  Zero-obligation arts: {len(zero_obl_articles)}/{len(article_ids)}")
    print(f"  Cross-reg edges:      {len(complements) + len(concept_refs)}")

    # Coverage score
    coverage_checks = [
        len(orphans) == 0,
        len(zero_obl_articles) < len(article_ids) * 0.5,
        len(complements) >= 50,
        type_counts.get("Concept", 0) >= 40,
        type_counts.get("Right", 0) >= 15,
    ]
    score = sum(coverage_checks) / len(coverage_checks)
    print(f"\n  Coverage score: {score:.0%} ({sum(coverage_checks)}/{len(coverage_checks)} checks pass)")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
