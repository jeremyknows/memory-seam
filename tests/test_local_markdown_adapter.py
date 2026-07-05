from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from memory_seam import (
    ADAPTER_PROTOCOL_VERSION,
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)
from memory_seam.local_adapters.markdown import LocalMarkdownAdapter, MAX_FILE_BYTES, MAX_SCAN_FILES

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification_for_local_markdown", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified


def test_local_markdown_adapter_passes_lane_a_certification(tmp_path: Path):
    (tmp_path / "authority.md").write_text(
        "# Authority\n\nReceipt-first local note recall proves authority.",
        encoding="utf-8",
    )
    outside = tmp_path.parent / "outside-certification-note.md"
    outside.write_text("# Outside\n\nmemory seam certification zero match", encoding="utf-8")
    (tmp_path / "outside.md").symlink_to(outside)

    assert_source_adapter_certified(
        LocalMarkdownAdapter(tmp_path),
        tmp_path,
        config=AdapterCertificationConfig(recall_query="authority receipt"),
    )


def test_adapter_declares_protocol_version(tmp_path: Path):
    adapter = LocalMarkdownAdapter(tmp_path)

    assert adapter.adapter_protocol_version == ADAPTER_PROTOCOL_VERSION


def test_recall_finds_matching_markdown_file(tmp_path: Path):
    (tmp_path / "alpha.md").write_text("# Alpha\n\nReceipts prove authority before recall.", encoding="utf-8")
    (tmp_path / "beta.md").write_text("# Beta\n\nUnrelated content.", encoding="utf-8")

    items = LocalMarkdownAdapter(tmp_path).recall_items(
        "authority receipt", scope="wiki", token_subject="agent:test", n=2
    )

    assert [item["title"] for item in items] == ["Alpha"]
    assert items[0]["path"] == "alpha.md"
    assert "authority" in items[0]["snippet"].lower()


def test_items_expose_only_normalized_root_relative_paths(tmp_path: Path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "note.md").write_text("# Note\n\nLocal markdown recall.", encoding="utf-8")
    (tmp_path / "bad\\name.md").write_text("# Bad\n\nmarkdown", encoding="utf-8")

    items = LocalMarkdownAdapter(tmp_path).recall_items("markdown", scope="wiki", token_subject=None, n=10)
    item = items[0]

    assert [found["path"] for found in items] == ["nested/note.md"]
    assert item["path"] == "nested/note.md"
    assert not item["path"].startswith("/")
    assert "\\" not in item["path"]
    assert ".." not in Path(item["path"]).parts
    assert str(tmp_path) not in repr(item)


def test_snippet_is_capped(tmp_path: Path):
    content = "# Long\n\n" + ("before " * 80) + "needle " + ("after " * 80)
    (tmp_path / "long.md").write_text(content, encoding="utf-8")

    item = LocalMarkdownAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=1)[0]

    assert len(item["snippet"]) <= 200
    assert "needle" in item["snippet"]


def test_size_cap_skips_large_files(tmp_path: Path):
    (tmp_path / "huge.md").write_text("needle\n" + ("x" * (MAX_FILE_BYTES + 1)), encoding="utf-8")
    (tmp_path / "small.md").write_text("# Small\n\nneedle", encoding="utf-8")

    items = LocalMarkdownAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["small.md"]


def test_hidden_directories_are_skipped(tmp_path: Path):
    hidden = tmp_path / ".obsidian"
    hidden.mkdir()
    (hidden / "private.md").write_text("# Hidden\n\nneedle", encoding="utf-8")
    (tmp_path / "visible.md").write_text("# Visible\n\nneedle", encoding="utf-8")

    items = LocalMarkdownAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.md"]


def test_symlinked_files_and_dirs_are_not_followed(tmp_path: Path):
    outside = tmp_path.parent / "outside-local-markdown.md"
    outside.write_text("# Outside\n\nneedle", encoding="utf-8")
    (tmp_path / "outside.md").symlink_to(outside)
    outside_dir = tmp_path.parent / "outside-local-markdown-dir"
    outside_dir.mkdir(exist_ok=True)
    (outside_dir / "nested.md").write_text("# Outside dir\n\nneedle", encoding="utf-8")
    (tmp_path / "linked-dir").symlink_to(outside_dir, target_is_directory=True)
    (tmp_path / "visible.md").write_text("# Visible\n\nneedle", encoding="utf-8")

    items = LocalMarkdownAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.md"]


def test_invalid_utf8_uses_replacement_and_marks_item_degraded(tmp_path: Path):
    (tmp_path / "bad.md").write_bytes(b"# Bad\n\nneedle \xff recall")

    item = LocalMarkdownAdapter(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=1)[0]

    assert item["degraded"] is True
    assert item["degraded_reasons"] == ["utf8_replacement"]
    assert "Invalid UTF-8" in item["degraded_note"]
    assert "\ufffd" in item["snippet"]


def test_empty_folder_returns_items_empty_reason_in_runtime_envelope(tmp_path: Path):
    runtime = _runtime(LocalMarkdownAdapter(tmp_path))

    response = runtime.handle(RuntimeRequest("GET", "/context?include=memory"))
    body = response["body"]

    assert response["status_code"] == 200
    assert body["items"] == []
    assert body["reason"] == "zero_markdown_files"
    assert body["adapter_scan_summary"] == {
        "files_scanned": 0,
        "files_skipped": 0,
        "truncated": False,
        "reason": "zero_markdown_files",
    }


def test_missing_root_and_not_a_directory_return_friendly_empty_reasons(tmp_path: Path):
    missing = LocalMarkdownAdapter(tmp_path / "missing")
    regular_file = tmp_path / "file.txt"
    regular_file.write_text("not a directory", encoding="utf-8")
    not_dir = LocalMarkdownAdapter(regular_file)

    assert missing.context_items(include=["memory"], token_subject=None) == []
    assert missing.last_empty_reason == "missing_root"
    assert not_dir.context_items(include=["memory"], token_subject=None) == []
    assert not_dir.last_empty_reason == "not_a_directory"


def test_scan_summary_tracks_scanned_skipped_and_truncated(tmp_path: Path):
    (tmp_path / "ignored.txt").write_text("needle", encoding="utf-8")
    for index in range(MAX_SCAN_FILES + 1):
        (tmp_path / f"{index:04d}.md").write_text("# Note\n\nneedle", encoding="utf-8")

    adapter = LocalMarkdownAdapter(tmp_path)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=1)

    assert items[-1]["title"] == "Local markdown scan truncated"
    assert items[-1]["truncated"] is True
    assert "Scan stopped after" in items[-1]["snippet"]
    assert adapter.last_scan_summary["files_scanned"] == MAX_SCAN_FILES
    assert adapter.last_scan_summary["files_skipped"] == 1
    assert adapter.last_scan_summary["truncated"] is True


def _runtime(adapter: LocalMarkdownAdapter) -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="local-markdown-test"),
        provider=AdapterMemorySeamProvider(adapter, provider_name="local-markdown-test"),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:test",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )
