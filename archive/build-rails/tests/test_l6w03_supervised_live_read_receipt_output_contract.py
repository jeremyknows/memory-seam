from __future__ import annotations

import json
from pathlib import Path
from typing import cast

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6w03-supervised-live-read-receipt-output-contract.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PERMITTED_FIELD_TERMS = (
    "public issue refs",
    "public PR refs",
    "repository file names",
    "source floor commit refs",
    "operation class",
    "operation count",
    "max operation count",
    "one-operation binding boolean",
    "approval status labels",
    "report-safe descriptor ref",
    "report-safe source-card ref",
    "numeric counters",
    "zero guarded callback counters",
    "stop-condition status",
    "stop reason label",
    "expiry status label",
    "usefulness classification labels",
    "report-safe boolean flags",
)

REJECTED_FIELD_TERMS = (
    "raw private source text",
    "raw source content",
    "private absolute paths",
    "source URIs",
    "backend locator strings",
    "platform IDs",
    "message IDs",
    "provider IDs",
    "account IDs",
    "tenant IDs",
    "prompts",
    "queries",
    "broad recall text",
    "index query text",
    "raw request payloads",
    "backend responses",
    "provider responses",
    "source-stat responses",
    "source-read responses",
    "callback payloads",
    "private correlation refs",
    "trace IDs",
    "custody refs",
    "audit refs",
    "cache keys",
    "Runtime Registry refs",
    "credentials",
    "auth files",
    "environment secrets",
    "keychain entries",
    "OAuth material",
    "auth-file material",
    "tokens",
    "API keys",
    "cookie values",
    "session material",
    "raw approval text",
    "copied approval comments",
    "stale approval comments",
    "variant approval text",
    "unsafe submitted value",
)

ZERO_COUNTER_KEYS = (
    "source_discovery_counter",
    "runtime_registry_consumption_counter",
    "persistence_record_counter",
    "audit_record_counter",
    "custody_record_counter",
    "cache_mutation_counter",
    "activation_counter",
    "publication_or_visibility_counter",
    "provider_prod_canary_counter",
    "atlas_gate_movement_counter",
)

GUARDED_CALLBACK_KEYS = (
    "provider",
    "backend",
    "source_stat",
    "source_read",
    "write",
    "custody",
    "delete",
    "reindex",
    "rollback",
    "cache_purge",
)

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
    "source://",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def doc_text() -> str:
    return normalized(DOC)


def extract_fixture() -> dict[str, object]:
    raw = DOC.read_text(encoding="utf-8")
    start = raw.index("```json") + len("```json")
    end = raw.index("```", start)
    return json.loads(raw[start:end].strip())


def test_l6w03_receipt_contract_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w03-supervised-live-read-receipt-output-contract.md" in docs_index
    assert "tests/test_l6w03_supervised_live_read_receipt_output_contract.py" in inventory
    assert "L6W.03 report-safe supervised live-read receipt output contract" in inventory
    assert "RECEIPT_CONTRACT_ONLY_NO_APPROVAL_NO_EXECUTION" in inventory


def test_l6w03_is_schema_fixture_only_non_approval_no_execution():
    text = doc_text()

    required_terms = [
        "L6W.03 report-safe supervised live-read receipt output contract",
        "Status: `RECEIPT_CONTRACT_ONLY_NO_APPROVAL_NO_EXECUTION`",
        "Rail issue: #201",
        "Prerequisite: #200 closed/PASS",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`",
        "Denial dependency: `docs/l6w02-supervised-live-read-approval-denial-matrix.md`",
        "docs/tests/schema-fixture-only",
        "does not approve, implement, recognize, execute, or simulate a live/private read",
        "`NO_APPROVAL_PRESENT`",
        "separate future issue-bound owner approval and later approved implementation recognition",
    ]
    for term in required_terms:
        assert term in text


def test_l6w03_permits_only_report_safe_metadata_receipt_fields():
    text = doc_text()

    for term in PERMITTED_FIELD_TERMS:
        assert term in text

    required_binding_terms = [
        "`operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        "`operation_count`: `1` or `0` when held/denied before read",
        "`max_operation_count`: `1`",
        "`one_operation_binding`: `true`",
        "`allowed`: `false`",
        "`allowed_result_count`: `0`",
        "`live_read_invoked`: `false` in all current fixtures/tests and in any stale/variant/held receipt",
        "report-safe descriptor/source-card refs",
        "booleans, zero counters, one-operation binding, stop-condition status",
    ]
    for term in required_binding_terms:
        assert term in text


