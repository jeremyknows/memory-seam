from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import memory_seam.cli as cli_module
import memory_seam.local_adapters.markdown as markdown_module
from memory_seam import (
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)
from memory_seam.cli import local_adapter_response, main, no_live_response
from memory_seam.local_adapters.git_tree import LocalGitTreeAdapter
from memory_seam.local_adapters.jsonl_export import LocalJsonlExportAdapter
from memory_seam.local_adapters.markdown import LocalMarkdownAdapter
from memory_seam.local_adapters.plaintext import LocalPlainTextAdapter
from memory_seam.local_adapters.sqlite_notes import LocalSqliteAdapter
from memory_seam.receipts import build_receipt_summary


AdapterBuilder = Callable[[Path], Any]


def test_zero_match_diagnostics_for_each_local_adapter_class(tmp_path: Path):
    for name, builder in _zero_match_builders():
        adapter = builder(tmp_path / name)
        response = _runtime(adapter).handle(
            RuntimeRequest("GET", "/recall?query=needle&scope=wiki&n=5&read_receipt=metadata_only")
        )
        body = response["body"]

        assert body["items"] == []
        assert body["reason"] == "zero_match"
        assert body["recall_diagnostics"] == {
            "zero_reason": "zero_match",
            "files_scanned": 1,
            "files_skipped": 0,
            "truncated": False,
            "suggestion": "zero-match: scanned 1 files, none matched 'needle'",
        }
        assert body["read_receipt"]["usefulness_shape"]["verdict"] == "not_useful"
        assert body["receipt_summary"] == {
            "verdict": "not_useful",
            "reason_code": "disabled_baseline_better",
            "posture_verdict": "safe",
            "blocking_fields": [],
        }


def test_degradation_reasons_roll_up_from_adapter_items_and_scan_summary(monkeypatch, tmp_path: Path):
    (tmp_path / "bad.md").write_bytes(b"# Bad\n\nneedle \xff recall")
    utf8_body = _runtime(LocalMarkdownAdapter(tmp_path)).handle(
        RuntimeRequest("GET", "/recall?query=needle&scope=wiki&n=5&read_receipt=metadata_only")
    )["body"]

    assert utf8_body["degraded"] is True
    assert utf8_body["degraded_reasons"] == ["utf8_replacement"]

    capped_root = tmp_path / "capped"
    capped_root.mkdir()
    (capped_root / "a.md").write_text("# A\n\nneedle", encoding="utf-8")
    (capped_root / "b.md").write_text("# B\n\nneedle", encoding="utf-8")
    monkeypatch.setattr(markdown_module, "MAX_SCAN_FILES", 1)

    capped_body = _runtime(LocalMarkdownAdapter(capped_root)).handle(
        RuntimeRequest("GET", "/recall?query=needle&scope=wiki&n=5&read_receipt=metadata_only")
    )["body"]

    assert capped_body["degraded"] is True
    assert "scan_truncated" in capped_body["degraded_reasons"]


def test_human_cli_prints_warning_for_degraded_results(monkeypatch, tmp_path: Path, capsys):
    response = {
        "status_code": 200,
        "body": {
            "endpoint": "recall",
            "items": [{"title": "Agent Notes", "path": "notes.md", "snippet": "needle"}],
            "adapter_scan_summary": {"files_scanned": 1},
            "degraded_reasons": ["scan_truncated", "utf8_replacement"],
            "read_receipt": {
                "usefulness_shape": {
                    "verdict": "useful",
                    "reason_code": "safe_context_degraded",
                }
            },
        },
    }
    monkeypatch.setattr(cli_module, "local_adapter_response", lambda *args, **kwargs: response)

    assert main(["recall", str(tmp_path), "needle"]) == 0

    captured = capsys.readouterr()
    assert "WARNING: degraded result: scan_truncated, utf8_replacement" in captured.out
    assert "Receipt: verdict=useful; reason=safe_context_degraded;" in captured.out


def test_human_cli_prints_reason_rich_empty_result(tmp_path: Path):
    (tmp_path / "ignored.txt").write_text("needle lives outside markdown", encoding="utf-8")

    response = _run_cli("recall", str(tmp_path), "needle")

    assert response.returncode == 0
    assert "No matches. Scanned 0 markdown files (1 other files skipped) - wrong adapter? try --adapter plaintext" in response.stdout
    assert "No matches.\n" not in response.stdout


def test_receipt_summary_shape_and_hold_triggers(tmp_path: Path):
    (tmp_path / "notes.md").write_text("# Notes\n\nreceipt summary needle", encoding="utf-8")

    body = local_adapter_response("recall", root=tmp_path, query="needle", n=5)["body"]

    assert body["receipt_summary"] == {
        "verdict": "useful",
        "reason_code": "safe_context_sufficient",
        "posture_verdict": "safe",
        "blocking_fields": [],
    }
    assert build_receipt_summary(
        {
            "read_receipt": {
                "usefulness_shape": {
                    "verdict": "useful",
                    "reason_code": "safe_context_sufficient",
                }
            },
            "service_started": True,
        }
    ) == {
        "verdict": "useful",
        "reason_code": "safe_context_sufficient",
        "posture_verdict": "hold",
        "blocking_fields": ["service_started"],
    }
    assert no_live_response("context", include="project", mode="startup", agent=None, query="", scope="wiki", n=5)[
        "body"
    ]["receipt_summary"] == {
        "verdict": "missing",
        "reason_code": "receipt_missing",
        "posture_verdict": "hold",
        "blocking_fields": [],
    }


