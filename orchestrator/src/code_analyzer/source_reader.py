"""Uniform source access for scanners, including notebook extraction (v07 T1.2).

Jupyter notebooks hold a material share of real ML code, and before this
module a notebook-only repo scanned completely clean (the `notebook_only`
benchmark fixture existed to prove it). `.ipynb` files are JSON; scanners
need the Python inside. This reader concatenates the code cells into one
Python source stream that tree-sitter and the content regexes can process.

Line-number convention: evidence lines for notebooks refer to the EXTRACTED
representation — code cells joined in order, each preceded by a
`# %% [cell N]` marker line (jupytext-style), magics/shell lines commented
out in place so line counts are stable and the stream stays parseable. The
excerpt carries the actual code line, which is what makes the evidence
findable in the notebook UI.

Failure contract (v06 §4 / v07 §5): a file that cannot be read or parsed
returns empty source PLUS an error string. Callers append the error to
ctx.shared["source_read_errors"], which build_profile surfaces in stats —
"no findings in this notebook" must be distinguishable from "could not read
the notebook".
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK_SUFFIX = ".ipynb"


def read_source_bytes(path: Path) -> tuple[bytes, str | None]:
    """Return (source_bytes, error). Notebooks come back as extracted Python."""
    try:
        raw = path.read_bytes()
    except OSError as e:
        return b"", f"{path.name}: {e}"
    if path.suffix.lower() != NOTEBOOK_SUFFIX:
        return raw, None
    try:
        return _extract_notebook(raw), None
    except Exception as e:  # noqa: BLE001 — malformed JSON, wrong schema, etc.
        return b"", f"{path.name}: notebook extraction failed: {type(e).__name__}: {e}"


def _extract_notebook(raw: bytes) -> bytes:
    nb = json.loads(raw.decode("utf-8", errors="replace"))
    cells = nb.get("cells")
    if not isinstance(cells, list):
        raise ValueError("no cells array (nbformat < 4 is unsupported)")
    out: list[str] = []
    for i, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        src = cell.get("source") or []
        if isinstance(src, str):
            src = src.splitlines(keepends=True)
        out.append(f"# %% [cell {i}]\n")
        for line in src:
            if not line.endswith("\n"):
                line += "\n"
            # IPython magics / shell escapes are not Python; comment them out
            # in place so the stream parses and line numbers stay stable.
            if line.lstrip().startswith(("%", "!")):
                line = "# MAGIC " + line
            out.append(line)
    return "".join(out).encode("utf-8")
