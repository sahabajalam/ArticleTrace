"""Aggregates raw findings + scanner shared state into an AISystemProfile."""

from __future__ import annotations

from typing import Any

from src.code_analyzer.models import (
    AIComponent,
    AISystemProfile,
    DataSignals,
    DecisionSurface,
    Evidence,
    Finding,
    RepoInfo,
)


AI_COMPONENT_CLASSIFICATION: dict[str, str] = {
    # LLM SDKs
    "openai": "llm_sdk",
    "anthropic": "llm_sdk",
    "google.generativeai": "llm_sdk",
    "langchain": "llm_sdk",
    "llama_index": "llm_sdk",
    # ML frameworks
    "torch": "ml_framework",
    "tensorflow": "ml_framework",
    "sklearn": "ml_framework",
    "scikit-learn": "ml_framework",
    "transformers": "ml_framework",
    # Biometric libs
    "face_recognition": "biometric_lib",
    "deepface": "biometric_lib",
    "mediapipe.solutions.face": "biometric_lib",
    "dlib.get_frontal_face_detector": "biometric_lib",
    "fer": "biometric_lib",
    # Vector stores
    "chromadb": "vector_store",
    "pinecone": "vector_store",
    "faiss": "vector_store",
}


def build_profile(
    scan_id: str,
    repo_info: RepoInfo,
    findings: list[Finding],
    shared: dict[str, Any],
) -> AISystemProfile:
    components = _infer_components(shared)
    surfaces = [
        DecisionSurface(
            endpoint=s["endpoint"],
            file=s["file"],
            line=s["line"],
            calls_model=s["calls_model"],
            has_human_review=s["has_human_review"],
            has_audit_log=s["has_audit_log"],
        )
        for s in shared.get("decision_surfaces", []) or []
    ]
    signals = _infer_data_signals(findings, shared, repo_info)
    stats = {
        "total_findings": len([f for f in findings if not f.suppressed]),
        "by_severity": _by_severity(findings),
        "by_rule": _by_rule(findings),
        "suppressed": len([f for f in findings if f.suppressed]),
        # Coverage honesty (v06 §4 / v07 §5): a caller must be able to tell
        # "these signals found nothing" from "these signals were never read".
        "manifest_scan": shared.get("manifest_scan") or {"files": [], "errors": []},
        "source_read_errors": shared.get("source_read_errors") or [],
        "llm_triage": shared.get("llm_triage") or {"status": "skipped", "reason": "not run"},
    }
    return AISystemProfile(
        scan_id=scan_id,
        repo=repo_info,
        ai_components=components,
        decision_surfaces=surfaces,
        data_signals=signals,
        findings=findings,
        stats=stats,
    )


def _infer_components(shared: dict[str, Any]) -> list[AIComponent]:
    by_name: dict[tuple[str, str], list[Evidence]] = {}
    for rid, items in (shared.get("imports_by_rule") or {}).items():
        for rel_path, matches in items:
            for symbol, line, excerpt in matches:
                kind = AI_COMPONENT_CLASSIFICATION.get(symbol)
                if not kind:
                    # Try longest prefix match
                    prefix = next(
                        (
                            k
                            for k in AI_COMPONENT_CLASSIFICATION
                            if symbol.startswith(k)
                        ),
                        None,
                    )
                    if prefix:
                        kind = AI_COMPONENT_CLASSIFICATION[prefix]
                if not kind:
                    continue
                key = (kind, symbol)
                by_name.setdefault(key, []).append(
                    Evidence(file=rel_path, line=line, excerpt=excerpt, symbol=symbol)
                )
    out: list[AIComponent] = []
    for (kind, name), evidence in by_name.items():
        out.append(AIComponent(kind=kind, name=name, evidence=evidence[:5]))  # type: ignore[arg-type]
    return out


def _infer_data_signals(
    findings: list[Finding], shared: dict[str, Any], repo_info: RepoInfo
) -> DataSignals:
    pii = shared.get("pii_fields", []) or []
    rule_ids = {f.rule_id for f in findings if not f.suppressed}
    # AI-004 fires when model card absent; flip logic
    has_model_card = "AI-004" not in rule_ids
    # AI-005 fires when DPIA marker missing AND PII present
    has_dpia = "AI-005" not in rule_ids if pii else True
    # AI-006 fires on missing data card
    has_data_card = "AI-006" not in rule_ids
    # AI-007 fires on missing audit log on inference sites
    audit_state = "present"
    if "AI-007" in rule_ids:
        any_logged = any(
            s.get("has_audit_log") for s in shared.get("decision_surfaces", []) or []
        )
        audit_state = "partial" if any_logged else "none"
    return DataSignals(
        pii_fields=pii,
        has_dpia_doc=has_dpia,
        has_model_card=has_model_card,
        has_data_card=has_data_card,
        audit_logging=audit_state,  # type: ignore[arg-type]
    )


def _by_severity(findings: list[Finding]) -> dict[str, int]:
    out: dict[str, int] = {}
    for f in findings:
        if f.suppressed:
            continue
        out[f.severity.value] = out.get(f.severity.value, 0) + 1
    return out


def _by_rule(findings: list[Finding]) -> dict[str, int]:
    out: dict[str, int] = {}
    for f in findings:
        if f.suppressed:
            continue
        out[f.rule_id] = out.get(f.rule_id, 0) + 1
    return out
