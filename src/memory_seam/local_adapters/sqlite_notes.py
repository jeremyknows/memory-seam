"""Read-only first-party adapter for explicitly mapped local SQLite notes."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import os
from pathlib import Path
import sqlite3
from typing import Any
from urllib.parse import quote

from memory_seam.adapters import ADAPTER_PROTOCOL_VERSION
from memory_seam.local_adapters.markdown import (
    MAX_SNIPPET_CHARS,
    _clamp_recall_n,
    _empty_summary,
    _query_terms,
    _scan_notice,
    _score,
    _snippet,
    _with_limit_note,
)

LOCAL_SQLITE_ADAPTER_NAME = "local-sqlite-notes"
DEFAULT_ROW_CAP = 5_000
DEFAULT_PROGRESS_OP_LIMIT = 100_000
SQLITE_PROGRESS_STEP = 1_000

SENSITIVE_APP_CACHE_SUFFIXES = (
    ("Library", "Messages"),
    ("Library", "Mail"),
    ("Library", "Safari"),
    ("Library", "Caches"),
    ("Library", "Application Support", "Google", "Chrome"),
    ("Library", "Application Support", "Firefox"),
    ("Library", "Application Support", "Mozilla", "Firefox"),
)


@dataclass(frozen=True)
class LocalSqliteAdapter:
    """Structural SourceAdapter for a deliberately copied SQLite notes table.

    The adapter requires explicit table/column mapping. It never autodetects
    schema, opens write-capable connections, attaches databases, or reports the
    absolute database path.
    """

    db_path: str | Path
    table: str
    title_column: str
    body_column: str
    id_column: str | None = None
    row_cap: int = DEFAULT_ROW_CAP
    statement_op_limit: int = DEFAULT_PROGRESS_OP_LIMIT
    adapter_name: str = LOCAL_SQLITE_ADAPTER_NAME
    adapter_protocol_version: str = ADAPTER_PROTOCOL_VERSION
    _db_path: Path = field(init=False, repr=False)
    _last_scan_summary: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _last_empty_reason: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_db_path", Path(self.db_path).expanduser().absolute())
        _require_identifier(self.table, "table")
        _require_identifier(self.title_column, "title_column")
        _require_identifier(self.body_column, "body_column")
        if self.id_column is not None:
            _require_identifier(self.id_column, "id_column")
        if int(self.row_cap) <= 0:
            raise ValueError("row_cap must be positive")
        if int(self.statement_op_limit) <= 0:
            raise ValueError("statement_op_limit must be positive")
        self._set_scan_state(_empty_summary("not_scanned"), "not_scanned")

    @classmethod
    def list_tables(cls, db_path: str | Path) -> list[str]:
        """Return user table names from sqlite_master using a read-only connection."""

        path = Path(db_path).expanduser().absolute()
        if _is_sensitive_app_cache_path(path):
            raise ValueError("sensitive_app_cache_blocked")
        if _has_symlink_component(path):
            raise ValueError("database_symlink_blocked")
        with _open_read_only_connection(path) as connection:
            rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ? ORDER BY name",
                ("table", "sqlite_%"),
            ).fetchall()
        return [str(row[0]) for row in rows]

    @property
    def last_scan_summary(self) -> dict[str, Any]:
        return dict(self._last_scan_summary)

    @property
    def last_empty_reason(self) -> str | None:
        return self._last_empty_reason

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        return self._items(query="", scope="context", n=self.row_cap, limit_note=None)

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        effective_n, limit_note = _clamp_recall_n(n)
        return self._items(query=query, scope=scope, n=effective_n, limit_note=limit_note)

    def _items(self, *, query: str, scope: str, n: int, limit_note: dict[str, Any] | None) -> list[dict[str, Any]]:
        path_status = self._path_status()
        if path_status is not None:
            return self._empty_result(path_status, limit_note=limit_note)

        timed_out = {"value": False}
        try:
            with _open_read_only_connection(self._db_path) as connection:
                self._install_progress_handler(connection, timed_out)
                rows = connection.execute(self._select_sql(), (int(self.row_cap),)).fetchall()
        except (PermissionError, sqlite3.Error, OSError) as error:
            return self._empty_result(_friendly_reason(error, timed_out=timed_out["value"]), limit_note=limit_note)

        terms = _query_terms(query)
        if scope != "context" and not terms:
            return self._empty_result("empty_query", limit_note=limit_note)
        matches: list[tuple[int, str, str, dict[str, Any]]] = []
        rows_seen = len(rows)
        rows_indexed = 0
        truncated = rows_seen >= int(self.row_cap)

        for row in rows:
            row_identity = _value_text(row["__memory_seam_rowid"])
            title = _value_text(row["__memory_seam_title"])
            body = _value_text(row["__memory_seam_body"])
            if not row_identity:
                row_identity = str(rows_indexed)
            if not title and not body:
                continue

            rows_indexed += 1
            score, best_index = _score(title, body, terms, match_all_if_empty=scope == "context")
            if score <= 0:
                continue
            item = self._item(
                row_identity=row_identity,
                title=title or f"{self.table} row {row_identity}",
                snippet=_snippet(body or title, terms, best_index),
                scope=scope,
                score=score,
            )
            matches.append((score, item["title"].casefold(), item["path"], item))

        if rows_seen == 0:
            return self._empty_result("zero_rows", rows_scanned=0, rows_indexed=0, truncated=False, limit_note=limit_note)

        summary = {
            "rows_scanned": rows_seen,
            "rows_indexed": rows_indexed,
            "row_cap": int(self.row_cap),
            "truncated": truncated,
            "reason": None,
        }
        if truncated:
            summary["scan_notice"] = _scan_notice(
                "row_cap_reached",
                "Local SQLite row cap reached",
                f"SQLite table scan stopped at {int(self.row_cap)} rows; narrow the copied database table for complete recall.",
            )
        if not matches and not truncated:
            summary["reason"] = "zero_match"
            self._set_scan_state(_with_limit_note(summary, limit_note), "zero_match")
            return []
        summary = _with_limit_note(summary, limit_note)
        self._set_scan_state(summary, None)

        matches.sort(key=lambda match: (-match[0], match[1], match[2]))
        limit = max(0, int(n))
        return [item for _, _, _, item in matches[:limit]]

    def _path_status(self) -> str | None:
        if _is_sensitive_app_cache_path(self._db_path):
            return "sensitive_app_cache_blocked"
        try:
            if _has_symlink_component(self._db_path):
                return "database_symlink_blocked"
            if not self._db_path.exists():
                return "missing_database"
            if not self._db_path.is_file():
                return "not_a_file"
            _validated_database_path(self._db_path)
        except PermissionError:
            return "permission_denied"
        except OSError:
            return "database_unavailable"
        return None

    def _select_sql(self) -> str:
        row_id = _quote_identifier(self.id_column) if self.id_column else "rowid"
        return (
            "SELECT "
            f"{row_id} AS __memory_seam_rowid, "
            f"{_quote_identifier(self.title_column)} AS __memory_seam_title, "
            f"{_quote_identifier(self.body_column)} AS __memory_seam_body "
            f"FROM {_quote_identifier(self.table)} "
            "LIMIT ?"
        )

    def _install_progress_handler(self, connection: sqlite3.Connection, timed_out: dict[str, bool]) -> None:
        remaining = max(1, int(self.statement_op_limit) // SQLITE_PROGRESS_STEP)

        def progress() -> int:
            nonlocal remaining
            remaining -= 1
            if remaining <= 0:
                timed_out["value"] = True
                return 1
            return 0

        connection.set_progress_handler(progress, SQLITE_PROGRESS_STEP)

    def _item(self, *, row_identity: str, title: str, snippet: str, scope: str, score: int) -> dict[str, Any]:
        rel = f"{self.table}/{_path_segment(row_identity)}"
        return {
            "id": f"local-sqlite:{rel}",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_sqlite_notes",
            "backend": "local_sqlite_read_only",
            "retrieval_backend": "sqlite_table_scan",
            "canonicality": "user_copied_database",
            "private_class": "user_local_reportable_row",
            "title": title,
            "path": rel,
            "snippet": snippet[:MAX_SNIPPET_CHARS],
            "score": score,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": False,
            "adapter_protocol_version": self.adapter_protocol_version,
            "degraded": False,
            "degraded_reasons": [],
        }

    def _row_cap_item(self, *, scope: str, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": "local-sqlite-row-cap-truncated",
            "scope": scope,
            "include_family": "memory",
            "source_tier": "local_sqlite_notes",
            "backend": "local_sqlite_read_only",
            "retrieval_backend": "sqlite_table_scan",
            "canonicality": "scan_notice",
            "private_class": "reportable_scan_notice",
            "title": "Local SQLite row cap reached",
            "path": "",
            "snippet": f"SQLite table scan stopped at {int(self.row_cap)} rows; narrow the copied database table for complete recall.",
            "score": 0,
            "redaction_applied": False,
            "redaction_labels": [],
            "truncated": True,
            "degraded": True,
            "degraded_reasons": ["row_cap_reached"],
            "degraded_reason": "row_cap_reached",
            "adapter_protocol_version": self.adapter_protocol_version,
            "scan_summary": dict(summary),
        }

    def _empty_result(
        self,
        reason: str,
        *,
        rows_scanned: int = 0,
        rows_indexed: int = 0,
        truncated: bool = False,
        limit_note: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        self._set_scan_state(
            _with_limit_note(
                {
                    "rows_scanned": rows_scanned,
                    "rows_indexed": rows_indexed,
                    "row_cap": int(self.row_cap),
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


def _open_read_only_connection(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(_readonly_uri(_validated_database_path(path)), uri=True, timeout=0.05)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    return connection


def _validated_database_path(path: Path) -> Path:
    expanded = path.expanduser().absolute()
    if _has_symlink_component(expanded):
        raise PermissionError("database symlink blocked")
    approved_root = expanded.parent.resolve(strict=True)
    resolved = Path(os.path.realpath(expanded, strict=True))
    try:
        resolved.relative_to(approved_root)
    except ValueError as exc:
        raise PermissionError("database path escaped approved root") from exc
    if not resolved.is_file():
        raise PermissionError("database is not a regular file")
    return resolved


def _readonly_uri(path: Path) -> str:
    return f"file:{quote(path.as_posix(), safe='/')}?mode=ro"


def _quote_identifier(identifier: str | None) -> str:
    if identifier is None:
        raise ValueError("identifier is required")
    return '"' + identifier.replace('"', '""') + '"'


def _require_identifier(identifier: str, field_name: str) -> None:
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError(f"{field_name} is required")
    if "\x00" in identifier or "/" in identifier or "\\" in identifier:
        raise ValueError(f"{field_name} must be a single SQLite identifier")


def _value_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return " ".join(str(value).split())


def _path_segment(value: str) -> str:
    encoded = quote(value, safe="-._~")
    return encoded or "row"


def _is_sensitive_app_cache_path(path: Path) -> bool:
    expanded = path.expanduser().absolute()
    try:
        parts = Path(os.path.realpath(expanded, strict=True)).parts
    except OSError:
        parts = expanded.parts
    parts = tuple(part.casefold() for part in parts)
    for suffix in SENSITIVE_APP_CACHE_SUFFIXES:
        folded_suffix = tuple(part.casefold() for part in suffix)
        length = len(folded_suffix)
        for index in range(0, len(parts) - length + 1):
            if parts[index : index + length] == folded_suffix:
                return True
    return False


def _has_symlink_component(path: Path) -> bool:
    expanded = path.expanduser().absolute()
    parts = expanded.parts
    if not parts:
        return False
    current = Path(parts[0])
    for part in parts[1:]:
        current = current / part
        try:
            if current.is_symlink():
                return True
        except OSError:
            return False
    return False


def _friendly_reason(error: BaseException, *, timed_out: bool = False) -> str:
    if timed_out:
        return "statement_timeout"
    message = str(error).lower()
    if "no such table" in message:
        return "missing_table"
    if "no such column" in message:
        return "missing_column"
    if "locked" in message or "busy" in message:
        return "database_locked"
    if "readonly" in message or "not authorized" in message:
        return "read_only_violation"
    if "permission" in message or "access" in message:
        return "permission_denied"
    if "unable to open database file" in message:
        return "database_unavailable"
    if "interrupted" in message:
        return "statement_timeout"
    return "database_unavailable"


__all__ = [
    "DEFAULT_PROGRESS_OP_LIMIT",
    "DEFAULT_ROW_CAP",
    "LOCAL_SQLITE_ADAPTER_NAME",
    "LocalSqliteAdapter",
    "MAX_SNIPPET_CHARS",
    "SENSITIVE_APP_CACHE_SUFFIXES",
]
