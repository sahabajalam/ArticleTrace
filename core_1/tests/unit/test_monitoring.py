"""Tests for drift and bias detection."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from src.monitoring.bias import BiasDetector
from src.monitoring.drift import DriftDetector
from src.database.models import DecisionLog


class TestBiasDetector:
    """Test bias detection."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return MagicMock()

    @pytest.fixture
    def detector(self, mock_db):
        """Create detector instance."""
        return BiasDetector(mock_db)

    def test_no_protected_attributes(self, detector):
        """Test no bias when no protected attributes present."""
        decision = DecisionLog(
            id="test-001",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            input_data={"system_type": "chatbot"},
        )

        result = detector.check_single_decision(decision)

        assert not result["protected_attributes_present"]
        assert len(result["attributes"]) == 0

    def test_detects_protected_attributes(self, detector):
        """Test detection of protected attributes."""
        decision = DecisionLog(
            id="test-002",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            input_data={
                "system_type": "hr_tool",
                "gender": "male",
                "age": 35,
            },
        )

        result = detector.check_single_decision(decision)

        assert result["protected_attributes_present"]
        assert "gender" in result["attributes"]
        assert "age" in result["attributes"]

    def test_detects_nested_protected_attributes(self, detector):
        """Test detection of nested protected attributes."""
        decision = DecisionLog(
            id="test-003",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            input_data={
                "system_type": "hr_tool",
                "protected_attributes": {"ethnicity": "asian"},
            },
        )

        result = detector.check_single_decision(decision)

        assert result["protected_attributes_present"]
        assert "ethnicity" in result["attributes"]


class TestChiSquareCalculation:
    """Test chi-square bias calculation."""

    def test_contingency_table_creation(self):
        """Test contingency table is created correctly."""
        # Simulated data showing bias
        # Male: 80% HIGH_RISK, 20% LOW_RISK
        # Female: 40% HIGH_RISK, 60% LOW_RISK

        from scipy.stats import chi2_contingency

        # Contingency table:
        #            HIGH_RISK  LOW_RISK
        # Male          80        20
        # Female        40        60
        table = np.array([[80, 20], [40, 60]])

        chi2, p_value, dof, expected = chi2_contingency(table)

        # Should detect significant difference
        assert p_value < 0.05  # Statistically significant
        assert chi2 > 10  # Strong association

    def test_no_bias_in_balanced_data(self):
        """Test no bias detected in balanced data."""
        from scipy.stats import chi2_contingency

        # Balanced table:
        #            HIGH_RISK  LOW_RISK
        # Male          50        50
        # Female        50        50
        table = np.array([[50, 50], [50, 50]])

        chi2, p_value, dof, expected = chi2_contingency(table)

        # Should not detect significant difference
        assert p_value > 0.05  # Not statistically significant


class TestProtectedAttributes:
    """Test protected attribute handling."""

    def test_all_protected_attributes_defined(self):
        """Test all expected protected attributes are in list."""
        from src.monitoring.bias import BiasDetector

        expected = ["age", "gender", "race", "ethnicity", "disability"]

        for attr in expected:
            assert attr in BiasDetector.PROTECTED_ATTRIBUTES

    def test_gdpr_special_categories(self):
        """Test GDPR special categories are handled."""
        from src.compliance.gdpr import GDPRMonitor

        expected = [
            "race",
            "ethnicity",
            "political_opinions",
            "religious_beliefs",
            "genetic_data",
            "biometric_data",
            "health_data",
        ]

        for attr in expected:
            assert attr in GDPRMonitor.SPECIAL_CATEGORY_ATTRIBUTES


