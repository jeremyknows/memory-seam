from __future__ import annotations

from pathlib import Path

from memory_seam.l6ag_default_off_runtime_integration import (
    L6AH_DENIED_STATUS,
    L6AH_PASS_STATUS,
    build_l6ah01_exact_approval_fixture,
    build_l6ah01_report_safe_adapter_value_fixture,
    integrate_l6ah01_report_safe_adapter_value,
    validate_l6ah01_runtime_integration_output,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ah04-integration-use-proof-held-activation-map.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_USE_PROOF_PACKET_HELD_ACTIVATION_MAP_DEFAULT_OFF_RUNTIME_INTEGRATION"
VERDICT = "PASS_USE_PROOF_PACKET_HELD_ACTIVATION_MAP"
NEXT_FRONTIER = "SOURCE_FLOOR_PARENT_STATUS_RECONCILIATION_ALLOWED_FOR_ISSUE_315_ONLY"
SOURCE_FLOOR_ENTERING_SLICE = "8399a037adf09a07a2074f055a03a8b595b8c577"
IMPLEMENTATION_MERGE_COMMIT = "365dd286566ad3d1a1c34bd7752ad7fa4f41b483"
RECEIPT_REVIEW_MERGE_COMMIT = "91538337422bffc46ca4a53540fcf728f669f8cf"
TRUST_BOUNDARY_MERGE_COMMIT = "8399a037adf09a07a2074f055a03a8b595b8c577"
CONSUMED_APPROVAL_COMMENT = "4654131093"
PARENT_SUCCESSOR_COMMENT = "4654131206"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

HELD_ACTIVATION_SURFACES = (
    "Live/private reads",
    "Source discovery / broad recall / index query",
    "Runtime Registry",
    "Provider/backend/source callbacks",
    "Persistence / custody / mutation / rollback / cache purge",
    "Service/listener/startup/global activation",
    "Credentials/auth/env/keychain/OAuth/auth files",
    "Publication / visibility / provider-prod-canary / Gate / Atlas Gate",
    "Broad `allowed=true`",
    "Cron / automation",
)

RESIDUAL_HOLDS = (
    "live/private reads",
    "source-card reads",
    "raw private content/source text/approval prose",
    "credentials/auth/env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "callbacks/provider routes",
    "runtime persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
    "service/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "additional adapter calls or runtime-use smokes unless separately exact-approved",
    "broad `allowed=true` behavior",
)

UNSAFE_REPORT_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials",
    "auth material",
    "environment values",
    "keychain material",
    "OAuth material",
    "auth-file material",
    "private absolute paths",
    "source URIs",
    "platform IDs",
    "prompts",
    "queries",
    "payloads",
    "backend responses",
    "private correlation refs",
    "Runtime Registry handles",
    "provider handles",
    "secret values",
    "token-like values",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ah04_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ah04-integration-use-proof-held-activation-map.md" in docs_index
    assert "tests/test_l6ah04_integration_use_proof_held_activation_map.py" in inventory
    assert "L6AH.04 integration use-proof packet" in inventory
    assert STATUS in inventory


def test_l6ah04_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AH.04 integration use-proof packet and held-activation map",
        f"Status: `{STATUS}`",
        "Rail issue: #314",
        "Parent issue: #6",
        "Depends on: #313 closed/PASS via PR #318",
        "Starting source floor: `df8e034cd0d53c675212b6f7aa594abd4bd272d3`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed implementation PR: #316",
        "Reviewed receipt-review PR: #317",
        "Reviewed trust-boundary PR: #318",
        f"Implementation merge commit: `{IMPLEMENTATION_MERGE_COMMIT}`",
        f"Receipt-review merge commit: `{RECEIPT_REVIEW_MERGE_COMMIT}`",
        f"Trust-boundary merge commit: `{TRUST_BOUNDARY_MERGE_COMMIT}`",
        f"Issue-bound approval consumed by implementation: #311 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_USE_PROOF_PACKET_HELD_ACTIVATION_MAP`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ah04_fixture_only_invocation_matches_runtime_integration_behavior() -> None:
    approval = build_l6ah01_exact_approval_fixture()
    adapter_value = build_l6ah01_report_safe_adapter_value_fixture()
    receipt = integrate_l6ah01_report_safe_adapter_value(approval, adapter_value)

    assert receipt["status"] == L6AH_PASS_STATUS
    assert receipt["approval_result"] == "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_RUNTIME_INTEGRATION_FIXTURE_ONLY"
    assert receipt["allowed"] == "EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE"
    assert receipt["allowed"] is not True
    assert receipt["integration_slice_count"] == 1
    assert receipt["runtime_use_smoke_count"] == 0
    assert receipt["live_adapter_invoked"] is False
    assert receipt["callback_invoked"] is False
    assert receipt["registry_consumed"] is False
    assert receipt["persistence_attempted"] is False
    assert receipt["activation_attempted"] is False
    assert receipt["broad_allowed_attempted"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert validate_l6ah01_runtime_integration_output(receipt) == []

    text = normalized(DOC)
    for term in (
        "Fixture-only invocation proof",
        "Caller supplies `build_l6ah01_exact_approval_fixture()` metadata",
        "Caller supplies `build_l6ah01_report_safe_adapter_value_fixture()` metadata",
        "Caller invokes `integrate_l6ah01_report_safe_adapter_value(approval, adapter_value)`",
        "Caller validates the receipt with `validate_l6ah01_runtime_integration_output(receipt)`",
        "`PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_FIXTURE_ONLY`",
        "`allowed=\"EXACT_FIXTURE_ONLY_RUNTIME_INTEGRATION_SLICE\"`",
        "`integration_slice_count=1`",
        "`runtime_use_smoke_count=0`",
        "all guarded counters zero",
        "does not prove runtime use",
        "does not call the adapter",
        "does not activate service/global behavior",
    ):
        assert term in text


def test_l6ah04_denial_behavior_and_validator_guards() -> None:
    missing_approval_receipt = integrate_l6ah01_report_safe_adapter_value(None)
    assert missing_approval_receipt["status"] == L6AH_DENIED_STATUS
    assert missing_approval_receipt["approval_result"] == "DENY_BEFORE_RUNTIME_INTEGRATION"
    assert missing_approval_receipt["allowed"] is False
    assert missing_approval_receipt["integration_slice_count"] == 0
    assert missing_approval_receipt["runtime_use_smoke_count"] == 0
    assert all(value == 0 for value in missing_approval_receipt["guarded_counters"].values())

    approval = build_l6ah01_exact_approval_fixture()
    held_surface_receipt = integrate_l6ah01_report_safe_adapter_value(
        approval | {"runtime_registry_authorized": True}
    )
    assert held_surface_receipt["status"] == L6AH_DENIED_STATUS
    assert "HELD_SURFACE_AUTHORIZATION_REQUESTED" in held_surface_receipt["denial_reasons"]

    adapter_value = build_l6ah01_report_safe_adapter_value_fixture()
    unsafe_adapter_value_receipt = integrate_l6ah01_report_safe_adapter_value(
        approval,
        adapter_value | {"raw_source_text": "raw private source text"},
    )
    assert unsafe_adapter_value_receipt["status"] == L6AH_DENIED_STATUS
    assert "UNEXPECTED_ADAPTER_VALUE_FIELD" in unsafe_adapter_value_receipt["denial_reasons"]
    assert "UNSAFE_ADAPTER_VALUE_KEY" in unsafe_adapter_value_receipt["denial_reasons"]
    assert "raw private source text" not in repr(unsafe_adapter_value_receipt).lower()

    assert "broad_allowed_true" in validate_l6ah01_runtime_integration_output(
        missing_approval_receipt | {"allowed": True}
    )
    assert "live_adapter_invoked_not_false" in validate_l6ah01_runtime_integration_output(
        missing_approval_receipt | {"live_adapter_invoked": True}
    )
    assert "registry_consumed_not_false" in validate_l6ah01_runtime_integration_output(
        missing_approval_receipt | {"registry_consumed": True}
    )

    text = normalized(DOC)
    for term in (
        "Denial behavior proof",
        "missing, stale, copied, mismatched, broadened, non-owner",
        "requests runtime-use smoke authority",
        "requests any held surface",
        "denies report-unsafe adapter-value metadata before echoing unsafe input",
        "`DENIED_DEFAULT_OFF`",
        "`allowed=false`",
        "validator rejection for broad `allowed=true`",
        "Runtime Registry consumption",
        "activation attempts",
    ):
        assert term in text


def test_l6ah04_held_activation_map_names_remaining_blockers() -> None:
    text = normalized(DOC)

    assert "Held-activation map before any service/global/live/provider/Gate use" in text
    for surface in HELD_ACTIVATION_SURFACES:
        assert surface in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text
    for term in (
        "Fresh exact owner approval",
        "executable descriptor/source-card binding",
        "explicit live-read authority",
        "one-operation limit",
        "denial-before-callback proof",
        "Separate design, approval, and denial-before-registry proof",
        "General allow semantics remain held",
        "Automation changes remain held",
    ):
        assert term in text


def test_l6ah04_report_safe_boundaries_and_next_blocker() -> None:
    text = normalized(DOC)

    assert "Use-proof packet boundaries" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_example_markers:
        assert marker not in lowered

    for term in (
        "Next exact blocker: #315 source-floor anchor, parent status, and next frontier reconciliation",
        "committed docs/tests and public issue/PR/source-floor metadata only",
        "must not create successor issues or cron automation",
        "activate runtime use",
        "perform live/private reads",
        "fetch private/raw source material",
        "fetch credentials/auth/env/keychain/OAuth/auth-file material",
        "consume Runtime Registry",
        "create callbacks",
        "persist or mutate state",
        "publish or change visibility",
        "move provider/prod/canary/Gate or Atlas Gate",
        "execute rollback/cache purge",
        "introduce broad `allowed=true` behavior",
        "perform additional adapter calls/runtime-use smokes",
        "Next open rail issue after #314: #315",
    ):
        assert term in text
