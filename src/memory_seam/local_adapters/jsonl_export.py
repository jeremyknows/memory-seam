"""Read-only first-party adapter for local JSONL/JSON exports."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
import json
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
    _safe_relative_path,
    _score,
    _snippet,
    _with_limit_note,
)

LOCAL_JSONL_EXPORT_ADAPTER_NAME = "local-jsonl-export"
JSON_EXPORT_EXTENSIONS = frozenset({".jsonl", ".json"})
MAX_RECORDS_PER_FILE = 10_000
TITLE_FIELDS = ("title", "name", "subject")
BODY_FIELDS = ("body", "text", "content")


@dataclass(frozen=True)
class LocalJsonlExportAdapter:
    """Structural SourceAdapter for local JSONL/JSON export files.

    The adapter never follows symlinks, writes indexes, starts services, calls
    networks, or reports absolute local paths.
    """

    root: str | Path
    title_field: str | None = None
    body_field: str | None = None
    adapter_name: str = LOCAL_JSONL_EXPORT_ADAPTER_NAME
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
        return self._items(query="", scope="context", n=MAX_SCAN_FILES, limit_note=None)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        effective_n, limit_note = _clamp_recall_n(n)
        return self._items(query=query, scope=scope, n=effective_n, limit_note=limit_note)

    def _items(self, *, query: str, scope: str, n: int, limit_note: dict[str, Any] | None) -> list[dict[str, Any]]:
        root_status = self._root_status()
        if root_status is not None:
            return self._empty_result(root_status, limit_note=limit_note)

        terms = _query_terms(query)
        matches: list[tuple[int, str, str, dict[str, Any]]] = []
        files_scanned = 0
        files_skipped = 0
        json_files_seen = 0
        records_seen = 0
        records_indexed = 0
        malformed_records = 0
        files_with_record_cap = 0
        truncated = False
        permission_denied = False

        for event in self._json_file_events():
            if event["status"] == "permission_denied":
                permission_denied = True
                files_skipped += 1
                continue
            if event["status"] != "file":
                files_skipped += 1
                continue

            json_files_seen += 1
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

            file_truncated = False
            for parsed in self._records_for_file(path=path, content=content):
                if parsed["status"] == "malformed":
                    malformed_records += 1
                    continue

                record_index = int(parsed["record_index"])
                records_seen += 1
                if record_index >= MAX_RECORDS_PER_FILE:
                    file_truncated = True
                    continue

                record = parsed["record"]
                title, body = _record_text(
                    record,
                    title_field=self.title_field,
                    body_field=self.body_field,
                    fallback_title=f"{Path(rel).stem} #{record_index}",
                )
                if not body and not title:
                    continue

                records_indexed += 1
                score, best_index = _score(title, body, terms)
                if score <= 0:
                    continue
                item = self._item(
                    rel=rel,
                    record_index=record_index,
                    title=title,
                    snippet=_snippet(body or title, terms, best_index),
                    scope=scope,
                    score=score,
                    replacement_used=replacement_used,
                )
                matches.append((score, title.lower(), rel, item))

            if file_truncated:
                files_with_record_cap += 1

        if json_files_seen == 0:
            reason = "permission_denied" if permission_denied else "zero_json_export_files"
            return self._empty_result(
                reason,
                files_scanned=files_scanned,
                files_skipped=files_skipped,
                records_seen=records_seen,
                records_indexed=records_indexed,
                malformed_records=malformed_records,
                files_with_record_cap=files_with_record_cap,
                truncated=truncated,
                limit_note=limit_note,
            )

        summary = {
            "files_scanned": files_scanned,
            "files_skipped": files_skipped,
            "records_seen": records_seen,
            "records_indexed": records_indexed,
            "malformed_records": malformed_records,
            "files_with_record_cap": files_with_record_cap,
            "truncated": truncated,
            "reason": None,
        }
        if not matches and not truncated and not files_with_record_cap:
            summary["reason"] = "zero_match"
            self._set_scan_state(_with_limit_note(summary, limit_note), "zero_match")
            return []
        summary = _with_limit_note(summary, limit_note)
        self._set_scan_state(summary, None)

        matches.sort(key=lambda match: (-match[0], match[1], match[2], match[3]["record_index"]))
        limit = max(0, int(n))
        items = [item for _, _, _, item in matches[:limit]]
        if files_with_record_cap:
            items.append(self._record_cap_item(scope=scope, summary=summary))
        if truncated:
            items.append(self._scan_truncated_item(scope=scope, summary=summary))
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

    def _json_file_events(self) -> Iterable[dict[str, Any]]:
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
                    if path.is_symlink() or path.suffix.lower() not in JSON_EXPORT_EXTENSIONS:
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

    def _records_for_file(self, *, path: Path, content: str) -> Iterator[dict[str, Any]]:
        if path.suffix.lower() == ".jsonl":
            record_index = 0
            for line in content.splitlines():
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    yield {"status": "malformed"}
                    continue
                if not isinstance(record, Mapping):
                    yield {"status": "malformed"}
                    continue
                yield {"status": "record", "record_index": record_index, "record": record}
                record_index += 1
            return

        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            yield {"status": "malformed"}
            return

        for record_index, record in enumerate(_records_from_json_payload(payload)):
            yield {"status": "record", "record_index": record_index, "record": record}

    def _item(
        self,
        *,
        rel: str,
        record_index: int,
        title: str,
        snippet: str,
        scope: str,
        score: int,
        replacement_used: bool,
    ) -> dict[str, Any]:
        degraded_reasons = ["utf8_replacement"] if replacement_used else []
        item = {
            "id": f"local-jsonl:{rel}#{record_index}",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_jsonl_export",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_jsonl_export_scan",
            "canonicality": "user_folder",
            "private_class": "user_local_reportable_path",
            "title": title,
            "path": rel,
            "record_index": record_index,
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
            item["degraded_note"] = "Invalid UTF-8 bytes were replaced while reading this JSON export file."
        return item

    def _record_cap_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": "local-jsonl-record-cap-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_jsonl_export",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_jsonl_export_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local JSON export record cap reached",
            "path": "",
            "snippet": f"One or more JSON export files were capped at {MAX_RECORDS_PER_FILE} records; narrow the export for complete recall.",
            "score": 0,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": True,
            "degraded": True,
            "degraded_reasons": ["record_cap_reached"],
            "degraded_reason": "record_cap_reached",
            "adapter_protocol_version": self.adapter_protocol_version,
            "scan_summary": dict(summary),
        }

    def _scan_truncated_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": "local-jsonl-scan-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_jsonl_export",
            "backend": "local_filesystem_read_only",
            "retrieval_backend": "recursive_jsonl_export_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local JSON export scan truncated",
            "path": "",
            "snippet": f"Scan stopped after {MAX_SCAN_FILES} JSON export files; narrow the folder or query for complete recall.",
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
        records_seen: int = 0,
        records_indexed: int = 0,
        malformed_records: int = 0,
        files_with_record_cap: int = 0,
        truncated: bool = False,
        limit_note: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        self._set_scan_state(
            _with_limit_note(
                {
                    "files_scanned": files_scanned,
                    "files_skipped": files_skipped,
                    "records_seen": records_seen,
                    "records_indexed": records_indexed,
                    "malformed_records": malformed_records,
                    "files_with_record_cap": files_with_record_cap,
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


def _records_from_json_payload(payload: Any) -> Iterator[Mapping[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, Mapping):
                yield item
        return
    if not isinstance(payload, Mapping):
        return
    for key in ("records", "items", "data"):
        records = payload.get(key)
        if isinstance(records, list):
            for item in records:
                if isinstance(item, Mapping):
                    yield item
            return
    yield payload


def _record_text(
    record: Mapping[str, Any],
    *,
    title_field: str | None,
    body_field: str | None,
    fallback_title: str,
) -> tuple[str, str]:
    title = _field_text(record, title_field)
    if not title:
        title = _first_field_text(record, TITLE_FIELDS)
    body = _field_text(record, body_field)
    if not body:
        body = _first_field_text(record, BODY_FIELDS)
    if not body:
        body = _compact_json(record)
    return title or fallback_title, body


def _first_field_text(record: Mapping[str, Any], fields: Iterable[str]) -> str:
    for field in fields:
        text = _field_text(record, field)
        if text:
            return text
    return ""


def _field_text(record: Mapping[str, Any], field: str | None) -> str:
    if not field or field not in record:
        return ""
    value = record[field]
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, int | float | bool):
        return str(value)
    return _compact_json(value)


def _compact_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except TypeError:
        return str(value)


__all__ = [
    "JSON_EXPORT_EXTENSIONS",
    "LOCAL_JSONL_EXPORT_ADAPTER_NAME",
    "LocalJsonlExportAdapter",
    "MAX_FILE_BYTES",
    "MAX_RECORDS_PER_FILE",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
