from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from memory_seam.local_adapters.factory import LOCAL_ADAPTERS, build_local_adapter
from memory_seam.local_adapters.git_tree import LocalGitTreeAdapter
from memory_seam.local_adapters.jsonl_export import LocalJsonlExportAdapter
from memory_seam.local_adapters.markdown import LocalMarkdownAdapter
from memory_seam.local_adapters.plaintext import LocalPlainTextAdapter
from memory_seam.local_adapters.sqlite_notes import LocalSqliteAdapter


def test_local_adapter_registry_is_single_source_of_truth():
    assert tuple(LOCAL_ADAPTERS) == ("markdown", "plaintext", "jsonl", "git-tree", "sqlite")


@pytest.mark.parametrize(
    ("name", "expected_type"),
    [
        ("markdown", LocalMarkdownAdapter),
        ("plaintext", LocalPlainTextAdapter),
        ("jsonl", LocalJsonlExportAdapter),
        ("git-tree", LocalGitTreeAdapter),
    ],
)
def test_build_local_adapter_constructs_folder_adapters(name: str, expected_type: type, tmp_path: Path):
    adapter = build_local_adapter(name, tmp_path)

    assert isinstance(adapter, expected_type)


def test_build_local_adapter_constructs_sqlite_adapter_with_explicit_mapping(tmp_path: Path):
    db_path = tmp_path / "notes.db"
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE notes(note_id INTEGER PRIMARY KEY, title TEXT, body TEXT)")

    adapter = build_local_adapter(
        "sqlite",
        db_path,
        table="notes",
        title_column="title",
        body_column="body",
        id_column="note_id",
    )

    assert isinstance(adapter, LocalSqliteAdapter)


def test_build_local_adapter_unknown_name_lists_valid_adapters(tmp_path: Path):
    with pytest.raises(ValueError, match="unknown local adapter 'word-docs'; valid adapters: markdown, plaintext, jsonl, git-tree, sqlite"):
        build_local_adapter("word-docs", tmp_path)


@pytest.mark.parametrize("missing", ["table", "title_column", "body_column"])
def test_build_local_adapter_sqlite_names_missing_required_kwargs(missing: str, tmp_path: Path):
    config = {"table": "notes", "title_column": "title", "body_column": "body"}
    config[missing] = None

    with pytest.raises(ValueError) as excinfo:
        build_local_adapter("sqlite", tmp_path / "notes.db", **config)

    message = str(excinfo.value)
    assert "sqlite adapter requires explicit kwargs: table, title_column, body_column" in message
    assert f"missing {missing}" in message
