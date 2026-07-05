from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-positive-authorization-receipt-fixture-contract.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "l6i09_positive_authorization_receipt_fixture.json"

GUARDED_COUNTERS = (
    "provider_calls",
    "backend_calls",
    "source_stat_calls",
    "source_read_calls",
    "write_callbacks",
    "custody_callbacks",
    "delete_callbacks",
    "reindex_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
)

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def fixture() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_l6i09_packet_is_schema_fixture_only_and_not_approval():
    text = normalized(PACKET)

    required_terms = [
        "L6I.09 positive-authorization receipt fixture contract",
        "docs/tests/schema-fixture only",
        "non-authoritative",
        "non-persistent",
        "does not approve implementation",
        "does not create approval parser behavior",
        "Source floor: `7980a5b` or later `origin/main`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "Dependency: L6I.08 closed/PASS via issue `#150` and PR `#157`",
        "tests/fixtures/l6i09_positive_authorization_receipt_fixture.json",
        "Proceed to L6I.10 as docs/tests-only custody persistence threat-model and storage non-goals work",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text


def test_l6i09_fixture_has_required_positive_recognized_mutation_held_fields():
    data = fixture()
    receipt = data["positive_authorization_recognized_mutation_held_fixture"]

    assert data["schema_version"] == "l6i09-positive-authorization-receipt-fixture-v0"
    assert data["fixture_status"] == "non_authoritative_schema_fixture_only"
    assert data["source_floor"] == "7980a5b-or-later"
    assert data["dependency"] == "L6I.08 closed/PASS via issue #150 and PR #157"

    required_fields = {
        "schema_version",
        "status",
        "operation_class",
        "approval_ref",
        "actor_binding_ref",
        "custody_owner_role",
        "rollback_audit_plan_ref",
        "mutation_attempted",
        "mutation_supported",
        "authorization_allowed_runtime_path",
        "fixture_is_authoritative",
        "fixture_is_persistent",
        "guarded_counters",
        "report_safety",
        "held_surfaces",
    }
    assert required_fields <= set(receipt)
    assert receipt["schema_version"] == "l6i09-positive-authorization-receipt-shape-v0"
    assert receipt["status"] == "positive_authorization_recognized_mutation_held"
    assert receipt["operation_class"] == "write_intent_preflight_candidate"
    assert receipt["approval_ref"] == "public-approval-ref-placeholder"
    assert receipt["actor_binding_ref"] == "actor-binding-ref-placeholder"
    assert receipt["custody_owner_role"] == "librarian"
    assert receipt["rollback_audit_plan_ref"] == "docs/l6-write-custody-rollback-audit-plan.md"
    assert receipt["mutation_attempted"] is False
    assert receipt["mutation_supported"] is False
    assert receipt["authorization_allowed_runtime_path"] is False
    assert receipt["fixture_is_authoritative"] is False
    assert receipt["fixture_is_persistent"] is False


def test_l6i09_denied_receipt_semantics_remain_separate_from_hypothetical_fixture():
    data = fixture()
    denied = data["denied_receipt_semantics"]
    positive = data["positive_authorization_recognized_mutation_held_fixture"]

    assert denied["schema_family"] == "l6-write-intent-denial-receipt-v1"
    assert denied["status"] == "denied_no_mutation_path"
    assert denied["approval_recognized"] is False
    assert denied["mutation_attempted"] is False
    assert denied["mutation_supported"] is False
    assert denied["semantic_boundary"] == "runtime_denial_metadata_only"

    assert positive["schema_version"] != denied["schema_family"]
    assert positive["status"] != denied["status"]
    assert positive["status"] == "positive_authorization_recognized_mutation_held"
    assert positive["fixture_is_authoritative"] is False
    assert positive["fixture_is_persistent"] is False


def test_l6i09_fixture_is_non_persistent_and_all_guarded_counters_zero():
    data = fixture()
    receipt = data["positive_authorization_recognized_mutation_held_fixture"]

    assert data["non_persistence"] == {
        "persistent_storage_allowed": False,
        "custody_receipt_persisted": False,
        "audit_trail_persisted": False,
        "cache_mutated": False,
        "durable_write_record_created": False,
    }
    assert set(receipt["guarded_counters"]) == set(GUARDED_COUNTERS)
    assert all(receipt["guarded_counters"][counter] == 0 for counter in GUARDED_COUNTERS)

    held_surfaces = set(receipt["held_surfaces"])
    required_holds = {
        "runtime_approval_acceptance",
        "positive_allowed_runtime_path",
        "write_execution",
        "custody_transfer",
        "custody_persistence",
        "delete_execution",
        "reindex_execution",
        "rollback_execution",
        "cache_purge_execution",
        "provider_backend_callbacks",
        "source_stat_source_read_callbacks",
        "source_discovery",
        "live_private_source_reads",
        "credential_auth_env_keychain_oauth_authfile_reads",
        "runtime_registry_consumption",
        "service_listener_startup_cron_activation",
        "publication_or_visibility_change",
        "provider_prod_canary_authority",
        "atlas_gate_movement",
    }
    assert required_holds <= held_surfaces


def test_l6i09_fixture_and_docs_are_report_safe_and_discoverable():
    data = fixture()
    report_safety = data["positive_authorization_recognized_mutation_held_fixture"]["report_safety"]

    assert report_safety["public_issue_or_pr_refs_only"] is True
    unsafe_flags = [key for key in report_safety if key.endswith("_included")]
    assert unsafe_flags
    assert all(report_safety[key] is False for key in unsafe_flags)

    combined = " ".join(
        [
            normalized(PACKET),
            normalized(DOCS_INDEX),
            normalized(CONTRACT_TEST_INVENTORY),
            json.dumps(data, sort_keys=True),
        ]
    )
    assert "l6-positive-authorization-receipt-fixture-contract.md" in combined
    assert "tests/test_l6i09_positive_authorization_receipt_fixture_contract.py" in combined
    assert "l6i09_positive_authorization_receipt_fixture.json" in combined
    assert "non-authoritative `positive_authorization_recognized_mutation_held` receipt shape" in combined

    hygiene_terms = [
        "raw private source text",
        "credentials",
        "OAuth/auth-file material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "raw payload content",
        "private correlation refs",
    ]
    for term in hygiene_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
