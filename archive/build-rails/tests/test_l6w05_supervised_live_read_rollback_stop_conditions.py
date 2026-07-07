from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6w05-supervised-live-read-rollback-stop-conditions.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STOP_CLASSES = (
    "denial_before_callback",
    "approval_expired_or_missing",
    "approval_binding_mismatch",
    "approval_variant_or_stale_source",
    "report_hygiene_failure",
    "operator_revocation",
    "scope_broadened_or_allowed_true",
    "callback_or_mutation_requested",
    "registry_activation_or_production_requested",
)

STOP_REASONS = (
    "DENIED_BEFORE_CALLBACK",
    "MISSING_OR_EXPIRED_APPROVAL",
    "BOUND_FIELD_MISMATCH",
    "STALE_VARIANT_OR_COPIED_APPROVAL",
    "REPORT_HYGIENE_FAILURE",
    "OPERATOR_REVOKED_APPROVAL",
    "BROADENED_SCOPE_OR_ALLOWED_TRUE",
    "CALLBACK_OR_MUTATION_REQUESTED",
    "REGISTRY_ACTIVATION_OR_PRODUCTION_REQUESTED",
)

ZERO_COUNTER_TERMS = (
    "provider",
    "backend",
    "source-stat",
    "source-read",
    "write",
    "custody",
    "delete",
    "reindex",
    "rollback",
    "cache-purge",
    "`source_discovery_counter`: `0`",
    "`runtime_registry_consumption_counter`: `0`",
    "`credential_auth_read_counter`: `0`",
    "`persistence_record_counter`: `0`",
    "`audit_record_counter`: `0`",
    "`custody_record_counter`: `0`",
    "`cache_mutation_counter`: `0`",
    "`activation_counter`: `0`",
    "`publication_or_visibility_counter`: `0`",
    "`provider_prod_canary_counter`: `0`",
    "`atlas_gate_movement_counter`: `0`",
)

UNSAFE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
    "source://",
    "I approve Memory Seam",
    "allowed=true route is present",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6w05_stop_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w05-supervised-live-read-rollback-stop-conditions.md" in docs_index
    assert "tests/test_l6w05_supervised_live_read_rollback_stop_conditions.py" in inventory
    assert "L6W.05 rollback and stop-condition proof for future supervised live read" in inventory
    assert "ROLLBACK_STOP_PROOF_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6w05_is_docs_tests_only_non_approval_no_live():
    text = normalized(DOC)

    required_terms = [
        "Status: `ROLLBACK_STOP_PROOF_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #203",
        "Prerequisite: #202 closed/PASS",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "docs/tests-only rollback and stop-condition evidence",
        "does not approve, recognize, implement, or execute any live/private read",
        "This rollback/stop packet is `NO_APPROVAL_PRESENT`",
        "not an approval request, not an approval grant, and not a live-read implementation",
    ]
    for term in required_terms:
        assert term in text


def test_l6w05_covers_required_stop_classes_and_reversibility():
    text = normalized(DOC)

    for stop_class in STOP_CLASSES:
        assert f"`{stop_class}`" in text
    for stop_reason in STOP_REASONS:
        assert f"`{stop_reason}`" in text

    required_reversibility_terms = [
        "evaluate approval and receipt safety before all provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "rollback not required because counters remain zero",
        "fresh future issue-bound owner approval",
        "discarded from in-memory candidate state only",
        "no retry or broadening without fresh review",
        "no callback has been reached",
        "suppress unsafe receipt output before echoing raw approval text",
        "stop immediately on a future owner revocation signal",
        "deny broadened source access, source discovery, workspace scans, family scans, broad recall, index queries, multi-operation requests, positive allowed results, or any `allowed=true` route",
        "deny provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback requests, mutation execution, rollback execution, and cache purge before counters increment",
        "deny Runtime Registry consumption, activation/config mutation, publication, visibility change, provider/prod/canary authority, or Atlas Gate movement before any external or persistent action",
    ]
    for term in required_reversibility_terms:
        assert term in text


def test_l6w05_requires_stop_before_callbacks_and_zero_side_effect_counters():
    text = normalized(DOC)

    required_result_terms = [
        "`approval_result`: `DENIED_BEFORE_CALLBACK`",
        "`status`: `STOPPED_ROLLBACK_NOT_REQUIRED_NO_SIDE_EFFECTS`",
        "`live_read_invoked`: `false`",
        "`allowed`: `false`",
        "`allowed_result_count`: `0`",
        "`rollback_required`: `false`",
        "`rollback_executed`: `false`",
        "`cache_purge_executed`: `false`",
        "`NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED`",
        "`operation_count`: `0`",
        "`max_operation_count`: `1`",
        "`callbacks_invoked`: `false`",
        "`source_discovery_attempted`: `false`",
        "`runtime_registry_consumed`: `false`",
        "`persistence_attempted`: `false`",
        "`mutation_attempted`: `false`",
        "`production_authority_claimed`: `false`",
        "`guarded_counters_zero`: `true`",
    ]
    for term in required_result_terms:
        assert term in text
    for counter_term in ZERO_COUNTER_TERMS:
        assert counter_term in text


def test_l6w05_preserves_report_safety_and_hard_holds():
    text = normalized(DOC)

    report_safe_terms = [
        "The receipt must not echo raw approval text",
        "raw source content",
        "private paths",
        "source URIs",
        "raw platform IDs",
        "raw prompts/queries",
        "raw payload content",
        "raw backend responses",
        "private correlation refs",
        "credentials",
        "auth/env/keychain/OAuth/auth-file material",
        "Runtime Registry data",
        "audit/custody/cache record bodies",
        "operator-local filesystem details",
    ]
    for term in report_safe_terms:
        assert term in text

    held_terms = [
        "before provider/backend/source-stat/source-read callbacks",
        "before source discovery",
        "Runtime Registry consumption",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "persistence/audit/custody/cache writes",
        "activation",
        "publication",
        "visibility change",
        "provider/prod/canary authority",
        "Atlas Gate movement",
        "mutation execution",
        "rollback execution",
        "cache-purge execution",
        "any `allowed=true` route",
    ]
    for term in held_terms:
        assert term in text
    for marker in UNSAFE_MARKERS:
        assert marker not in text
