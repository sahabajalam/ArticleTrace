"""Risk Classifier — aggregates findings into an EU AI Act risk posture.

Purely deterministic. No LLM call. Rule severities + prohibited-triggers drive
the category; the compliance score is a simple weighted deduction.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.agents.base import BaseAgent
from src.state.scan_state import RiskCategory, RiskPosture, ScanState


PROHIBITED_RULE_IDS: set[str] = {"AI-008", "AI-009"}

# v07 T2.1: a PROHIBITED verdict is a deployment claim, and evidence living
# only under tests/examples/ (path dampeners put such findings at ~0.36) is
# capability evidence, not deployment evidence. DL-027's follow-up was
# exactly this: deepface classified PROHIBITED because AI-009 matched a
# how-to file under tests/. A trigger must clear this bar to escalate;
# below it, the finding stays critical-severity and is reported as a
# dampened trigger for a human to judge.
PROHIBITED_MIN_CONFIDENCE = 0.5


class RiskClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="risk_classifier")

    async def execute(self, state: ScanState) -> dict[str, Any]:
        start = datetime.utcnow()
        profile = state["profile"] or {}
        findings: list[dict[str, Any]] = [
            f for f in profile.get("findings", []) if not f.get("suppressed", False)
        ]

        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        prohibited_triggers: list[str] = []
        dampened_triggers: list[str] = []
        for f in findings:
            sev = f.get("severity", "info").lower()
            if sev in counts:
                counts[sev] += 1
            if f.get("rule_id") in PROHIBITED_RULE_IDS:
                if float(f.get("confidence", 1.0)) >= PROHIBITED_MIN_CONFIDENCE:
                    prohibited_triggers.append(f["rule_id"])
                else:
                    dampened_triggers.append(f["rule_id"])

        category, reason = self._classify(counts, prohibited_triggers, dampened_triggers)
        score = self._score(counts)

        posture = RiskPosture(
            category=category,
            critical_count=counts["critical"],
            high_count=counts["high"],
            medium_count=counts["medium"],
            low_count=counts["low"],
            prohibited_triggers=sorted(set(prohibited_triggers)),
            dampened_triggers=sorted(set(dampened_triggers)),
            reason=reason,
            compliance_score=score,
        )

        duration = (datetime.utcnow() - start).total_seconds()
        update = {
            "risk_posture": posture.model_dump(mode="json"),
            "current_step": "risk_classified",
        }
        update.update(
            self.audit_update(
                action="classify_risk",
                summary=f"{category.value} score={score:.0f} triggers={prohibited_triggers}",
                duration_seconds=duration,
            )
        )
        return update

    @staticmethod
    def _classify(
        counts: dict[str, int],
        prohibited: list[str],
        dampened: list[str] | None = None,
    ) -> tuple[RiskCategory, str]:
        dampened = dampened or []
        if prohibited:
            return (
                RiskCategory.PROHIBITED,
                f"Prohibited-practice triggers: {', '.join(sorted(set(prohibited)))}. "
                f"See AI Act Art 5.",
            )
        if counts["critical"] > 0:
            note = ""
            if dampened:
                note = (
                    f" Prohibited-practice pattern(s) {', '.join(sorted(set(dampened)))} "
                    "matched only in test/example context — capability present; "
                    "verify deployment before treating as Art 5."
                )
            return (
                RiskCategory.HIGH_RISK,
                f"{counts['critical']} critical finding(s) — likely Annex III system."
                + note,
            )
        if counts["high"] >= 2:
            return (
                RiskCategory.HIGH_RISK,
                f"{counts['high']} high-severity findings indicate Annex III concerns.",
            )
        if counts["high"] == 1 or counts["medium"] >= 2:
            return (
                RiskCategory.LIMITED_RISK,
                "Transparency / documentation gaps detected; "
                "no prohibited or Annex III triggers.",
            )
        return (
            RiskCategory.MINIMAL_RISK,
            "No blocking findings; basic hygiene recommendations may apply.",
        )

    @staticmethod
    def _score(counts: dict[str, int]) -> float:
        score = 100.0
        score -= counts["critical"] * 25
        score -= counts["high"] * 10
        score -= counts["medium"] * 4
        score -= counts["low"] * 1
        return max(0.0, min(100.0, score))
