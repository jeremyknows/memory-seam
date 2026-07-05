from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "local_markdown_provider.py"
SPEC = importlib.util.spec_from_file_location("local_markdown_provider", EXAMPLE_PATH)
assert SPEC and SPEC.loader
local_markdown_provider = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = local_markdown_provider
SPEC.loader.exec_module(local_markdown_provider)

QUICKSTART_PATH = Path(__file__).resolve().parents[1] / "examples" / "my_notes_quickstart.py"
QUICKSTART_SPEC = importlib.util.spec_from_file_location("my_notes_quickstart", QUICKSTART_PATH)
assert QUICKSTART_SPEC and QUICKSTART_SPEC.loader
my_notes_quickstart = importlib.util.module_from_spec(QUICKSTART_SPEC)
sys.modules[QUICKSTART_SPEC.name] = my_notes_quickstart
QUICKSTART_SPEC.loader.exec_module(my_notes_quickstart)

LocalMarkdownProvider = local_markdown_provider.LocalMarkdownProvider
MAX_FILE_BYTES = local_markdown_provider.MAX_FILE_BYTES
MAX_SCAN_FILES = local_markdown_provider.MAX_SCAN_FILES


def test_recall_finds_matching_markdown_file(tmp_path: Path):
    (tmp_path / "alpha.md").write_text("# Alpha\n\nReceipts prove authority before recall.", encoding="utf-8")
    (tmp_path / "beta.md").write_text("# Beta\n\nUnrelated content.", encoding="utf-8")

    items = LocalMarkdownProvider(tmp_path).recall_items(
        "authority receipt", scope="wiki", token_subject="agent:test", n=2
    )

    assert [item["title"] for item in items] == ["Alpha"]
    assert items[0]["path"] == "alpha.md"
    assert "authority" in items[0]["snippet"].lower()


def test_items_expose_only_safe_relative_paths(tmp_path: Path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "note.md").write_text("# Note\n\nLocal markdown recall.", encoding="utf-8")

    item = LocalMarkdownProvider(tmp_path).recall_items("markdown", scope="wiki", token_subject=None, n=1)[0]

    assert item["path"] == "nested/note.md"
    assert not item["path"].startswith("/")
    assert ".." not in Path(item["path"]).parts
    assert str(tmp_path) not in repr(item)


def test_snippet_is_capped(tmp_path: Path):
    content = "# Long\n\n" + ("before " * 80) + "needle " + ("after " * 80)
    (tmp_path / "long.md").write_text(content, encoding="utf-8")

    item = LocalMarkdownProvider(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=1)[0]

    assert len(item["snippet"]) <= 200
    assert "needle" in item["snippet"]


def test_size_cap_skips_large_files(tmp_path: Path):
    (tmp_path / "huge.md").write_text("needle\n" + ("x" * (MAX_FILE_BYTES + 1)), encoding="utf-8")
    (tmp_path / "small.md").write_text("# Small\n\nneedle", encoding="utf-8")

    items = LocalMarkdownProvider(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["small.md"]


def test_hidden_directories_are_skipped(tmp_path: Path):
    hidden = tmp_path / ".obsidian"
    hidden.mkdir()
    (hidden / "private.md").write_text("# Hidden\n\nneedle", encoding="utf-8")
    (tmp_path / "visible.md").write_text("# Visible\n\nneedle", encoding="utf-8")

    items = LocalMarkdownProvider(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.md"]


def test_empty_folder_returns_no_items(tmp_path: Path):
    assert LocalMarkdownProvider(tmp_path).context_items(include=["memory"], token_subject=None) == []
    assert LocalMarkdownProvider(tmp_path).recall_items("anything", scope="wiki", token_subject=None, n=3) == []


def test_scan_cap_adds_explicit_truncated_note(tmp_path: Path):
    for index in range(MAX_SCAN_FILES + 1):
        (tmp_path / f"{index:04d}.md").write_text("# Note\n\nneedle", encoding="utf-8")

    items = LocalMarkdownProvider(tmp_path).recall_items("needle", scope="wiki", token_subject=None, n=1)

    assert items[-1]["title"] == "Local markdown scan truncated"
    assert items[-1]["truncated"] is True
    assert "Scan stopped after" in items[-1]["snippet"]


def test_quickstart_runtime_posture_flags_stay_fail_closed(tmp_path: Path):
    (tmp_path / "note.md").write_text("# Authority\n\nReceipt-first local note recall.", encoding="utf-8")

    response = my_notes_quickstart.run_recall(tmp_path, query="receipt authority")
    body = response["body"]

    assert response["status_code"] == 200
    assert body["items"][0]["path"] == "note.md"
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["raw_fallback_used"] is False
    assert body["write_custody_or_reindex"] is False
    assert body["read_receipt"]["usefulness_shape"]["verdict"] == "useful"
