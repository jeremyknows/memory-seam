from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path

from memory_seam.write_intent_preflight_gate import (
    L6_WRITE_INTENT_APPROVAL_CONTEXT_REQUIRED_FIELDS,
    L6_WRITE_INTENT_DENIAL_REASON,
    L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION,
    L6_WRITE_INTENT_GUARDED_COUNTERS,
    L6_WRITE_INTENT_HELD_SURFACES,
    L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS,
    L6_WRITE_INTENT_OPERATION_CLASS,
    L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
    L6_WRITE_INTENT_PREFLIGHT_GATE_FIXTURE,
    L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF,
    L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION,
    L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE,
    L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS,
    L6_WRITE_INTENT_REPORT_SAFETY,
    WriteIntentPreflightCallbackHarness,
    build_l6_write_intent_denial_receipt_metadata,
    build_l6_write_intent_approval_context_fixture,
    build_l6_write_intent_preflight_gate_fixture,
    parse_write_intent_operation_class,
    run_write_intent_preflight_gate,
    validate_l6_write_intent_approval_context,
    validate_l6_write_intent_preflight_gate_result,
)
REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-intent-preflight-gate.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
SMOKE_EXAMPLE = REPO_ROOT / "examples" / "write_intent_preflight_smoke.py"

_smoke_spec = importlib.util.spec_from_file_location("write_intent_preflight_smoke", SMOKE_EXAMPLE)
assert _smoke_spec is not None and _smoke_spec.loader is not None
_smoke_module = importlib.util.module_from_spec(_smoke_spec)
_smoke_spec.loader.exec_module(_smoke_module)
SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST = _smoke_module.SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST
run_synthetic_write_intent_preflight_smoke = _smoke_module.run_synthetic_write_intent_preflight_smoke

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


def test_gate_doc_records_exact_bounded_default_off_scope():
    text = normalized(DOC)
    required_terms = [
        "L6I.01 write-intent preflight gate skeleton",
        "Status: `write_intent_preflight_gate_default_off_denies`",
        "Slice: `L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON`",
        "Approval reference: `issue-137-comment-4643939613`",
        "Rollback/audit reference: `docs/l6-write-custody-rollback-audit-plan.md`",
        "default-off, synthetic, no-production gate",
        "operation class `write intent` only",
        "maximum `1` synthetic no-production operation",
        "denies before provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "does not execute writes, custody transfer, delete, reindex, rollback, cache purge",
        "does not perform provider/backend/source-stat/source-read callbacks",
        "does not perform live/private source reads, source discovery, unsupervised reads, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, global configuration mutation, recurring activation, publication, visibility changes, or Atlas Gate movement",
    ]
    for term in required_terms:
        assert term in text


def test_fixture_is_report_safe_default_off_and_no_production():
    fixture = build_l6_write_intent_preflight_gate_fixture()

    assert fixture["schema_version"] == L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION
    assert fixture["status"] == L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS
    assert fixture["slice"] == L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE
    assert fixture["approval_ref"] == L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF
    assert fixture["rollback_ref"] == L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF
    assert fixture["operation_class"] == L6_WRITE_INTENT_OPERATION_CLASS
    assert fixture["max_synthetic_operations"] == L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS
    assert fixture["default_off"] is True
    assert fixture["synthetic_no_production_only"] is True
    assert fixture["denied_before_callback"] is True
    assert fixture["allowed"] is False
    assert tuple(fixture["guarded_counters"]) == L6_WRITE_INTENT_GUARDED_COUNTERS
    assert tuple(fixture["held_surfaces"]) == L6_WRITE_INTENT_HELD_SURFACES
    assert fixture["report_safety"] == L6_WRITE_INTENT_REPORT_SAFETY


