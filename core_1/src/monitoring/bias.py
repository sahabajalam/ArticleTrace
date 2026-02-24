"""Bias detection using statistical tests.

Detects when protected attributes correlate with decisions,
which may indicate discriminatory patterns.
"""

from datetime import datetime, timedelta
from typing import Any

import numpy as np
from scipy.stats import chi2_contingency
from sqlalchemy.orm import Session

from src.config import get_settings
from src.database.models import BiasReport, DecisionLog


class BiasDetector:
    """Detects bias in agent decisions using chi-square tests.

    Tests whether protected attributes (age, gender, race, etc.)
    correlate with decision outcomes.
    """

    PROTECTED_ATTRIBUTES = [
        "age",
        "age_group",
        "gender",
        "sex",
        "race",
        "ethnicity",
        "disability",
        "national_origin",
        "nationality",
        "religion",
    ]

    def __init__(self, db: Session):
        """Initialize bias detector."""
        self.db = db
        self.settings = get_settings()
        self.p_value_threshold = self.settings.bias_p_value_threshold

    def check_for_bias(self, agent_name: str, window_days: int = 30) -> dict[str, Any]:
        """Check for bias across all protected attributes.

        Args:
            agent_name: Name of agent to check
            window_days: Number of days to analyze

        Returns:
            Bias detection results
        """
        since = datetime.utcnow() - timedelta(days=window_days)

        decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= since,
            )
            .all()
        )

        if len(decisions) < 30:
            return {
                "bias_detected": False,
                "message": "Insufficient data for bias analysis",
                "decision_count": len(decisions),
            }

        # Find which protected attributes are present
        present_attributes = self._find_protected_attributes(decisions)

        if not present_attributes:
            return {
                "bias_detected": False,
                "message": "No protected attributes found in decision inputs",
                "decision_count": len(decisions),
            }

        # Test each attribute
        bias_results = []
        for attr in present_attributes:
            result = self._test_attribute_bias(decisions, attr)
            if result["bias_detected"]:
                bias_results.append(result)

                # Log to database
                self._log_bias_report(
                    agent_name=agent_name,
                    bias_detected=True,
                    protected_attribute=attr,
                    p_value=result["p_value"],
                    chi_square=result["chi_square"],
                    contingency_table=result.get("contingency_table"),
                )

        return {
            "bias_detected": len(bias_results) > 0,
            "biased_attributes": bias_results,
            "tested_attributes": present_attributes,
            "decision_count": len(decisions),
            "window_days": window_days,
        }

    def check_single_decision(self, decision: DecisionLog) -> dict[str, Any]:
        """Check if a single decision may involve protected attributes.

        This is a quick check - full bias analysis requires batch data.

        Args:
            decision: Decision to check

        Returns:
            Warning if protected attributes are present
        """
        input_data = decision.input_data or {}
        protected_found = []

        for attr in self.PROTECTED_ATTRIBUTES:
            if attr in input_data:
                protected_found.append(attr)
            if isinstance(input_data.get("protected_attributes"), dict):
                if attr in input_data["protected_attributes"]:
                    protected_found.append(attr)

        return {
            "protected_attributes_present": len(protected_found) > 0,
            "attributes": protected_found,
            "warning": (
                f"Protected attributes in input: {protected_found}"
                if protected_found
                else None
            ),
        }

    def _find_protected_attributes(
        self, decisions: list[DecisionLog]
    ) -> list[str]:
        """Find which protected attributes are present in decisions."""
        found_attrs: set[str] = set()

        for decision in decisions:
            input_data = decision.input_data or {}

            for attr in self.PROTECTED_ATTRIBUTES:
                if attr in input_data:
                    found_attrs.add(attr)

                # Check nested protected_attributes dict
                if isinstance(input_data.get("protected_attributes"), dict):
                    if attr in input_data["protected_attributes"]:
                        found_attrs.add(attr)

        return list(found_attrs)

    def _test_attribute_bias(
        self, decisions: list[DecisionLog], attribute: str
    ) -> dict[str, Any]:
        """Test if a specific attribute correlates with predictions.

        Uses chi-square test of independence.

        Args:
            decisions: List of decisions
            attribute: Protected attribute to test

        Returns:
            Test results
        """
        # Build contingency table
        attr_values: dict[str, dict[str, int]] = {}

        for d in decisions:
            input_data = d.input_data or {}

            # Get attribute value
            attr_value = input_data.get(attribute)
            if attr_value is None:
                nested = input_data.get("protected_attributes", {})
                attr_value = nested.get(attribute) if isinstance(nested, dict) else None

            if attr_value is None:
                continue

            # Convert to string for grouping
            attr_value = str(attr_value)

            if attr_value not in attr_values:
                attr_values[attr_value] = {}

            prediction = d.prediction
            attr_values[attr_value][prediction] = (
                attr_values[attr_value].get(prediction, 0) + 1
            )

        if len(attr_values) < 2:
            return {
                "bias_detected": False,
                "message": f"Insufficient variation in {attribute}",
            }

        # Build numpy contingency table
        all_predictions = set()
        for counts in attr_values.values():
            all_predictions.update(counts.keys())

        all_predictions = sorted(all_predictions)
        attr_keys = sorted(attr_values.keys())

        table = np.zeros((len(attr_keys), len(all_predictions)))
        for i, attr_key in enumerate(attr_keys):
            for j, pred in enumerate(all_predictions):
                table[i, j] = attr_values[attr_key].get(pred, 0)

        # Run chi-square test
        try:
            chi2, p_value, dof, expected = chi2_contingency(table)

            bias_detected = p_value < self.p_value_threshold

            return {
                "attribute": attribute,
                "bias_detected": bias_detected,
                "chi_square": float(chi2),
                "p_value": float(p_value),
                "degrees_of_freedom": int(dof),
                "threshold": self.p_value_threshold,
                "contingency_table": {
                    "rows": attr_keys,
                    "columns": list(all_predictions),
                    "values": table.tolist(),
                },
                "severity": "CRITICAL" if p_value < 0.01 else "HIGH",
            }

        except ValueError as e:
            return {
                "attribute": attribute,
                "bias_detected": False,
                "error": str(e),
            }

    def get_bias_summary(self, agent_name: str) -> dict[str, Any]:
        """Get summary of bias reports for an agent.

        Args:
            agent_name: Agent to summarize

        Returns:
            Summary of bias detection history
        """
        reports = (
            self.db.query(BiasReport)
            .filter(BiasReport.agent_name == agent_name)
            .order_by(BiasReport.timestamp.desc())
            .limit(100)
            .all()
        )

        bias_detected_count = sum(1 for r in reports if r.bias_detected)
        biased_attributes = list(
            set(r.protected_attribute for r in reports if r.bias_detected)
        )

        return {
            "total_reports": len(reports),
            "bias_detected_count": bias_detected_count,
            "biased_attributes": biased_attributes,
            "latest_report": reports[0].timestamp.isoformat() if reports else None,
        }

    def _log_bias_report(
        self,
        agent_name: str,
        bias_detected: bool,
        protected_attribute: str,
        p_value: float,
        chi_square: float,
        contingency_table: dict[str, Any] | None = None,
    ) -> BiasReport:
        """Store bias report in database."""
        report = BiasReport(
            timestamp=datetime.utcnow(),
            agent_name=agent_name,
            bias_detected=bias_detected,
            protected_attribute=protected_attribute,
            p_value=p_value,
            chi_square_statistic=chi_square,
            contingency_table=contingency_table,
        )

        self.db.add(report)
        self.db.commit()
        return report
