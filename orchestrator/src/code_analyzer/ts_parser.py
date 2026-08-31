"""Tree-sitter parser registry.

Uses tree-sitter-language-pack which ships pre-built bindings for ~165
languages. We use Python / JavaScript / TypeScript for Phase 1.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

try:
    from tree_sitter_language_pack import get_parser as _get_parser
except ImportError:  # pragma: no cover - falls back at import time
    _get_parser = None  # type: ignore[assignment]


LANG_BY_EXT: dict[str, str] = {
    ".py": "python",
    # Notebooks are read through source_reader.read_source_bytes, which hands
    # the parser extracted Python — the extension maps to the language of the
    # extracted stream, not of the raw JSON.
    ".ipynb": "python",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
}


def detect_language(path: Path) -> str | None:
    return LANG_BY_EXT.get(path.suffix.lower())


@lru_cache(maxsize=16)
def get_parser(language: str):  # type: ignore[no-untyped-def]
    if _get_parser is None:
        raise RuntimeError(
            "tree-sitter-language-pack not installed. "
            "Run: uv add tree-sitter-language-pack"
        )
    return _get_parser(language)


def parse_file(path: Path, source_bytes: bytes | None = None):  # type: ignore[no-untyped-def]
    lang = detect_language(path)
    if lang is None:
        return None, None
    if source_bytes is None:
        source_bytes = path.read_bytes()
    parser = get_parser(lang)
    tree = parser.parse(source_bytes)
    return tree, lang
