"""Drift detection using Evidently.

Detects when agent performance degrades through:
1. Data Drift - input distribution changes
2. Prediction Drift - output distribution changes
3. Concept Drift - input-output relationship changes
"""

from datetime import datetime, timedelta
from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from src.config import get_settings
from src.database.models import DecisionLog, DriftReport


class DriftDetector:
    """Detects drift in agent decisions using Evidently.

    Types of drift:
    - Data drift: Input feature distributions change
    - Prediction drift: Output distributions change
    - Concept drift: Relationship between input/output changes
    """

    def __init__(self, db: Session):
        """Initialize drift detector."""
        self.db = db
        self.settings = get_settings()
        self.drift_threshold = self.settings.drift_threshold

    def check_data_drift(self, agent_name: str) -> dict[str, Any]:
        """Check if input data distribution has changed.

        Compares baseline (first 2 weeks) with current (last 7 days).

        Args:
            agent_name: Name of the agent to check

        Returns:
            Drift detection results
        """
        # Load baseline data
        baseline_df = self._load_baseline_data(agent_name)

        # Load current data
        current_df = self._load_current_data(agent_name, window_days=7)

        if len(baseline_df) < 50 or len(current_df) < 20:
            return {
                "drift_detected": False,
                "message": "Insufficient data for drift detection",
                "baseline_count": len(baseline_df),
                "current_count": len(current_df),
            }

        try:
            # Use Evidently for drift detection
            from evidently.metrics import DatasetDriftMetric
            from evidently.report import Report

            report = Report(metrics=[DatasetDriftMetric()])
            report.run(reference_data=baseline_df, current_data=current_df)

            results = report.as_dict()
            drift_result = results["metrics"][0]["result"]
            drift_score = drift_result.get("drift_share", 0)
            drift_detected = drift_score > self.drift_threshold

            # Store report
            self._log_drift_report(
                agent_name=agent_name,
                drift_detected=drift_detected,
                drift_score=drift_score,
                drift_type="data",
                report_data=results,
            )

            return {
                "drift_detected": drift_detected,
                "drift_score": drift_score,
                "threshold": self.drift_threshold,
                "baseline_count": len(baseline_df),
                "current_count": len(current_df),
                "drifted_features": drift_result.get("drifted_columns", []),
            }

        except Exception as e:
            return {
                "drift_detected": False,
                "error": str(e),
                "message": "Drift detection failed",
            }

    def check_prediction_drift(self, agent_name: str) -> dict[str, Any]:
        """Check if prediction distribution has changed.

        Args:
            agent_name: Name of the agent to check

        Returns:
            Prediction drift results
        """
        since_baseline = self._get_baseline_end_date(agent_name)
        since_current = datetime.utcnow() - timedelta(days=7)

        # Get baseline prediction distribution
        baseline_preds = self._get_prediction_distribution(
            agent_name,
            start_date=since_baseline - timedelta(days=14),
            end_date=since_baseline,
        )

        # Get current prediction distribution
        current_preds = self._get_prediction_distribution(
            agent_name,
            start_date=since_current,
            end_date=datetime.utcnow(),
        )

        if not baseline_preds or not current_preds:
            return {
                "drift_detected": False,
                "message": "Insufficient prediction data",
            }

        # Calculate distribution shift using chi-square
        from scipy.stats import chisquare

        # Align categories
        all_categories = set(baseline_preds.keys()) | set(current_preds.keys())
        baseline_counts = [baseline_preds.get(c, 0) for c in all_categories]
        current_counts = [current_preds.get(c, 0) for c in all_categories]

        # Add smoothing to avoid division by zero
        baseline_counts = [c + 1 for c in baseline_counts]
        current_counts = [c + 1 for c in current_counts]

        # Normalize to same total
        total_baseline = sum(baseline_counts)
        total_current = sum(current_counts)
        expected = [c * total_current / total_baseline for c in baseline_counts]

        chi2, p_value = chisquare(current_counts, f_exp=expected)

        drift_detected = p_value < 0.05  # Significant distribution change

        self._log_drift_report(
            agent_name=agent_name,
            drift_detected=drift_detected,
            drift_score=1 - p_value,
            drift_type="prediction",
            report_data={
                "chi2": chi2,
                "p_value": p_value,
                "baseline_distribution": baseline_preds,
                "current_distribution": current_preds,
            },
        )

        return {
            "drift_detected": drift_detected,
            "chi_square": chi2,
            "p_value": p_value,
            "baseline_distribution": baseline_preds,
            "current_distribution": current_preds,
        }

    def check_confidence_drift(self, agent_name: str) -> dict[str, Any]:
        """Check if confidence scores have drifted.

        A drop in confidence may indicate model uncertainty.

        Args:
            agent_name: Name of the agent

        Returns:
            Confidence drift results
        """
        since_baseline = self._get_baseline_end_date(agent_name)
        since_current = datetime.utcnow() - timedelta(days=7)

        # Get baseline confidence stats
        baseline_decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= since_baseline - timedelta(days=14),
                DecisionLog.timestamp < since_baseline,
            )
            .all()
        )

        current_decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= since_current,
            )
            .all()
        )

        if len(baseline_decisions) < 20 or len(current_decisions) < 10:
            return {
                "drift_detected": False,
                "message": "Insufficient data",
            }

        baseline_conf = [d.confidence for d in baseline_decisions]
        current_conf = [d.confidence for d in current_decisions]

        import numpy as np

        baseline_mean = np.mean(baseline_conf)
        current_mean = np.mean(current_conf)
        baseline_std = np.std(baseline_conf)

        # Significant drop if current mean is more than 2 std below baseline
        confidence_drop = baseline_mean - current_mean
        drift_detected = confidence_drop > (2 * baseline_std)

        return {
            "drift_detected": drift_detected,
            "baseline_mean_confidence": baseline_mean,
            "current_mean_confidence": current_mean,
            "confidence_drop": confidence_drop,
            "baseline_std": baseline_std,
        }

    def _load_baseline_data(self, agent_name: str) -> pd.DataFrame:
        """Load first 2 weeks of decisions as baseline."""
        first_decision = (
            self.db.query(DecisionLog)
            .filter(DecisionLog.agent_name == agent_name)
            .order_by(DecisionLog.timestamp.asc())
            .first()
        )

        if not first_decision:
            return pd.DataFrame()

        baseline_start = first_decision.timestamp
        baseline_end = baseline_start + timedelta(days=14)

        decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= baseline_start,
                DecisionLog.timestamp <= baseline_end,
            )
            .all()
        )

        return self._decisions_to_dataframe(decisions)

    def _load_current_data(self, agent_name: str, window_days: int) -> pd.DataFrame:
        """Load recent decisions."""
        since = datetime.utcnow() - timedelta(days=window_days)

        decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= since,
            )
            .all()
        )

        return self._decisions_to_dataframe(decisions)

    def _decisions_to_dataframe(self, decisions: list[DecisionLog]) -> pd.DataFrame:
        """Convert decisions to DataFrame for Evidently."""
        records = []
        for d in decisions:
            record = {
                "confidence": d.confidence,
                "prediction": d.prediction,
            }
            # Flatten input data
            if d.input_data:
                for k, v in d.input_data.items():
                    if isinstance(v, (int, float, str, bool)):
                        record[f"input_{k}"] = v
            records.append(record)

        return pd.DataFrame(records)

    def _get_baseline_end_date(self, agent_name: str) -> datetime:
        """Get end date of baseline period."""
        first_decision = (
            self.db.query(DecisionLog)
            .filter(DecisionLog.agent_name == agent_name)
            .order_by(DecisionLog.timestamp.asc())
            .first()
        )

        if first_decision:
            return first_decision.timestamp + timedelta(days=14)
        return datetime.utcnow() - timedelta(days=30)

    def _get_prediction_distribution(
        self,
        agent_name: str,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, int]:
        """Get prediction counts by category."""
        decisions = (
            self.db.query(DecisionLog)
            .filter(
                DecisionLog.agent_name == agent_name,
                DecisionLog.timestamp >= start_date,
                DecisionLog.timestamp < end_date,
            )
            .all()
        )

        distribution: dict[str, int] = {}
        for d in decisions:
            distribution[d.prediction] = distribution.get(d.prediction, 0) + 1

        return distribution

    def _log_drift_report(
        self,
        agent_name: str,
        drift_detected: bool,
        drift_score: float,
        drift_type: str,
        report_data: dict[str, Any],
    ) -> DriftReport:
        """Store drift report in database."""
        report = DriftReport(
            timestamp=datetime.utcnow(),
            agent_name=agent_name,
            drift_detected=drift_detected,
            drift_score=drift_score,
            drift_type=drift_type,
            report_data=report_data,
        )

        self.db.add(report)
        self.db.commit()
        return report