def test_l6w03_rejects_unsafe_receipt_fields_and_echoes():
    text = doc_text()

    for term in REJECTED_FIELD_TERMS:
        assert term in text

    required_rejection_terms = [
        "Unsafe input must be rejected before receipt output without echoing the unsafe value",
        "safe rejection may include only the stop reason label and zero counters",
        "`UNSAFE_RECEIPT_FIELD_REJECTED`",
        "proposed receipt output contains a prohibited field or unsafe echo",
    ]
    for term in required_rejection_terms:
        assert term in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6w03_fixture_is_metadata_only_and_zero_countered():
    fixture = extract_fixture()

    assert fixture["schema_id"] == "l6w03.report_safe_supervised_live_read_receipt.v1"
    assert fixture["status"] == "HELD_FOR_FUTURE_APPROVAL"
    assert fixture["approval_status"] == "NO_APPROVAL_PRESENT"
    assert fixture["operation_class"] == "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
    assert fixture["operation_count"] == 0
    assert fixture["max_operation_count"] == 1
    assert fixture["one_operation_binding"] is True
    assert fixture["allowed"] is False
    assert fixture["allowed_result_count"] == 0
    assert fixture["live_read_invoked"] is False
    assert fixture["descriptor_ref"] == "report-safe-descriptor-ref:l6w03-synthetic"
    assert fixture["source_card_ref"] == "report-safe-source-card-ref:l6w03-synthetic"
    assert fixture["stop_condition_status"] == "HELD_PENDING_FUTURE_ISSUE_BOUND_OWNER_APPROVAL"
    assert fixture["stop_reason"] == "NO_APPROVAL_PRESENT"
    assert fixture["usefulness_classification"] == "held"

    for key in ZERO_COUNTER_KEYS:
        assert fixture[key] == 0
    guarded = cast(dict[str, object], fixture["guarded_callback_counters"])
    assert set(guarded) == set(GUARDED_CALLBACK_KEYS)
    assert all(guarded[key] == 0 for key in GUARDED_CALLBACK_KEYS)
    assert fixture["report_safe_flags"] == {
        "raw_content_echoed": False,
        "credential_echoed": False,
        "private_path_echoed": False,
        "source_uri_echoed": False,
        "unsafe_payload_echoed": False,
    }


def test_l6w03_preserves_hard_holds_and_stop_statuses():
    text = doc_text()

    stop_statuses = (
        "`HELD_FOR_FUTURE_APPROVAL`",
        "`DENIED_BEFORE_CALLBACK`",
        "`UNSAFE_RECEIPT_FIELD_REJECTED`",
        "`STOPPED_REQUIRES_NEW_HUMAN_REVIEW`",
    )
    for status in stop_statuses:
        assert status in text

    held_terms = [
        "all guarded counters and side-effect counters are zero",
        "No status in this packet authorizes `allowed=true`",
        "non-zero allowed results",
        "provider/backend/source-stat/source-read callbacks",
        "live/private reads",
        "source discovery",
        "Runtime Registry consumption",
        "persistence",
        "activation",
        "publication",
        "production/provider/prod/canary authority",
        "Atlas Gate movement",
        "mutation execution",
        "rollback callbacks",
        "cache purge callbacks",
        "custody/write/delete/reindex behavior",
        "no-live/no-callback/no-production/no-persistence/no-activation/no-mutation/no-`allowed=true`",
    ]
    for term in held_terms:
        assert term in text
