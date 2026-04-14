"""Live smoke test: exercises legal_research against the running
knowledge_engine (8001) with realistic findings.

Run:
    cd orchestrator
    python test_legal_research_live.py
"""

import asyncio
import json
import sys

sys.path.insert(0, "src")

from src.agents.legal_research import LegalResearchAgent


FINDINGS = [
    {
        "rule_id": "AI-003",
        "title": "User-facing AI decision endpoint without human review",
        "severity": "high",
        "obligation_anchors": ["human_oversight", "automated_decision"],
        "mapped_articles": ["AIACT_ART_14", "GDPR_ART_22", "AIACT_ART_26"],
        "evidence": [{"file": "frontend_api/src/routes/score.ts", "line": 32}],
        "suppressed": False,
    },
    {
        "rule_id": "AI-002",
        "title": "Generative AI / LLM SDK usage",
        "severity": "high",
        "obligation_anchors": ["transparency", "ai_disclosure"],
        "mapped_articles": ["AIACT_ART_50", "AIACT_ART_52", "AIACT_ART_13"],
        "evidence": [{"file": "app/services/llm_client.py", "line": 10}],
        "suppressed": False,
    },
    {
        "rule_id": "AI-001",
        "title": "Biometric / face / emotion recognition library usage",
        "severity": "critical",
        "obligation_anchors": ["biometric_identification", "prohibited_practice"],
        "mapped_articles": ["AIACT_ART_5"],
        "evidence": [{"file": "app/services/biometric_matcher.py", "line": 17}],
        "suppressed": False,
    },
]

STATE = {
    "scan_id": "test_live",
    "profile": {"findings": FINDINGS},
}


async def main():
    agent = LegalResearchAgent()
    print(f"KB URL: {agent.kb_url}")
    out = await agent.execute(STATE)  # type: ignore

    citations_by_rule = {
        fc["rule_id"]: fc for fc in out.get("finding_citations", [])
    }
    for rid in ("AI-003", "AI-002", "AI-001"):
        fc = citations_by_rule.get(rid)
        print(f"\n=== {rid} ===")
        if not fc:
            print("  (no record)")
            continue
        cits = fc.get("citations", [])
        print(f"  {len(cits)} citation(s)")
        for c in cits:
            print(
                f"   • {c['regulation']} Art. {c['article_number']} "
                f"(score={c['relevance_score']:.3f})"
            )
            if c.get("title"):
                print(f"     title: {c['title']}")
            if c.get("text_snippet"):
                print(f"     snippet: {c['text_snippet'][:100]}...")
        chain = fc.get("reasoning_chain", [])
        if chain:
            print("  chain:")
            for step in chain:
                print(f"    {step}")

    audit = out.get("audit_log", [])
    if audit:
        print(f"\nAudit: {json.dumps(audit[-1], indent=2, default=str)}")


if __name__ == "__main__":
    asyncio.run(main())
