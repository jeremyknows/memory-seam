from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION_GUIDE = ROOT / "docs" / "atlas-query-migration.md"
README = ROOT / "README.md"


def test_atlas_query_migration_guide_is_linked_from_readme():
    assert "docs/atlas-query-migration.md" in README.read_text(encoding="utf-8")


def test_atlas_query_migration_guide_names_target_imports_and_dependency_shape():
    text = MIGRATION_GUIDE.read_text(encoding="utf-8")

    assert "from memory_seam import" in text
    for symbol in [
        "MemorySeamProvider",
        "NullMemorySeamProvider",
        "RuntimeRequest",
        "assert_atlas_query_bridge_contract",
        "atlas_query_bridge_contract_fixture",
        "atlas_query_bridge_plan",
        "atlas_query_route_bridge",
        "route_request",
    ]:
        assert symbol in text

    assert "memory-seam @ file:///path/to/memory-seam" in text
    assert "-e /path/to/memory-seam" in text
    assert "not a Git submodule" in text
    assert "not a pinned production checkout path" in text


def test_atlas_query_migration_guide_preserves_adapter_boundary_and_held_surfaces():
    normalized = " ".join(MIGRATION_GUIDE.read_text(encoding="utf-8").split())

    required_terms = [
        "The downstream reference adapter owns the Atlas Query adapter implementation",
        "Memory Seam owns only the no-live core contract",
        "must not start listeners",
        "read credentials/keychain/env secrets",
        "consume Runtime Registry at runtime",
        "mutate client/runtime config",
        "perform unsupervised/private/live source reads",
        "add write/custody/reindex behavior",
        "move provider/prod/canary authority",
    ]
    for term in required_terms:
        assert term in normalized


def test_atlas_query_migration_guide_has_adapter_local_rollback_plan():
    text = MIGRATION_GUIDE.read_text(encoding="utf-8")
    rollback = text.split("## Rollback plan", 1)[1].split("## Acceptance smoke", 1)[0]

    assert "Remove the Memory Seam path/editable dependency" in rollback
    assert "Revert the adapter PR" in rollback
    assert "Restore the previous Atlas Query-local contract definitions" in rollback
    assert "standalone Memory Seam repository untouched" in rollback
    assert "no submodule cleanup" in rollback
    assert "no package unpublish step" in rollback
