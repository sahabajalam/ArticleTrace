"""Detects library imports across Python, JavaScript, TypeScript via tree-sitter,
and cross-references dependency manifests (v07 T1.1).

Python queries:   import_statement, import_from_statement
JS/TS queries:    import_statement, require call_expression

Matches any prefix of the dotted module path.
"""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext
from src.code_analyzer.source_reader import read_source_bytes
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
            source, read_err = read_source_bytes(path)
            if read_err:
                ctx.shared.setdefault("source_read_errors", []).append(read_err)
            if not source:
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
        findings.extend(self._manifest_pass(ctx, applicable, findings))
        return findings

    def _manifest_pass(
        self, ctx: ScanContext, applicable: list[RuleSpec], import_findings: list[Finding]
    ) -> list[Finding]:
        """Cross-reference dependency manifests against the same rule patterns.

        v07 T1.1, after Cisco aibom's Tier 2. Three outcomes per rule:
        - declared + imported: the import finding gains a small confidence
          boost and the manifest line as extra evidence — two independent
          signals agree.
        - declared only: a medium-confidence finding of its own. A dependency
          declared but never statically imported is exactly the shadow left by
          dynamic loading (importlib plugins) — the manifest_only benchmark
          fixture scanned clean before this existed.
        - imported only: unchanged behaviour.

        Per v06 §4 / v07 §5, manifest parse failures are recorded in
        ctx.shared["manifest_scan"]["errors"], never swallowed: "no declared
        deps" must be distinguishable from "could not read the manifest".
        """
        declared, scan_report = _collect_declared_deps(ctx)
        ctx.shared["manifest_scan"] = scan_report
        if not declared:
            return []

        found_rule_ids = {f.rule_id for f in import_findings}
        new_findings: list[Finding] = []
        for rule in applicable:
            patterns: list[str] = rule.patterns.get("imports", []) or []
            hits: list[tuple[str, str, str, int | None, str]] = []
            for needle in patterns:
                for dist, mf_rel, line, raw in declared:
                    if _dist_matches_needle(dist, needle):
                        hits.append((needle, dist, mf_rel, line, raw))
            if not hits:
                continue

            bucket = ctx.shared.setdefault("imports_by_rule", {})
            for needle, dist, mf_rel, line, raw in hits:
                bucket.setdefault(rule.id, []).append(
                    (mf_rel, [(needle, line, raw)])
                )

            if rule.id in found_rule_ids:
                # Two signals agree — nudge, never past certainty.
                for fnd in import_findings:
                    if fnd.rule_id == rule.id:
                        fnd.confidence = min(0.99, round(fnd.confidence + 0.05, 2))
                        if len(fnd.evidence) < 10:
                            needle, dist, mf_rel, line, raw = hits[0]
                            fnd.evidence.append(Evidence(
                                file=mf_rel, line=line,
                                excerpt=f"also declared in manifest: {raw}",
                                symbol=dist,
                            ))
                continue

            sup, reason = ctx.is_suppressed(rule.id, hits[0][2])
            conf = round(rule.base_confidence * 0.7, 2)  # declared, not seen used
            evidence = [
                Evidence(
                    file=mf_rel, line=line,
                    excerpt=f"declared in manifest (no static import located): {raw}",
                    symbol=dist,
                )
                for _needle, dist, mf_rel, line, raw in hits[:10]
            ]
            fnd = self.build_finding(rule, evidence, confidence=conf)
            fnd.suppressed = sup
            fnd.suppress_reason = reason
            new_findings.append(fnd)
        return new_findings


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


def _emit_module(node: Any, source: bytes, out: list[tuple[str, int, str]]) -> None:
    if node is None or node.type != "dotted_name":
        return
    line = node.start_point[0] + 1
    out.append((_node_text(node, source), line, _excerpt_line(source, line)))


def _walk_py_imports(node: Any, source: bytes, out: list[tuple[str, int, str]]) -> None:
    """Collect imported MODULE paths — the thing rules match on.

    Read the grammar's field names, never descendant order. The previous
    implementation took the first `dotted_name` descendant, and
    `_all_descendants` walks a LIFO stack, so for

        from deepface.commons import package_utils, folder_utils

    it reached the imported *names* before the module and recorded
    `folder_utils`. Every `from X import Y` therefore matched on Y and the
    module X was never seen: `from deepface import DeepFace`,
    `from openai import OpenAI` and friends were invisible to AI-001/AI-002
    while the scan still reported success. Scanning serengil/deepface — a face
    recognition library, with `deepface` in AI-001's import list — returned
    LIMITED_RISK and no AI components.
    """
    if node.type == "import_statement":
        # `import a.b`, `import a.b as c`, and `import a, b` (several names).
        for child in node.children_by_field_name("name"):
            _emit_module(
                child.child_by_field_name("name")
                if child.type == "aliased_import"
                else child,
                source,
                out,
            )
    elif node.type == "import_from_statement":
        # `from a.b import c` / `from . import c` — the module is the
        # module_name field. A bare relative import has no dotted_name and is
        # correctly skipped: it names no third-party library.
        module = node.child_by_field_name("module_name")
        if module is not None and module.type == "relative_import":
            module = next(
                (c for c in module.children if c.type == "dotted_name"), None
            )
        _emit_module(module, source, out)

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


