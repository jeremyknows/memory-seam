from __future__ import annotations

import pytest

from memory_seam.contracts import DEFAULT_CONTEXT_SOURCE_MAX_BYTES
from memory_seam.descriptors import ContextSourceDescriptor


BASE_DESCRIPTOR_KWARGS = {
    "subject": "agent:example",
    "include_family": "project",
    "root_ref": "profile",
    "relative_path": "docs/project.md",
    "source_tier": "fixture",
    "private_class": "internal",
    "canonicality": "canonical",
    "retrieval_backend": "filesystem",
    "max_bytes": 100,
}


DESCRIPTOR_VALIDATION_FUZZ_TABLE = [
    pytest.param(
        {"relative_path": ".env"},
        "protected source names",
        "protected filename .env",
        id="protected-env-filename",
    ),
    pytest.param(
        {"relative_path": "docs/auth.json"},
        "protected source names",
        "protected filename auth.json",
        id="protected-auth-json-filename",
    ),
    pytest.param(
        {"relative_path": "db/state.db-wal"},
        "protected source names",
        "protected state sidecar filename",
        id="protected-state-db-wal-filename",
    ),
    pytest.param(
        {"relative_path": "sessions/current.md"},
        "protected source fragments",
        "protected sessions fragment",
        id="protected-sessions-fragment",
    ),
    pytest.param(
        {"relative_path": "keychain/item.md"},
        "protected source fragments",
        "protected keychain fragment",
        id="protected-keychain-fragment",
    ),
    pytest.param(
        {"relative_path": "../project.md"},
        "parent components",
        "leading parent traversal",
        id="leading-parent-path",
    ),
    pytest.param(
        {"relative_path": "docs/../project.md"},
        "parent components",
        "interior parent traversal",
        id="interior-parent-path",
    ),
    pytest.param(
        {"relative_path": "docs//project.md"},
        "empty/current/parent components",
        "empty path segment",
        id="empty-path-segment",
    ),
    pytest.param(
        {"relative_path": "docs/*.md"},
        "wildcards",
        "star wildcard",
        id="star-wildcard-path",
    ),
    pytest.param(
        {"relative_path": "docs/project?.md"},
        "wildcards",
        "question wildcard",
        id="question-wildcard-path",
    ),
    pytest.param(
        {"relative_path": "docs/[abc].md"},
        "wildcards",
        "bracket wildcard",
        id="bracket-wildcard-path",
    ),
    pytest.param(
        {"include_family": "secrets"},
        "unknown include_family",
        "invalid include family",
        id="invalid-include-family",
    ),
    pytest.param(
        {"max_bytes": DEFAULT_CONTEXT_SOURCE_MAX_BYTES + 1},
        "max_bytes must be",
        "oversized max_bytes",
        id="oversized-max-bytes",
    ),
]


@pytest.mark.parametrize(("overrides", "error_fragment", "case_label"), DESCRIPTOR_VALIDATION_FUZZ_TABLE)
def test_descriptor_validation_fuzz_table_rejects_before_materialization_or_read(
    tmp_path, monkeypatch, overrides, error_fragment, case_label
):
    """Invalid descriptor rows fail as policy data before sources can materialize.

    The patched read helpers make the contract explicit: this validation layer may
    parse strings, but it must not inspect or read host files while rejecting bad
    descriptor metadata.
    """

    def fail_if_read(*args, **kwargs):  # pragma: no cover - should never be called
        pytest.fail(f"descriptor validation attempted a filesystem read for {case_label}")

    monkeypatch.setattr("pathlib.Path.read_text", fail_if_read)
    monkeypatch.setattr("pathlib.Path.read_bytes", fail_if_read)

    root = tmp_path / "profile"
    root.mkdir()
    (root / "docs").mkdir()
    (root / "docs" / "project.md").write_text("must not be read by validation", encoding="utf-8")

    kwargs = {**BASE_DESCRIPTOR_KWARGS, **overrides}
    with pytest.raises(ValueError, match=error_fragment):
        ContextSourceDescriptor(**kwargs)
