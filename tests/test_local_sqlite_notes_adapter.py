from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

from memory_seam import (
    ADAPTER_PROTOCOL_VERSION,
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)
from memory_seam.local_adapters.sqlite_notes import LocalSqliteAdapter, _open_read_only_connection

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification_for_local_sqlite", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified


def test_local_sqlite_adapter_passes_lane_a_certification(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(
        db_path,
        [
            (1, "Authority", "Receipt-first local sqlite recall proves authority."),
            (2, "Outside", "memory seam certification zero match"),
        ],
    )

    assert_source_adapter_certified(
        LocalSqliteAdapter(
            db_path=db_path,
            table="notes",
            id_column="note_id",
            title_column="headline",
            body_column="body",
        ),
        tmp_path,
        config=AdapterCertificationConfig(
            recall_query="authority receipt",
            allowed_retrieval_backends=frozenset({"sqlite_table_scan"}),
        ),
    )


def test_adapter_declares_protocol_version(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [])

    adapter = LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
    )

    assert adapter.adapter_protocol_version == ADAPTER_PROTOCOL_VERSION


def test_explicit_mapping_and_id_column_define_items(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(
        db_path,
        [
            (42, "Launch Note", "The sqlite adapter uses explicit receipt mapping."),
            (43, "Other", "Unrelated content."),
        ],
    )

    items = LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
    ).recall_items("receipt", scope="wiki", token_subject=None, n=10)

    assert len(items) == 1
    assert items[0]["id"] == "local-sqlite:notes/42"
    assert items[0]["path"] == "notes/42"
    assert items[0]["title"] == "Launch Note"
    assert len(items[0]["snippet"]) <= 200
    assert "receipt mapping" in items[0]["snippet"]


def test_read_only_connection_rejects_write_attempt(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [(1, "Title", "Body")])

    with _open_read_only_connection(db_path) as connection:
        with pytest.raises(sqlite3.OperationalError):
            connection.execute("INSERT INTO notes(note_id, headline, body) VALUES (?, ?, ?)", (2, "No", "Write"))


def test_sensitive_app_cache_blocklist_returns_empty_reason(tmp_path: Path):
    db_path = tmp_path / "Library" / "Messages" / "chat.db"
    db_path.parent.mkdir(parents=True)
    _create_notes_db(db_path, [(1, "Blocked", "needle")])

    adapter = LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
    )

    assert adapter.recall_items("needle", scope="wiki", token_subject=None, n=10) == []
    assert adapter.last_empty_reason == "sensitive_app_cache_blocked"
    assert adapter.last_scan_summary["reason"] == "sensitive_app_cache_blocked"


def test_locked_database_returns_friendly_empty_reason(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [(1, "Locked", "needle")])
    lock = sqlite3.connect(db_path)
    lock.execute("PRAGMA journal_mode=DELETE")
    lock.execute("BEGIN EXCLUSIVE")

    try:
        adapter = LocalSqliteAdapter(
            db_path=db_path,
            table="notes",
            id_column="note_id",
            title_column="headline",
            body_column="body",
        )
        items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)
    finally:
        lock.rollback()
        lock.close()

    assert items == []
    assert adapter.last_empty_reason == "database_locked"
    assert adapter.last_scan_summary["reason"] == "database_locked"


def test_missing_table_returns_friendly_empty_reason(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [(1, "Title", "Body")])

    adapter = LocalSqliteAdapter(
        db_path=db_path,
        table="missing_notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
    )

    assert adapter.context_items(include=["memory"], token_subject=None) == []
    assert adapter.last_empty_reason == "missing_table"
    assert adapter.last_scan_summary["reason"] == "missing_table"


def test_missing_table_reason_flows_into_runtime_empty_envelope(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [(1, "Title", "Body")])
    runtime = _runtime(
        LocalSqliteAdapter(
            db_path=db_path,
            table="missing_notes",
            id_column="note_id",
            title_column="headline",
            body_column="body",
        )
    )

    response = runtime.handle(RuntimeRequest("GET", "/context?include=memory"))
    body = response["body"]

    assert response["status_code"] == 200
    assert body["items"] == []
    assert body["reason"] == "missing_table"
    assert body["adapter_scan_summary"]["reason"] == "missing_table"


def test_row_cap_limits_scan_and_adds_truncation_notice(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(
        db_path,
        [
            (1, "One", "needle"),
            (2, "Two", "needle"),
            (3, "Three", "needle"),
        ],
    )

    adapter = LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
        row_cap=2,
    )
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items[:2]] == ["notes/1", "notes/2"]
    assert items[-1]["title"] == "Local SQLite row cap reached"
    assert items[-1]["truncated"] is True
    assert adapter.last_scan_summary["rows_scanned"] == 2
    assert adapter.last_scan_summary["truncated"] is True


def test_statement_progress_limit_returns_timeout_reason(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [(index, f"Title {index}", "needle") for index in range(20_000)])

    adapter = LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
        row_cap=20_000,
        statement_op_limit=1,
    )

    assert adapter.recall_items("needle", scope="wiki", token_subject=None, n=10) == []
    assert adapter.last_empty_reason == "statement_timeout"
    assert adapter.last_scan_summary["reason"] == "statement_timeout"


def test_list_tables_reads_schema_only(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    _create_notes_db(db_path, [])
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, title TEXT, body TEXT)")

    assert LocalSqliteAdapter.list_tables(db_path) == ["notes", "tasks"]


def _runtime(adapter: LocalSqliteAdapter) -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="local-sqlite-test"),
        provider=AdapterMemorySeamProvider(adapter, provider_name="local-sqlite-test"),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:test",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def _create_notes_db(db_path: Path, rows: list[tuple[int, str, str]]) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE notes(note_id INTEGER PRIMARY KEY, headline TEXT, body TEXT)")
        connection.executemany("INSERT INTO notes(note_id, headline, body) VALUES (?, ?, ?)", rows)
