"""Alert management and routing system.

Routes alerts to appropriate channels based on severity:
- CRITICAL/HIGH: Slack + Email
- MEDIUM: Slack only
- LOW: Dashboard only
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Any

import httpx
from sqlalchemy.orm import Session

from src.config import get_settings
from src.database.models import AlertLog


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Alert:
    """Alert data structure."""

    def __init__(
        self,
        alert_type: str,
        severity: AlertSeverity,
        title: str,
        message: str,
        action_required: str | None = None,
        related_violation_id: str | None = None,
        related_decision_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self.alert_type = alert_type
        self.severity = severity
        self.title = title
        self.message = message
        self.action_required = action_required
        self.related_violation_id = related_violation_id
        self.related_decision_id = related_decision_id
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()


class AlertManager:
    """Manages alert routing and delivery."""

    # Routing rules: severity -> channels
    ROUTING = {
        AlertSeverity.CRITICAL: ["slack", "email"],
        AlertSeverity.HIGH: ["slack", "email"],
        AlertSeverity.MEDIUM: ["slack"],
        AlertSeverity.LOW: ["dashboard"],
    }

    # Slack color by severity
    SLACK_COLORS = {
        AlertSeverity.CRITICAL: "#FF0000",  # Red
        AlertSeverity.HIGH: "#FFA500",  # Orange
        AlertSeverity.MEDIUM: "#FFFF00",  # Yellow
        AlertSeverity.LOW: "#00FF00",  # Green
    }

    # Emoji by alert type
    ALERT_EMOJI = {
        "COMPLIANCE_VIOLATION": "🚨",
        "DATA_DRIFT": "📊",
        "PREDICTION_DRIFT": "📈",
        "BIAS_DETECTED": "⚖️",
        "PERFORMANCE_DEGRADATION": "⚡",
        "SYSTEM_ERROR": "❌",
    }

    def __init__(self, db: Session):
        """Initialize alert manager."""
        self.db = db
        self.settings = get_settings()

    def send_alert(self, alert: Alert) -> dict[str, Any]:
        """Send alert to appropriate channels.

        Args:
            alert: Alert to send

        Returns:
            Delivery results
        """
        channels = self.ROUTING.get(alert.severity, ["dashboard"])
        results: dict[str, Any] = {
            "channels": channels,
            "sent": [],
            "failed": [],
        }

        # Log alert to database
        alert_log = self._log_alert(alert, channels)

        # Send to each channel
        for channel in channels:
            try:
                if channel == "slack" and self.settings.slack_webhook_url:
                    self._send_slack(alert)
                    results["sent"].append("slack")
                elif channel == "email" and self.settings.smtp_host:
                    self._send_email(alert)
                    results["sent"].append("email")
                elif channel == "dashboard":
                    # Dashboard alerts are just logged
                    results["sent"].append("dashboard")
            except Exception as e:
                results["failed"].append({"channel": channel, "error": str(e)})

        # Update alert log with results
        alert_log.sent_successfully = len(results["failed"]) == 0
        if results["failed"]:
            alert_log.send_error = str(results["failed"])
        self.db.commit()

        return results

    def send_compliance_violation_alert(
        self,
        regulation: str,
        article: str,
        severity: str,
        description: str,
        recommendation: str | None = None,
        related_decision_id: str | None = None,
    ) -> dict[str, Any]:
        """Send alert for compliance violation.

        Args:
            regulation: EU_AI_ACT or GDPR
            article: Article number
            severity: Alert severity
            description: Violation description
            recommendation: Recommended action
            related_decision_id: Related decision ID

        Returns:
            Delivery results
        """
        alert = Alert(
            alert_type="COMPLIANCE_VIOLATION",
            severity=AlertSeverity(severity),
            title=f"{regulation} {article} Violation",
            message=description,
            action_required=recommendation,
            related_decision_id=related_decision_id,
            metadata={"regulation": regulation, "article": article},
        )

        return self.send_alert(alert)

    def send_drift_alert(
        self,
        agent_name: str,
        drift_type: str,
        drift_score: float,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send alert for detected drift.

        Args:
            agent_name: Name of agent
            drift_type: Type of drift (data, prediction, confidence)
            drift_score: Drift score
            details: Additional details

        Returns:
            Delivery results
        """
        alert = Alert(
            alert_type="DATA_DRIFT" if drift_type == "data" else "PREDICTION_DRIFT",
            severity=AlertSeverity.HIGH,
            title=f"Drift Detected: {agent_name}",
            message=f"{drift_type.capitalize()} drift detected with score {drift_score:.2%}",
            action_required="Review agent performance and consider retraining",
            metadata={
                "agent_name": agent_name,
                "drift_type": drift_type,
                "drift_score": drift_score,
                **(details or {}),
            },
        )

        return self.send_alert(alert)

    def send_bias_alert(
        self,
        agent_name: str,
        attribute: str,
        p_value: float,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send alert for detected bias.

        Args:
            agent_name: Name of agent
            attribute: Protected attribute with bias
            p_value: Statistical p-value
            details: Additional details

        Returns:
            Delivery results
        """
        alert = Alert(
            alert_type="BIAS_DETECTED",
            severity=AlertSeverity.CRITICAL,
            title=f"Bias Detected: {agent_name}",
            message=f"Protected attribute '{attribute}' correlates with decisions (p={p_value:.4f})",
            action_required="Review model for discriminatory patterns, consider removing attribute",
            metadata={
                "agent_name": agent_name,
                "attribute": attribute,
                "p_value": p_value,
                **(details or {}),
            },
        )

        return self.send_alert(alert)

    def _send_slack(self, alert: Alert) -> None:
        """Send alert to Slack webhook."""
        if not self.settings.slack_webhook_url:
            return

        emoji = self.ALERT_EMOJI.get(alert.alert_type, "⚠️")
        color = self.SLACK_COLORS.get(alert.severity, "#808080")

        payload = {
            "channel": self.settings.slack_channel,
            "attachments": [
                {
                    "color": color,
                    "title": f"{emoji} {alert.title}",
                    "text": alert.message,
                    "fields": [
                        {
                            "title": "Severity",
                            "value": alert.severity.value,
                            "short": True,
                        },
                        {
                            "title": "Type",
                            "value": alert.alert_type,
                            "short": True,
                        },
                    ],
                    "footer": "AI Governance Monitoring",
                    "ts": int(alert.timestamp.timestamp()),
                }
            ],
        }

        if alert.action_required:
            payload["attachments"][0]["fields"].append(
                {
                    "title": "Action Required",
                    "value": alert.action_required,
                    "short": False,
                }
            )

        httpx.post(self.settings.slack_webhook_url, json=payload, timeout=10.0)

    def _send_email(self, alert: Alert) -> None:
        """Send alert via email."""
        if not all(
            [
                self.settings.smtp_host,
                self.settings.smtp_user,
                self.settings.smtp_password,
                self.settings.alert_email_to,
            ]
        ):
            return

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[{alert.severity.value}] {alert.title}"
        msg["From"] = self.settings.smtp_user
        msg["To"] = self.settings.alert_email_to

        # Plain text version
        text = f"""
AI Governance Alert

Severity: {alert.severity.value}
Type: {alert.alert_type}
Time: {alert.timestamp.isoformat()}

{alert.message}

{"Action Required: " + alert.action_required if alert.action_required else ""}
"""

        # HTML version
        color_map = {
            AlertSeverity.CRITICAL: "#dc3545",
            AlertSeverity.HIGH: "#fd7e14",
            AlertSeverity.MEDIUM: "#ffc107",
            AlertSeverity.LOW: "#28a745",
        }

        html = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <div style="background-color: {color_map.get(alert.severity, '#6c757d')}; color: white; padding: 10px 20px; border-radius: 5px;">
        <h2 style="margin: 0;">{alert.title}</h2>
    </div>
    <div style="padding: 20px;">
        <p><strong>Severity:</strong> {alert.severity.value}</p>
        <p><strong>Type:</strong> {alert.alert_type}</p>
        <p><strong>Time:</strong> {alert.timestamp.isoformat()}</p>
        <hr>
        <p>{alert.message}</p>
        {f'<p><strong>Action Required:</strong> {alert.action_required}</p>' if alert.action_required else ''}
    </div>
    <div style="background-color: #f8f9fa; padding: 10px 20px; font-size: 12px; color: #6c757d;">
        AI Governance Monitoring System
    </div>
</body>
</html>
"""

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as server:
            server.starttls()
            server.login(self.settings.smtp_user, self.settings.smtp_password)
            server.send_message(msg)

    def _log_alert(self, alert: Alert, channels: list[str]) -> AlertLog:
        """Log alert to database."""
        alert_log = AlertLog(
            timestamp=alert.timestamp,
            alert_type=alert.alert_type,
            severity=alert.severity.value,
            title=alert.title,
            message=alert.message,
            related_violation_id=alert.related_violation_id,
            related_decision_id=alert.related_decision_id,
            channels=channels,
        )

        self.db.add(alert_log)
        self.db.commit()
        return alert_log

    def get_recent_alerts(self, limit: int = 50) -> list[AlertLog]:
        """Get recent alerts."""
        return (
            self.db.query(AlertLog)
            .order_by(AlertLog.timestamp.desc())
            .limit(limit)
            .all()
        )

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> AlertLog | None:
        """Acknowledge an alert."""
        alert = self.db.query(AlertLog).filter(AlertLog.id == alert_id).first()

        if alert:
            alert.acknowledged = True
            alert.acknowledged_at = datetime.utcnow()
            alert.acknowledged_by = acknowledged_by
            self.db.commit()

        return alert
