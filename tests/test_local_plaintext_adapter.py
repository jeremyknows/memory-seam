from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from memory_seam import ADAPTER_PROTOCOL_VERSION
from memory_seam.local_adapters.plaintext import (
    DEFAULT_PLAINTEXT_EXTENSIONS,
    LocalPlainTextAdapter,
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
)

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification_for_local_plaintext", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified


def test_local_plaintext_adapter_passes_lane_a_certification(tmp_path: Path):
    (tmp_path / "authority.txt").write_text(
        "Authority\n\nReceipt-first local note recall proves authority.",
        encoding="utf-8",
    )
    outside = tmp_path.parent / "outside-certification-note.txt"
    outside.write_text("Outside\n\nmemory seam certification zero match", encoding="utf-8")
    (tmp_path / "outside.txt").symlink_to(outside)

    assert_source_adapter_certified(
        LocalPlainTextAdapter(tmp_path),
        tmp_path,
        config=AdapterCertificationConfig(
            recall_query="authority receipt",
            allowed_retrieval_backends=frozenset({"recursive_plaintext_scan"}),
        ),
    )


def test_adapter_declares_protocol_version_and_default_allowlist(tmp_path: Path):
    adapter = LocalPlainTextAdapter(tmp_path)

    assert adapter.adapter_protocol_version == ADAPTER_PROTOCOL_VERSION
    assert DEFAULT_PLAINTEXT_EXTENSIONS == (".txt", ".md", ".rst", ".log")


def test_default_allowlist_reads_plain_text_extensions(tmp_path: Path):
    (tmp_path / "alpha.txt").write_text("Alpha needle", encoding="utf-8")
    (tmp_path / "beta.md").write_text("# Beta\n\nneedle", encoding="utf-8")
    (tmp_path / "gamma.rst").write_text("Gamma\n=====\nneedle", encoding="utf-8")
    (tmp_path / "delta.log").write_text("INFO needle", encoding="utf-8")
    (tmp_path / "ignored.json").write_text('{"needle": true}', encoding="utf-8")

    items = LocalPlainTextAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["alpha.txt", "beta.md", "delta.log", "gamma.rst"]


def test_configurable_allowlist_accepts_extensions_without_leading_dot(tmp_path: Path):
    (tmp_path / "include.memo").write_text("custom needle", encoding="utf-8")
    (tmp_path / "exclude.txt").write_text("default needle", encoding="utf-8")

    items = LocalPlainTextAdapter(tmp_path, extension_allowlist=("memo",)).recall_items(
        "needle",
        scope="wiki",
        token_subject=None,
        n=10,
    )

    assert [item["path"] for item in items] == ["include.memo"]


def test_binary_files_are_skipped_and_counted(tmp_path: Path):
    (tmp_path / "binary.txt").write_bytes(b"needle\x00not text")
    (tmp_path / "visible.txt").write_text("visible needle", encoding="utf-8")

    adapter = LocalPlainTextAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.txt"]
    assert adapter.last_scan_summary["files_scanned"] == 2
    assert adapter.last_scan_summary["files_skipped"] == 1
    assert adapter.last_scan_summary["binary_files_skipped"] == 1


def test_mixed_folder_keeps_paths_safe_and_skips_hidden_symlink_large_and_binary(tmp_path: Path):
    hidden = tmp_path / ".private"
    hidden.mkdir()
    (hidden / "hidden.txt").write_text("needle", encoding="utf-8")
    (tmp_path / "bad\\name.txt").write_text("needle", encoding="utf-8")
    (tmp_path / "huge.txt").write_text("needle\n" + ("x" * (MAX_FILE_BYTES + 1)), encoding="utf-8")
    (tmp_path / "binary.log").write_bytes(b"needle\x00")
    outside = tmp_path.parent / "outside-local-plaintext.txt"
    outside.write_text("outside needle", encoding="utf-8")
    (tmp_path / "outside.txt").symlink_to(outside)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "visible.rst").write_text("Visible\n=======\nneedle", encoding="utf-8")

    adapter = LocalPlainTextAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["nested/visible.rst"]
    assert not items[0]["path"].startswith("/")
    assert "\\" not in items[0]["path"]
    assert ".." not in Path(items[0]["path"]).parts
    assert str(tmp_path) not in repr(items[0])
    assert adapter.last_scan_summary["binary_files_skipped"] == 1


def test_invalid_utf8_uses_replacement_and_marks_item_degraded(tmp_path: Path):
    (tmp_path / "bad.txt").write_bytes(b"needle \xff recall")

    item = LocalPlainTextAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=1)[0]

    assert item["degraded"] is True
    assert item["degraded_reasons"] == ["utf8_replacement"]
    assert "Invalid UTF-8" in item["degraded_note"]
    assert "\ufffd" in item["snippet"]


def test_empty_folder_returns_friendly_reason(tmp_path: Path):
    adapter = LocalPlainTextAdapter(tmp_path)

    assert adapter.context_items(include=["memory"], token_subject=None) == []
    assert adapter.last_empty_reason == "zero_plaintext_files"
    assert adapter.last_scan_summary == {
        "files_scanned": 0,
        "files_skipped": 0,
        "binary_files_skipped": 0,
        "truncated": False,
        "reason": "zero_plaintext_files",
    }


def test_scan_cap_adds_truncation_item(tmp_path: Path):
    for index in range(MAX_SCAN_FILES + 1):
        (tmp_path / f"{index:04d}.txt").write_text("needle", encoding="utf-8")

    adapter = LocalPlainTextAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=1)

    assert items[-1]["title"] == "Local plain-text scan truncated"
    assert items[-1]["truncated"] is True
    assert adapter.last_scan_summary["files_scanned"] == MAX_SCAN_FILES
    assert adapter.last_scan_summary["truncated"] is True
