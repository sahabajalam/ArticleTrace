"""Tests for the scan state module and the deterministic scoring it feeds.

Replaces coverage lost with tests/unit/test_risk_classifier.py, which was
written against the v01 free-text classifier (`PROHIBITED_PATTERNS`,
`_check_prohibited`, `create_initial_state(system_description=...)`) that the
v02 static-scanner pivot removed. Those tests had not imported since commit
5210e51; these exercise the API that actually exists.

Classification tiers and prohibited-trigger escalation are covered in
test_t2_verdicts.py; this file covers state construction and scoring.
"""

from src.agents.risk_classifier import RiskClassifierAgent
from src.code_analyzer.models import AISystemProfile, DataSignals, RepoInfo
from src.state.scan_state import RiskCategory, create_initial_state


def _profile() -> AISystemProfile:
    return AISystemProfile(
        scan_id="scn_test",
        repo=RepoInfo(
            url="https://github.com/x/y", ref="main", commit="abc123",
            languages=["python"], total_files=10, scanned_files=8,
        ),
        ai_components=[], decision_surfaces=[], data_signals=DataSignals(),
        findings=[], stats={},
    )


# ── state construction ────────────────────────────────────────────────────────

def test_initial_state_carries_scan_identity_and_profile():
    state = create_initial_state("scn_1", "https://github.com/x/y", "main", _profile())
    assert state["scan_id"] == "scn_1"
    assert state["repo_url"] == "https://github.com/x/y"
    assert state["ref"] == "main"
    assert state["profile"]["scan_id"] == "scn_test"


def test_initial_state_starts_unclassified_and_running():
    state = create_initial_state("scn_1", "https://github.com/x/y", "main", _profile())
    assert state["risk_posture"] is None
    assert state["narrative"] is None
    assert state["final_report"] is None
    assert state["current_step"] == "initialized"
    assert state["workflow_status"] == "running"
    assert state["errors"] == []
    assert state["completed_at"] is None


# ── deterministic compliance score ────────────────────────────────────────────

def _score(**counts) -> float:
    base = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    base.update(counts)
    return RiskClassifierAgent._score(base)


def test_clean_repo_scores_100():
    assert _score() == 100.0


def test_severity_weights_are_ordered():
    assert _score(critical=1) == 75.0
    assert _score(high=1) == 90.0
    assert _score(medium=1) == 96.0
    assert _score(low=1) == 99.0


def test_score_floors_at_zero_never_negative():
    assert _score(critical=99) == 0.0


def test_score_is_bounded_to_the_declared_range():
    for counts in ({}, {"critical": 4}, {"critical": 3, "high": 5, "medium": 9}):
        assert 0.0 <= _score(**counts) <= 100.0


# ── classification tiers not covered by the T2 escalation tests ───────────────

def test_no_findings_is_minimal_risk():
    cat, _ = RiskClassifierAgent._classify(
        {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}, [], []
    )
    assert cat == RiskCategory.MINIMAL_RISK


def test_two_high_findings_reach_high_risk():
    cat, _ = RiskClassifierAgent._classify(
        {"critical": 0, "high": 2, "medium": 0, "low": 0, "info": 0}, [], []
    )
    assert cat == RiskCategory.HIGH_RISK


def test_single_high_is_limited_risk():
    cat, _ = RiskClassifierAgent._classify(
        {"critical": 0, "high": 1, "medium": 0, "low": 0, "info": 0}, [], []
    )
    assert cat == RiskCategory.LIMITED_RISK