def test_parser_accepts_only_write_intent_class_without_payload_parsing():
    assert parse_write_intent_operation_class("write intent") == "write intent"
    assert parse_write_intent_operation_class(" write_intent ") == "write intent"
    assert parse_write_intent_operation_class("WRITE-INTENT") == "write intent"
    assert parse_write_intent_operation_class("delete") is None
    assert parse_write_intent_operation_class("custody receipt persistence") is None


def test_gate_denies_write_intent_before_all_guarded_callbacks():
    harness = WriteIntentPreflightCallbackHarness.build()
    result = run_write_intent_preflight_gate("write intent", harness)

    assert result["operation_class"] == "write intent"
    assert result["operation_count"] == 1
    assert result["max_synthetic_operations"] == 1
    assert result["recognized_write_intent"] is True
    assert result["default_off"] is True
    assert result["synthetic_no_production_only"] is True
    assert result["allowed"] is False
    assert result["denied_before_callback"] is True
    assert result["callbacks_invoked"] is False
    assert result["denial_reason"] == L6_WRITE_INTENT_DENIAL_REASON
    assert result["counters"] == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert harness.counters == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert validate_l6_write_intent_preflight_gate_result(result) == []


def test_local_write_intent_preflight_smoke_outputs_report_safe_denial_and_zero_counters():
    smoke = run_synthetic_write_intent_preflight_smoke()

    assert smoke["smoke"] == "l6_write_intent_preflight_no_production"
    assert smoke["request"] == SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST
    assert smoke["request"] == {
        "operation_class": "write intent",
        "synthetic_operation_count": 1,
        "production": False,
        "payload_included": False,
        "source_read_requested": False,
        "credential_read_requested": False,
    }
    assert smoke["allowed"] is False
    assert smoke["denied_before_callback"] is True
    assert smoke["callbacks_invoked"] is False
    assert smoke["operation_class"] == "write intent"
    assert smoke["operation_count"] == 1
    assert smoke["guarded_counters_zero"] is True
    assert smoke["guarded_counters"] == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert smoke["receipt"] == {
        "schema_version": L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION,
        "emitted_for": "denied_no_mutation_path",
        "operation_class": "write intent",
        "denial_reason_code": L6_WRITE_INTENT_DENIAL_REASON,
        "counter_summary": {
            "guarded_counter_count": len(L6_WRITE_INTENT_GUARDED_COUNTERS),
            "guarded_counters_zero": True,
            "nonzero_guarded_counter_count": 0,
        },
    }
    assert smoke["validation_errors"] == []
    assert smoke["report_safe"] is True
    assert smoke["production_executed"] is False


def test_local_write_intent_preflight_smoke_cli_emits_report_safe_json():
    completed = subprocess.run(
        [sys.executable, str(SMOKE_EXAMPLE)],
        check=True,
        capture_output=True,
        text=True,
    )
    smoke = json.loads(completed.stdout)

    assert smoke["smoke"] == "l6_write_intent_preflight_no_production"
    assert smoke["allowed"] is False
    assert smoke["denied_before_callback"] is True
    assert smoke["callbacks_invoked"] is False
    assert smoke["guarded_counters_zero"] is True
    assert smoke["guarded_counters"] == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert smoke["receipt"]["emitted_for"] == "denied_no_mutation_path"
    assert smoke["validation_errors"] == []
    assert smoke["report_safe"] is True
    assert smoke["production_executed"] is False


