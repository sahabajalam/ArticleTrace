"""Stream-dump the live Neo4j instance to JSONL, then verify the dump.

Reads from the instance pointed at by .env (NEO4J_URI / USER / PASSWORD).
Writes:
  backups/<TS>_nodes.jsonl    — one node per line {labels, properties}
  backups/<TS>_rels.jsonl     — one rel per line  {type, start, end, properties}
  backups/<TS>_indexes.json   — vector + property indexes
  backups/<TS>_meta.json      — counts + source URI + timestamp

Streaming + line-delimited so a mid-export drop is recoverable rather than corrupt.
Embeddings (lists of 3072 floats) are preserved as JSON arrays.

Every run ends with a self-check (`verify_dump`) that re-reads the files off disk
and compares them against the counts in `meta.json`. A backup that is never read
back is a silent success — the failure class in BUG_LOG DL-003/019/020/023/025 —
so the script exits non-zero and says what is wrong rather than printing
"BACKUP COMPLETE" over a truncated file. The check runs on every invocation,
local or CI; it is not a CI-only step.

Usage:
  cd knowledge_engine
  python scripts/10_backup_to_jsonl.py              # dump, then verify
  python scripts/10_backup_to_jsonl.py --verify TS  # verify an existing dump only
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BACKUP_DIR = PROJECT_ROOT / "backups"

# meta.json keys the verifier needs; a dump missing any of them cannot be checked.
_REQUIRED_META_KEYS = (
    "nodes_file", "rels_file", "indexes_file", "node_count", "rel_count",
)


class DumpVerificationError(RuntimeError):
    """A dump on disk does not match what its own meta.json claims."""


class _JsonlScan(NamedTuple):
    lines: int           # complete, newline-terminated records
    last: str | None     # last record read, terminated or not
    unterminated: bool   # the file ends mid-record


def _scan_jsonl(path: Path) -> _JsonlScan:
    """Count records in a JSONL file and report whether the last one is complete.

    A file cut off mid-write ends without a newline. Counting only terminated
    lines means such a file is both short by one *and* flagged, rather than
    accidentally matching the expected count.
    """
    lines = 0
    last: str | None = None
    unterminated = False
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            last = line
            if line.endswith("\n"):
                lines += 1
            else:
                unterminated = True
    return _JsonlScan(lines, last, unterminated)


def verify_dump(ts: str, backup_dir: Path | None = None) -> dict:
    """Check the dump for `ts` against its meta.json; return the meta on success.

    Raises `DumpVerificationError` listing every problem found — missing files,
    a record cut off mid-write, line counts that disagree with `node_count` /
    `rel_count`, or a final record that is not parseable JSON.
    """
    backup_dir = BACKUP_DIR if backup_dir is None else backup_dir
    meta_path = backup_dir / f"{ts}_meta.json"
    if not meta_path.is_file():
        raise DumpVerificationError(
            f"No meta file at {meta_path} — cannot verify a dump that never "
            f"recorded what it wrote."
        )
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DumpVerificationError(f"{meta_path.name} is not valid JSON: {exc}") from exc

    missing_keys = [k for k in _REQUIRED_META_KEYS if k not in meta]
    if missing_keys:
        raise DumpVerificationError(
            f"{meta_path.name} is missing required key(s): {', '.join(missing_keys)}"
        )

    problems: list[str] = []

    for kind, file_key, count_key in (
        ("node", "nodes_file", "node_count"),
        ("relationship", "rels_file", "rel_count"),
    ):
        path = backup_dir / meta[file_key]
        expected = meta[count_key]

        if not path.is_file():
            problems.append(
                f"{path.name}: file is missing, but meta.json claims "
                f"{expected:,} {kind}s"
            )
            continue

        scan = _scan_jsonl(path)
        if scan.unterminated:
            problems.append(
                f"{path.name}: last line has no terminating newline — the dump "
                f"was cut off mid-record"
            )
        if scan.lines != expected:
            problems.append(
                f"{path.name}: {scan.lines:,} complete {kind} lines on disk, "
                f"meta.json claims {expected:,} "
                f"(off by {scan.lines - expected:+,})"
            )
        if scan.last is not None:
            try:
                json.loads(scan.last)
            except json.JSONDecodeError as exc:
                problems.append(
                    f"{path.name}: last record is not valid JSON ({exc}) — "
                    f"the file is corrupt, not merely short"
                )
        elif expected:
            problems.append(
                f"{path.name}: file is empty, but meta.json claims "
                f"{expected:,} {kind}s"
            )

    indexes_path = backup_dir / meta["indexes_file"]
    if not indexes_path.is_file():
        problems.append(f"{indexes_path.name}: file is missing")
    else:
        try:
            json.loads(indexes_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{indexes_path.name}: not valid JSON ({exc})")

    if problems:
        raise DumpVerificationError(
            f"Dump {ts} failed self-check ({len(problems)} problem"
            f"{'' if len(problems) == 1 else 's'}):\n  - "
            + "\n  - ".join(problems)
        )

    return meta


def _run_verification(ts: str, backup_dir: Path | None = None) -> int:
    """Verify and print the result. Returns a process exit code."""
    backup_dir = BACKUP_DIR if backup_dir is None else backup_dir
    print(f"Self-check: re-reading dump {ts} from {backup_dir} ...")
    try:
        meta = verify_dump(ts, backup_dir)
    except DumpVerificationError as exc:
        # Whole block on stderr, so the failure stays in one piece rather than
        # interleaving with stdout in a CI log.
        print(file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("BACKUP VERIFICATION FAILED — DO NOT TRUST THIS DUMP", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(exc, file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        return 1
    print(
        f"  [OK] {meta['node_count']:,} node lines and {meta['rel_count']:,} "
        f"relationship lines match meta.json"
    )
    return 0


def run_backup() -> tuple[str, Path]:
    """Dump the live instance. Returns (timestamp, output dir). Does not verify."""
    # Imported here, not at module scope, so `--verify` (and the tests) work on a
    # machine with no .env and no credentials — verification is pure filesystem work.
    from src.config import settings

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = BACKUP_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes_path = out_dir / f"{ts}_nodes.jsonl"
    rels_path = out_dir / f"{ts}_rels.jsonl"
    indexes_path = out_dir / f"{ts}_indexes.json"
    meta_path = out_dir / f"{ts}_meta.json"

    from neo4j import GraphDatabase

    print(f"Source URI: {settings.neo4j_uri}")
    print(f"Output dir: {out_dir}")
    print()

    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    node_count = 0
    rel_count = 0

    try:
        with driver.session() as session:
            print("[1/3] Dumping nodes -> ", nodes_path.name, " ...")
            with nodes_path.open("w", encoding="utf-8") as f:
                result = session.run("MATCH (n) RETURN n, elementId(n) AS eid, labels(n) AS labels")
                for record in result:
                    n = record["n"]
                    f.write(json.dumps({
                        "eid": record["eid"],
                        "labels": record["labels"],
                        "properties": dict(n),
                    }, default=str, ensure_ascii=False) + "\n")
                    node_count += 1
                    if node_count % 200 == 0:
                        print(f"  ... {node_count} nodes")
            print(f"  [OK] {node_count} nodes written")
            print()

            print("[2/3] Dumping relationships -> ", rels_path.name, " ...")
            with rels_path.open("w", encoding="utf-8") as f:
                result = session.run(
                    "MATCH (a)-[r]->(b) RETURN type(r) AS t, elementId(a) AS s, "
                    "elementId(b) AS e, properties(r) AS p"
                )
                for record in result:
                    f.write(json.dumps({
                        "type": record["t"],
                        "start": record["s"],
                        "end": record["e"],
                        "properties": dict(record["p"]),
                    }, default=str, ensure_ascii=False) + "\n")
                    rel_count += 1
                    if rel_count % 500 == 0:
                        print(f"  ... {rel_count} rels")
            print(f"  [OK] {rel_count} rels written")
            print()

            print("[3/3] Dumping indexes/constraints -> ", indexes_path.name, " ...")
            vector_indexes = [dict(r) for r in session.run("SHOW VECTOR INDEXES")]
            other_indexes = [dict(r) for r in session.run("SHOW INDEXES")]
            constraints = [dict(r) for r in session.run("SHOW CONSTRAINTS")]
            indexes_path.write_text(
                json.dumps({
                    "vector_indexes": vector_indexes,
                    "all_indexes": other_indexes,
                    "constraints": constraints,
                }, default=str, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"  [OK] {len(vector_indexes)} vector indexes, "
                  f"{len(other_indexes)} total indexes, {len(constraints)} constraints")
            print()
    finally:
        driver.close()

    meta = {
        "timestamp_utc": ts,
        "source_uri": settings.neo4j_uri,
        "source_user": settings.neo4j_user,
        "node_count": node_count,
        "rel_count": rel_count,
        "nodes_file": nodes_path.name,
        "rels_file": rels_path.name,
        "indexes_file": indexes_path.name,
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"  Timestamp: {ts}")
    print(f"  Nodes:     {node_count:,}")
    print(f"  Rels:      {rel_count:,}")
    print(f"  Sizes:")
    for p in (nodes_path, rels_path, indexes_path, meta_path):
        size_mb = p.stat().st_size / 1024 / 1024
        print(f"    {p.name:40s} {size_mb:8.2f} MB")
    print()

    return ts, out_dir


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--verify" in argv:
        i = argv.index("--verify")
        if i + 1 >= len(argv):
            print("Usage: 10_backup_to_jsonl.py --verify <TIMESTAMP>")
            print("       (e.g. 10_backup_to_jsonl.py --verify 20260619_183622)")
            return 2
        return _run_verification(argv[i + 1])

    ts, out_dir = run_backup()

    # Only after the dump has been read back does this count as a backup.
    if _run_verification(ts, out_dir) != 0:
        return 1

    print("=" * 60)
    print("BACKUP COMPLETE AND VERIFIED")
    print("=" * 60)
    print(f"  Timestamp: {ts}")
    print(f"  Output:    {out_dir}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
