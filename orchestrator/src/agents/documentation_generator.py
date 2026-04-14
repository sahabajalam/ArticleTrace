"""Documentation Generator — turns findings + citations into a narrative report.

This is the main LLM node. It gets:
  - the AISystemProfile (components, stats, top findings)
  - the RiskPosture (category, score, triggers)
  - the per-rule citations (legal anchors)

…and produces:
  - executive_summary (3-4 sentences)
  - risk_narrative (why this category, what triggered it)
  - top_findings_narrative (prose explanation of most serious issues)
  - remediation_plan (prioritized actions mapped to finding rule_ids)

LLM output is JSON-constrained. On failure we fall back to a deterministic
template so a scan always produces a readable report.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any

from src.agents.base import BaseAgent
from src.state.scan_state import NarrativeReport, RemediationStep, ScanState


MAX_FINDINGS_IN_PROMPT = 15


class DocumentationGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="documentation_generator")

    async def execute(self, state: ScanState) -> dict[str, Any]:
        start = datetime.utcnow()
        profile = state.get("profile") or {}
        posture = state.get("risk_posture") or {}
        citations_by_rule = {
            rec["rule_id"]: rec.get("citations", [])
            for rec in (state.get("finding_citations") or [])
        }

        findings = [
            f for f in profile.get("findings", []) if not f.get("suppressed", False)
        ]
        findings.sort(
            key=lambda f: (_SEV_RANK.get(f.get("severity", "info"), 99), -f.get("confidence", 0))
        )
        top = findings[:MAX_FINDINGS_IN_PROMPT]

        prompt = _build_prompt(profile, posture, top, citations_by_rule)

        narrative: NarrativeReport
        cost = 0.0
        try:
            text, cost = await self.invoke_llm(prompt, scan_id=state.get("scan_id"))
            narrative = _parse_narrative(text, findings)
        except Exception as e:
            self.logger.warning("LLM narrative failed, using fallback: %s", e)
            narrative = _fallback_narrative(profile, posture, findings)

        duration = (datetime.utcnow() - start).total_seconds()
        return {
            "narrative": narrative.model_dump(mode="json"),
            "current_step": "narrative_generated",
            **self.audit_update(
                "generate_narrative",
                f"remediation_steps={len(narrative.remediation_plan)}",
                cost_usd=cost,
                duration_seconds=duration,
            ),
        }


_SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def _build_prompt(
    profile: dict[str, Any],
    posture: dict[str, Any],
    findings: list[dict[str, Any]],
    citations_by_rule: dict[str, list[dict[str, Any]]],
) -> str:
    components = [
        f"{c.get('kind')}:{c.get('name')}"
        for c in profile.get("ai_components") or []
    ]
    stats = profile.get("stats") or {}
    findings_block = []
    for f in findings:
        cites = citations_by_rule.get(f["rule_id"], [])
        cite_str = ", ".join(
            c.get("article_number", "?") for c in cites[:3]
        ) or "—"
        ev = (f.get("evidence") or [{}])[0]
        findings_block.append(
            f"- [{f['rule_id']}] {f['title']} (sev={f['severity']}, conf={f['confidence']:.2f})\n"
            f"    file: {ev.get('file')}:{ev.get('line')}\n"
            f"    citations: {cite_str}"
        )

    return f"""You are an EU AI Act compliance writer. Produce a JSON report with these keys:
  executive_summary     (3-4 sentences, plain prose)
  risk_narrative        (2-3 sentences explaining the risk category)
  top_findings_narrative (4-8 sentences covering the most serious issues)
  remediation_plan      (list of {{priority, finding_rule_ids, title, description, effort}})

Rules:
- priority must be one of: immediate, short_term, long_term
- effort must be one of: low, medium, high
- Group related findings into one remediation step when possible
- Reference the legal citations where relevant
- Do NOT invent article numbers — use only what appears in the data

### System profile
Repo: {profile.get("repo", {}).get("url", "unknown")}
Languages: {", ".join(profile.get("repo", {}).get("languages", []))}
AI components: {", ".join(components) or "(none detected)"}
Total findings: {stats.get("total_findings", 0)}
Breakdown: critical={posture.get("critical_count", 0)} high={posture.get("high_count", 0)} medium={posture.get("medium_count", 0)} low={posture.get("low_count", 0)}

### Risk posture
Category: {posture.get("category")}
Score: {posture.get("compliance_score")}
Reason: {posture.get("reason")}

### Findings (top {len(findings)})
{chr(10).join(findings_block)}

Respond with ONLY valid JSON, no prose around it."""


def _parse_narrative(text: str, findings: list[dict[str, Any]]) -> NarrativeReport:
    # strip fenced code blocks if present
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    payload = m.group(1) if m else text.strip()
    # fallback: find first {...}
    if not payload.lstrip().startswith("{"):
        m2 = re.search(r"\{.*\}", payload, re.DOTALL)
        if m2:
            payload = m2.group(0)
    data = json.loads(payload)

    valid_rule_ids = {f["rule_id"] for f in findings}
    steps: list[RemediationStep] = []
    for s in data.get("remediation_plan", []):
        try:
            rule_ids = [rid for rid in s.get("finding_rule_ids", []) if rid in valid_rule_ids]
            steps.append(
                RemediationStep(
                    priority=s.get("priority", "short_term"),
                    finding_rule_ids=rule_ids or list(valid_rule_ids)[:1],
                    title=s.get("title", "Remediation"),
                    description=s.get("description", ""),
                    effort=s.get("effort", "medium"),
                )
            )
        except Exception:
            continue

    return NarrativeReport(
        executive_summary=str(data.get("executive_summary", "")).strip() or "—",
        risk_narrative=str(data.get("risk_narrative", "")).strip() or "—",
        top_findings_narrative=str(data.get("top_findings_narrative", "")).strip() or "—",
        remediation_plan=steps,
    )


def _fallback_narrative(
    profile: dict[str, Any],
    posture: dict[str, Any],
    findings: list[dict[str, Any]],
) -> NarrativeReport:
    category = posture.get("category", "UNKNOWN")
    score = posture.get("compliance_score", 0)
    total = len(findings)
    summary = (
        f"Scan classified this system as {category} with a compliance score of {score:.0f}/100. "
        f"{total} unsuppressed finding(s) were detected across the repository."
    )
    risk_narr = posture.get("reason") or "See posture details."
    top_narr = "; ".join(
        f"{f['rule_id']}: {f['title']}" for f in findings[:5]
    ) or "No findings."

    plan: list[RemediationStep] = []
    by_rule: dict[str, list[str]] = {}
    for f in findings:
        by_rule.setdefault(f["rule_id"], []).append(f["rule_id"])
    for rid, group in list(by_rule.items())[:5]:
        f = next((x for x in findings if x["rule_id"] == rid), None)
        if not f:
            continue
        prio = "immediate" if f.get("severity") in ("critical", "high") else "short_term"
        plan.append(
            RemediationStep(
                priority=prio,
                finding_rule_ids=[rid],
                title=f.get("title", rid),
                description=f.get("remediation") or "See rule documentation.",
                effort="medium",
            )
        )

    return NarrativeReport(
        executive_summary=summary,
        risk_narrative=risk_narr,
        top_findings_narrative=top_narr,
        remediation_plan=plan,
    )
