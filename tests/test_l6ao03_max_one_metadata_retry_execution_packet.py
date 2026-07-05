from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from memory_seam.l6ao_auth_held_default_off_intake import (
    L6AO03_PACKET_STATUS,
    L6AO03_REFUSED_STATUS,
    assert_l6ao03_execution_packet_report_safe,
    build_l6ao03_max_one_metadata_retry_execution_packet,
    evaluate_l6ao03_execution_authorization,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ao03-max-one-metadata-retry-execution-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def assert_retry_refused_and_counters_zero(receipt: dict[str, object]) -> None:
    counters = receipt["guarded_counters"]
    assert isinstance(counters, Mapping)
    assert receipt["retry_authorized"] is False
    assert receipt["retry_executed"] is False
    assert all(value == 0 for value in counters.values())
    assert_l6ao03_execution_packet_report_safe(receipt)


def test_l6ao03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ao03-max-one-metadata-retry-execution-packet.md" in docs_index
    assert "tests/test_l6ao03_max_one_metadata_retry_execution_packet.py" in inventory
    assert "L6AO.03 max-one metadata retry execution packet" in inventory
    assert L6AO03_PACKET_STATUS in inventory


def test_execution_packet_names_exact_target_output_and_stop_conditions() -> None:
    packet = build_l6ao03_max_one_metadata_retry_execution_packet()
    target = packet["target"]

    assert packet["status"] == L6AO03_PACKET_STATUS
    assert target["endpoint"] == "memory_seam_recall"
    assert target["agent"] == "sax"
    assert target["scope"] == "wiki"
    assert target["n"] == 3
    assert target["query_label"] == "supervised_metadata_readiness"
    assert target["evidence_class"] == "SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE"
    assert target["max_operation_count"] == 1
    assert target["report_safe_metadata_only"] is True
    assert target["denial_before_read_required"] is True
    assert "items_count" in packet["report_safe_output_fields"]
    assert "safe_item_labels" in packet["report_safe_output_fields"]
    assert "missing_fresh_exact_non_secret_binding_approval" in packet["denial_before_read_stop_conditions"]
    assert "missing_explicit_retry_issue_authorization" in packet["denial_before_read_stop_conditions"]
    assert_retry_refused_and_counters_zero(packet)


def test_absent_approval_or_retry_issue_authorization_refuses_before_read() -> None:
    cases = (
        ({}, {"missing_fresh_exact_non_secret_binding_approval", "missing_explicit_retry_issue_authorization"}),
        ({"fresh_exact_non_secret_binding_approval": True}, {"missing_explicit_retry_issue_authorization"}),
        ({"explicit_retry_issue_authorization": True}, {"missing_fresh_exact_non_secret_binding_approval"}),
    )

    for candidate, reasons in cases:
        receipt = evaluate_l6ao03_execution_authorization(candidate)

        assert receipt["status"] == L6AO03_REFUSED_STATUS
        assert reasons.issubset(set(receipt["refusal_reasons"]))
        assert_retry_refused_and_counters_zero(receipt)


def test_stale_wrong_or_multi_operation_authority_refuses_before_read() -> None:
    base = {
        "fresh_exact_non_secret_binding_approval": True,
        "explicit_retry_issue_authorization": True,
    }
    cases = (
        ({"binding_approval_state": "stale"}, "stale_or_mismatched_binding_approval"),
        ({"binding_approval_fresh": False}, "stale_or_mismatched_binding_approval"),
        ({"endpoint": "wrong_endpoint"}, "wrong_endpoint"),
        ({"scope": "all"}, "wrong_scope"),
        ({"n": 4}, "wrong_n"),
        ({"query_text": "broadened query"}, "wrong_query_text"),
        ({"max_operation_count": 2}, "max_operation_count_not_one"),
        ({"report_safe_metadata_only": False}, "report_safe_metadata_only_not_true"),
        ({"denial_before_read_required": False}, "denial_before_read_not_required"),
    )

    for override, reason in cases:
        receipt = evaluate_l6ao03_execution_authorization(base | override)

        assert receipt["status"] == L6AO03_REFUSED_STATUS
        assert reason in receipt["refusal_reasons"]
        assert_retry_refused_and_counters_zero(receipt)


def test_held_surface_requests_and_broad_allow_refuse_before_read() -> None:
    base = {
        "fresh_exact_non_secret_binding_approval": True,
        "explicit_retry_issue_authorization": True,
    }
    cases = (
        ("raw_output_requested", "raw_private_source_or_auth_content_requested"),
        ("credential_read_requested", "secret_env_keychain_oauth_auth_file_or_credential_read_requested"),
        ("runtime_registry_requested", "runtime_registry_provider_callback_or_service_activation_requested"),
        ("provider_callback_requested", "runtime_registry_provider_callback_or_service_activation_requested"),
        ("service_activation_requested", "runtime_registry_provider_callback_or_service_activation_requested"),
        ("source_discovery_requested", "source_discovery_broad_recall_or_broad_allowed_true_requested"),
        ("allowed", "source_discovery_broad_recall_or_broad_allowed_true_requested"),
        ("write_requested", "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested"),
        ("atlas_gate_requested", "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested"),
    )

    for field, reason in cases:
        receipt = evaluate_l6ao03_execution_authorization(base | {field: True})

        assert receipt["status"] == L6AO03_REFUSED_STATUS
        assert reason in receipt["refusal_reasons"]
        assert_retry_refused_and_counters_zero(receipt)


def test_receipt_assertion_rejects_unsafe_fields_nonzero_counters_or_retry() -> None:
    receipt = build_l6ao03_max_one_metadata_retry_execution_packet()

    for unsafe in (
        receipt | {"raw_private_source": "forbidden"},
        receipt | {"retry_executed": True},
        receipt | {"retry_authorized": True},
        receipt | {"guarded_counters": receipt["guarded_counters"] | {"source_items_returned": 1}},
        receipt | {"report_safe_output_fields": ["raw_private_source"]},
    ):
        try:
            assert_l6ao03_execution_packet_report_safe(unsafe)
        except AssertionError:
            pass
        else:  # pragma: no cover - defensive guard
            raise AssertionError("unsafe L6AO.03 execution packet should fail closed")


def test_doc_names_acceptance_boundaries_and_verification() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AO.03 max-one metadata retry execution packet scaffold",
        "Rail issue: #382",
        "Parent issue: #6",
        "Source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`",
        L6AO03_PACKET_STATUS,
        L6AO03_REFUSED_STATUS,
        "memory_seam_recall",
        "query_label=`supervised_metadata_readiness`",
        "scope=`wiki`",
        "n=`3`",
        "evidence_class=`SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`",
        "report_safe_metadata_only=`true`",
        "missing_fresh_exact_non_secret_binding_approval",
        "missing_explicit_retry_issue_authorization",
        "stale_or_mismatched_binding_approval",
        "raw_private_source_or_auth_content_requested",
        "runtime_registry_provider_callback_or_service_activation_requested",
        "provider_prod_canary_gate_atlas_gate_write_or_mutation_requested",
        "retry_authorized=false",
        "retry_executed=false",
        "python -m pytest -q tests/test_l6ao03_max_one_metadata_retry_execution_packet.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text

    lowered = text.lower()
    for forbidden_marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "source://",
        "private path value",
        "raw source text",
    ):
        assert forbidden_marker not in lowered
