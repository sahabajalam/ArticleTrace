"""AST-level detection: HTTP routes, inference call sites, overrides.

Split into two scanners so an LLM review pass can sit between them:

  - ``AstScanner``        — Phase 1: walk the tree, collect decision-surface
    dicts into ``ctx.shared["decision_surfaces"]``. Emits no findings.
  - ``AstRulesScanner``   — Phase 2: read the (by-now LLM-enriched) surfaces
    from ``ctx.shared`` and apply the three rules (decision_endpoint,
    audit_missing, no_override).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext
from src.code_analyzer.source_reader import read_source_bytes
from src.code_analyzer.ts_parser import detect_language, parse_file


# tokens that look like model-inference sites
INFERENCE_CALL_PATTERNS = re.compile(
    r"\b(?:predict|generate|chat\.completions\.create|messages\.create|"
    r"invoke|__call__|embed|transcribe|classify|score)\b"
)

HUMAN_REVIEW_KEYWORDS = re.compile(
    r"\b(?:human_review|approval|approver|reviewer|reviewed_by|override)\b",
    re.IGNORECASE,
)

AUDIT_KEYWORDS = re.compile(
    r"\b(?:logger|log\.|audit|audit_log|structlog|decision_log)\b",
    re.IGNORECASE,
)

PY_ROUTE_DECORATORS = re.compile(
    r"@(?:app|router|api|blueprint)\.(?:get|post|put|patch|delete)\b"
)
JS_ROUTE_METHODS = re.compile(
    r"\b(?:app|router)\.(?:get|post|put|patch|delete)\s*\("
)


class AstScanner(Scanner):
    """Phase 1: collect decision surfaces. Emits no findings.

    Runs unconditionally (does not gate on ``applicable_rules``) because
    the surfaces feed downstream rules *and* profile building.
    """

    technique = "ast_scan"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        del rules  # surface collection is rule-agnostic
        all_surfaces: list[dict[str, Any]] = []
        for path in ctx.files:
            lang = detect_language(path)
            if lang is None:
                continue
            source, read_err = read_source_bytes(path)
            if read_err:
                ctx.shared.setdefault("source_read_errors", []).append(read_err)
            if not source:
                continue
            all_surfaces.extend(
                _find_decision_surfaces(path, source, lang, ctx.rel(path))
            )
        ctx.shared["decision_surfaces"] = all_surfaces
        return []


class AstRulesScanner(Scanner):
    """Phase 2: apply AST-surface rules using ``ctx.shared["decision_surfaces"]``.

    Expects surfaces to already be populated (and optionally LLM-enriched)
    by ``AstScanner`` + the LLM reviewer step in the pipeline.
    """

    technique = "ast_scan"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        applicable = self.applicable_rules(rules)
        if not applicable:
            return []
        surfaces: list[dict[str, Any]] = ctx.shared.get("decision_surfaces", [])
        findings: list[Finding] = []
        for rule in applicable:
            kind = rule.patterns.get("kind")
            if kind == "decision_endpoint":
                findings.extend(self._rule_decision_endpoint(rule, ctx, surfaces))
            elif kind == "audit_missing":
                findings.extend(self._rule_audit_missing(rule, ctx, surfaces))
            elif kind == "no_override":
                findings.extend(self._rule_no_override(rule, ctx, surfaces))
        return findings

    # ---- rule impls -----------------------------------------------------

    def _rule_decision_endpoint(
        self, rule: RuleSpec, ctx: ScanContext, surfaces: list[dict[str, Any]]
    ) -> list[Finding]:
        out: list[Finding] = []
        for s in surfaces:
            if not s["calls_model"] or s["has_human_review"]:
                continue
            sup, reason = ctx.is_suppressed(rule.id, s["file"])
            conf = self.apply_dampeners(rule, s["file"], rule.base_confidence)
            ev = [
                Evidence(
                    file=s["file"], line=s["line"],
                    excerpt=s["excerpt"], symbol=s["endpoint"],
                )
            ]
            f = self.build_finding(rule, ev, confidence=conf)
            f.suppressed, f.suppress_reason = sup, reason
            out.append(f)
        return out

    def _rule_audit_missing(
        self, rule: RuleSpec, ctx: ScanContext, surfaces: list[dict[str, Any]]
    ) -> list[Finding]:
        out: list[Finding] = []
        for s in surfaces:
            if not s["calls_model"] or s["has_audit_log"]:
                continue
            sup, reason = ctx.is_suppressed(rule.id, s["file"])
            conf = self.apply_dampeners(rule, s["file"], rule.base_confidence)
            ev = [Evidence(file=s["file"], line=s["line"], excerpt=s["excerpt"])]
            f = self.build_finding(rule, ev, confidence=conf)
            f.suppressed, f.suppress_reason = sup, reason
            out.append(f)
        return out

    def _rule_no_override(
        self, rule: RuleSpec, ctx: ScanContext, surfaces: list[dict[str, Any]]
    ) -> list[Finding]:
        """Flag files with decision endpoints but no sibling override/appeal route."""
        out: list[Finding] = []
        by_file: dict[str, list[dict[str, Any]]] = {}
        for s in surfaces:
            if s["calls_model"]:
                by_file.setdefault(s["file"], []).append(s)
        override_re = re.compile(r"\b(override|appeal|reject|contest)\b", re.IGNORECASE)
        for file, items in by_file.items():
            try:
                text = (ctx.repo_root / file).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if override_re.search(text):
                continue
            sup, reason = ctx.is_suppressed(rule.id, file)
            conf = self.apply_dampeners(rule, file, rule.base_confidence)
            s = items[0]
            ev = [Evidence(file=file, line=s["line"], excerpt=s["excerpt"], symbol=s["endpoint"])]
            f = self.build_finding(rule, ev, confidence=conf)
            f.suppressed, f.suppress_reason = sup, reason
            out.append(f)
        return out


# ----------------------------------------------------------------------

def _find_decision_surfaces(
    path: Path, source: bytes, lang: str, rel_path: str
) -> list[dict[str, Any]]:
    """Light heuristic: a decorated / registered route whose body references
    an inference call. Tree-sitter gives us precise ranges; we text-match inside."""
    tree, _ = parse_file(path, source)
    if tree is None:
        return []
    out: list[dict[str, Any]] = []
    lines = source.splitlines()

    def line_text(i: int) -> str:
        try:
            return lines[i].decode("utf-8", errors="replace")
        except IndexError:
            return ""

    def window(start: int, end: int) -> str:
        return "\n".join(
            line_text(i) for i in range(max(0, start), min(len(lines), end + 1))
        )

    if lang == "python":
        for node in _iter(tree.root_node):
            if node.type != "decorator":
                continue
            dec_text = source[node.start_byte : node.end_byte].decode(
                "utf-8", errors="replace"
            )
            if not PY_ROUTE_DECORATORS.search(dec_text):
                continue
            func = _next_sibling_of_type(node, "function_definition")
            if func is None:
                continue
            start = node.start_point[0]
            end = func.end_point[0]
            body = window(start, end)
            if not INFERENCE_CALL_PATTERNS.search(body):
                continue
            method = _extract_method(dec_text)
            route = _extract_route_string(dec_text) or func.child_by_field_name("name")
            route_str = (
                _extract_route_string(dec_text)
                or (
                    source[route.start_byte : route.end_byte].decode(
                        "utf-8", errors="replace"
                    )
                    if hasattr(route, "start_byte")
                    else "?"
                )
            )
            out.append(
                {
                    "endpoint": f"{method.upper()} {route_str}",
                    "file": rel_path,
                    "line": start + 1,
                    "excerpt": line_text(start).strip()[:200],
                    "calls_model": True,
                    "has_human_review": bool(HUMAN_REVIEW_KEYWORDS.search(body)),
                    "has_audit_log": bool(AUDIT_KEYWORDS.search(body)),
                }
            )

    elif lang in ("javascript", "typescript", "tsx"):
        for node in _iter(tree.root_node):
            if node.type != "call_expression":
                continue
            call_text = source[node.start_byte : node.end_byte].decode(
                "utf-8", errors="replace"
            )
            m = JS_ROUTE_METHODS.match(call_text)
            if not m:
                continue
            if not INFERENCE_CALL_PATTERNS.search(call_text):
                continue
            start = node.start_point[0]
            route_str_match = re.search(r"['\"`]([^'\"`]+)['\"`]", call_text)
            route_str = route_str_match.group(1) if route_str_match else "?"
            method_match = re.search(
                r"\b(get|post|put|patch|delete)\s*\(", call_text, re.IGNORECASE
            )
            method = method_match.group(1).upper() if method_match else "?"
            out.append(
                {
                    "endpoint": f"{method} {route_str}",
                    "file": rel_path,
                    "line": start + 1,
                    "excerpt": line_text(start).strip()[:200],
                    "calls_model": True,
                    "has_human_review": bool(HUMAN_REVIEW_KEYWORDS.search(call_text)),
                    "has_audit_log": bool(AUDIT_KEYWORDS.search(call_text)),
                }
            )
    return out


def _iter(node: Any):  # type: ignore[no-untyped-def]
    stack = [node]
    while stack:
        n = stack.pop()
        yield n
        stack.extend(n.children)


def _next_sibling_of_type(node: Any, type_name: str):  # type: ignore[no-untyped-def]
    parent = node.parent
    if parent is None:
        return None
    found_self = False
    for c in parent.children:
        if c.id == node.id:
            found_self = True
            continue
        if found_self and c.type == type_name:
            return c
    return None


def _extract_method(decorator_text: str) -> str:
    m = re.search(
        r"\.(get|post|put|patch|delete)\s*\(", decorator_text, re.IGNORECASE
    )
    return m.group(1) if m else "?"


def _extract_route_string(decorator_text: str) -> str | None:
    m = re.search(r"['\"]([^'\"]+)['\"]", decorator_text)
    return m.group(1) if m else None
