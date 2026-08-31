"""Import extraction — the front of the detection path.

Every import-based rule (AI-001 biometric libs, AI-002 LLM SDKs) matches on the
module path these functions return. A regression here is silent: the scan still
completes, still reports findings from other scanners, and simply never sees
the library. Scanning serengil/deepface once returned LIMITED_RISK with zero AI
components because `from deepface.commons import ...` was recorded as
`folder_utils`.
"""

from pathlib import Path

import pytest

from src.code_analyzer.scanners.import_scanner import _extract_imports, _module_matches


def modules(tmp_path: Path, code: str) -> list[str]:
    p = tmp_path / "sample.py"
    p.write_text(code, encoding="utf-8")
    return [m for m, _line, _excerpt in _extract_imports(p, p.read_bytes(), "python")]


# ── the regression this file exists for ───────────────────────────────────────

def test_from_import_records_the_module_not_the_imported_name(tmp_path):
    """`from X import Y` must yield X. It used to yield Y."""
    assert modules(tmp_path, "from deepface.commons import package_utils, folder_utils") == [
        "deepface.commons"
    ]


def test_from_import_single_level_module(tmp_path):
    assert modules(tmp_path, "from deepface import DeepFace") == ["deepface"]


@pytest.mark.parametrize(
    "code,expected",
    [
        ("from openai import OpenAI", "openai"),
        ("from anthropic import Anthropic", "anthropic"),
        ("from langchain.chains import LLMChain", "langchain.chains"),
    ],
)
def test_modern_from_import_style_is_visible(tmp_path, code, expected):
    """The dominant modern import style — invisible before the fix."""
    assert modules(tmp_path, code) == [expected]


# ── forms that already worked, kept so the fix does not regress them ──────────

def test_plain_import(tmp_path):
    assert modules(tmp_path, "import mediapipe.solutions.face_detection") == [
        "mediapipe.solutions.face_detection"
    ]


def test_aliased_import(tmp_path):
    assert modules(tmp_path, "import face_recognition.api as face_recognition") == [
        "face_recognition.api"
    ]


def test_multiple_names_in_one_import(tmp_path):
    """`import a, b` yields both; only the first was recorded before."""
    assert modules(tmp_path, "import os, deepface") == ["os", "deepface"]


# ── relative imports name no third-party library ──────────────────────────────

def test_bare_relative_import_is_skipped(tmp_path):
    assert modules(tmp_path, "from . import sibling") == []


def test_dotted_relative_import_records_its_path(tmp_path):
    assert modules(tmp_path, "from .relative.mod import thing") == ["relative.mod"]


# ── prefix matching against rule patterns ─────────────────────────────────────

def test_rule_matches_any_prefix_of_the_module_path(tmp_path):
    mods = modules(tmp_path, "from deepface.commons import folder_utils")
    assert any(_module_matches(m, "deepface") for m in mods)


def test_rule_does_not_match_an_unrelated_lookalike(tmp_path):
    mods = modules(tmp_path, "from deepfaker_utils import helper")
    assert not any(_module_matches(m, "deepface") for m in mods)
