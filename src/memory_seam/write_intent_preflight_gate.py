"""Default-off synthetic write-intent preflight gate skeleton.

This module implements the bounded L6I.01 slice approved for issue #137:
parse operation class ``write intent`` and deny before every guarded callback.
It does not execute writes, custody transfer, delete, reindex, rollback, cache
purge, provider/backend calls, source-stat/source-read calls, source discovery,
live/private reads, Runtime Registry access, activation, persistence, global
configuration mutation, publication, visibility changes, or Atlas Gate movement.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS = "write_intent_preflight_gate_default_off_denies"
L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION = "l6-write-intent-preflight-gate-v1"
L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION = "l6-write-intent-denial-receipt-v1"
L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE = "L6_WRITE_INTENT_PREFLIGHT_GATE_SKELETON"
L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF = "issue-137-comment-4643939613"
L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_ISSUE = 137
L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_AUTHOR_ASSOCIATION = "OWNER"
L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_CREATED_AT = "2026-06-07T20:03:10Z"
L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_EXPIRES_AT = "2026-06-08T20:03:10Z"
L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF = "docs/l6-write-custody-rollback-audit-plan.md"
L6_WRITE_INTENT_OPERATION_CLASS = "write intent"
L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS = 1
L6_WRITE_INTENT_DENIAL_REASON = "write_intent_preflight_default_off_denied"

L6_WRITE_INTENT_APPROVAL_CONTEXT_REQUIRED_FIELDS = (
    "approval_ref",
    "approval_issue",
    "author_association",
    "operation_class",
    "max_synthetic_operations",
    "approval_created_at",
    "approval_expires_at",
    "evaluation_time",
)

L6_WRITE_INTENT_GUARDED_COUNTERS = (
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

L6_WRITE_INTENT_HELD_SURFACES = (
    "write_execution",
    "custody_transfer",
    "delete_execution",
    "reindex_execution",
    "rollback_execution",
    "cache_purge_execution",
    "provider_backend_calls",
    "source_stat_calls",
    "source_read_calls",
    "source_discovery",
    "live_private_source_reads",
    "unsupervised_reads",
    "recurring_runner_or_activation",
    "runtime_registry_consumption",
    "global_config_mutation",
    "credential_auth_env_keychain_oauth_authfile_reads",
    "provider_prod_canary_authority",
    "publication_or_visibility_change",
    "atlas_gate_movement",
)

L6_WRITE_INTENT_REPORT_SAFETY = {
    "raw_private_text": False,
    "credentials_or_auth_material": False,
    "private_paths": False,
    "raw_platform_ids": False,
    "raw_query_payloads": False,
    "raw_payload_content": False,
    "private_correlation_refs": False,
}


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS}


def _parse_report_safe_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class WriteIntentPreflightCallbackHarness:
    """Synthetic callback bundle that fails if denial-before-callback regresses."""

    callbacks: Mapping[str, Callable[[], None]]
    counters: dict[str, int]

    @classmethod
    def build(cls) -> "WriteIntentPreflightCallbackHarness":
        counters = _zero_counters()

        def make_callback(name: str) -> Callable[[], None]:
            def callback() -> None:
                counters[name] += 1
                raise AssertionError(f"unexpected_write_intent_callback:{name}")

            return callback

        callbacks = {name: make_callback(name) for name in L6_WRITE_INTENT_GUARDED_COUNTERS}
        return cls(callbacks=callbacks, counters=counters)


L6_WRITE_INTENT_PREFLIGHT_GATE_FIXTURE: dict[str, Any] = {
    "schema_version": L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION,
    "status": L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS,
    "slice": L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE,
    "approval_ref": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
    "rollback_ref": L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF,
    "operation_class": L6_WRITE_INTENT_OPERATION_CLASS,
    "max_synthetic_operations": L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS,
    "default_off": True,
    "synthetic_no_production_only": True,
    "denied_before_callback": True,
    "allowed": False,
    "guarded_counters": L6_WRITE_INTENT_GUARDED_COUNTERS,
    "held_surfaces": L6_WRITE_INTENT_HELD_SURFACES,
    "report_safety": L6_WRITE_INTENT_REPORT_SAFETY,
}


def parse_write_intent_operation_class(operation_class: str) -> str | None:
    """Return the allowed operation class only for the exact write-intent slice.

    The parser accepts safe spelling variants for the same synthetic class, but
    maps every accepted value to the report-safe canonical ``write intent``. It
    does not parse payloads or inspect source data.
    """

    normalized = " ".join(operation_class.strip().lower().replace("_", " ").replace("-", " ").split())
    if normalized == L6_WRITE_INTENT_OPERATION_CLASS:
        return L6_WRITE_INTENT_OPERATION_CLASS
    return None


def build_l6_write_intent_preflight_gate_fixture() -> dict[str, Any]:
    """Return a copied default-off gate fixture with no mutation authority."""

    return deepcopy(L6_WRITE_INTENT_PREFLIGHT_GATE_FIXTURE)


def build_l6_write_intent_approval_context_fixture() -> dict[str, Any]:
    """Return the report-safe approval context shape required for #137.

    The context contains only public issue/comment references, actor association,
    operation-class scope, count limits, and timestamps. It intentionally omits
    raw approval text, raw actor/login IDs, payloads, credentials, and private
    references.
    """

    return {
        "approval_ref": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
        "approval_issue": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_ISSUE,
        "author_association": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_AUTHOR_ASSOCIATION,
        "operation_class": L6_WRITE_INTENT_OPERATION_CLASS,
        "max_synthetic_operations": L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS,
        "approval_created_at": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_CREATED_AT,
        "approval_expires_at": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_EXPIRES_AT,
        "evaluation_time": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_CREATED_AT,
        "raw_approval_text_included": False,
        "raw_actor_id_included": False,
    }


def validate_l6_write_intent_approval_context(approval_context: Mapping[str, Any]) -> tuple[str, ...]:
    """Return report-safe denial codes for stale or mismatched approvals."""

    errors: list[str] = []
    for field in L6_WRITE_INTENT_APPROVAL_CONTEXT_REQUIRED_FIELDS:
        if field not in approval_context:
            errors.append(f"missing_{field}")
    if approval_context.get("approval_ref") != L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF:
        errors.append("mismatched_approval_ref")
    if approval_context.get("approval_issue") != L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_ISSUE:
        errors.append("mismatched_approval_issue")
    if approval_context.get("author_association") != L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_AUTHOR_ASSOCIATION:
        errors.append("mismatched_approval_actor")
    if parse_write_intent_operation_class(str(approval_context.get("operation_class", ""))) != L6_WRITE_INTENT_OPERATION_CLASS:
        errors.append("mismatched_approval_operation_class")
    max_count = approval_context.get("max_synthetic_operations")
    if not isinstance(max_count, int) or max_count > L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS:
        errors.append("exceeded_approval_max_synthetic_operations")
    created_at = _parse_report_safe_timestamp(approval_context.get("approval_created_at"))
    expires_at = _parse_report_safe_timestamp(approval_context.get("approval_expires_at"))
    evaluation_time = _parse_report_safe_timestamp(approval_context.get("evaluation_time"))
    if created_at is None:
        errors.append("invalid_approval_created_at")
    if expires_at is None:
        errors.append("invalid_approval_expires_at")
    if evaluation_time is None:
        errors.append("invalid_approval_evaluation_time")
    if created_at is not None and expires_at is not None and expires_at <= created_at:
        errors.append("stale_approval_window")
    if evaluation_time is not None and expires_at is not None and evaluation_time >= expires_at:
        errors.append("approval_expired")
    if approval_context.get("raw_approval_text_included") is not False:
        errors.append("unsafe_raw_approval_text_included")
    if approval_context.get("raw_actor_id_included") is not False:
        errors.append("unsafe_raw_actor_id_included")
    return tuple(errors)


def _counter_summary(counters: Mapping[str, int]) -> dict[str, Any]:
    nonzero_counters = tuple(
        counter for counter in L6_WRITE_INTENT_GUARDED_COUNTERS if counters.get(counter, 0) != 0
    )
    return {
        "guarded_counter_count": len(L6_WRITE_INTENT_GUARDED_COUNTERS),
        "guarded_counters_zero": not nonzero_counters,
        "nonzero_guarded_counter_count": len(nonzero_counters),
    }


def build_l6_write_intent_denial_receipt_metadata(result: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return report-safe receipt metadata for denied/no-mutation gate results only."""

    counters = result.get("counters")
    if not isinstance(counters, Mapping):
        return None
    counter_summary = _counter_summary(counters)
    denied_no_mutation_path = (
        result.get("allowed") is False
        and result.get("denied_before_callback") is True
        and result.get("callbacks_invoked") is False
        and counter_summary["guarded_counters_zero"] is True
    )
    if not denied_no_mutation_path:
        return None
    return {
        "schema_version": L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION,
        "emitted_for": "denied_no_mutation_path",
        "operation_class": result.get("operation_class", "unsupported_operation_class"),
        "denial_reason_code": result.get("denial_reason", "write_intent_preflight_denied"),
        "counter_summary": counter_summary,
        "approval_reference_shape": {
            "kind": "public_issue_comment_reference",
            "reference": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
            "issue": 137,
            "raw_approval_text_included": False,
        },
        "rollback_audit_reference_shape": {
            "kind": "repository_document_reference",
            "reference": L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF,
            "raw_private_text_included": False,
        },
        "residual_holds": L6_WRITE_INTENT_HELD_SURFACES,
        "report_safety": deepcopy(L6_WRITE_INTENT_REPORT_SAFETY),
    }


