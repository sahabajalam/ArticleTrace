"""EU AI Act compliance monitoring.

Monitors Article 14 (Human Oversight) requirements for high-risk AI systems.

Article 14 Requirements:
1. High-risk systems must enable human oversight
2. Humans can intervene in system decisions
3. Humans can override automated decisions
"""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from src.config import get_settings
from src.database.models import ComplianceViolation, DecisionLog


class ComplianceResult:
    """Result of compliance check."""

    def __init__(
        self,
        compliant: bool,
        violations: list[dict[str, Any]] | None = None,
        warnings: list[dict[str, Any]] | None = None,
    ):
        self.compliant = compliant
        self.violations = violations or []
        self.warnings = warnings or []


class Article14Monitor:
    """Monitors EU AI Act Article 14 compliance (Human Oversight).

    Rules:
    1. HIGH_RISK/PROHIBITED decisions require human review
    2. Human review rate should be ~10% for mature systems
    3. Human override rate >15% indicates quality issues
    """

    HIGH_RISK_CATEGORIES = ["HIGH_RISK", "PROHIBITED"]

    def __init__(self, db: Session):
        """Initialize monitor with database session."""
        self.db = db
        self.settings = get_settings()
        self.target_human_review_rate = self.settings.human_review_target_rate
        self.max_human_override_rate = self.settings.max_human_override_rate

    def check_decision(self, decision: DecisionLog) -> ComplianceResult:
        """Check if a single decision complies with Article 14.

        Args:
            decision: Decision log entry to check

        Returns:
            ComplianceResult with violations and warnings
        """
        violations = []
        warnings = []

        # Rule 1: Critical decisions require human oversight
        if decision.prediction in self.HIGH_RISK_CATEGORIES:
            if not decision.human_reviewed:
                violations.append(
                    {
                        "rule": "Article 14(1) - Human oversight required",
                        "severity": "HIGH",
                        "message": f"{decision.prediction} decision without human review",
                        "recommendation": "Require human approval for HIGH_RISK/PROHIBITED classifications",
                        "decision_id": decision.id,
                    }
                )

        # Rule 2: Check overall human oversight rate (for mature systems)
        days_since_first = self._get_days_since_first_decision(decision.agent_name)

        if days_since_first > 30:  # Mature system
            human_review_rate = self._calculate_human_review_rate(
                agent=decision.agent_name,
                window_days=7,
            )

            # Too much human intervention indicates agent underperformance
            if human_review_rate > (self.target_human_review_rate * 2):
                warnings.append(
                    {
                        "rule": "Article 14 - Excessive human intervention",
                        "severity": "MEDIUM",
                        "message": f"Human review rate {human_review_rate:.1%} exceeds 2x target",
                        "recommendation": "Agent may be underperforming - consider retraining",
                    }
                )

        # Rule 3: Human override rate (quality indicator)
        human_override_rate = self._calculate_human_override_rate(
            agent=decision.agent_name,
            window_days=7,
        )

        if human_override_rate > self.max_human_override_rate:
            violations.append(
                {
                    "rule": "Article 14(4)(d) - System performance",
                    "severity": "MEDIUM",
                    "message": f"Override rate {human_override_rate:.1%} indicates quality issues",
                    "recommendation": "Investigate agent degradation, consider retraining",
                }
            )

        # Log violations to database
        for violation in violations:
            self._log_violation(
                regulation="EU_AI_ACT",
                article="Article 14",
                violation_type=violation["rule"],
                severity=violation["severity"],
                description=violation["message"],
                recommendation=violation.get("recommendation"),
                related_decision_id=decision.id,
            )

        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            warnings=warnings,
        )

    def get_compliance_status(self) -> dict[str, Any]:
        """Get overall Article 14 compliance status.

        Returns:
            Status dict with compliance metrics
        """
        # Check for recent violations
        recent_violations = (
            self.db.query(ComplianceViolation)
            .filter(
                ComplianceViolation.regulation == "EU_AI_ACT",
                ComplianceViolation.article == "Article 14",
                ComplianceViolation.status == "OPEN",
                ComplianceViolation.timestamp >= datetime.utcnow() - timedelta(days=7),
            )
            .count()
        )

        # Calculate overall human oversight rate
        since = datetime.utcnow() - timedelta(days=7)
        total = (
            self.db.query(DecisionLog).filter(DecisionLog.timestamp >= since).count()
        )
        reviewed = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.timestamp >= since,
                DecisionLog.human_reviewed == True,  # noqa: E712
            )
            .count()
        )

        human_oversight_rate = reviewed / total if total > 0 else 0.0

        # High-risk decisions without review
        high_risk_unreviewed = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.timestamp >= since,
                DecisionLog.prediction.in_(self.HIGH_RISK_CATEGORIES),
                DecisionLog.human_reviewed == False,  # noqa: E712
            )
            .count()
        )

        # Determine status
        if recent_violations > 0 or high_risk_unreviewed > 0:
            status = "VIOLATION"
        elif human_oversight_rate < self.target_human_review_rate * 0.5:
            status = "WARNING"
        else:
            status = "COMPLIANT"

        return {
            "status": status,
            "article": "Article 14",
            "human_oversight_rate": human_oversight_rate,
            "target_rate": self.target_human_review_rate,
            "open_violations": recent_violations,
            "high_risk_unreviewed": high_risk_unreviewed,
            "total_decisions_7d": total,
            "reviewed_decisions_7d": reviewed,
        }

    def _calculate_human_review_rate(self, agent: str, window_days: int) -> float:
        """Calculate % of decisions that were human-reviewed."""
        since = datetime.utcnow() - timedelta(days=window_days)

        total = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent,
                DecisionLog.timestamp >= since,
            )
            .count()
        )

        reviewed = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent,
                DecisionLog.timestamp >= since,
                DecisionLog.human_reviewed == True,  # noqa: E712
            )
            .count()
        )

        return reviewed / total if total > 0 else 0.0

    def _calculate_human_override_rate(self, agent: str, window_days: int) -> float:
        """Calculate % of decisions that were overridden by humans."""
        since = datetime.utcnow() - timedelta(days=window_days)

        total = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent,
                DecisionLog.timestamp >= since,
            )
            .count()
        )

        overridden = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent,
                DecisionLog.timestamp >= since,
                DecisionLog.human_override == True,  # noqa: E712
            )
            .count()
        )

        return overridden / total if total > 0 else 0.0

    def _get_days_since_first_decision(self, agent: str) -> int:
        """Get days since first decision for agent."""
        first_decision = (
            self.db.query(DecisionLog)
            .filter(DecisionLog.agent_name == agent)
            .order_by(DecisionLog.timestamp.asc())
            .first()
        )

        if first_decision:
            delta = datetime.utcnow() - first_decision.timestamp
            return delta.days
        return 0

    def _log_violation(
        self,
        regulation: str,
        article: str,
        violation_type: str,
        severity: str,
        description: str,
        recommendation: str | None = None,
        related_decision_id: str | None = None,
    ) -> ComplianceViolation:
        """Store violation in database."""
        violation = ComplianceViolation(
            timestamp=datetime.utcnow(),
            regulation=regulation,
            article=article,
            violation_type=violation_type,
            severity=severity,
            description=description,
            recommendation=recommendation,
            related_decision_id=related_decision_id,
            status="OPEN",
        )

        self.db.add(violation)
        self.db.commit()
        return violation
