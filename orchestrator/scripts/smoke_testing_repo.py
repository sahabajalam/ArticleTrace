"""Smoke test the full scan against the bundled `testing_repo/` fixture."""

from __future__ import annotations

import asyncio
from collections import Counter
from pathlib import Path

from src.code_analyzer.scan import run_scan


async def main() -> None:
    repo = Path(__file__).resolve().parents[2] / "testing_repo"
    assert repo.exists(), f"missing fixture at {repo}"

    profile = await run_scan(
        scan_id="testing-repo-001",
        local_path=repo,
        enrich_with_kg=False,
    )

    by_rule = Counter(f.rule_id for f in profile.findings)
    print("=" * 60)
    print(f"Total findings : {len(profile.findings)}")
    print(f"Stats          : {profile.stats}")
    print()
    print("Findings by rule:")
    for rule_id in sorted(by_rule):
        print(f"  {rule_id} : {by_rule[rule_id]}")
    print()
    print("Decision surfaces (post-LLM review):")
    for s in profile.decision_surfaces:
        print(f"  {s.endpoint}  ({s.file}:{s.line})")


if __name__ == "__main__":
    asyncio.run(main())