def run_write_intent_preflight_gate(
    operation_class: str,
    harness: WriteIntentPreflightCallbackHarness | None = None,
    approval_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Deny a synthetic write-intent request before guarded callbacks.

    This skeleton performs classification plus counter copying only. It never
    calls ``harness.callbacks`` and therefore cannot perform provider/backend,
    source-stat/source-read, write/custody/delete/reindex/rollback/cache-purge,
    or production work.
    """

    harness = harness or WriteIntentPreflightCallbackHarness.build()
    parsed_operation_class = parse_write_intent_operation_class(operation_class)
    recognized = parsed_operation_class == L6_WRITE_INTENT_OPERATION_CLASS
    approval_denial_codes = (
        validate_l6_write_intent_approval_context(approval_context) if approval_context is not None else ()
    )
    denial_reason = L6_WRITE_INTENT_DENIAL_REASON if recognized else "unsupported_operation_class_denied"
    if recognized and approval_denial_codes:
        denial_reason = f"write_intent_approval_{approval_denial_codes[0]}_denied"
    result = {
        "schema_version": L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION,
        "status": L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS,
        "slice": L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE,
        "approval_ref": L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF,
        "rollback_ref": L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF,
        "operation_class": parsed_operation_class if recognized else "unsupported_operation_class",
        "operation_count": 1 if recognized else 0,
        "max_synthetic_operations": L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS,
        "recognized_write_intent": recognized,
        "default_off": True,
        "synthetic_no_production_only": True,
        "allowed": False,
        "denied_before_callback": True,
        "callbacks_invoked": False,
        "denial_reason": denial_reason,
        "approval_denial_codes": approval_denial_codes,
        "counters": deepcopy(harness.counters),
        "held_surfaces": L6_WRITE_INTENT_HELD_SURFACES,
        "report_safety": deepcopy(L6_WRITE_INTENT_REPORT_SAFETY),
    }
    result["denial_receipt_metadata"] = build_l6_write_intent_denial_receipt_metadata(result)
    return result


def validate_l6_write_intent_preflight_gate_result(result: dict[str, Any]) -> list[str]:
    """Return report-safe validation codes for a gate denial result."""

    errors: list[str] = []
    if result.get("schema_version") != L6_WRITE_INTENT_PREFLIGHT_GATE_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if result.get("status") != L6_WRITE_INTENT_PREFLIGHT_GATE_STATUS:
        errors.append("unexpected_status")
    if result.get("slice") != L6_WRITE_INTENT_PREFLIGHT_GATE_SLICE:
        errors.append("unexpected_slice")
    if result.get("approval_ref") != L6_WRITE_INTENT_PREFLIGHT_GATE_APPROVAL_REF:
        errors.append("unexpected_approval_ref")
    if result.get("rollback_ref") != L6_WRITE_INTENT_PREFLIGHT_GATE_ROLLBACK_REF:
        errors.append("unexpected_rollback_ref")
    if result.get("operation_count", 0) > L6_WRITE_INTENT_MAX_SYNTHETIC_OPERATIONS:
        errors.append("exceeded_max_synthetic_operations")
    for boolean_field in ("default_off", "synthetic_no_production_only", "denied_before_callback"):
        if result.get(boolean_field) is not True:
            errors.append(f"{boolean_field}_not_true")
    if result.get("allowed") is not False:
        errors.append("allowed_not_false")
    if result.get("callbacks_invoked") is not False:
        errors.append("callbacks_invoked_not_false")
    counters = result.get("counters")
    if not isinstance(counters, dict):
        errors.append("missing_counters")
    else:
        for counter in L6_WRITE_INTENT_GUARDED_COUNTERS:
            if counters.get(counter) != 0:
                errors.append(f"nonzero_counter_{counter}")
    if result.get("report_safety") != L6_WRITE_INTENT_REPORT_SAFETY:
        errors.append("unsafe_report_safety_flag")
    metadata = result.get("denial_receipt_metadata")
    if result.get("allowed") is False and result.get("denied_before_callback") is True:
        if not isinstance(metadata, dict):
            errors.append("missing_denial_receipt_metadata")
        else:
            if metadata.get("schema_version") != L6_WRITE_INTENT_DENIAL_RECEIPT_SCHEMA_VERSION:
                errors.append("unexpected_denial_receipt_schema_version")
            if metadata.get("emitted_for") != "denied_no_mutation_path":
                errors.append("unexpected_denial_receipt_emission_path")
            if metadata.get("operation_class") != result.get("operation_class"):
                errors.append("unexpected_denial_receipt_operation_class")
            if metadata.get("denial_reason_code") != result.get("denial_reason"):
                errors.append("unexpected_denial_receipt_reason")
            counter_summary = metadata.get("counter_summary")
            expected_summary = _counter_summary(counters) if isinstance(counters, Mapping) else None
            if not isinstance(counter_summary, dict) or counter_summary != expected_summary:
                errors.append("unexpected_denial_receipt_counter_summary")
            approval_shape = metadata.get("approval_reference_shape")
            if not isinstance(approval_shape, dict) or approval_shape.get("raw_approval_text_included") is not False:
                errors.append("unsafe_denial_receipt_approval_shape")
            rollback_shape = metadata.get("rollback_audit_reference_shape")
            if not isinstance(rollback_shape, dict) or rollback_shape.get("raw_private_text_included") is not False:
                errors.append("unsafe_denial_receipt_rollback_shape")
            if tuple(metadata.get("residual_holds", ())) != L6_WRITE_INTENT_HELD_SURFACES:
                errors.append("unexpected_denial_receipt_residual_holds")
            if metadata.get("report_safety") != L6_WRITE_INTENT_REPORT_SAFETY:
                errors.append("unsafe_denial_receipt_report_safety")
    held_surfaces = tuple(result.get("held_surfaces", ()))
    for surface in L6_WRITE_INTENT_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
