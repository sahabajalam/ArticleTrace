"""GDPR compliance monitoring.

Monitors Article 22 (Automated Decision-Making) requirements.

Article 22 Requirements:
1. Right not to be subject to solely automated decisions
2. Right to human intervention
3. Right to contest decisions
4. Special category data requires explicit consent (Article 9)
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


class GDPRMonitor:
    """Monitors GDPR Article 22 compliance (Automated Decision-Making).

    Rules:
    1. Users must be informed of automated decision-making
    2. Human intervention must be available
    3. Special category data (Article 9) requires consent
    """

    SPECIAL_CATEGORY_ATTRIBUTES = [
        "race",
        "ethnicity",
        "political_opinions",
        "religious_beliefs",
        "trade_union_membership",
        "genetic_data",
        "biometric_data",
        "health_data",
        "sex_life",
        "sexual_orientation",
    ]

    PROTECTED_ATTRIBUTES = [
        "age",
        "gender",
        "race",
        "ethnicity",
        "disability",
        "national_origin",
        "religion",
    ]

    def __init__(self, db: Session):
        """Initialize monitor with database session."""
        self.db = db
        self.settings = get_settings()

    def check_decision(self, decision: DecisionLog) -> ComplianceResult:
        """Check if a decision complies with GDPR Article 22.

        Args:
            decision: Decision log entry to check

        Returns:
            ComplianceResult with violations and warnings
        """
        violations = []
        warnings = []

        metadata = decision.metadata or {}
        input_data = decision.input_data or {}

        # Rule 1: Transparency - user informed of automated decision?
        if not metadata.get("user_informed", False):
            violations.append(
                {
                    "rule": "GDPR Article 22(1) - Transparency",
                    "severity": "HIGH",
                    "message": "User not informed of automated decision",
                    "recommendation": "Add transparency notice explaining automated processing",
                }
            )

        # Rule 2: Human intervention available?
        if not metadata.get("human_intervention_available", True):
            violations.append(
                {
                    "rule": "GDPR Article 22(3) - Right to intervention",
                    "severity": "CRITICAL",
                    "message": "No human review mechanism available",
                    "recommendation": "Implement appeal/review process for decisions",
                }
            )

        # Rule 3: Special category data (Article 9)
        special_data_used = self._check_special_category_data(input_data)

        if special_data_used:
            has_consent = metadata.get("explicit_consent", False)
            has_legal_basis = metadata.get("article_9_exception", None)

            if not (has_consent or has_legal_basis):
                violations.append(
                    {
                        "rule": "GDPR Article 9 - Special category data",
                        "severity": "CRITICAL",
                        "message": f"Processing special category data without legal basis: {special_data_used}",
                        "recommendation": "Obtain explicit consent or identify Article 9(2) exception",
                    }
                )

        # Rule 4: Protected attributes in decision (potential bias)
        protected_attrs = self._check_protected_attributes(input_data)
        if protected_attrs:
            warnings.append(
                {
                    "rule": "GDPR Article 22(4) - Fairness",
                    "severity": "MEDIUM",
                    "message": f"Protected attributes in decision input: {protected_attrs}",
                    "recommendation": "Review if attributes are necessary and non-discriminatory",
                }
            )

        # Rule 5: Significant decision without safeguards
        is_significant = metadata.get("significant_decision", False)
        if is_significant and not decision.human_reviewed:
            violations.append(
                {
                    "rule": "GDPR Article 22(1) - Significant decisions",
                    "severity": "HIGH",
                    "message": "Significant decision made without human involvement",
                    "recommendation": "Require human review for decisions with legal/significant effects",
                }
            )

        # Log violations
        for violation in violations:
            self._log_violation(
                regulation="GDPR",
                article="Article 22",
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
        """Get overall GDPR Article 22 compliance status.

        Returns:
            Status dict with compliance metrics
        """
        # Check for recent violations
        recent_violations = (
            self.db.query(ComplianceViolation)
            .filter(
                ComplianceViolation.regulation == "GDPR",
                ComplianceViolation.article == "Article 22",
                ComplianceViolation.status == "OPEN",
                ComplianceViolation.timestamp >= datetime.utcnow() - timedelta(days=7),
            )
            .count()
        )

        # Count critical violations
        critical_violations = (
            self.db.query(ComplianceViolation)
            .filter(
                ComplianceViolation.regulation == "GDPR",
                ComplianceViolation.status == "OPEN",
                ComplianceViolation.severity == "CRITICAL",
                ComplianceViolation.timestamp >= datetime.utcnow() - timedelta(days=7),
            )
            .count()
        )

        # Calculate transparency rate (decisions where user was informed)
        since = datetime.utcnow() - timedelta(days=7)
        total = (
            self.db.query(DecisionLog).filter(DecisionLog.timestamp >= since).count()
        )

        # Note: This checks metadata['user_informed'] - needs JSON query
        # Simplified: count all with metadata
        informed_count = 0  # Would need JSON query for actual count

        # Determine status
        if critical_violations > 0:
            status = "VIOLATION"
        elif recent_violations > 0:
            status = "WARNING"
        else:
            status = "COMPLIANT"

        return {
            "status": status,
            "article": "Article 22",
            "open_violations": recent_violations,
            "critical_violations": critical_violations,
            "total_decisions_7d": total,
        }

    def _check_special_category_data(self, input_data: dict[str, Any]) -> list[str]:
        """Check if input contains special category data."""
        found = []
        for attr in self.SPECIAL_CATEGORY_ATTRIBUTES:
            if attr in input_data:
                found.append(attr)
            # Also check nested
            if isinstance(input_data.get("protected_attributes"), dict):
                if attr in input_data["protected_attributes"]:
                    found.append(attr)
        return found

    def _check_protected_attributes(self, input_data: dict[str, Any]) -> list[str]:
        """Check if input contains protected attributes."""
        found = []
        for attr in self.PROTECTED_ATTRIBUTES:
            if attr in input_data:
                found.append(attr)
            if isinstance(input_data.get("protected_attributes"), dict):
                if attr in input_data["protected_attributes"]:
                    found.append(attr)
        return found

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
