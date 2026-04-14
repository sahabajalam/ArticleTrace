"""Detects library imports across Python, JavaScript, TypeScript via tree-sitter.

Python queries:   import_statement, import_from_statement
JS/TS queries:    import_statement, require call_expression

Matches any prefix of the dotted module path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext
from src.code_analyzer.ts_parser import detect_language, parse_file


PY_IMPORT_QUERY = """
(import_statement name: (dotted_name) @mod)
(import_statement name: (aliased_import name: (dotted_name) @mod))
(import_from_statement module_name: (dotted_name) @mod)
(import_from_statement module_name: (relative_import (dotted_name) @mod))
"""

JS_IMPORT_QUERY = """
(import_statement source: (string (string_fragment) @mod))
(call_expression
  function: (identifier) @fn (#eq? @fn "require")
  arguments: (arguments (string (string_fragment) @mod)))
"""


class ImportScanner(Scanner):
    technique = "import_scan"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        applicable = self.applicable_rules(rules)
        if not applicable:
            return []
        findings: list[Finding] = []
        for path in ctx.files:
            lang = detect_language(path)
            if lang is None:
                continue
            try:
                source = path.read_bytes()
            except OSError:
                continue
            imports = _extract_imports(path, source, lang)
            if not imports:
                continue
            rel = ctx.rel(path)
            for rule in applicable:
                patterns: list[str] = rule.patterns.get("imports", []) or []
                matched: list[tuple[str, int, str]] = []
                for mod, line, excerpt in imports:
                    for needle in patterns:
                        if _module_matches(mod, needle):
                            matched.append((needle, line, excerpt))
                            break
                if not matched:
                    continue
                suppressed, reason = ctx.is_suppressed(rule.id, rel)
                conf = self.apply_dampeners(rule, rel, rule.base_confidence)
                evidence = [
                    Evidence(file=rel, line=ln, excerpt=ex, symbol=sym)
                    for sym, ln, ex in matched[:10]
                ]
                f = self.build_finding(rule, evidence, confidence=conf)
                f.suppressed = suppressed
                f.suppress_reason = reason
                findings.append(f)
                # share with cooccurrence scanner
                bucket = ctx.shared.setdefault("imports_by_rule", {})
                bucket.setdefault(rule.id, []).append((rel, matched))
        return findings


def _module_matches(mod: str, needle: str) -> bool:
    """needle = 'openai' matches 'openai', 'openai.chat' etc.
    needle = 'mediapipe.solutions.face' matches exactly that prefix."""
    mod = mod.strip()
    if mod == needle:
        return True
    return mod.startswith(needle + ".")


def _extract_imports(path: Path, source: bytes, lang: str) -> list[tuple[str, int, str]]:
    """Return list of (module_name, line, excerpt)."""
    tree, _ = parse_file(path, source)
    if tree is None:
        return []
    out: list[tuple[str, int, str]] = []
    if lang == "python":
        _walk_py_imports(tree.root_node, source, out)
    elif lang in ("javascript", "typescript", "tsx"):
        _walk_js_imports(tree.root_node, source, out)
    return out


def _node_text(node: Any, source: bytes) -> str:
    return source[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _excerpt_line(source: bytes, line: int) -> str:
    try:
        ln = source.splitlines()[line - 1].decode("utf-8", errors="replace")
        return ln.strip()[:200]
    except IndexError:
        return ""


def _walk_py_imports(node: Any, source: bytes, out: list[tuple[str, int, str]]) -> None:
    if node.type in ("import_statement", "import_from_statement"):
        # find dotted_name / aliased_import children
        for child in _all_descendants(node):
            if child.type == "dotted_name":
                name = _node_text(child, source)
                line = child.start_point[0] + 1
                out.append((name, line, _excerpt_line(source, line)))
                # only take first dotted_name per import statement
                break
    for c in node.children:
        _walk_py_imports(c, source, out)


def _walk_js_imports(node: Any, source: bytes, out: list[tuple[str, int, str]]) -> None:
    if node.type == "import_statement":
        # find source string
        for child in _all_descendants(node):
            if child.type == "string":
                name = _node_text(child, source).strip("\"'`")
                line = node.start_point[0] + 1
                out.append((name, line, _excerpt_line(source, line)))
                break
    elif node.type == "call_expression":
        fn = node.child_by_field_name("function")
        args = node.child_by_field_name("arguments")
        if fn is not None and _node_text(fn, source) == "require" and args is not None:
            for child in _all_descendants(args):
                if child.type == "string":
                    name = _node_text(child, source).strip("\"'`")
                    line = node.start_point[0] + 1
                    out.append((name, line, _excerpt_line(source, line)))
                    break
    for c in node.children:
        _walk_js_imports(c, source, out)


def _all_descendants(node: Any):  # type: ignore[no-untyped-def]
    stack = list(node.children)
    while stack:
        n = stack.pop()
        yield n
        stack.extend(n.children)
