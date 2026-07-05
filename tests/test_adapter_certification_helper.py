from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified
EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "local_markdown_provider.py"
SPEC = importlib.util.spec_from_file_location("local_markdown_provider_for_certification", EXAMPLE_PATH)
assert SPEC and SPEC.loader
local_markdown_provider = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = local_markdown_provider
SPEC.loader.exec_module(local_markdown_provider)

LocalMarkdownProvider = local_markdown_provider.LocalMarkdownProvider


def test_local_markdown_provider_passes_adapter_certification(tmp_path: Path):
    (tmp_path / "authority.md").write_text(
        "# Authority\n\nReceipt-first local note recall proves authority.",
        encoding="utf-8",
    )
    outside = tmp_path.parent / "outside-certification-note.md"
    outside.write_text("# Outside\n\nmemory seam certification zero match", encoding="utf-8")
    (tmp_path / "outside.md").symlink_to(outside)

    assert_source_adapter_certified(
        LocalMarkdownProvider(tmp_path),
        tmp_path,
        config=AdapterCertificationConfig(recall_query="authority receipt"),
    )


def test_adapter_certification_rejects_absolute_item_paths(tmp_path: Path):
    class UnsafeAdapter:
        adapter_name = "unsafe-absolute-path"

        def context_items(self, *, include, token_subject):
            return []

        def recall_items(self, query, *, scope, token_subject, n):
            if query.startswith("__memory_seam_adapter_certification_zero_match__"):
                return []
            return [
                {
                    "id": "unsafe",
                    "scope": scope,
                    "include_family": "memory",
                    "source_tier": "fixture",
                    "backend": "test",
                    "retrieval_backend": "metadata_only",
                    "canonicality": "fixture",
                    "private_class": "test",
                    "title": "Unsafe",
                    "path": "/tmp/private.md",
                    "snippet": "unsafe",
                }
            ]

    with pytest.raises(AssertionError):
        assert_source_adapter_certified(UnsafeAdapter(), tmp_path)
