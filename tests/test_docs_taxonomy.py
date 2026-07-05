from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
AUTOPILOT_TEMPLATE = REPO_ROOT / "docs" / "issue-railed-autopilot.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def test_docs_index_defines_public_runtime_adapter_example_and_private_sections():
    text = DOCS_INDEX.read_text(encoding="utf-8")

    required_headings = [
        "## Public package docs",
        "## Runtime, contracts, and schema notes",
        "## Adapter and downstream migration notes",
        "## Examples",
        "## Omitted Internal Material",
    ]
    for heading in required_headings:
        assert heading in text

    required_links = [
        "../README.md",
        "../CHANGELOG.md",
        "../CONTRIBUTING.md",
        "../SECURITY.md",
        "public-hygiene.md",
        "packaging.md",
        "issue-railed-autopilot.md",
        "l4-closure-review.md",
        "default-off-runtime.md",
        "envelope-schema-snapshots.md",
        "contract-test-inventory.md",
        "downstream-integration-smoke-plan.md",
        "atlas-query-bridge.md",
        "atlas-query-migration.md",
        "adapter-certification.md",
        "../examples/quickstart_smoke.py",
        "../examples/null_and_fake_providers.py",
    ]
    for link in required_links:
        assert link in text


def test_docs_index_preserves_private_staging_and_no_live_boundaries():
    normalized = " ".join(DOCS_INDEX.read_text(encoding="utf-8").split())

    required_terms = [
        "without private provenance",
        "Runtime Registry access",
        "live reads",
        "services",
        "package publication",
        "write/custody behavior",
        "Internal planning and provenance documents are maintained privately and omitted from this repository",
        "Token-like strings",
    ]
    for term in required_terms:
        assert term in normalized


def test_root_and_release_docs_point_to_taxonomy_index():
    root_text = README.read_text(encoding="utf-8")

    assert "Start with `docs/README.md` for the documentation taxonomy" in root_text
    assert "See `CHANGELOG.md` for the API/schema stability ledger" in root_text
    assert "docs/" + "release-readiness.md" not in root_text
    assert "docs/" + "release-decision-hold-packet.md" not in root_text


def test_issue_railed_autopilot_template_is_reusable_and_non_scheduling():
    normalized = " ".join(AUTOPILOT_TEMPLATE.read_text(encoding="utf-8").split())

    required_terms = [
        "# Issue-railed autopilot template",
        "reusable prompt and operating checklist",
        "documentation only",
        "do not create, update, remove, or schedule jobs",
        "issue numbers, titles, priority/order",
        "Allowed without further confirmation",
        "Hard holds",
        "Per-tick operating loop",
        "Verify repo state",
        "Choose the lowest open safe issue",
        "short-lived branch",
        "Run the required verification gate",
        "Push/open PR",
        "After merge, verify origin/main/local main",
        "Final report",
        "Final harvest checklist",
        "decision aid, not an executable release script",
    ]
    for term in required_terms:
        assert term in normalized

    forbidden_terms = [
        "crontab -e",
        "gh workflow run",
        "make public",
        "twine upload",
    ]
    for term in forbidden_terms:
        assert term not in normalized


def test_changelog_scaffolds_api_stability_entries_without_release_authority():
    normalized = " ".join(CHANGELOG.read_text(encoding="utf-8").split())

    required_terms = [
        "# Changelog",
        "stability ledger for public API, schema, contract",
        "## [Unreleased]",
        "every PR updates `[Unreleased]`",
        "ADAPTER_PROTOCOL_VERSION",
        "tests/adapter_certification.py",
        "## [0.1.0]",
        "## Stability Policy",
        "Breaking",
        "Non-breaking",
        "Documentation-only",
        "### Initial public release baseline",
        "contracts, policy, descriptors",
        "provider protocols/null provider",
        "Atlas Query bridge helper",
        "versioned standalone fixture",
        "Default-off read-only runtime skeleton",
        "denial-before-read behavior",
        "metadata-only receipts",
        "safe source-card adapter interfaces",
        "minimal no-live CLI smoke",
        "### Entry Template",
        "Surface: exported API, schema snapshot, CLI, docs, packaging, or downstream fixture",
        "Evidence: issue #NN / PR #NN plus local and CI checks",
        "## Runtime Boundary",
        "does not authorize service/listener activation",
        "service/listener activation",
        "live source reads",
        "Runtime Registry consumption",
        "write/custody/reindex work",
    ]
    for term in required_terms:
        assert term in normalized

    forbidden_terms = [
        "twine upload",
        "gh repo edit --visibility public",
        "Runtime Registry endpoint",
    ]
    for term in forbidden_terms:
        assert term not in normalized


def test_prerelease_process_docs_are_omitted_from_public_taxonomy():
    normalized = " ".join(DOCS_INDEX.read_text(encoding="utf-8").split())

    assert "## Omitted Internal Material" in normalized
    assert "Internal planning and provenance documents are maintained privately and omitted from this repository" in normalized
    assert "release-" + "readiness.md" not in normalized
    assert "release-decision-" + "hold-packet.md" not in normalized
    assert "internal-" + "removed.txt" not in normalized


def test_contract_test_inventory_maps_tests_to_invariants_and_gaps():
    normalized = " ".join(CONTRACT_TEST_INVENTORY.read_text(encoding="utf-8").split())

    required_terms = [
        "# Contract test inventory",
        "maps the committed contract tests to the safety boundary each one protects",
        "## Inventory",
        "Test file",
        "Tests covered",
        "Protected invariant",
        "tests/test_core_import_boundary.py",
        "tests/test_core_behavior.py",
        "tests/test_runtime.py",
        "tests/test_public_api_contract.py",
        "tests/test_safe_source_cards.py",
        "tests/test_envelope_schema_snapshots.py",
        "tests/test_atlas_query_bridge.py",
        "tests/test_atlas_query_migration_guide.py",
        "tests/test_cli_no_live_smoke.py",
        "tests/test_quickstart_examples.py",
        "tests/test_null_and_fake_provider_examples.py",
        "tests/test_dogfood_usefulness.py",
        "tests/test_synthetic_recall_ranking_fixture.py",
        "tests/test_downstream_integration_smoke_plan.py",
        "tests/test_public_hygiene_scan.py",
        "tests/test_local_wheel_install_smoke.py",
        "tests/test_readme_operator_quickstart.py",
        "tests/test_docs_taxonomy.py",
        "## Missing coverage candidates",
        "Final L4 closure review packet",
        "does not execute a release",
        "perform live/private reads",
        "add write/custody/reindex behavior",
    ]
    for term in required_terms:
        assert term in normalized
