"""Repo ingestion — shallow clone, language detect, file index, suppressions."""

from __future__ import annotations

import shutil
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml
from git import Repo

from src.code_analyzer.models import RepoInfo
from src.code_analyzer.ts_parser import detect_language


EXCLUDE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", ".env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "dist", "build", ".next", ".nuxt", ".svelte-kit",
    "target", "out", "coverage", ".cache", ".tox",
    ".idea", ".vscode",
}
EXCLUDE_SUFFIXES = {
    ".min.js", ".min.css", ".lock", ".png", ".jpg", ".jpeg",
    ".gif", ".webp", ".ico", ".svg", ".pdf", ".zip", ".gz",
    ".whl", ".so", ".dylib", ".exe", ".bin",
}
MAX_FILE_BYTES = 1_000_000  # skip files > 1 MB
# Notebooks routinely exceed 1 MB because saved outputs (plots, dataframes)
# live in the JSON; extraction keeps only code cells, so the raw-size cap
# would silently drop exactly the files T1.2 exists to scan.
MAX_NOTEBOOK_BYTES = 5_000_000
MAX_FILES = 5_000


@dataclass
class IngestResult:
    repo_root: Path
    repo_info: RepoInfo
    files: list[Path]
    suppressions: list[dict]
    cleanup: callable  # type: ignore[valid-type]


def clone_repo(url: str, ref: str = "main", depth: int = 1) -> tuple[Path, str, callable]:
    """Shallow-clone `url` into a temp dir. Returns (path, commit_sha, cleanup_fn)."""
    tmp = Path(tempfile.mkdtemp(prefix="alloycode-"))
    try:
        repo = Repo.clone_from(
            url, tmp, depth=depth, multi_options=[f"--branch={ref}"] if ref else None
        )
    except Exception:
        # retry without branch if specified branch doesn't exist
        shutil.rmtree(tmp, ignore_errors=True)
        tmp = Path(tempfile.mkdtemp(prefix="alloycode-"))
        repo = Repo.clone_from(url, tmp, depth=depth)
    commit = repo.head.commit.hexsha

    def _cleanup() -> None:
        shutil.rmtree(tmp, ignore_errors=True)

    return tmp, commit, _cleanup


def ingest(url: str, ref: str = "main") -> IngestResult:
    root, commit, cleanup = clone_repo(url, ref=ref)
    files = list(_iter_files(root))
    lang_counter: Counter[str] = Counter()
    for p in files:
        lang = detect_language(p)
        if lang:
            lang_counter[lang] += 1
    info = RepoInfo(
        url=url,
        ref=ref,
        commit=commit,
        languages=[l for l, _ in lang_counter.most_common()],
        total_files=_count_all_files(root),
        scanned_files=len(files),
    )
    suppressions = _load_suppressions(root)
    return IngestResult(
        repo_root=root,
        repo_info=info,
        files=files,
        suppressions=suppressions,
        cleanup=cleanup,
    )


def ingest_local(path: Path) -> IngestResult:
    """Used in tests — treat a local directory as an already-cloned repo."""
    root = path.resolve()
    files = list(_iter_files(root))
    lang_counter: Counter[str] = Counter()
    for p in files:
        lang = detect_language(p)
        if lang:
            lang_counter[lang] += 1
    info = RepoInfo(
        url=f"file://{root}",
        ref="local",
        commit=None,
        languages=[l for l, _ in lang_counter.most_common()],
        total_files=_count_all_files(root),
        scanned_files=len(files),
    )
    suppressions = _load_suppressions(root)

    def _noop() -> None:
        return None

    return IngestResult(
        repo_root=root,
        repo_info=info,
        files=files,
        suppressions=suppressions,
        cleanup=_noop,
    )


def _iter_files(root: Path) -> Iterable[Path]:
    count = 0
    for p in root.rglob("*"):
        if count >= MAX_FILES:
            break
        if not p.is_file():
            continue
        # Exclusions apply to path segments INSIDE the repo, never to the
        # repo's own location on disk. Matching absolute parts meant a repo
        # cloned under any ancestor named `env`, `out`, `build`, `.cache`,
        # etc. scanned as 0 files — and then reported MINIMAL_RISK with
        # errors:0, indistinguishable from a genuinely clean repo.
        if any(seg in EXCLUDE_DIRS for seg in p.relative_to(root).parts):
            continue
        if any(p.name.endswith(s) for s in EXCLUDE_SUFFIXES):
            continue
        try:
            cap = MAX_NOTEBOOK_BYTES if p.suffix.lower() == ".ipynb" else MAX_FILE_BYTES
            if p.stat().st_size > cap:
                continue
        except OSError:
            continue
        count += 1
        yield p


def _count_all_files(root: Path) -> int:
    n = 0
    for p in root.rglob("*"):
        if p.is_file() and not any(
            seg in EXCLUDE_DIRS for seg in p.relative_to(root).parts
        ):
            n += 1
    return n


def _load_suppressions(root: Path) -> list[dict]:
    path = root / ".alloycode.yml"
    if not path.is_file():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return list(data.get("suppress", []) or [])
    except Exception:
        return []
