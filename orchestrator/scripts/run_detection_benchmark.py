"""Detection benchmark (v07 T0) — measures what the scanners actually catch.

Runs the real scan pipeline (deterministic path, no LLM, no network beyond the
pinned clones) over a hand-labelled corpus and scores per-rule detection
against pre-registered ground truth in detection_benchmark/corpus.json.

Why this exists: DL-019, DL-020 and DL-027 were all silent recall collapses —
the scanner shipped confident, clean output while a detection path was dead.
The retrieval side has golden tests in CI; this is the same discipline for the
scanner itself. If a run diverges from an expectation, that is a finding to
investigate, not an expectation to edit.

Exit codes: 0 = every non-xfail expectation met and no xfail unexpectedly
passed; 1 = a miss, a false positive on a control repo, or an xpass.

Usage:
  cd orchestrator
  ./.venv/bin/python scripts/run_detection_benchmark.py [--only NAME] [--out results.json]
  # Windows: ./.venv/Scripts/python.exe scripts/run_detection_benchmark.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.code_analyzer.ingest import ingest_local  # noqa: E402
from src.code_analyzer.scan import _scan_and_profile  # noqa: E402

BENCH_DIR = PROJECT_ROOT / "detection_benchmark"
CACHE_DIR = BENCH_DIR / ".cache"


def checkout_pinned(repo: str, sha: str, name: str) -> Path:
    """Fetch exactly one pinned commit into a cached working tree.

    `git clone --depth 1` cannot target an arbitrary SHA; init + fetch of the
    SHA can (GitHub allows reachable-SHA fetch). Cached per (name, sha) so
    reruns are offline; a cache dir whose HEAD does not match the pin is
    rebuilt rather than trusted.
    """
    dest = CACHE_DIR / f"{name}-{sha[:12]}"
    head_ok = False
    if dest.exists():
        head = subprocess.run(
            ["git", "-C", str(dest), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip()
        head_ok = head == sha
        if not head_ok:
            subprocess.run(["rm", "-rf", str(dest)], check=True, timeout=120)
    if not head_ok:
        dest.mkdir(parents=True)
        for cmd in (
            ["git", "init", "-q"],
            ["git", "remote", "add", "origin", repo],
            ["git", "fetch", "-q", "--depth", "1", "origin", sha],
            ["git", "checkout", "-q", sha],
        ):
            subprocess.run(cmd, cwd=dest, check=True, timeout=600)
    return dest


def scan_tree(root: Path) -> dict:
    """Run ingest + the deterministic scanner pipeline; return a scored view."""
    result = ingest_local(root)
    profile = _scan_and_profile(scan_id=f"bench_{root.name}", result=result, use_llm=False)
    d = profile.model_dump() if hasattr(profile, "model_dump") else profile.dict()
    findings = d.get("findings") or []
    by_rule: dict[str, int] = {}
    for f in findings:
        if f.get("suppressed"):
            continue
        by_rule[f["rule_id"]] = by_rule.get(f["rule_id"], 0) + 1
    components = [
        {"kind": c.get("kind"), "name": c.get("name")}
        for c in (d.get("ai_components") or [])
    ]
    repo_info = d.get("repo") or {}
    return {
        "by_rule": by_rule,
        "components": components,
        "total_findings": sum(by_rule.values()),
        # v07 §5: "found nothing" must be distinguishable from "didn't look".
        "coverage": {
            "total_files": repo_info.get("total_files"),
            "scanned_files": repo_info.get("scanned_files"),
            "languages": repo_info.get("languages"),
        },
    }


def score_entry(entry: dict, observed: dict) -> tuple[bool, list[str]]:
    """True iff every expectation in the entry holds; details name each miss."""
    expect = entry["expect"]
    problems: list[str] = []

    if expect.get("zero"):
        if observed["total_findings"] != 0:
            problems.append(
                f"FALSE POSITIVES on control repo: {observed['by_rule']}"
            )
        return (not problems), problems

    for rule_id, spec in (expect.get("rules") or {}).items():
        got = observed["by_rule"].get(rule_id, 0)
        if got < spec["min"]:
            problems.append(f"{rule_id}: expected >= {spec['min']}, found {got}")

    for comp in expect.get("components") or []:
        hit = any(
            c["kind"] == comp["kind"] and c["name"] == comp["name"]
            for c in observed["components"]
        )
        if not hit:
            problems.append(
                f"component {comp['kind']}/{comp['name']} not detected "
                f"(got: {observed['components']})"
            )
    return (not problems), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Scanner detection benchmark (v07 T0)")
    ap.add_argument("--only", default="", help="run a single corpus entry by name")
    ap.add_argument("--out", default="", help="write full results JSON here")
    args = ap.parse_args()

    corpus = json.loads((BENCH_DIR / "corpus.json").read_text(encoding="utf-8"))
    entries = [
        e for e in corpus["entries"] if not args.only or e["name"] == args.only
    ]
    if not entries:
        print(f"[bench] no corpus entry named {args.only!r}")
        return 2

    rows: list[dict] = []
    failed = False
    for entry in entries:
        name = entry["name"]
        try:
            if entry["kind"] == "git":
                root = checkout_pinned(entry["repo"], entry["sha"], name)
            else:
                root = BENCH_DIR / entry["path"]
                if not root.exists():
                    raise FileNotFoundError(root)
            observed = scan_tree(root)
        except Exception as e:  # a broken entry must fail loudly, not score 0
            print(f"[bench] {name}: ERROR — {type(e).__name__}: {e}")
            rows.append({"name": name, "status": "ERROR", "error": str(e)})
            failed = True
            continue

        ok, problems = score_entry(entry, observed)
        xfail = bool(entry.get("xfail"))

        if xfail and ok:
            status = "XPASS"  # strict: an xfail that passes must be promoted
            failed = True
        elif xfail:
            status = "XFAIL"
        elif ok:
            status = "PASS"
        else:
            status = "FAIL"
            failed = True

        cov = observed["coverage"]
        print(
            f"[bench] {name:18} {status:6} findings={observed['total_findings']:<4} "
            f"rules={observed['by_rule']} "
            f"scanned={cov['scanned_files']}/{cov['total_files']}"
        )
        for p in problems:
            marker = "known gap" if xfail else "PROBLEM"
            print(f"         {marker}: {p}")
        if status == "XPASS":
            print(
                "         XPASS: this known gap now detects — promote the entry "
                "to xfail=false with real expectations (see corpus.json _doc)."
            )
        rows.append(
            {"name": name, "status": status, "observed": observed, "problems": problems}
        )

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"\n[bench] summary: {counts}")
    scored = [r for r in rows if r["status"] in ("PASS", "FAIL")]
    if scored:
        rate = sum(1 for r in scored if r["status"] == "PASS") / len(scored)
        print(f"[bench] detection pass rate (non-xfail): {rate:.0%} "
              f"({sum(1 for r in scored if r['status'] == 'PASS')}/{len(scored)})")

    if args.out:
        Path(args.out).write_text(json.dumps({"summary": counts, "rows": rows}, indent=2))
        print(f"[bench] wrote {args.out}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