# ── dependency-manifest cross-referencing (v07 T1.1) ──────────────────────────

_MANIFEST_NAMES = re.compile(r"^(requirements[^/]*\.txt|pyproject\.toml|package\.json)$")

# PEP 503-ish: distribution names and import names differ in separators and
# case (face-recognition dist vs face_recognition import, google-generativeai
# dist vs google.generativeai import). Normalise both sides before comparing.
def _norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.strip().lower())


def _dist_matches_needle(dist: str, needle: str) -> bool:
    """A declared distribution satisfies a rule's import pattern when it equals
    the full needle (google-generativeai ~ google.generativeai) or the needle's
    top-level package (dlib ~ dlib.get_frontal_face_detector). npm scoped names
    (@anthropic-ai/sdk) compare whole."""
    nd = _norm(dist)
    if nd == _norm(needle):
        return True
    top = needle.split("/")[0].split(".")[0] if not needle.startswith("@") else needle
    return nd == _norm(top)


_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def _parse_requirement(line: str) -> str | None:
    """Extract the distribution name from one PEP 508 requirement line."""
    bare = line.strip()
    if not bare or bare.startswith(("#", "-", "git+", "http://", "https://")):
        return None
    m = _REQ_LINE.match(bare)
    return m.group(1) if m else None


def _collect_declared_deps(
    ctx: ScanContext,
) -> tuple[list[tuple[str, str, int | None, str]], dict]:
    """All declared dependencies across recognised manifests in the file set.

    Returns (deps, report): deps as (dist, manifest_rel_path, line, raw_text);
    report = {"files": [...], "errors": [...]} for the coverage stats.
    """
    deps: list[tuple[str, str, int | None, str]] = []
    report: dict = {"files": [], "errors": []}
    for path in ctx.files:
        if not _MANIFEST_NAMES.match(path.name):
            continue
        rel = ctx.rel(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            report["errors"].append(f"{rel}: {e}")
            continue
        report["files"].append(rel)
        try:
            if path.name == "package.json":
                deps.extend(_deps_from_package_json(text, rel))
            elif path.name == "pyproject.toml":
                deps.extend(_deps_from_pyproject(text, rel))
            else:
                deps.extend(_deps_from_requirements(text, rel))
        except Exception as e:  # noqa: BLE001 — report, never swallow (v07 §5)
            report["errors"].append(f"{rel}: parse failed: {e}")
    return deps, report


def _deps_from_requirements(text: str, rel: str) -> list[tuple[str, str, int | None, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        dist = _parse_requirement(line)
        if dist:
            out.append((dist, rel, i, line.strip()[:120]))
    return out


def _line_of(text: str, token: str) -> int | None:
    for i, line in enumerate(text.splitlines(), start=1):
        if token in line:
            return i
    return None


def _deps_from_pyproject(text: str, rel: str) -> list[tuple[str, str, int | None, str]]:
    data = tomllib.loads(text)
    out = []
    reqs: list[str] = list((data.get("project") or {}).get("dependencies") or [])
    for group in ((data.get("project") or {}).get("optional-dependencies") or {}).values():
        reqs.extend(group or [])
    for req in reqs:
        dist = _parse_requirement(req)
        if dist:
            out.append((dist, rel, _line_of(text, dist), str(req)[:120]))
    poetry = ((data.get("tool") or {}).get("poetry") or {}).get("dependencies") or {}
    for dist in poetry:
        if dist.lower() != "python":
            out.append((dist, rel, _line_of(text, dist), f"[tool.poetry.dependencies] {dist}"))
    return out


def _deps_from_package_json(text: str, rel: str) -> list[tuple[str, str, int | None, str]]:
    data = json.loads(text)
    out = []
    for section in ("dependencies", "devDependencies"):
        for dist, ver in (data.get(section) or {}).items():
            out.append((dist, rel, _line_of(text, f'"{dist}"'), f"{dist}: {ver}"))
    return out
