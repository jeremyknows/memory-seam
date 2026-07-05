"""Read-only first-party adapter for local plain-text folders."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path
from typing import Any

from memory_seam.adapters import ADAPTER_PROTOCOL_VERSION
from memory_seam.local_adapters.markdown import (
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    MAX_SNIPPET_CHARS,
    _empty_summary,
    _clamp_recall_n,
    _query_terms,
    _read_regular_file_no_follow,
    _safe_relative_path,
    _scan_notice,
    _score,
    _snippet,
    _title_for,
    _with_limit_note,
)

LOCAL_PLAINTEXT_ADAPTER_NAME = "local-plain-text-folder"
DEFAULT_PLAINTEXT_EXTENSIONS = (".txt", ".md", ".rst", ".log")


@dataclass(frozen=True)
class LocalPlainTextAdapter:
    """Structural SourceAdapter for a local folder of plain-text files.

    The adapter never follows symlinks, writes indexes, starts services, calls
    networks, or reports absolute local paths.
    """

    root: str | Path
    extension_allowlist: Iterable[str] = DEFAULT_PLAINTEXT_EXTENSIONS
    adapter_name: str = LOCAL_PLAINTEXT_ADAPTER_NAME
    adapter_protocol_version: str = ADAPTER_PROTOCOL_VERSION
    _root: Path = field(init=False, repr=False)
    _extensions: frozenset[str] = field(init=False, repr=False)
    _last_scan_summary: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _last_empty_reason: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_root", Path(self.root).expanduser().absolute())
        object.__setattr__(
            self,
            "_extensions",
            frozenset(_normalize_extension(extension) for extension in self.extension_allowlist),
        )
        self._set_scan_state(_empty_summary("not_scanned"), "not_scanned")

    @property
    def last_scan_summary(self) -> dict[str, Any]:
        return dict(self._last_scan_summary)

    @property
    def last_empty_reason(self) -> str | None:
        return self._last_empty_reason

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        return self._items(query="", scope="context", n=MAX_SCAN_FILES, limit_note=None)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        effective_n, limit_note = _clamp_recall_n(n)
        return self._items(query=query, scope=scope, n=effective_n, limit_note=limit_note)

    def _items(self, *, query: str, scope: str, n: int, limit_note: dict[str, Any] | None) -> list[dict[str, Any]]:
        root_status = self._root_status()
        if root_status is not None:
            return self._empty_result(root_status, limit_note=limit_note)

        terms = _query_terms(query)
        if scope != "context" and not terms:
            return self._empty_result("empty_query", limit_note=limit_note)
        matches: list[tuple[int, str, dict[str, Any]]] = []
        files_scanned = 0
        files_skipped = 0
        binary_files_skipped = 0
        plaintext_seen = 0
        truncated = False
        permission_denied = False

        for event in self._text_file_events():
            if event["status"] == "permission_denied":
                permission_denied = True
                files_skipped += 1
                continue
            if event["status"] != "file":
                files_skipped += 1
                continue

            plaintext_seen += 1
            if files_scanned >= MAX_SCAN_FILES:
                truncated = True
                break

            path = event["path"]
            files_scanned += 1
            rel = _safe_relative_path(path, self._root)
            if rel is None:
                files_skipped += 1
                continue

            read_status, raw = _read_regular_file_no_follow(path)
            if read_status == "permission_denied":
                permission_denied = True
                files_skipped += 1
                continue
            if read_status != "ok" or raw is None:
                files_skipped += 1
                continue

            if b"\x00" in raw[: min(len(raw), 4096)]:
                files_skipped += 1
                binary_files_skipped += 1
                continue

            replacement_used = False
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("utf-8", errors="replace")
                replacement_used = True

            title = _title_for(path, content)
            score, best_index = _score(title, content, terms, match_all_if_empty=scope == "context")
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
            matches.append((score, title.casefold(), item))

        if plaintext_seen == 0:
            reason = "permission_denied" if permission_denied else "zero_plaintext_files"
            return self._empty_result(
                reason,
                files_scanned=files_scanned,
                files_skipped=files_skipped,
                truncated=truncated,
                binary_files_skipped=binary_files_skipped,
                limit_note=limit_note,
            )

        summary = {
            "files_scanned": files_scanned,
            "files_skipped": files_skipped,
            "binary_files_skipped": binary_files_skipped,
            "truncated": truncated,
            "reason": None,
        }
        if truncated:
            summary["scan_notice"] = _scan_notice(
                "scan_file_cap_reached",
                "Local plain-text scan truncated",
                f"Scan stopped after {MAX_SCAN_FILES} plain-text files; narrow the folder or query for complete recall.",
            )
        if not matches and not truncated:
            summary["reason"] = "zero_match"
            self._set_scan_state(_with_limit_note(summary, limit_note), "zero_match")
            return []
        summary = _with_limit_note(summary, limit_note)
        self._set_scan_state(summary, None)

        matches.sort(key=lambda match: (-match[0], match[1], match[2]["path"]))
        limit = max(0, int(n))
        return [item for _, _, item in matches[:limit]]

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

    def _text_file_events(self) -> Iterable[dict[str, Any]]:
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
                    if path.is_symlink() or path.suffix.lower() not in self._extensions:
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
            "id": f"local-text-{digest}",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_plaintext",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_plaintext_scan",
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
            item["degraded_note"] = "Invalid UTF-8 bytes were replaced while reading this text file."
        return item

    def _truncated_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": "local-text-scan-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_plaintext",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_plaintext_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local plain-text scan truncated",
            "path": "",
            "snippet": f"Scan stopped after {MAX_SCAN_FILES} plain-text files; narrow the folder or query for complete recall.",
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
        binary_files_skipped: int = 0,
        truncated: bool = False,
        limit_note: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        self._set_scan_state(
            _with_limit_note(
                {
                    "files_scanned": files_scanned,
                    "files_skipped": files_skipped,
                    "binary_files_skipped": binary_files_skipped,
                    "truncated": truncated,
                    "reason": reason,
                },
                limit_note,
            ),
            reason,
        )
        return []

    def _set_scan_state(self, summary: dict[str, Any], empty_reason: str | None) -> None:
        object.__setattr__(self, "_last_scan_summary", dict(summary))
        object.__setattr__(self, "_last_empty_reason", empty_reason)


def _normalize_extension(extension: str) -> str:
    normalized = extension.strip().lower()
    if not normalized:
        return normalized
    if not normalized.startswith("."):
        return f".{normalized}"
    return normalized


__all__ = [
    "DEFAULT_PLAINTEXT_EXTENSIONS",
    "LOCAL_PLAINTEXT_ADAPTER_NAME",
    "LocalPlainTextAdapter",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
