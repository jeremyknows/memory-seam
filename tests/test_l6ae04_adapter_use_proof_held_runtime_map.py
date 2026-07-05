from __future__ import annotations

from pathlib import Path

from memory_seam.l6ad_report_safe_source_card_value_adapter import (
    L6AE_DENIED_STATUS,
    L6AE_PASS_STATUS,
    adapt_l6ae01_report_safe_source_card_value,
    build_l6ae01_exact_approval_fixture,
    build_l6ae01_report_safe_fixture,
    validate_l6ae01_adapter_output,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ae04-adapter-use-proof-held-runtime-map.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_USE_PROOF_PACKET_HELD_RUNTIME_MAP_DEFAULT_OFF_ADAPTER"
VERDICT = "PASS_USE_PROOF_PACKET_HELD_RUNTIME_MAP"
NEXT_FRONTIER = "SOURCE_FLOOR_PARENT_STATUS_RECONCILIATION_ALLOWED_FOR_ISSUE_285_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
SOURCE_FLOOR_ENTERING_SLICE = "0797449e29fd2296d994a27a3337bde234af2ffa"
IMPLEMENTATION_MERGE_COMMIT = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
RECEIPT_REVIEW_MERGE_COMMIT = "45a09f62df38180b429abfb408b80ab59c348a6d"
TRUST_BOUNDARY_MERGE_COMMIT = "0797449e29fd2296d994a27a3337bde234af2ffa"
CONSUMED_APPROVAL_COMMENT = "4652448584"
PREAUTH_COMMENT = "4652981113"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"
FRESH_EVALUATED_AT = "2026-06-08T20:00:00Z"

RUNTIME_SURFACES = (
    "Live/private source-card read",
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
    "live/private reads and any additional source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
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


def test_l6ae04_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ae04-adapter-use-proof-held-runtime-map.md" in docs_index
    assert "tests/test_l6ae04_adapter_use_proof_held_runtime_map.py" in inventory
    assert "L6AE.04 adapter use-proof packet" in inventory
    assert STATUS in inventory


def test_l6ae04_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AE.04 adapter use-proof packet and held-runtime map",
        f"Status: `{STATUS}`",
        "Rail issue: #284",
        "Parent issue: #6",
        "Depends on: #283 closed/PASS via PR #288",
        f"Starting source floor for resumed rail: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed implementation PR: #286",
        "Reviewed receipt-review PR: #287",
        "Reviewed trust-boundary PR: #288",
        f"Implementation merge commit: `{IMPLEMENTATION_MERGE_COMMIT}`",
        f"Receipt-review merge commit: `{RECEIPT_REVIEW_MERGE_COMMIT}`",
        f"Trust-boundary merge commit: `{TRUST_BOUNDARY_MERGE_COMMIT}`",
        f"Issue-bound approval consumed by implementation: #281 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Issue-bound preauthorization for this packet: #284 comment `{PREAUTH_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_USE_PROOF_PACKET_HELD_RUNTIME_MAP`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ae04_positive_fixture_value_path_matches_adapter_behavior() -> None:
    approval = build_l6ae01_exact_approval_fixture()
    fixture = build_l6ae01_report_safe_fixture()
    receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        fixture,
        evaluated_at=FRESH_EVALUATED_AT,
    )

    assert receipt["status"] == L6AE_PASS_STATUS
    assert receipt["approval_result"] == "EXACT_ISSUE_BOUND_OWNER_APPROVAL_MATCH_FIXTURE_ONLY"
    assert receipt["allowed"] == "EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER"
    assert receipt["allowed"] is not True
    assert receipt["allowed_result_count"] == 1
    assert receipt["descriptor_ref"] == "descriptor:l6ae/report-safe-source-card-value-adapter-fixture"
    assert receipt["source_card_ref"] == "source-card:l6ae/report-safe-source-card-value-adapter-fixture"
    assert receipt["live_read_invoked"] is False
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert validate_l6ae01_adapter_output(receipt) == []

    text = normalized(DOC)
    for term in (
        "Fixture-only value path proven",
        "Caller supplies `build_l6ae01_exact_approval_fixture()` metadata",
        "Caller supplies `build_l6ae01_report_safe_fixture()` metadata",
        "`PASS_REPORT_SAFE_VALUE_ADAPTER_FIXTURE_ONLY`",
        "`allowed=\"EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER\"`",
        "`allowed_result_count=1`",
        "`live_read_invoked=false`",
        "all guarded counters zero",
        "does not prove runtime wiring",
        "does not prove runtime wiring, live source-card reading, source discovery, provider callback safety",
    ):
        assert term in text


def test_l6ae04_denial_behavior_matches_adapter_and_validator_guards() -> None:
    missing_approval_receipt = adapt_l6ae01_report_safe_source_card_value(
        None,
        evaluated_at=FRESH_EVALUATED_AT,
    )
    assert missing_approval_receipt["status"] == L6AE_DENIED_STATUS
    assert missing_approval_receipt["approval_result"] == "DENY_BEFORE_ADAPTER_ACTION"
    assert missing_approval_receipt["allowed"] is False
    assert missing_approval_receipt["allowed_result_count"] == 0
    assert missing_approval_receipt["live_read_invoked"] is False
    assert all(value == 0 for value in missing_approval_receipt["guarded_counters"].values())

    approval = build_l6ae01_exact_approval_fixture()
    held_surface_receipt = adapt_l6ae01_report_safe_source_card_value(
        approval | {"runtime_registry_authorized": True},
        evaluated_at=FRESH_EVALUATED_AT,
    )
    assert held_surface_receipt["status"] == L6AE_DENIED_STATUS
    assert "HELD_SURFACE_AUTHORIZATION_REQUESTED" in held_surface_receipt["denial_reasons"]

    fixture = build_l6ae01_report_safe_fixture()
    unsafe_fixture_receipt = adapt_l6ae01_report_safe_source_card_value(
        approval,
        fixture | {"raw_source_text": "raw private source text"},
        evaluated_at=FRESH_EVALUATED_AT,
    )
    assert unsafe_fixture_receipt["status"] == L6AE_DENIED_STATUS
    assert "UNSAFE_OR_NON_FIXTURE_INPUT_REJECTED" in unsafe_fixture_receipt["denial_reasons"]
    assert "raw private source text" not in repr(unsafe_fixture_receipt).lower()

    assert "broad_allowed_true" in validate_l6ae01_adapter_output(
        missing_approval_receipt | {"allowed": True}
    )
    assert "live_read_invoked_not_false" in validate_l6ae01_adapter_output(
        missing_approval_receipt | {"live_read_invoked": True}
    )

    text = normalized(DOC)
    for term in (
        "Denial behavior proven",
        "missing approval metadata denies before adapter action",
        "stale, copied, mismatched, broadened",
        "any request to authorize held surfaces",
        "unsafe fixture keys or echo attempts",
        "output validator rejects broad `allowed=true`",
        "nonzero guarded counters",
        "positive result counts outside the exact narrow adapter label",
    ):
        assert term in text


def test_l6ae04_held_runtime_map_names_remaining_blockers() -> None:
    text = normalized(DOC)

    assert "Held-runtime map before any integration" in text
    for surface in RUNTIME_SURFACES:
        assert surface in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text
    for term in (
        "Fresh exact owner approval",
        "executable descriptor/source-card binding",
        "one-operation limit",
        "denial-before-callback proof",
        "separate design, approval, and denial-before-registry proof",
        "explicit live-read authority are required before any read",
        "General allow semantics remain held",
        "Automation changes remain held",
    ):
        assert term in text


def test_l6ae04_report_safe_boundaries_and_next_blocker() -> None:
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
        "Next exact blocker: #285 source-floor anchor, parent status, and next frontier reconciliation",
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
        "Next open rail issue after #284: #285",
    ):
        assert term in text
