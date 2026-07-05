"""Read-only first-party adapter for tracked files in the current Git tree."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import hashlib
from pathlib import Path, PurePosixPath
import stat as stat_module
import subprocess
from typing import Any

from memory_seam.adapters import ADAPTER_PROTOCOL_VERSION
from memory_seam.local_adapters.markdown import (
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    MAX_SNIPPET_CHARS,
    _empty_summary,
    _query_terms,
    _score,
    _snippet,
    _title_for,
)
from memory_seam.local_adapters.plaintext import _normalize_extension

LOCAL_GIT_TREE_ADAPTER_NAME = "local-git-current-tree"
DEFAULT_GIT_TREE_EXTENSIONS = (
    ".md",
    ".txt",
    ".rst",
    ".py",
    ".js",
    ".ts",
    ".toml",
    ".yaml",
    ".json",
    ".cfg",
    ".ini",
)
GIT_TREE_ADAPTER_PROTOCOL_VERSION = ADAPTER_PROTOCOL_VERSION
PRISM_POSTURE_RULINGS = {
    "current_tree": "BINDING",
    "history": "REJECTED",
    "enumeration": "git_ls_files_z_only",
}


@dataclass(frozen=True)
class LocalGitTreeAdapter:
    """Structural SourceAdapter for tracked text files in a local Git tree.

    The adapter enumerates only the current tracked tree with
    ``git -C <root> ls-files -z``. It never reads ``.git`` directly, asks for
    history, follows submodules, writes indexes, starts services, or reports
    absolute local paths.
    """

    root: str | Path
    extension_allowlist: Iterable[str] = DEFAULT_GIT_TREE_EXTENSIONS
    adapter_name: str = LOCAL_GIT_TREE_ADAPTER_NAME
    adapter_protocol_version: str = GIT_TREE_ADAPTER_PROTOCOL_VERSION
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
        return self._items(query="", scope="context", n=MAX_SCAN_FILES)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        return self._items(query=query, scope=scope, n=n)

    def _items(self, *, query: str, scope: str, n: int) -> list[dict[str, Any]]:
        root_status = self._root_status()
        if root_status is not None:
            return self._empty_result(root_status)

        listing = self._git_ls_files()
        if listing["status"] != "ok":
            return self._empty_result(str(listing["reason"]))

        terms = _query_terms(query)
        matches: list[tuple[int, str, dict[str, Any]]] = []
        files_scanned = 0
        files_skipped = 0
        binary_files_skipped = 0
        gitlinks_skipped = 0
        text_candidates_seen = 0
        truncated = False

        for raw_rel in listing["paths"]:
            rel = _safe_git_relative_path(str(raw_rel))
            if rel is None:
                files_skipped += 1
                continue
            if PurePosixPath(rel).suffix.lower() not in self._extensions:
                files_skipped += 1
                continue

            text_candidates_seen += 1
            if files_scanned >= MAX_SCAN_FILES:
                truncated = True
                break

            path = self._root.joinpath(*PurePosixPath(rel).parts)
            try:
                stat = path.stat(follow_symlinks=False)
            except OSError:
                files_skipped += 1
                continue
            if not stat_module.S_ISREG(stat.st_mode):
                files_skipped += 1
                if stat_module.S_ISDIR(stat.st_mode):
                    gitlinks_skipped += 1
                continue

            files_scanned += 1
            if stat.st_size > MAX_FILE_BYTES:
                files_skipped += 1
                continue

            try:
                raw = path.read_bytes()
            except PermissionError:
                files_skipped += 1
                continue
            except OSError:
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

        if text_candidates_seen == 0:
            return self._empty_result(
                "zero_git_text_files",
                files_scanned=files_scanned,
                files_skipped=files_skipped,
                binary_files_skipped=binary_files_skipped,
                gitlinks_skipped=gitlinks_skipped,
                truncated=truncated,
            )

        summary = {
            "files_scanned": files_scanned,
            "files_skipped": files_skipped,
            "binary_files_skipped": binary_files_skipped,
            "gitlinks_skipped": gitlinks_skipped,
            "truncated": truncated,
            "reason": None,
            "posture_rulings": dict(PRISM_POSTURE_RULINGS),
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

    def _git_ls_files(self) -> dict[str, Any]:
        try:
            result = subprocess.run(
                ["git", "-C", str(self._root), "ls-files", "-z"],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except FileNotFoundError:
            return {"status": "error", "reason": "git_unavailable"}
        except (OSError, subprocess.SubprocessError):
            return {"status": "error", "reason": "git_unavailable"}

        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace").lower()
            reason = "not_a_git_repository" if "not a git repository" in stderr else "git_unavailable"
            return {"status": "error", "reason": reason}

        paths = [entry.decode("utf-8", errors="replace") for entry in result.stdout.split(b"\x00") if entry]
        return {"status": "ok", "paths": paths}

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
            "id": f"local-git-tree-{digest}",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_git_current_tree",
            "backend": "local_git_read_only",
            "retrieval_backend": "git_current_tree_scan",
            "canonicality": "git_tracked_current_tree",
            "private_class": "user_local_reportable_path",
            "title": title,
            "path": rel,
            "snippet": snippet[:MAX_SNIPPET_CHARS],
            "score": score,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": False,
            "adapter_protocol_version": self.adapter_protocol_version,
            "posture_rulings": dict(PRISM_POSTURE_RULINGS),
            "degraded": replacement_used,
            "degraded_reasons": degraded_reasons,
        }
        if replacement_used:
            item["degraded_note"] = "Invalid UTF-8 bytes were replaced while reading this tracked Git file."
        return item

    def _truncated_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": "local-git-tree-scan-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_git_current_tree",
            "backend": "local_git_read_only",
            "retrieval_backend": "git_current_tree_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local Git current-tree scan truncated",
            "path": "",
            "snippet": f"Scan stopped after {MAX_SCAN_FILES} tracked text files; narrow the repository or query for complete recall.",
            "score": 0,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": True,
            "degraded": True,
            "degraded_reasons": ["scan_file_cap_reached"],
            "degraded_reason": "scan_file_cap_reached",
            "adapter_protocol_version": self.adapter_protocol_version,
            "posture_rulings": dict(PRISM_POSTURE_RULINGS),
            "scan_summary": dict(summary),
        }

    def _empty_result(
        self,
        reason: str,
        *,
        files_scanned: int = 0,
        files_skipped: int = 0,
        binary_files_skipped: int = 0,
        gitlinks_skipped: int = 0,
        truncated: bool = False,
    ) -> list[dict[str, Any]]:
        self._set_scan_state(
            {
                "files_scanned": files_scanned,
                "files_skipped": files_skipped,
                "binary_files_skipped": binary_files_skipped,
                "gitlinks_skipped": gitlinks_skipped,
                "truncated": truncated,
                "reason": reason,
                "posture_rulings": dict(PRISM_POSTURE_RULINGS),
            },
            reason,
        )
        return []

    def _set_scan_state(self, summary: dict[str, Any], empty_reason: str | None) -> None:
        object.__setattr__(self, "_last_scan_summary", dict(summary))
        object.__setattr__(self, "_last_empty_reason", empty_reason)


def _safe_git_relative_path(value: str) -> str | None:
    if not value or "\\" in value or value.startswith("/"):
        return None
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or rel.as_posix() != value:
        return None
    return value


__all__ = [
    "DEFAULT_GIT_TREE_EXTENSIONS",
    "GIT_TREE_ADAPTER_PROTOCOL_VERSION",
    "LOCAL_GIT_TREE_ADAPTER_NAME",
    "LocalGitTreeAdapter",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
    "PRISM_POSTURE_RULINGS",
]
