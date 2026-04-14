"""Smoke test: end-to-end AST + LLM review pipeline on a tiny fixture repo.

Creates two Python files in a temp dir:
  - app.py       : a real FastAPI decision endpoint that calls an LLM
                   with NO human review and NO audit log
  - test_app.py  : a test that also matches the regex heuristic but is
                   clearly a test (LLM should mark is_test_or_mock=True)

Runs the scan pipeline via ``ingest_local`` and prints:
  - number of decision surfaces left after LLM review
  - the LLM rationale per surface
  - findings emitted by ``AstRulesScanner``
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from src.code_analyzer.scan import run_scan


APP_PY = '''
from fastapi import FastAPI

app = FastAPI()
client = None  # pretend OpenAI client

@app.post("/score")
def score_applicant(payload: dict):
    """Real decision endpoint: scores a loan application via an LLM.
    No human review, no audit log -- should trigger two findings."""
    result = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": str(payload)}],
    )
    return {"score": result.choices[0].message.content}

@app.get("/health")
def health():
    return {"ok": True}
'''

TEST_PY = '''
from fastapi.testclient import TestClient

def test_predict_mock():
    """Test that exercises a mocked predict() -- should be dropped by the LLM."""
    class FakeModel:
        def predict(self, x):
            return 0.5
    m = FakeModel()
    assert m.predict([1, 2, 3]) == 0.5
'''


async def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "app.py").write_text(APP_PY, encoding="utf-8")
        (root / "test_app.py").write_text(TEST_PY, encoding="utf-8")

        profile = await run_scan(
            scan_id="smoke-001",
            local_path=root,
            enrich_with_kg=False,
        )

        print("=" * 60)
        print("PROFILE")
        print("=" * 60)
        print(f"scan_id           : {profile.scan_id}")
        print(f"findings count    : {len(profile.findings)}")
        print(f"repo              : {profile.repo.url or profile.repo.ref}")
        print(f"stats             : {profile.stats}")
        print()
        print("DECISION SURFACES (post-LLM review)")
        print("-" * 60)
        for s in profile.decision_surfaces or []:
            print(
                f"  {s.endpoint}  ({s.file}:{s.line})  "
                f"calls_model={s.calls_model} "
                f"review={s.has_human_review} "
                f"audit={s.has_audit_log}"
            )
        print()
        print("FINDINGS")
        print("-" * 60)
        for f in profile.findings:
            print(f"  [{f.rule_id}] conf={f.confidence:.2f} suppressed={f.suppressed}")
            for ev in f.evidence:
                print(f"      -> {ev.file}:{ev.line}  {ev.excerpt[:80]}")


if __name__ == "__main__":
    asyncio.run(main())