def test_denial_receipt_metadata_is_report_safe_and_denied_path_only():
    result = run_write_intent_preflight_gate("write intent")
    metadata = result["denial_receipt_metadata"]

    assert metadata == build_l6_write_intent_denial_receipt_metadata(result)
    assert metadata["schema_version"] == L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION
    assert metadata["emitted_for"] == "denied_no_mutation_path"
    assert metadata["operation_class"] == "write intent"
    assert metadata["denial_reason_code"] == L6_WRITE_INTENT_DENIAL_REASON
    assert metadata["counter_summary"] == {
        "guarded_counter_count": len(L6_WRITE_INTENT_GUARDED_COUNTERS),
        "guarded_counters_zero": True,
        "nonzero_guarded_counter_count": 0,
    }
    assert metadata["approval_reference_shape"] == {
        "kind": "public_issue_comment_reference",
        "reference": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
        "issue": 137,
        "raw_approval_text_included": False,
    }
    assert metadata["rollback_audit_reference_shape"] == {
        "kind": "repository_document_reference",
        "reference": L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF,
        "raw_private_text_included": False,
    }
    assert tuple(metadata["residual_holds"]) == L6_WRITE_INTENT_HELD_SURFACES
    assert metadata["report_safety"] == L6_WRITE_INTENT_REPORT_SAFETY

    mutated = dict(result)
    mutated["allowed"] = True
    assert build_l6_write_intent_denial_receipt_metadata(mutated) is None
    nonzero = dict(result)
    nonzero["counters"] = dict(result["counters"])
    nonzero["counters"]["write_callbacks"] = 1
    assert build_l6_write_intent_denial_receipt_metadata(nonzero) is None


def test_unsupported_denial_receipt_metadata_stays_safe_without_operation_count():
    result = run_write_intent_preflight_gate("delete")
    metadata = result["denial_receipt_metadata"]

    assert result["operation_count"] == 0
    assert metadata["operation_class"] == "unsupported_operation_class"
    assert metadata["denial_reason_code"] == "unsupported_operation_class_denied"
    assert metadata["counter_summary"]["guarded_counters_zero"] is True
    assert validate_l6_write_intent_preflight_gate_result(result) == []


def test_approval_context_fixture_is_report_safe_and_valid_within_window():
    approval_context = build_l6_write_intent_approval_context_fixture()

    assert tuple(approval_context[field] for field in L6_WRITE_INTENT_APPROVAL_CONTEXT_REQUIRED_FIELDS)
    assert approval_context["approval_ref"] == L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF
    assert approval_context["approval_issue"] == 137
    assert approval_context["author_association"] == "OWNER"
    assert approval_context["operation_class"] == "write intent"
    assert approval_context["max_synthetic_operations"] == 1
    assert approval_context["raw_approval_text_included"] is False
    assert approval_context["raw_actor_id_included"] is False
    assert validate_l6_write_intent_approval_context(approval_context) == ()


def test_stale_or_mismatched_approval_matrix_denies_before_callbacks_with_safe_metadata():
    cases = [
        ("wrong issue", {"approval_issue": 999}, "mismatched_approval_issue"),
        ("wrong actor", {"author_association": "CONTRIBUTOR"}, "mismatched_approval_actor"),
        ("wrong ref", {"approval_ref": "issue-000-comment-redacted"}, "mismatched_approval_ref"),
        ("wrong operation", {"operation_class": "delete"}, "mismatched_approval_operation_class"),
        (
            "exceeded max count",
            {"max_synthetic_operations": 2},
            "exceeded_approval_max_synthetic_operations",
        ),
        (
            "stale window",
            {"approval_expires_at": "2026-06-07T20:03:10Z"},
            "stale_approval_window",
        ),
        (
            "expired approval",
            {"evaluation_time": "2026-06-08T20:03:10Z"},
            "approval_expired",
        ),
    ]

    for _name, overrides, expected_code in cases:
        approval_context = build_l6_write_intent_approval_context_fixture()
        approval_context.update(overrides)
        harness = WriteIntentPreflightCallbackHarness.build()
        result = run_write_intent_preflight_gate("write intent", harness, approval_context)
        metadata = result["denial_receipt_metadata"]

        assert expected_code in validate_l6_write_intent_approval_context(approval_context)
        assert expected_code in result["approval_denial_codes"]
        assert result["allowed"] is False
        assert result["denied_before_callback"] is True
        assert result["callbacks_invoked"] is False
        assert result["denial_reason"].startswith("write_intent_approval_")
        assert result["counters"] == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
        assert harness.counters == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
        assert metadata["emitted_for"] == "denied_no_mutation_path"
        assert metadata["counter_summary"]["guarded_counters_zero"] is True
        assert metadata["approval_reference_shape"]["raw_approval_text_included"] is False
        assert metadata["report_safety"] == L6_WRITE_INTENT_REPORT_SAFETY
        assert validate_l6_write_intent_preflight_gate_result(result) == []


