"""Tests for the backup dump self-check in scripts/10_backup_to_jsonl.py.

The point of the check is that a truncated or corrupt dump must not be able to
report success — BUG_LOG's recurring failure class (DL-003, DL-019, DL-020,
DL-023, DL-025) is a component reporting success while doing nothing. So each
test here breaks a dump in a different way and asserts the check says so.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# The script's filename starts with a digit, so it is not importable by name.
# It deliberately imports `src.config` lazily, which is what lets this load
# without credentials — verification is pure filesystem work.
_SCRIPT = PROJECT_ROOT / "scripts" / "10_backup_to_jsonl.py"
_spec = importlib.util.spec_from_file_location("backup_to_jsonl", _SCRIPT)
backup = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(backup)

TS = "20260831_120000"


def write_dump(
    backup_dir: Path,
    *,
    nodes: int = 3,
    rels: int = 2,
    node_count: int | None = None,
    rel_count: int | None = None,
) -> Path:
    """Write a well-formed dump. `*_count` override meta to simulate a mismatch."""
    backup_dir.mkdir(parents=True, exist_ok=True)

    (backup_dir / f"{TS}_nodes.jsonl").write_text(
        "".join(
            json.dumps({"eid": f"n{i}", "labels": ["Entity"], "properties": {"id": f"E{i}"}})
            + "\n"
            for i in range(nodes)
        ),
        encoding="utf-8",
    )
    (backup_dir / f"{TS}_rels.jsonl").write_text(
        "".join(
            json.dumps({"type": "REL", "start": f"n{i}", "end": f"n{i + 1}", "properties": {}})
            + "\n"
            for i in range(rels)
        ),
        encoding="utf-8",
    )
    (backup_dir / f"{TS}_indexes.json").write_text(
        json.dumps({"vector_indexes": [], "all_indexes": [], "constraints": []}),
        encoding="utf-8",
    )
    (backup_dir / f"{TS}_meta.json").write_text(
        json.dumps(
            {
                "timestamp_utc": TS,
                "source_uri": "neo4j+s://example.databases.neo4j.io",
                "source_user": "neo4j",
                "node_count": nodes if node_count is None else node_count,
                "rel_count": rels if rel_count is None else rel_count,
                "nodes_file": f"{TS}_nodes.jsonl",
                "rels_file": f"{TS}_rels.jsonl",
                "indexes_file": f"{TS}_indexes.json",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return backup_dir


@pytest.fixture
def dump_dir(tmp_path) -> Path:
    return write_dump(tmp_path / "backups")


class TestIntactDump:
    def test_a_complete_dump_passes(self, dump_dir):
        meta = backup.verify_dump(TS, dump_dir)

        assert meta["node_count"] == 3
        assert meta["rel_count"] == 2

    def test_an_empty_graph_is_consistent_not_broken(self, tmp_path):
        """Zero nodes is a real (if alarming) state; it is not a truncation."""
        d = write_dump(tmp_path / "backups", nodes=0, rels=0)

        assert backup.verify_dump(TS, d)["node_count"] == 0

    def test_the_runner_returns_zero(self, dump_dir):
        assert backup._run_verification(TS, dump_dir) == 0


class TestTruncation:
    def test_dropping_whole_lines_is_caught(self, dump_dir):
        """The acceptance case: truncate a dump file, the check must fail."""
        path = dump_dir / f"{TS}_nodes.jsonl"
        kept = path.read_text(encoding="utf-8").splitlines(keepends=True)[:1]
        path.write_text("".join(kept), encoding="utf-8")

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        message = str(exc_info.value)
        assert f"{TS}_nodes.jsonl" in message
        assert "1 complete node lines" in message
        assert "claims 3" in message
        assert "-2" in message

    def test_a_record_cut_off_mid_write_is_caught(self, dump_dir):
        """A byte-level cut leaves a partial final line, not a missing one."""
        path = dump_dir / f"{TS}_rels.jsonl"
        raw = path.read_bytes()
        path.write_bytes(raw[: len(raw) - 12])

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        message = str(exc_info.value)
        assert "cut off mid-record" in message
        assert "not valid JSON" in message

    def test_an_emptied_file_is_caught(self, dump_dir):
        (dump_dir / f"{TS}_nodes.jsonl").write_text("", encoding="utf-8")

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        assert "file is empty" in str(exc_info.value)

    def test_the_runner_returns_nonzero(self, dump_dir):
        (dump_dir / f"{TS}_nodes.jsonl").write_text("", encoding="utf-8")

        assert backup._run_verification(TS, dump_dir) == 1


class TestCountMismatch:
    def test_meta_overstating_relationships_is_caught(self, tmp_path):
        d = write_dump(tmp_path / "backups", rels=2, rel_count=4423)

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, d)

        message = str(exc_info.value)
        assert "2 complete relationship lines" in message
        assert "4,423" in message

    def test_every_problem_is_reported_not_just_the_first(self, tmp_path):
        d = write_dump(tmp_path / "backups", node_count=99, rel_count=99)

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, d)

        message = str(exc_info.value)
        assert "2 problems" in message
        assert f"{TS}_nodes.jsonl" in message
        assert f"{TS}_rels.jsonl" in message


class TestMissingOrCorruptFiles:
    def test_a_missing_meta_file_is_not_a_pass(self, tmp_path):
        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, tmp_path)

        assert "No meta file" in str(exc_info.value)

    def test_a_missing_jsonl_file_is_caught(self, dump_dir):
        (dump_dir / f"{TS}_rels.jsonl").unlink()

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        assert "file is missing" in str(exc_info.value)

    def test_a_missing_indexes_file_is_caught(self, dump_dir):
        (dump_dir / f"{TS}_indexes.json").unlink()

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        assert f"{TS}_indexes.json" in str(exc_info.value)

    def test_a_corrupt_indexes_file_is_caught(self, dump_dir):
        (dump_dir / f"{TS}_indexes.json").write_text("{not json", encoding="utf-8")

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        assert "not valid JSON" in str(exc_info.value)

    def test_meta_without_the_counts_cannot_claim_success(self, dump_dir):
        (dump_dir / f"{TS}_meta.json").write_text(
            json.dumps({"timestamp_utc": TS}), encoding="utf-8"
        )

        with pytest.raises(backup.DumpVerificationError) as exc_info:
            backup.verify_dump(TS, dump_dir)

        assert "missing required key" in str(exc_info.value)


class TestCli:
    def test_verify_flag_checks_an_existing_dump(self, dump_dir, monkeypatch):
        monkeypatch.setattr(backup, "BACKUP_DIR", dump_dir)

        assert backup.main(["--verify", TS]) == 0

    def test_verify_flag_without_a_timestamp_is_a_usage_error(self):
        assert backup.main(["--verify"]) == 2
