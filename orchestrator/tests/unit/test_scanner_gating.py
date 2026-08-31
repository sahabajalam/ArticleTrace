"""Regression tests for the three defects the detection benchmark's first run
caught (BUG_LOG DL-028/029/030): absolute-path exclusion, dead repo-level
findings, and ungated PII keywords."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from src.code_analyzer.ingest import ingest_local
from src.code_analyzer.models import Evidence
from src.code_analyzer.rule_loader import load_rules
from src.code_analyzer.scan import _scan_and_profile
from src.code_analyzer.scanners import ContentScanner, ScanContext


# ── DL-028: exclusions must be repo-relative, not absolute ────────────────────

def test_repo_under_excluded_ancestor_still_scans(tmp_path):
    """A repo cloned under a directory named like an excluded dir (.cache,
    build, env…) used to ingest 0 files and scan clean."""
    root = tmp_path / ".cache" / "myrepo"
    root.mkdir(parents=True)
    (root / "app.py").write_text("import face_recognition\n")
    result = ingest_local(root)
    assert len(result.files) == 1
    assert result.repo_info.scanned_files == 1


def test_excluded_dirs_inside_repo_still_excluded(tmp_path):
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "junk.js").write_text("var x = 1;\n")
    (tmp_path / "app.py").write_text("import os\n")
    result = ingest_local(tmp_path)
    assert [p.name for p in result.files] == ["app.py"]


# ── DL-029: repo-level (absent-marker) findings must be emittable ─────────────

def test_evidence_line_none_is_valid_for_repo_level_facts():
    ev = Evidence(file=".", line=None, excerpt="Missing model card", symbol="<repo>")
    assert ev.line is None


def test_evidence_line_zero_still_rejected():
    with pytest.raises(ValidationError):
        Evidence(file="a.py", line=0)


def test_missing_model_card_finding_is_actually_emitted(tmp_path):
    """AI-004/AI-006 crashed on Evidence(line=0) inside the scanner's
    try/except, so they had never produced a finding on any repo."""
    (tmp_path / "app.py").write_text("from deepface import DeepFace\n")
    profile = _scan_and_profile("t", ingest_local(tmp_path), use_llm=False)
    rule_ids = {f.rule_id for f in profile.findings}
    assert "AI-004" in rule_ids
    assert "AI-006" in rule_ids


# ── DL-030: AI-005 requires evidence of AI usage ──────────────────────────────

def _content_findings(tmp_path: Path, code: str, with_ai_import: bool):
    (tmp_path / "handlers.py").write_text(code)
    result = ingest_local(tmp_path)
    ctx = ScanContext(
        repo_root=result.repo_root, files=result.files,
        suppressions=result.suppressions,
    )
    if with_ai_import:
        # what ImportScanner leaves behind when an AI-001/002 import matched
        ctx.shared["imports_by_rule"] = {"AI-002": [("handlers.py", [("openai", 1, "x")])]}
    return ContentScanner().scan(ctx, load_rules())


def test_pii_keyword_alone_does_not_fire_ai005(tmp_path):
    """The word "email" in a plain web app is not an AI system (measured FP:
    a Flask docstring about URL generation)."""
    f = _content_findings(tmp_path, "# send email to the user\n", with_ai_import=False)
    assert not [x for x in f if x.rule_id == "AI-005"]


def test_pii_keyword_with_ai_usage_fires_ai005(tmp_path):
    f = _content_findings(tmp_path, "# send email to the user\n", with_ai_import=True)
    assert [x for x in f if x.rule_id == "AI-005"]


# ── DL-035: an empty rule corpus must never look like a clean scan ────────────

def test_missing_rules_dir_raises_instead_of_returning_empty(tmp_path):
    """Path.glob on a missing directory yields nothing and raises nothing, so
    a stale RULES_DIR produced 0 rules -> 0 findings -> MINIMAL_RISK."""
    from src.code_analyzer.rule_loader import EmptyRuleCorpus, load_rules
    with pytest.raises(EmptyRuleCorpus) as e:
        load_rules(tmp_path / "does-not-exist")
    assert "does not exist" in str(e.value)


def test_empty_rules_dir_also_raises(tmp_path):
    from src.code_analyzer.rule_loader import EmptyRuleCorpus, load_rules
    (tmp_path / "rules").mkdir()
    with pytest.raises(EmptyRuleCorpus):
        load_rules(tmp_path / "rules")


def test_real_corpus_loads_and_is_reported_in_stats(tmp_path):
    from src.code_analyzer.rule_loader import load_rules
    assert len(load_rules()) >= 10
    (tmp_path / "app.py").write_text("from deepface import DeepFace\n")
    profile = _scan_and_profile("t", ingest_local(tmp_path), use_llm=False)
    assert profile.stats["rules_loaded"] >= 10
