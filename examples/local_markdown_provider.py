#!/usr/bin/env python3
"""Local markdown-folder adapter for Memory Seam examples.

The adapter is read-only and stdlib-only. It scans markdown files under one
root folder after the Memory Seam runtime has already authorized the request.
It does not follow symlinks, call networks, start services, or write indexes.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
from typing import Iterable

MAX_FILE_BYTES = 1_000_000
MAX_SCAN_FILES = 2_000
MAX_SNIPPET_CHARS = 200


def _query_terms(query: str) -> tuple[str, ...]:
    return tuple(term.lower() for term in re.findall(r"[A-Za-z0-9_'-]+", query) if term.strip())


def _title_for(path: Path, content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return path.stem.replace("_", " ").replace("-", " ").strip() or path.name


def _safe_relative_path(path: Path, root: Path) -> str | None:
    try:
        rel = path.resolve(strict=True).relative_to(root).as_posix()
    except (OSError, ValueError):
        return None
    if rel.startswith("../") or rel == ".." or rel.startswith("/"):
        return None
    return rel


def _score(title: str, content: str, terms: tuple[str, ...]) -> tuple[int, int | None]:
    if not terms:
        return 1, 0
    title_lower = title.lower()
    content_lower = content.lower()
    score = 0
    best_index: int | None = None
    for term in terms:
        title_hits = title_lower.count(term)
        content_hits = content_lower.count(term)
        score += (title_hits * 8) + content_hits
        index = content_lower.find(term)
        if index >= 0 and (best_index is None or index < best_index):
            best_index = index
        elif title_hits and best_index is None:
            best_index = 0
    return score, best_index


def _snippet(content: str, terms: tuple[str, ...], fallback_index: int | None) -> str:
    compact = " ".join(content.split())
    if not compact:
        return ""
    compact_lower = compact.lower()
    index = None
    for term in terms:
        candidate = compact_lower.find(term)
        if candidate >= 0 and (index is None or candidate < index):
            index = candidate
    if index is None:
        index = fallback_index
    if index is None:
        index = 0

    half = MAX_SNIPPET_CHARS // 2
    start = max(0, index - half)
    end = min(len(compact), start + MAX_SNIPPET_CHARS)
    start = max(0, end - MAX_SNIPPET_CHARS)
    return compact[start:end]


@dataclass(frozen=True)
class LocalMarkdownProvider:
    """Structural SourceAdapter for a local folder of markdown files."""

    root: str | Path
    adapter_name: str = "local-markdown-folder"

    def __post_init__(self) -> None:
        object.__setattr__(self, "_root", Path(self.root).expanduser().resolve())

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict]:
        return self._items(query="", scope="context", n=MAX_SCAN_FILES)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict]:
        return self._items(query=query, scope=scope, n=n)

    def _items(self, *, query: str, scope: str, n: int) -> list[dict]:
        terms = _query_terms(query)
        matches: list[tuple[int, str, dict]] = []
        scanned = 0
        truncated = False

        for path in self._markdown_files():
            if scanned >= MAX_SCAN_FILES:
                truncated = True
                break
            scanned += 1
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            rel = _safe_relative_path(path, self._root)
            if rel is None:
                continue
            title = _title_for(path, content)
            score, best_index = _score(title, content, terms)
            if score <= 0:
                continue
            item = self._item(
                rel=rel,
                title=title,
                snippet=_snippet(content, terms, best_index),
                scope=scope,
                score=score,
            )
            matches.append((score, title.lower(), item))

        matches.sort(key=lambda match: (-match[0], match[1], match[2]["path"]))
        limit = max(0, int(n))
        items = [item for _, _, item in matches[:limit]]
        if truncated:
            items.append(self._truncated_item(scope=scope))
        return items

    def _markdown_files(self) -> Iterable[Path]:
        if not self._root.exists() or not self._root.is_dir():
            return
        for dirpath, dirnames, filenames in os.walk(self._root, followlinks=False):
            current = Path(dirpath)
            dirnames[:] = [
                name
                for name in dirnames
                if not name.startswith(".") and not (current / name).is_symlink()
            ]
            for filename in filenames:
                path = current / filename
                if path.is_symlink() or path.suffix.lower() != ".md":
                    continue
                yield path

    def _item(self, *, rel: str, title: str, snippet: str, scope: str, score: int) -> dict:
        digest = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:12]
        return {
            "id": f"local-md-{digest}",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_markdown",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_markdown_scan",
            "canonicality": "user_folder",
            "private_class": "user_local_reportable_path",
            "title": title,
            "path": rel,
            "snippet": snippet[:MAX_SNIPPET_CHARS],
            "score": score,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": False,
        }

    def _truncated_item(self, *, scope: str) -> dict:
        return {
            "id": "local-md-scan-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_markdown",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_markdown_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local markdown scan truncated",
            "path": "",
            "snippet": f"Scan stopped after {MAX_SCAN_FILES} markdown files; narrow the folder or query for complete recall.",
            "score": 0,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": True,
            "degraded_reason": "scan_file_cap_reached",
        }


__all__ = [
    "LocalMarkdownProvider",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
