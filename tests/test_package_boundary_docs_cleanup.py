from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "package-boundary.md"
README = REPO_ROOT / "README.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
PACKAGING = REPO_ROOT / "docs" / "packaging.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_package_boundary_doc_names_private_no_live_adapter_and_release_boundaries():
    text = normalized(DOC)

    required_terms = [
        "Package-boundary docs cleanup PASS",
        "public Apache-2.0 Python source package",
        "portable no-live/read-only memory boundary core",
        "Downstream adapters may import Memory Seam package surfaces",
        "Memory Seam core must not import downstream adapter, runtime, service, or private implementation code",
        "Package publication, registry upload, service activation, and provider/prod/canary use remain explicit maintainer decisions",
        "package publication automation",
        "service/listener activation",
        "credential/auth/env/keychain reads",
        "Runtime Registry consumption",
        "live/private source reads",
        "unsupervised reads",
        "writes/custody/reindex behavior",
        "production authority changes",
    ]
    for term in required_terms:
        assert term in text


def test_package_boundary_doc_records_trust_boundary_without_new_reads():
    text = normalized(DOC)

    required_terms = [
        "documentation only",
        "does not add executable denial paths that can materialize source/provider/file/stat/backend reads",
        "zero provider/backend/read/stat calls",
        "does not widen authority",
        "Public issue/PR/docs text must avoid raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, and private correlation refs",
        "pytest -q tests/test_package_boundary_docs_cleanup.py tests/test_docs_taxonomy.py tests/test_readme_operator_quickstart.py tests/test_atlas_query_migration_guide.py",
        "runtime/write authority changes still require explicit maintainer review",
    ]
    for term in required_terms:
        assert term in text


def test_package_boundary_cleanup_is_discoverable_from_package_docs():
    readme = normalized(README)
    docs_index = normalized(DOCS_INDEX)
    changelog = normalized(CHANGELOG)
    packaging = normalized(PACKAGING)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "docs/package-boundary.md" in readme
    assert "package-boundary.md" in docs_index
    assert "package boundary and release-authority docs cleanup" in changelog
    assert "docs/package-boundary.md" in packaging
    assert "tests/test_package_boundary_docs_cleanup.py" in inventory


def test_package_boundary_surfaces_avoid_release_ready_or_gate_ready_claims():
    docs = [
        DOC,
        README,
        DOCS_INDEX,
        CHANGELOG,
        PACKAGING,
    ]
    forbidden_claims = [
        "release-ready",
        "production-authoritative",
        "approved for publication",
    ]
    for path in docs:
        text = normalized(path)
        for claim in forbidden_claims:
            assert claim not in text
