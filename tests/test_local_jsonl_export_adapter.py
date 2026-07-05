from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import memory_seam.local_adapters.jsonl_export as jsonl_module
from memory_seam import ADAPTER_PROTOCOL_VERSION
from memory_seam.local_adapters.jsonl_export import (
    LocalJsonlExportAdapter,
    MAX_RECORDS_PER_FILE,
)

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification_for_local_jsonl_export", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified


def test_local_jsonl_export_adapter_passes_lane_a_certification(tmp_path: Path):
    _write_jsonl(
        tmp_path / "authority.jsonl",
        [{"title": "Authority", "body": "Receipt-first local export recall proves authority."}],
    )
    outside = tmp_path.parent / "outside-certification-note.jsonl"
    _write_jsonl(outside, [{"title": "Outside", "body": "memory seam certification zero match"}])
    (tmp_path / "outside.jsonl").symlink_to(outside)

    assert_source_adapter_certified(
        LocalJsonlExportAdapter(tmp_path),
        tmp_path,
        config=AdapterCertificationConfig(
            recall_query="authority receipt",
            allowed_retrieval_backends=frozenset({"recursive_jsonl_export_scan"}),
        ),
    )


def test_adapter_declares_protocol_version(tmp_path: Path):
    adapter = LocalJsonlExportAdapter(tmp_path)

    assert adapter.adapter_protocol_version == ADAPTER_PROTOCOL_VERSION


def test_explicit_field_mapping_wins_before_autodetect(tmp_path: Path):
    _write_jsonl(
        tmp_path / "export.jsonl",
        [
            {
                "title": "Autodetect title",
                "body": "autodetect body",
                "headline": "Explicit Title",
                "message": "needle lives in the explicit mapped body",
            }
        ],
    )

    items = LocalJsonlExportAdapter(tmp_path, title_field="headline", body_field="message").recall_items(
        "needle",
        scope="wiki",
        token_subject=None,
        n=10,
    )

    assert len(items) == 1
    assert items[0]["id"] == "local-jsonl:export.jsonl#0"
    assert items[0]["title"] == "Explicit Title"
    assert items[0]["path"] == "export.jsonl"
    assert items[0]["record_index"] == 0
    assert "explicit mapped body" in items[0]["snippet"]


def test_autodetect_reads_common_jsonl_and_json_shapes(tmp_path: Path):
    _write_jsonl(
        tmp_path / "messages.jsonl",
        [
            {"name": "Alpha", "text": "needle from jsonl text"},
            {"subject": "Beta", "content": "needle from jsonl content"},
        ],
    )
    (tmp_path / "array.json").write_text(
        json.dumps([{"title": "Gamma", "body": "needle from json array"}]),
        encoding="utf-8",
    )
    (tmp_path / "wrapped.json").write_text(
        json.dumps({"items": [{"title": "Delta", "body": "needle from wrapped items"}]}),
        encoding="utf-8",
    )

    items = LocalJsonlExportAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["title"] for item in items] == ["Alpha", "Beta", "Delta", "Gamma"]
    assert [item["id"] for item in items] == [
        "local-jsonl:messages.jsonl#0",
        "local-jsonl:messages.jsonl#1",
        "local-jsonl:wrapped.json#0",
        "local-jsonl:array.json#0",
    ]


def test_malformed_jsonl_rows_are_counted_and_do_not_crash(tmp_path: Path):
    (tmp_path / "mixed.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"title": "Good", "body": "needle survives malformed rows"}),
                "{not-json",
                json.dumps(["not", "an", "object"]),
                json.dumps({"title": "Other", "body": "no match"}),
            ]
        ),
        encoding="utf-8",
    )

    adapter = LocalJsonlExportAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["title"] for item in items] == ["Good"]
    assert adapter.last_scan_summary["malformed_records"] == 2
    assert adapter.last_scan_summary["records_seen"] == 2
    assert adapter.last_empty_reason is None


def test_mixed_dirs_keep_paths_safe_and_skip_hidden_symlink_and_non_json(tmp_path: Path):
    hidden = tmp_path / ".private"
    hidden.mkdir()
    _write_jsonl(hidden / "hidden.jsonl", [{"title": "Hidden", "body": "needle"}])
    (tmp_path / "bad\\name.jsonl").write_text(json.dumps({"title": "Bad", "body": "needle"}), encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("needle", encoding="utf-8")
    outside = tmp_path.parent / "outside-local-jsonl.jsonl"
    _write_jsonl(outside, [{"title": "Outside", "body": "needle"}])
    (tmp_path / "outside.jsonl").symlink_to(outside)
    nested = tmp_path / "nested"
    nested.mkdir()
    _write_jsonl(nested / "visible.jsonl", [{"title": "Visible", "body": "needle"}])

    adapter = LocalJsonlExportAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["nested/visible.jsonl"]
    assert not items[0]["path"].startswith("/")
    assert "\\" not in items[0]["path"]
    assert ".." not in Path(items[0]["path"]).parts
    assert str(tmp_path) not in repr(items[0])


def test_toctou_swap_to_symlink_is_not_followed(monkeypatch, tmp_path: Path):
    victim = tmp_path / "victim.jsonl"
    _write_jsonl(victim, [{"title": "Victim", "body": "needle"}])
    outside = tmp_path.parent / "jsonl-race-outside.jsonl"
    _write_jsonl(outside, [{"title": "Outside", "body": "needle"}])
    original = jsonl_module._safe_relative_path
    swapped = {"done": False}

    def swap_before_open(path: Path, root: Path) -> str | None:
        rel = original(path, root)
        if path == victim and not swapped["done"]:
            swapped["done"] = True
            victim.unlink()
            victim.symlink_to(outside)
        return rel

    monkeypatch.setattr(jsonl_module, "_safe_relative_path", swap_before_open)

    assert LocalJsonlExportAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10) == []


def test_record_cap_per_file_adds_truncation_note(tmp_path: Path):
    rows = [{"title": f"Row {index}", "body": "needle"} for index in range(MAX_RECORDS_PER_FILE + 1)]
    _write_jsonl(tmp_path / "large.jsonl", rows)

    adapter = LocalJsonlExportAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=1)

    assert len(items) == 1
    assert items[0]["id"] == "local-jsonl:large.jsonl#0"
    assert adapter.last_scan_summary["files_with_record_cap"] == 1
    assert adapter.last_scan_summary["records_indexed"] == MAX_RECORDS_PER_FILE
    assert adapter.last_scan_summary["scan_notice"]["title"] == "Local JSON export record cap reached"


def test_empty_folder_returns_friendly_reason(tmp_path: Path):
    adapter = LocalJsonlExportAdapter(tmp_path)

    assert adapter.context_items(include=["memory"], token_subject=None) == []
    assert adapter.last_empty_reason == "zero_json_export_files"
    assert adapter.last_scan_summary == {
        "files_scanned": 0,
        "files_skipped": 0,
        "records_seen": 0,
        "records_indexed": 0,
        "malformed_records": 0,
        "files_with_record_cap": 0,
        "truncated": False,
        "reason": "zero_json_export_files",
    }


def _write_jsonl(path: Path, rows: list[object]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
