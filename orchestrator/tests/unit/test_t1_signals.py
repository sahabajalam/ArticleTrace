"""v07 T1: manifest cross-referencing, notebook extraction, string patterns.

Each signal has a benchmark fixture proving it end-to-end; these tests pin the
unit-level contracts so a regression is named precisely, not just "fixture
went red".
"""

import json
from pathlib import Path

from src.code_analyzer.ingest import ingest_local
from src.code_analyzer.rule_loader import load_rules
from src.code_analyzer.scan import _scan_and_profile
from src.code_analyzer.scanners.import_scanner import (
    _dist_matches_needle,
    _parse_requirement,
)
from src.code_analyzer.source_reader import read_source_bytes


def profile_of(tmp_path: Path):
    return _scan_and_profile("t", ingest_local(tmp_path), use_llm=False)


def rule_counts(profile) -> dict:
    out: dict = {}
    for f in profile.findings:
        out[f.rule_id] = out.get(f.rule_id, 0) + 1
    return out


# ── T1.1 manifest cross-referencing ───────────────────────────────────────────

def test_requirement_line_parsing():
    assert _parse_requirement("deepface==0.0.93") == "deepface"
    assert _parse_requirement("openai>=1.0,<2  # pinned") == "openai"
    assert _parse_requirement("transformers[torch]~=4.40") == "transformers"
    assert _parse_requirement("# a comment") is None
    assert _parse_requirement("-r base.txt") is None
    assert _parse_requirement("git+https://github.com/x/y") is None


def test_dist_to_needle_matching():
    # separator/case drift between distribution and import names
    assert _dist_matches_needle("face-recognition", "face_recognition")
    assert _dist_matches_needle("google-generativeai", "google.generativeai")
    # dist satisfies a deep import path via its top-level package
    assert _dist_matches_needle("dlib", "dlib.get_frontal_face_detector")
    # lookalikes must not match
    assert not _dist_matches_needle("deepfaker-utils", "deepface")
    assert not _dist_matches_needle("openai-agents-helper", "openai")


def test_declared_only_dependency_produces_dampened_finding(tmp_path):
    (tmp_path / "requirements.txt").write_text("deepface==0.0.93\nflask>=3.0\n")
    (tmp_path / "loader.py").write_text("import importlib\n")
    profile = profile_of(tmp_path)
    ai001 = [f for f in profile.findings if f.rule_id == "AI-001"]
    assert len(ai001) == 1
    f = ai001[0]
    assert f.confidence < 0.9  # dampened: declared, not seen used
    assert "no static import located" in (f.evidence[0].excerpt or "")
    assert f.evidence[0].file == "requirements.txt"
    assert f.evidence[0].line == 1


def test_declared_plus_imported_boosts_instead_of_duplicating(tmp_path):
    (tmp_path / "requirements.txt").write_text("deepface==0.0.93\n")
    (tmp_path / "app.py").write_text("from deepface import DeepFace\n")
    profile = profile_of(tmp_path)
    ai001 = [f for f in profile.findings if f.rule_id == "AI-001"]
    assert len(ai001) == 1  # boosted, not doubled
    assert ai001[0].confidence > 0.9
    assert any("declared in manifest" in (e.excerpt or "") for e in ai001[0].evidence)


def test_pyproject_and_package_json_are_read(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["openai>=1.0"]\n'
    )
    sub = tmp_path / "web"
    sub.mkdir()
    (sub / "package.json").write_text(
        json.dumps({"dependencies": {"@anthropic-ai/sdk": "^0.20.0"}})
    )
    profile = profile_of(tmp_path)
    ai002 = [f for f in profile.findings if f.rule_id == "AI-002"]
    assert len(ai002) == 1
    declared = {e.symbol for e in ai002[0].evidence}
    assert declared == {"openai", "@anthropic-ai/sdk"}


def test_broken_manifest_reports_error_instead_of_swallowing(tmp_path):
    (tmp_path / "pyproject.toml").write_text("this is [not toml")
    (tmp_path / "app.py").write_text("import os\n")
    profile = profile_of(tmp_path)
    errs = profile.stats["manifest_scan"]["errors"]
    assert errs and "pyproject.toml" in errs[0]


# ── T1.2 notebook extraction ──────────────────────────────────────────────────

def _nb(cells) -> str:
    return json.dumps({"cells": cells, "nbformat": 4, "nbformat_minor": 5})


def test_notebook_code_cells_extracted_markdown_skipped(tmp_path):
    p = tmp_path / "a.ipynb"
    p.write_text(_nb([
        {"cell_type": "markdown", "source": ["# import nothing\n"]},
        {"cell_type": "code", "source": ["%matplotlib inline\n", "from openai import OpenAI\n"]},
    ]))
    source, err = read_source_bytes(p)
    assert err is None
    text = source.decode()
    assert "from openai import OpenAI" in text
    assert "# MAGIC %matplotlib" in text          # magics commented, line kept
    assert "import nothing" not in text.replace("# %%", "")  # markdown dropped


def test_corrupt_notebook_reports_error_not_exception(tmp_path):
    p = tmp_path / "bad.ipynb"
    p.write_text("{not json")
    source, err = read_source_bytes(p)
    assert source == b""
    assert err and "bad.ipynb" in err


def test_notebook_only_repo_produces_findings_and_error_channel(tmp_path):
    (tmp_path / "demo.ipynb").write_text(_nb([
        {"cell_type": "code", "source": ["from deepface import DeepFace\n"]},
    ]))
    (tmp_path / "broken.ipynb").write_text("{nope")
    profile = profile_of(tmp_path)
    assert any(f.rule_id == "AI-001" for f in profile.findings)
    assert any("broken.ipynb" in e for e in profile.stats["source_read_errors"])


# ── T1.3 string patterns ──────────────────────────────────────────────────────

def test_raw_llm_endpoint_fires_ai002_without_any_import(tmp_path):
    (tmp_path / "client.py").write_text(
        'import requests\nrequests.post("https://api.openai.com/v1/chat/completions")\n'
    )
    profile = profile_of(tmp_path)
    ai002 = [f for f in profile.findings if f.rule_id == "AI-002"]
    assert len(ai002) == 1
    assert "api.openai.com" in (ai002[0].evidence[0].symbol or "")


def test_from_pretrained_model_id_fires_ai002(tmp_path):
    (tmp_path / "model.py").write_text(
        'model = AutoModel.from_pretrained("Salesforce/codegen-350M")\n'
    )
    profile = profile_of(tmp_path)
    assert any(f.rule_id == "AI-002" for f in profile.findings)


def test_endpoint_in_docs_prose_does_not_fire(tmp_path):
    """README mentioning an endpoint is documentation, not usage — matching it
    would recreate the DL-030 class of false positive."""
    (tmp_path / "README.md").write_text(
        "Set your key before calling https://api.openai.com endpoints.\n"
    )
    (tmp_path / "app.py").write_text("import os\n")
    profile = profile_of(tmp_path)
    assert not any(f.rule_id == "AI-002" for f in profile.findings)