def test_gate_denies_unsupported_classes_without_operation_count_or_callbacks():
    harness = WriteIntentPreflightCallbackHarness.build()
    result = run_write_intent_preflight_gate("delete", harness)

    assert result["operation_class"] == "unsupported_operation_class"
    assert result["operation_count"] == 0
    assert result["recognized_write_intent"] is False
    assert result["allowed"] is False
    assert result["denied_before_callback"] is True
    assert result["callbacks_invoked"] is False
    assert result["denial_reason"] == "unsupported_operation_class_denied"
    assert result["counters"] == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert harness.counters == {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}
    assert validate_l6_write_intent_preflight_gate_result(result) == []


def test_callbacks_fail_fast_if_a_regression_invokes_one():
    harness = WriteIntentPreflightCallbackHarness.build()
    counter_name = L6_WRITE_INTENT_GUARDED_COUNTERS[0]

    try:
        harness.callbacks[counter_name]()
    except AssertionError as exc:
        assert str(exc) == f"unexpected_write_intent_callback:{counter_name}"
    else:  # pragma: no cover - defensive proof that callback cannot silently pass
        raise AssertionError("callback unexpectedly returned")

    assert harness.counters[counter_name] == 1


def test_validator_rejects_authorizing_or_nonzero_regressions_with_safe_codes():
    result = run_write_intent_preflight_gate("write intent")
    result["schema_version"] = "unexpected"
    result["status"] = "unexpected"
    result["slice"] = "unexpected"
    result["approval_ref"] = "unexpected"
    result["rollback_ref"] = "unexpected"
    result["operation_count"] = 2
    result["default_off"] = False
    result["synthetic_no_production_only"] = False
    result["allowed"] = True
    result["denied_before_callback"] = False
    result["callbacks_invoked"] = True
    result["counters"]["write_callbacks"] = 1
    result["report_safety"]["raw_payload_content"] = True
    result["held_surfaces"] = tuple(
        surface for surface in result["held_surfaces"] if surface != "cache_purge_execution"
    )

    assert validate_l6_write_intent_preflight_gate_result(result) == [
        "unexpected_schema_version",
        "unexpected_status",
        "unexpected_slice",
        "unexpected_approval_ref",
        "unexpected_rollback_ref",
        "exceeded_max_synthetic_operations",
        "default_off_not_true",
        "synthetic_no_production_only_not_true",
        "denied_before_callback_not_true",
        "allowed_not_false",
        "callbacks_invoked_not_false",
        "nonzero_counter_write_callbacks",
        "unsafe_report_safety_flag",
        "missing_held_surface_cache_purge_execution",
    ]


def test_builder_returns_copies_so_fixture_stays_stable():
    fixture = build_l6_write_intent_preflight_gate_fixture()
    fixture["default_off"] = False
    fixture["report_safety"]["credentials_or_auth_material"] = True

    fresh_fixture = build_l6_write_intent_preflight_gate_fixture()

    assert fresh_fixture["default_off"] is True
    assert fresh_fixture["report_safety"]["credentials_or_auth_material"] is False
    assert L6_WRITE_INTENT_PREFLIGHT_GATE_FIXTURE["default_off"] is True


def test_gate_artifacts_are_report_safe_and_discoverable():
    rendered = repr(build_l6_write_intent_preflight_gate_fixture()) + repr(
        run_write_intent_preflight_gate("write intent")
    )

    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)
    assert "l6-write-intent-preflight-gate.md" in docs_index
    assert "tests/test_l6_write_intent_preflight_gate.py" in inventory
    assert "L6I.01 write-intent preflight gate skeleton" in inventory
