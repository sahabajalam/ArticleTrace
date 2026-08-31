"""v07 T2: confidence-aware verdict escalation + the LLM triage contract."""

from src.agents.risk_classifier import PROHIBITED_MIN_CONFIDENCE, RiskClassifierAgent
from src.code_analyzer.finding_triage import apply_triage
from src.code_analyzer.models import Evidence, Finding
from src.state.scan_state import RiskCategory


# ── T2.1 escalation semantics ─────────────────────────────────────────────────

_COUNTS = {"critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0}


def test_armed_trigger_sets_prohibited():
    cat, reason = RiskClassifierAgent._classify(dict(_COUNTS), ["AI-009"], [])
    assert cat == RiskCategory.PROHIBITED
    assert "AI-009" in reason


def test_dampened_only_trigger_caps_at_high_risk():
    """DL-027 follow-up: deepface went PROHIBITED off a how-to file under
    tests/. Capability evidence in test/example context must not set a
    deployment verdict on its own."""
    cat, reason = RiskClassifierAgent._classify(dict(_COUNTS), [], ["AI-009"])
    assert cat == RiskCategory.HIGH_RISK
    assert "test/example context" in reason
    assert "AI-009" in reason


def test_armed_wins_over_dampened():
    cat, _ = RiskClassifierAgent._classify(dict(_COUNTS), ["AI-008"], ["AI-009"])
    assert cat == RiskCategory.PROHIBITED


def test_threshold_matches_test_path_dampener():
    """The tests/ dampener is x0.4, so a 0.9-confidence rule lands at 0.36 —
    below the bar; undampened evidence (0.9) is above. If either constant
    changes, this asserts the relationship still holds."""
    assert 0.9 * 0.4 < PROHIBITED_MIN_CONFIDENCE <= 0.9


# ── T2.2 triage contract: judge, never detector ───────────────────────────────

def _finding(conf: float = 0.9) -> Finding:
    return Finding(
        rule_id="AI-001", title="t", severity="critical", confidence=conf,
        evidence=[Evidence(file="a.py", line=1, excerpt="x")],
        mapped_articles=[], obligation_anchors=[], remediation="r",
    )


def test_demotion_halves_confidence_and_records_reason():
    f = _finding(0.9)
    c = apply_triage([f], [{"index": 0, "verdict": "demoted", "reason": "vendored copy"}])
    assert f.confidence == 0.45
    assert f.triage == "llm-demoted: vendored copy"
    assert c == {"confirmed": 0, "demoted": 1, "ignored": 0}


def test_confirmation_never_raises_confidence():
    f = _finding(0.36)
    apply_triage([f], [{"index": 0, "verdict": "confirmed"}])
    assert f.confidence == 0.36
    assert f.triage == "llm-confirmed"


def test_malformed_llm_output_is_ignored_not_fatal():
    f = _finding(0.9)
    c = apply_triage([f], [
        "not a dict",
        {"index": 99, "verdict": "demoted"},          # out of range
        {"index": -1, "verdict": "demoted"},           # negative
        {"index": 0, "verdict": "delete_this"},        # unknown verdict
        {"index": 0, "verdict": "demoted", "reason": "dup after ignore?"},
    ])
    # all five ignored: the unknown verdict consumes index 0 (ignored),
    # which also makes the later demotion a duplicate (ignored)
    assert c["ignored"] == 5
    assert c["demoted"] == 0
    assert f.confidence == 0.9  # untouched


def test_triage_cannot_delete_findings():
    fs = [_finding(), _finding()]
    apply_triage(fs, [{"index": 0, "verdict": "demoted", "reason": "x"}])
    assert len(fs) == 2


def test_demoted_prohibited_trigger_no_longer_escalates():
    """The full T2 interaction: LLM demotion drops a trigger below the
    escalation bar, so the classifier reports HIGH_RISK + dampened trigger
    instead of PROHIBITED. The LLM can defuse a verdict, never cause one."""
    f = _finding(0.9)
    f.rule_id = "AI-009"
    apply_triage([f], [{"index": 0, "verdict": "demoted", "reason": "sample code"}])
    assert f.confidence < PROHIBITED_MIN_CONFIDENCE
    cat, _ = RiskClassifierAgent._classify(dict(_COUNTS), [], [f.rule_id])
    assert cat == RiskCategory.HIGH_RISK