class TestDriftDetector:
    """Tests for DriftDetector class."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return MagicMock()

    @pytest.fixture
    def detector(self, mock_db):
        """Create detector instance."""
        return DriftDetector(mock_db)

    def test_initialization(self, detector):
        """Test DriftDetector initializes correctly."""
        assert detector.db is not None
        assert detector.drift_threshold > 0

    def test_check_data_drift_insufficient_data(self, detector, mock_db):
        """Test data drift check with insufficient data."""
        # Mock query to return empty list
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        result = detector.check_data_drift("test_agent")

        assert result["drift_detected"] is False
        assert "Insufficient data" in result.get("message", "")

    def test_check_data_drift_baseline_too_small(self, detector, mock_db):
        """Test data drift when baseline is too small."""
        # Mock first decision
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision

        # Mock baseline decisions (less than 50)
        mock_query.filter.return_value.all.return_value = [
            MagicMock(confidence=0.9, prediction="HIGH_RISK", input_data={})
            for _ in range(20)
        ]

        result = detector.check_data_drift("test_agent")

        assert result["drift_detected"] is False
        assert result["baseline_count"] < 50

    def test_decisions_to_dataframe(self, detector):
        """Test conversion of decisions to DataFrame."""
        decisions = [
            MagicMock(
                confidence=0.85,
                prediction="HIGH_RISK",
                input_data={"system_type": "chatbot", "score": 0.7},
            ),
            MagicMock(
                confidence=0.92,
                prediction="LOW_RISK",
                input_data={"system_type": "api", "score": 0.3},
            ),
        ]

        df = detector._decisions_to_dataframe(decisions)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "confidence" in df.columns
        assert "prediction" in df.columns
        assert "input_system_type" in df.columns
        assert "input_score" in df.columns

    def test_decisions_to_dataframe_handles_complex_input(self, detector):
        """Test DataFrame conversion handles complex input data."""
        decisions = [
            MagicMock(
                confidence=0.85,
                prediction="HIGH_RISK",
                input_data={
                    "simple_value": 42,
                    "nested_dict": {"key": "value"},  # Should be skipped
                    "list_value": [1, 2, 3],  # Should be skipped
                    "string_value": "test",
                },
            ),
        ]

        df = detector._decisions_to_dataframe(decisions)

        assert "input_simple_value" in df.columns
        assert "input_string_value" in df.columns
        assert "input_nested_dict" not in df.columns
        assert "input_list_value" not in df.columns

    def test_check_prediction_drift_insufficient_data(self, detector, mock_db):
        """Test prediction drift with insufficient data."""
        # Mock first decision for baseline
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision
        mock_query.filter.return_value.all.return_value = []

        result = detector.check_prediction_drift("test_agent")

        assert result["drift_detected"] is False
        assert "Insufficient" in result.get("message", "")

    def test_get_prediction_distribution(self, detector, mock_db):
        """Test prediction distribution calculation."""
        decisions = [
            MagicMock(prediction="HIGH_RISK"),
            MagicMock(prediction="HIGH_RISK"),
            MagicMock(prediction="LOW_RISK"),
            MagicMock(prediction="MINIMAL_RISK"),
        ]

        mock_db.query.return_value.filter.return_value.all.return_value = decisions

        distribution = detector._get_prediction_distribution(
            "test_agent",
            datetime.utcnow() - timedelta(days=7),
            datetime.utcnow(),
        )

        assert distribution["HIGH_RISK"] == 2
        assert distribution["LOW_RISK"] == 1
        assert distribution["MINIMAL_RISK"] == 1

    def test_check_confidence_drift_insufficient_data(self, detector, mock_db):
        """Test confidence drift with insufficient data."""
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision
        mock_query.filter.return_value.all.return_value = []

        result = detector.check_confidence_drift("test_agent")

        assert result["drift_detected"] is False
        assert "Insufficient" in result.get("message", "")

    def test_check_confidence_drift_no_drop(self, detector, mock_db):
        """Test confidence drift when no significant drop."""
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        # Baseline decisions with confidence around 0.9
        baseline_decisions = [
            MagicMock(confidence=0.88 + i * 0.01) for i in range(25)
        ]

        # Current decisions with similar confidence
        current_decisions = [
            MagicMock(confidence=0.87 + i * 0.01) for i in range(15)
        ]

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision

        # Mock different return values for different filter calls
        call_count = [0]
        def mock_all():
            call_count[0] += 1
            if call_count[0] == 1:
                return baseline_decisions
            return current_decisions

        mock_query.filter.return_value.all = mock_all

        result = detector.check_confidence_drift("test_agent")

        assert result["drift_detected"] is False
        assert "baseline_mean_confidence" in result

    def test_check_confidence_drift_significant_drop(self, detector, mock_db):
        """Test confidence drift when significant drop detected."""
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        # Baseline decisions with high confidence
        baseline_decisions = [
            MagicMock(confidence=0.95) for _ in range(25)
        ]

        # Current decisions with much lower confidence
        current_decisions = [
            MagicMock(confidence=0.60) for _ in range(15)
        ]

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision

        call_count = [0]
        def mock_all():
            call_count[0] += 1
            if call_count[0] == 1:
                return baseline_decisions
            return current_decisions

        mock_query.filter.return_value.all = mock_all

        result = detector.check_confidence_drift("test_agent")

        assert result["drift_detected"] is True
        assert result["confidence_drop"] > 0.2

    def test_get_baseline_end_date_with_decisions(self, detector, mock_db):
        """Test baseline end date calculation with existing decisions."""
        first_decision = MagicMock()
        first_decision.timestamp = datetime(2024, 1, 1, 0, 0, 0)

        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = first_decision

        end_date = detector._get_baseline_end_date("test_agent")

        expected = datetime(2024, 1, 15, 0, 0, 0)  # 14 days after first
        assert end_date == expected

    def test_get_baseline_end_date_no_decisions(self, detector, mock_db):
        """Test baseline end date when no decisions exist."""
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        end_date = detector._get_baseline_end_date("test_agent")

        # Should return 30 days ago
        expected = datetime.utcnow() - timedelta(days=30)
        assert abs((end_date - expected).total_seconds()) < 60  # Within a minute

    def test_log_drift_report(self, detector, mock_db):
        """Test drift report logging."""
        report = detector._log_drift_report(
            agent_name="test_agent",
            drift_detected=True,
            drift_score=0.75,
            drift_type="data",
            report_data={"details": "test"},
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


class TestDriftDetectorIntegration:
    """Integration tests for DriftDetector with mocked Evidently."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return MagicMock()

    @pytest.fixture
    def detector(self, mock_db):
        """Create detector instance."""
        return DriftDetector(mock_db)

    def test_check_data_drift_with_evidently(self, detector, mock_db):
        """Test data drift detection using Evidently."""
        first_decision = MagicMock()
        first_decision.timestamp = datetime.utcnow() - timedelta(days=30)

        # Create enough baseline and current decisions
        baseline_decisions = [
            MagicMock(
                confidence=0.9,
                prediction="HIGH_RISK",
                input_data={"score": 0.8},
            )
            for _ in range(60)
        ]

        current_decisions = [
            MagicMock(
                confidence=0.85,
                prediction="HIGH_RISK",
                input_data={"score": 0.75},
            )
            for _ in range(30)
        ]

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value.order_by.return_value.first.return_value = first_decision

        call_count = [0]
        def mock_all():
            call_count[0] += 1
            if call_count[0] <= 2:  # Baseline calls
                return baseline_decisions
            return current_decisions

        mock_query.filter.return_value.all = mock_all

        # Mock Evidently report
        with patch("src.monitoring.drift.Report") as MockReport:
            mock_report = MagicMock()
            mock_report.as_dict.return_value = {
                "metrics": [
                    {
                        "result": {
                            "drift_share": 0.05,
                            "drifted_columns": [],
                        }
                    }
                ]
            }
            MockReport.return_value = mock_report

            result = detector.check_data_drift("test_agent")

            assert "drift_detected" in result
            assert "drift_score" in result
            assert "threshold" in result


class TestPredictionDriftStatistics:
    """Tests for prediction drift statistical calculations."""

    def test_chi_square_detects_shift(self):
        """Test chi-square detects distribution shift."""
        from scipy.stats import chisquare

        # Baseline: mostly HIGH_RISK
        baseline = [80, 20]  # HIGH_RISK, LOW_RISK

        # Current: shifted to LOW_RISK
        current = [30, 70]

        # Normalize
        total_baseline = sum(baseline)
        total_current = sum(current)
        expected = [b * total_current / total_baseline for b in baseline]

        chi2, p_value = chisquare(current, f_exp=expected)

        assert p_value < 0.05  # Significant shift detected

    def test_chi_square_no_shift(self):
        """Test chi-square does not detect shift in similar distributions."""
        from scipy.stats import chisquare

        # Similar distributions
        baseline = [50, 50]
        current = [52, 48]

        total_baseline = sum(baseline)
        total_current = sum(current)
        expected = [b * total_current / total_baseline for b in baseline]

        chi2, p_value = chisquare(current, f_exp=expected)

        assert p_value > 0.05  # No significant shift
