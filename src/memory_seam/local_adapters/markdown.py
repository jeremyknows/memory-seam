"""Read-only first-party adapter for local markdown folders."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
from typing import Any

from memory_seam.adapters import ADAPTER_PROTOCOL_VERSION

LOCAL_MARKDOWN_ADAPTER_NAME = "local-markdown-folder"
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
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return None
    posix = PurePosixPath(rel)
    if "\\" in rel or rel.startswith("/") or posix.is_absolute() or ".." in posix.parts or not rel:
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


def _empty_summary(reason: str) -> dict[str, Any]:
    return {
        "files_scanned": 0,
        "files_skipped": 0,
        "truncated": False,
        "reason": reason,
    }


@dataclass(frozen=True)
class LocalMarkdownAdapter:
    """Structural SourceAdapter for a local folder of markdown files.

    The adapter never follows symlinks, writes indexes, starts services, calls
    networks, or reports absolute local paths.
    """

    root: str | Path
    adapter_name: str = LOCAL_MARKDOWN_ADAPTER_NAME
    adapter_protocol_version: str = ADAPTER_PROTOCOL_VERSION
    _root: Path = field(init=False, repr=False)
    _last_scan_summary: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _last_empty_reason: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_root", Path(self.root).expanduser().absolute())
        self._set_scan_state(_empty_summary("not_scanned"), "not_scanned")

    @property
    def last_scan_summary(self) -> dict[str, Any]:
        return dict(self._last_scan_summary)

    @property
    def last_empty_reason(self) -> str | None:
        return self._last_empty_reason

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        return self._items(query="", scope="context", n=MAX_SCAN_FILES)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        return self._items(query=query, scope=scope, n=n)

    def _items(self, *, query: str, scope: str, n: int) -> list[dict[str, Any]]:
        root_status = self._root_status()
        if root_status is not None:
            return self._empty_result(root_status)

        terms = _query_terms(query)
        matches: list[tuple[int, str, dict[str, Any]]] = []
        files_scanned = 0
        files_skipped = 0
        markdown_seen = 0
        truncated = False
        permission_denied = False

        for event in self._markdown_file_events():
            if event["status"] == "permission_denied":
                permission_denied = True
                files_skipped += 1
                continue
            if event["status"] != "file":
                files_skipped += 1
                continue

            markdown_seen += 1
            if files_scanned >= MAX_SCAN_FILES:
                truncated = True
                break

            path = event["path"]
            files_scanned += 1
            rel = _safe_relative_path(path, self._root)
            if rel is None:
                files_skipped += 1
                continue

            try:
                stat = path.stat(follow_symlinks=False)
            except OSError:
                files_skipped += 1
                continue
            if stat.st_size > MAX_FILE_BYTES:
                files_skipped += 1
                continue

            try:
                raw = path.read_bytes()
            except PermissionError:
                permission_denied = True
                files_skipped += 1
                continue
            except OSError:
                files_skipped += 1
                continue

            replacement_used = False
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("utf-8", errors="replace")
                replacement_used = True

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
                replacement_used=replacement_used,
            )
            matches.append((score, title.lower(), item))

        if markdown_seen == 0:
            reason = "permission_denied" if permission_denied else "zero_markdown_files"
            return self._empty_result(
                reason,
                files_scanned=files_scanned,
                files_skipped=files_skipped,
                truncated=truncated,
            )

        summary = {
            "files_scanned": files_scanned,
            "files_skipped": files_skipped,
            "truncated": truncated,
            "reason": None,
        }
        self._set_scan_state(summary, None)

        matches.sort(key=lambda match: (-match[0], match[1], match[2]["path"]))
        limit = max(0, int(n))
        items = [item for _, _, item in matches[:limit]]
        if truncated:
            items.append(self._truncated_item(scope=scope, summary=summary))
        return items

    def _root_status(self) -> str | None:
        try:
            if self._root.is_symlink():
                return "root_is_symlink"
            if not self._root.exists():
                return "missing_root"
            if not self._root.is_dir():
                return "not_a_directory"
        except PermissionError:
            return "permission_denied"
        except OSError:
            return "root_unavailable"
        return None

    def _markdown_file_events(self) -> Iterable[dict[str, Any]]:
        permission_errors: list[str] = []

        def onerror(error: OSError) -> None:
            permission_errors.append(type(error).__name__)

        try:
            walker = os.walk(self._root, topdown=True, onerror=onerror, followlinks=False)
            for dirpath, dirnames, filenames in walker:
                current = Path(dirpath)
                safe_dirnames: list[str] = []
                for dirname in dirnames:
                    child = current / dirname
                    if dirname.startswith(".") or child.is_symlink():
                        yield {"status": "skipped"}
                        continue
                    safe_dirnames.append(dirname)
                dirnames[:] = safe_dirnames

                for filename in filenames:
                    path = current / filename
                    if path.is_symlink() or path.suffix.lower() != ".md":
                        yield {"status": "skipped"}
                        continue
                    yield {"status": "file", "path": path}

                while permission_errors:
                    permission_errors.pop()
                    yield {"status": "permission_denied"}
        except PermissionError:
            yield {"status": "permission_denied"}
        except OSError:
            yield {"status": "skipped"}

    def _item(
        self,
        *,
        rel: str,
        title: str,
        snippet: str,
        scope: str,
        score: int,
        replacement_used: bool,
    ) -> dict[str, Any]:
        digest = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:12]
        degraded_reasons = ["utf8_replacement"] if replacement_used else []
        item = {
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
            "adapter_protocol_version": self.adapter_protocol_version,
            "degraded": replacement_used,
            "degraded_reasons": degraded_reasons,
        }
        if replacement_used:
            item["degraded_note"] = "Invalid UTF-8 bytes were replaced while reading this markdown file."
        return item

    def _truncated_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
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
            "degraded": True,
            "degraded_reasons": ["scan_file_cap_reached"],
            "degraded_reason": "scan_file_cap_reached",
            "adapter_protocol_version": self.adapter_protocol_version,
            "scan_summary": dict(summary),
        }

    def _empty_result(
        self,
        reason: str,
        *,
        files_scanned: int = 0,
        files_skipped: int = 0,
        truncated: bool = False,
    ) -> list[dict[str, Any]]:
        self._set_scan_state(
            {
                "files_scanned": files_scanned,
                "files_skipped": files_skipped,
                "truncated": truncated,
                "reason": reason,
            },
            reason,
        )
        return []

    def _set_scan_state(self, summary: dict[str, Any], empty_reason: str | None) -> None:
        object.__setattr__(self, "_last_scan_summary", dict(summary))
        object.__setattr__(self, "_last_empty_reason", empty_reason)


__all__ = [
    "LOCAL_MARKDOWN_ADAPTER_NAME",
    "LocalMarkdownAdapter",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
