from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_PLAN = REPO_ROOT / "docs" / "downstream-integration-smoke-plan.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def test_downstream_integration_smoke_plan_names_no_mutation_commands_and_expected_output():
    text = SMOKE_PLAN.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    required_terms = [
        "# Downstream integration smoke plan",
        "no-mutation smoke",
        "does not start services/listeners",
        "mutate global Hermes/MCP/runtime configuration",
        "read credentials/auth stores/keychains/secrets",
        "discover private sources",
        "perform live/private reads",
        "consume Runtime Registry",
        "publish packages",
        "change repository visibility",
        "write/custody/reindex behavior",
        "<DOWNSTREAM_CHECKOUT>",
        "synthetic_safe_content_provider",
        "route_request",
        "/context?include=project,memory&mode=downstream-smoke",
        "/recall?query=runtime+identity+rollback&scope=wiki&n=2",
        "memory-seam downstream no-live smoke ok",
        "package imports ok",
        "Rollback is local-only",
        "Held authority boundaries",
        "Acceptance checklist",
    ]
    for term in required_terms:
        assert term in normalized

    forbidden_terms = [
        "twine upload",
        "gh repo edit --visibility public",
        "launchctl load",
        "crontab -e",
        "Runtime Registry endpoint",
    ]
    for term in forbidden_terms:
        assert term not in normalized


def test_downstream_integration_smoke_plan_is_discoverable_from_docs_and_inventory():
    docs_index = DOCS_INDEX.read_text(encoding="utf-8")
    inventory = CONTRACT_TEST_INVENTORY.read_text(encoding="utf-8")

    assert "downstream-integration-smoke-plan.md" in docs_index
    assert "no-mutation downstream package import" in docs_index
    assert "downstream no-mutation smoke plan commands" in inventory
