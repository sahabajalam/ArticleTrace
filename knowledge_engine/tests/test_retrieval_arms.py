"""Unit tests for the v08 P1 retrieval arms (name index + COMPLEMENTS).

Pure logic only — query sanitisation and RRF fusion. Recall/precision effects
are measured by scripts/14_eval_p1_arms.py against the live graph; these tests
pin the contracts that ablation depends on.
"""

import pytest

from src.retrieval.engine import RetrievalEngine


# ── Lucene sanitisation ───────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "question",
    [
        "What is a DPIA? (Art. 35)",
        "human oversight: required?",
        "AI + biometrics && surveillance",
        'a "quoted" phrase ~fuzzy^boost',
        "path/with\\slashes [brackets] {braces}",
    ],
)
def test_reserved_characters_never_reach_the_parser(question):
    """Every Lucene reserved character is stripped, not escaped: a stray `?`
    or `:` from a natural question is a syntax error, not a poor match."""
    out = RetrievalEngine._lucene_terms(question)
    for ch in '+-&|!(){}[]^"~*?:\\/':
        assert ch not in out, f"{ch!r} survived in {out!r}"


def test_terms_are_or_joined():
    assert RetrievalEngine._lucene_terms("human oversight") == "human OR oversight"


def test_short_tokens_dropped():
    """One- and two-character tokens match half the graph and drown the arm."""
    assert RetrievalEngine._lucene_terms("is a AI of human") == "human"


def test_empty_when_nothing_survives():
    """No terms must yield an empty string so the caller can skip the arm
    rather than send an empty query to the index."""
    assert RetrievalEngine._lucene_terms("a b ?") == ""
    assert RetrievalEngine._lucene_terms("!!! ???") == ""


# ── three-way RRF fusion ──────────────────────────────────────────────────────

def _engine() -> RetrievalEngine:
    return RetrievalEngine.__new__(RetrievalEngine)  # no I/O needed for fusion


def _v(eid, sim=0.9):
    return {"entity_id": eid, "similarity": sim, "metadata": {}, "document": ""}


def _g(eid, score=1.0):
    return {"entity_id": eid, "graph_score": score, "node_data": {}, "hop_depth": 1}


def _n(eid, score=5.0):
    return {"entity_id": eid, "name_score": score, "metadata": {}, "document": ""}


def test_name_arm_contributes_entities_no_other_arm_found():
    e = _engine(); e.rrf_k = 60
    fused = e._rrf_fusion([_v("A")], [_g("B")], [_n("CONCEPT_X")])
    ids = {r["entity_id"] for r in fused}
    assert "CONCEPT_X" in ids
    entry = next(r for r in fused if r["entity_id"] == "CONCEPT_X")
    assert entry["sources"] == ["name"]
    assert entry["name_rank"] == 1


def test_agreement_across_arms_outranks_single_arm_hits():
    e = _engine(); e.rrf_k = 60
    fused = e._rrf_fusion([_v("AGREED"), _v("ONLY_V")], [_g("AGREED")], [_n("AGREED")])
    assert fused[0]["entity_id"] == "AGREED"
    assert set(fused[0]["sources"]) == {"vector", "graph", "name"}


def test_fusion_without_name_arm_is_unchanged():
    """Passing no name results must behave exactly as the two-arm version, so
    the ablation's `baseline` really is the old system."""
    e = _engine(); e.rrf_k = 60
    two = e._rrf_fusion([_v("A")], [_g("B")])
    three = e._rrf_fusion([_v("A")], [_g("B")], [])
    assert [r["entity_id"] for r in two] == [r["entity_id"] for r in three]
    assert [r["rrf_score"] for r in two] == [r["rrf_score"] for r in three]


def test_duplicate_ids_across_arms_are_merged_not_repeated():
    e = _engine(); e.rrf_k = 60
    fused = e._rrf_fusion([_v("X")], [_g("X")], [_n("X")])
    assert len(fused) == 1
    assert fused[0]["in_both"] is True