def test_recall_n_clamps_to_one_through_twenty_for_each_local_adapter_class(tmp_path: Path):
    for name, builder in _many_match_builders():
        low_adapter = builder(tmp_path / f"{name}-low")
        low_items = low_adapter.recall_items("needle", scope="wiki", token_subject=None, n=0)

        assert len(low_items) == 1
        assert low_adapter.last_scan_summary["n_requested"] == 0
        assert low_adapter.last_scan_summary["n_effective"] == 1
        assert "n clamped from 0 to 1" in low_adapter.last_scan_summary["n_limit_note"]

        high_adapter = builder(tmp_path / f"{name}-high")
        high_items = high_adapter.recall_items("needle", scope="wiki", token_subject=None, n=999)

        assert len(high_items) == 20
        assert high_adapter.last_scan_summary["n_requested"] == 999
        assert high_adapter.last_scan_summary["n_effective"] == 20
        assert "n clamped from 999 to 20" in high_adapter.last_scan_summary["n_limit_note"]

    limits_root = tmp_path / "limits-envelope"
    _markdown_many(limits_root)
    recall_body = local_adapter_response("recall", root=limits_root, query="needle", n=999)["body"]
    assert recall_body["limits"] == {"max_n": 20}


def _zero_match_builders() -> list[tuple[str, AdapterBuilder]]:
    return [
        ("markdown", _markdown_zero),
        ("plaintext", _plaintext_zero),
        ("jsonl", _jsonl_zero),
        ("git-tree", _git_zero),
        ("sqlite", _sqlite_zero),
    ]


def _many_match_builders() -> list[tuple[str, AdapterBuilder]]:
    return [
        ("markdown", _markdown_many),
        ("plaintext", _plaintext_many),
        ("jsonl", _jsonl_many),
        ("git-tree", _git_many),
        ("sqlite", _sqlite_many),
    ]


def _runtime(adapter: Any) -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="quick-wins-test"),
        provider=AdapterMemorySeamProvider(adapter, provider_name="quick-wins-test"),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:test",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def _markdown_zero(root: Path) -> LocalMarkdownAdapter:
    root.mkdir()
    (root / "alpha.md").write_text("# Alpha\n\nhaystack", encoding="utf-8")
    return LocalMarkdownAdapter(root)


def _plaintext_zero(root: Path) -> LocalPlainTextAdapter:
    root.mkdir()
    (root / "alpha.txt").write_text("haystack", encoding="utf-8")
    return LocalPlainTextAdapter(root)


def _jsonl_zero(root: Path) -> LocalJsonlExportAdapter:
    root.mkdir()
    (root / "alpha.jsonl").write_text(json.dumps({"title": "Alpha", "body": "haystack"}), encoding="utf-8")
    return LocalJsonlExportAdapter(root)


def _git_zero(root: Path) -> LocalGitTreeAdapter:
    _git_repo(root)
    (root / "alpha.txt").write_text("haystack", encoding="utf-8")
    _git(root, "add", "alpha.txt")
    return LocalGitTreeAdapter(root)


def _sqlite_zero(root: Path) -> LocalSqliteAdapter:
    root.mkdir()
    db_path = root / "notes.db"
    _create_notes_db(db_path, [(1, "Alpha", "haystack")])
    return _sqlite_adapter(db_path)


def _markdown_many(root: Path) -> LocalMarkdownAdapter:
    root.mkdir()
    for index in range(25):
        (root / f"{index:02d}.md").write_text(f"# Note {index}\n\nneedle", encoding="utf-8")
    return LocalMarkdownAdapter(root)


def _plaintext_many(root: Path) -> LocalPlainTextAdapter:
    root.mkdir()
    for index in range(25):
        (root / f"{index:02d}.txt").write_text("needle", encoding="utf-8")
    return LocalPlainTextAdapter(root)


def _jsonl_many(root: Path) -> LocalJsonlExportAdapter:
    root.mkdir()
    rows = [json.dumps({"title": f"Note {index}", "body": "needle"}) for index in range(25)]
    (root / "notes.jsonl").write_text("\n".join(rows), encoding="utf-8")
    return LocalJsonlExportAdapter(root)


def _git_many(root: Path) -> LocalGitTreeAdapter:
    _git_repo(root)
    for index in range(25):
        (root / f"{index:02d}.txt").write_text("needle", encoding="utf-8")
    _git(root, "add", ".")
    return LocalGitTreeAdapter(root)


def _sqlite_many(root: Path) -> LocalSqliteAdapter:
    root.mkdir()
    db_path = root / "notes.db"
    _create_notes_db(db_path, [(index, f"Note {index}", "needle") for index in range(25)])
    return _sqlite_adapter(db_path)


def _sqlite_adapter(db_path: Path) -> LocalSqliteAdapter:
    return LocalSqliteAdapter(
        db_path=db_path,
        table="notes",
        id_column="note_id",
        title_column="headline",
        body_column="body",
    )


def _create_notes_db(db_path: Path, rows: list[tuple[int, str, str]]) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE notes(note_id INTEGER PRIMARY KEY, headline TEXT, body TEXT)")
        connection.executemany("INSERT INTO notes(note_id, headline, body) VALUES (?, ?, ?)", rows)


def _git_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init")


def _git(cwd: Path, *args: str) -> None:
    git = shutil.which("git")
    assert git is not None, "git unavailable in test environment"
    result = subprocess.run(
        [git, *args],
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "memory_seam", *args],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
