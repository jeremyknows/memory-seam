"""Synthetic positive-authorization receipt skeleton held before mutation.

This module implements the bounded L6P.01 slice approved for issue #163. It
recognizes only a report-safe digest of the exact fresh approval phrase plus the
required public fields for that issue, then emits a non-persistent report-safe
receipt with status ``positive_authorization_recognized_mutation_held``.

It does not return an allowed result, execute mutation, call providers/backends,
stat or read sources, write/custody/delete/reindex/rollback/cache-purge, persist
a receipt, discover sources, consume Runtime Registry, mutate configuration,
activate services/listeners/startup/cron, publish, change repository visibility,
claim provider/prod/canary authority, or move Atlas Gate.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS = "positive_authorization_recognized_mutation_held"
L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS = "positive_authorization_denied_before_callback"
L6_POSITIVE_AUTHORIZATION_RECEIPT_SCHEMA_VERSION = "l6-positive-authorization-receipt-v1"
L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE = "L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON"
L6_POSITIVE_AUTHORIZATION_APPROVAL_REF = "issue-163-comment-4644464163"
L6_POSITIVE_AUTHORIZATION_APPROVAL_SOURCE_URL = (
    "fixture:l6-positive-authorization-approval-source:internal-review-2026"
)
L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE = 163
L6_POSITIVE_AUTHORIZATION_APPROVAL_PACKET = "docs/l6-positive-authorization-approval-decision-packet.md"
L6_POSITIVE_AUTHORIZATION_APPROVAL_AUTHOR_ASSOCIATION = "OWNER"
L6_POSITIVE_AUTHORIZATION_APPROVAL_SUBJECT = "memory-seam-l6-positive-authorization-receipt-skeleton"
L6_POSITIVE_AUTHORIZATION_APPROVAL_OWNER_SCOPE = "jeremyknows/memory-seam#163"
L6_POSITIVE_AUTHORIZATION_IMPLEMENTATION_ACTOR_ROLE = "sax"
L6_POSITIVE_AUTHORIZATION_APPROVAL_CREATED_AT = "2026-06-07T23:48:01Z"
L6_POSITIVE_AUTHORIZATION_APPROVAL_EXPIRES_AT = "2026-06-08T23:48:01Z"
L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256 = (
    "50daf0f4634692f97c6d92a0bae6ca42272a94d122fafd4c1f409e12c8b96429"
)
L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT = 1

L6_POSITIVE_AUTHORIZATION_REQUIRED_APPROVAL_FIELDS = (
    "approval_ref",
    "approval_source_url",
    "approval_issue",
    "approval_packet",
    "approval_phrase_sha256",
    "author_association",
    "approval_subject",
    "approval_owner_scope",
    "implementation_actor_role",
    "operation_class",
    "operation_count",
    "max_operation_count",
    "approval_created_at",
    "approval_expires_at",
    "evaluation_time",
)

L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS = (
    "allowed_result_count",
    "provider_callback_count",
    "backend_callback_count",
    "source_stat_callback_count",
    "source_read_callback_count",
    "write_callback_count",
    "custody_callback_count",
    "delete_callback_count",
    "reindex_callback_count",
    "rollback_callback_count",
    "cache_purge_callback_count",
    "persistent_receipt_count",
    "durable_write_record_count",
    "audit_persistence_count",
    "cache_mutation_count",
)

L6_POSITIVE_AUTHORIZATION_HELD_SURFACES = (
    "provider_backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "write_execution",
    "custody_transfer_or_persistence",
    "delete_execution",
    "reindex_execution",
    "rollback_execution",
    "cache_purge_execution",
    "receipt_persistence",
    "source_discovery",
    "live_private_reads",
    "runtime_registry_consumption",
    "global_config_mutation",
    "service_listener_startup_cron_activation",
    "publication_or_visibility_change",
    "provider_prod_canary_authority",
    "atlas_gate_movement",
)

L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY = {
    "raw_approval_text_included": False,
    "raw_actor_id_included": False,
    "raw_private_text_included": False,
    "credentials_or_auth_material_included": False,
    "private_paths_included": False,
    "raw_platform_ids_included": False,
    "raw_query_payloads_included": False,
    "raw_payload_content_included": False,
    "private_correlation_refs_included": False,
}

L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REQUEST_FLAGS = (
    "storage_persistence_requested",
    "receipt_persistence_requested",
    "audit_persistence_requested",
    "provider_callback_requested",
    "backend_callback_requested",
    "source_stat_callback_requested",
    "source_read_callback_requested",
    "write_callback_requested",
    "custody_callback_requested",
    "delete_callback_requested",
    "reindex_callback_requested",
    "rollback_callback_requested",
    "cache_purge_callback_requested",
    "live_private_read_requested",
    "source_discovery_requested",
    "runtime_registry_consumption_requested",
    "global_config_mutation_requested",
    "service_listener_startup_cron_activation_requested",
    "publication_requested",
    "repository_visibility_change_requested",
    "provider_prod_canary_authority_requested",
    "atlas_gate_movement_requested",
)

L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REPORT_INPUT_FIELDS = (
    "raw_approval_text",
    "raw_payload",
    "private_path",
    "token_shaped_string",
    "raw_platform_id",
    "private_correlation_ref",
    "raw_query_payload",
    "raw_payload_content",
)


def _zero_counters() -> dict[str, int]:
    return {counter: 0 for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS}


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
class PositiveAuthorizationCallbackHarness:
    """Synthetic callback bundle that fails if held paths invoke callbacks."""

    callbacks: Mapping[str, Callable[[], None]]
    counters: dict[str, int]

    @classmethod
    def build(cls) -> "PositiveAuthorizationCallbackHarness":
        counters = _zero_counters()

        def make_callback(name: str) -> Callable[[], None]:
            def callback() -> None:
                counters[name] += 1
                raise AssertionError(f"unexpected_positive_authorization_callback:{name}")

            return callback

        callbacks = {name: make_callback(name) for name in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS}
        return cls(callbacks=callbacks, counters=counters)


def build_l6_positive_authorization_approval_context_fixture() -> dict[str, Any]:
    """Return report-safe exact-approval fields for issue #163.

    The context binds the public issue/comment reference, packet path, actor
    roles, exact phrase digest, one-operation limit, and expiry window. It
    intentionally omits raw approval text, raw actor IDs, credentials, private
    payloads, and private references.
    """

    return {
        "approval_ref": L6_POSITIVE_AUTHORIZATION_APPROVAL_REF,
        "approval_source_url": L6_POSITIVE_AUTHORIZATION_APPROVAL_SOURCE_URL,
        "approval_issue": L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE,
        "approval_packet": L6_POSITIVE_AUTHORIZATION_APPROVAL_PACKET,
        "approval_phrase_sha256": L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256,
        "author_association": L6_POSITIVE_AUTHORIZATION_APPROVAL_AUTHOR_ASSOCIATION,
        "approval_subject": L6_POSITIVE_AUTHORIZATION_APPROVAL_SUBJECT,
        "approval_owner_scope": L6_POSITIVE_AUTHORIZATION_APPROVAL_OWNER_SCOPE,
        "implementation_actor_role": L6_POSITIVE_AUTHORIZATION_IMPLEMENTATION_ACTOR_ROLE,
        "operation_class": L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        "operation_count": 1,
        "max_operation_count": L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT,
        "approval_created_at": L6_POSITIVE_AUTHORIZATION_APPROVAL_CREATED_AT,
        "approval_expires_at": L6_POSITIVE_AUTHORIZATION_APPROVAL_EXPIRES_AT,
        "evaluation_time": L6_POSITIVE_AUTHORIZATION_APPROVAL_CREATED_AT,
        **deepcopy(L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY),
    }


def validate_l6_positive_authorization_approval_context(approval_context: Mapping[str, Any]) -> tuple[str, ...]:
    """Return report-safe denial codes for non-exact, stale, or unsafe approvals."""

    errors: list[str] = []
    for field in L6_POSITIVE_AUTHORIZATION_REQUIRED_APPROVAL_FIELDS:
        if field not in approval_context:
            errors.append(f"missing_{field}")
    expected_pairs = {
        "approval_ref": L6_POSITIVE_AUTHORIZATION_APPROVAL_REF,
        "approval_source_url": L6_POSITIVE_AUTHORIZATION_APPROVAL_SOURCE_URL,
        "approval_issue": L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE,
        "approval_packet": L6_POSITIVE_AUTHORIZATION_APPROVAL_PACKET,
        "approval_phrase_sha256": L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256,
        "author_association": L6_POSITIVE_AUTHORIZATION_APPROVAL_AUTHOR_ASSOCIATION,
        "approval_subject": L6_POSITIVE_AUTHORIZATION_APPROVAL_SUBJECT,
        "approval_owner_scope": L6_POSITIVE_AUTHORIZATION_APPROVAL_OWNER_SCOPE,
        "implementation_actor_role": L6_POSITIVE_AUTHORIZATION_IMPLEMENTATION_ACTOR_ROLE,
        "operation_class": L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        "max_operation_count": L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT,
    }
    for field, expected in expected_pairs.items():
        if approval_context.get(field) != expected:
            errors.append(f"mismatched_{field}")
    operation_count = approval_context.get("operation_count")
    if not isinstance(operation_count, int) or operation_count != 1:
        errors.append("invalid_operation_count")
    created_at = _parse_report_safe_timestamp(approval_context.get("approval_created_at"))
    expires_at = _parse_report_safe_timestamp(approval_context.get("approval_expires_at"))
    evaluation_time = _parse_report_safe_timestamp(approval_context.get("evaluation_time"))
    if created_at is None:
        errors.append("invalid_approval_created_at")
    if expires_at is None:
        errors.append("invalid_approval_expires_at")
    if evaluation_time is None:
        errors.append("invalid_approval_evaluation_time")
    if created_at is not None and expires_at is not None:
        if expires_at != created_at + timedelta(hours=24):
            errors.append("stale_or_broadened_approval_window")
    if evaluation_time is not None and created_at is not None and evaluation_time < created_at:
        errors.append("approval_not_yet_fresh")
    if evaluation_time is not None and expires_at is not None and evaluation_time >= expires_at:
        errors.append("approval_expired")
    for field, expected in L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY.items():
        if approval_context.get(field) is not expected:
            errors.append(f"unsafe_{field}")
    for field in L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REQUEST_FLAGS:
        if approval_context.get(field) is True:
            errors.append(f"forbidden_{field}")
    for field in L6_POSITIVE_AUTHORIZATION_FORBIDDEN_REPORT_INPUT_FIELDS:
        value = approval_context.get(field)
        if value not in (None, "", (), [], {}):
            errors.append(f"unsafe_report_input_{field}")
    return tuple(errors)


def build_l6_positive_authorization_receipt_metadata(result: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return a non-persistent report-safe receipt only for the exact held path."""

    counters = result.get("counters")
    if not isinstance(counters, Mapping):
        return None
    counters_zero = all(counters.get(counter) == 0 for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS)
    recognized_held_path = (
        result.get("status") == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
        and result.get("recognized_positive_authorization") is True
        and result.get("allowed") is False
        and result.get("mutation_attempted") is False
        and result.get("mutation_supported") is False
        and result.get("callbacks_invoked") is False
        and result.get("fixture_is_persistent") is False
        and counters_zero
    )
    if not recognized_held_path:
        return None
    return {
        "schema_version": L6_POSITIVE_AUTHORIZATION_RECEIPT_SCHEMA_VERSION,
        "status": L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS,
        "operation_class": L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        "operation_count": 1,
        "max_operation_count": L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT,
        "allowed": False,
        "mutation_attempted": False,
        "mutation_supported": False,
        "fixture_is_persistent": False,
        "counter_summary": deepcopy(dict(counters)),
        "approval_reference_shape": {
            "kind": "public_issue_comment_reference",
            "reference": L6_POSITIVE_AUTHORIZATION_APPROVAL_REF,
            "issue": L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE,
            "phrase_sha256": L6_POSITIVE_AUTHORIZATION_APPROVAL_PHRASE_SHA256,
            "raw_approval_text_included": False,
            "raw_actor_id_included": False,
        },
        "decision_packet_reference_shape": {
            "kind": "repository_document_reference",
            "reference": L6_POSITIVE_AUTHORIZATION_APPROVAL_PACKET,
            "raw_private_text_included": False,
        },
        "residual_holds": L6_POSITIVE_AUTHORIZATION_HELD_SURFACES,
        "report_safety": deepcopy(L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY),
    }


def run_positive_authorization_receipt_skeleton(
    operation_class: str,
    harness: PositiveAuthorizationCallbackHarness | None = None,
    approval_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Recognize only the exact issue #163 approval shape and hold mutation.

    The function copies synthetic counters only. It never invokes
    ``harness.callbacks`` and cannot reach provider/backend/source or mutation
    callbacks. Invalid, stale, variant, copied, broadened, or missing approval
    fields deny before callbacks and emit no positive receipt metadata.
    """

    harness = harness or PositiveAuthorizationCallbackHarness.build()
    approval_denial_codes = (
        validate_l6_positive_authorization_approval_context(approval_context)
        if approval_context is not None
        else ("missing_approval_context",)
    )
    operation_matches = operation_class == L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE
    recognized = operation_matches and not approval_denial_codes
    status = L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS if recognized else L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS
    denial_reason = "" if recognized else "positive_authorization_approval_denied_before_callback"
    result = {
        "schema_version": L6_POSITIVE_AUTHORIZATION_RECEIPT_SCHEMA_VERSION,
        "status": status,
        "slice": L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
        "approval_ref": L6_POSITIVE_AUTHORIZATION_APPROVAL_REF,
        "approval_issue": L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE,
        "approval_packet": L6_POSITIVE_AUTHORIZATION_APPROVAL_PACKET,
        "operation_class": operation_class if operation_matches else "unsupported_operation_class",
        "operation_count": 1 if operation_matches else 0,
        "max_operation_count": L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT,
        "recognized_positive_authorization": recognized,
        "synthetic_no_production_only": True,
        "allowed": False,
        "mutation_attempted": False,
        "mutation_supported": False,
        "denied_before_callback": not recognized,
        "callbacks_invoked": False,
        "fixture_is_persistent": False,
        "denial_reason": denial_reason,
        "approval_denial_codes": approval_denial_codes,
        "counters": deepcopy(harness.counters),
        "held_surfaces": L6_POSITIVE_AUTHORIZATION_HELD_SURFACES,
        "report_safety": deepcopy(L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY),
    }
    result["positive_authorization_receipt_metadata"] = build_l6_positive_authorization_receipt_metadata(result)
    return result


def validate_l6_positive_authorization_receipt_result(result: dict[str, Any]) -> list[str]:
    """Return report-safe validation codes for positive-held or denied results."""

    errors: list[str] = []
    if result.get("schema_version") != L6_POSITIVE_AUTHORIZATION_RECEIPT_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if result.get("slice") != L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE:
        errors.append("unexpected_slice")
    if result.get("approval_ref") != L6_POSITIVE_AUTHORIZATION_APPROVAL_REF:
        errors.append("unexpected_approval_ref")
    if result.get("approval_issue") != L6_POSITIVE_AUTHORIZATION_APPROVAL_ISSUE:
        errors.append("unexpected_approval_issue")
    if result.get("operation_count", 0) > L6_POSITIVE_AUTHORIZATION_MAX_OPERATION_COUNT:
        errors.append("exceeded_max_operation_count")
    if result.get("synthetic_no_production_only") is not True:
        errors.append("synthetic_no_production_only_not_true")
    for field in ("allowed", "mutation_attempted", "mutation_supported", "callbacks_invoked", "fixture_is_persistent"):
        if result.get(field) is not False:
            errors.append(f"{field}_not_false")
    counters = result.get("counters")
    if not isinstance(counters, dict):
        errors.append("missing_counters")
    else:
        for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS:
            if counters.get(counter) != 0:
                errors.append(f"nonzero_counter_{counter}")
    if result.get("report_safety") != L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY:
        errors.append("unsafe_report_safety")
    metadata = result.get("positive_authorization_receipt_metadata")
    if result.get("recognized_positive_authorization") is True:
        if result.get("status") != L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS:
            errors.append("unexpected_positive_status")
        if not isinstance(metadata, dict):
            errors.append("missing_positive_authorization_receipt_metadata")
        else:
            if metadata.get("status") != L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS:
                errors.append("unexpected_receipt_status")
            for field in ("allowed", "mutation_attempted", "mutation_supported", "fixture_is_persistent"):
                if metadata.get(field) is not False:
                    errors.append(f"receipt_{field}_not_false")
            counter_summary = metadata.get("counter_summary")
            if not isinstance(counter_summary, dict) or counter_summary != counters:
                errors.append("unexpected_receipt_counter_summary")
            approval_shape = metadata.get("approval_reference_shape")
            if not isinstance(approval_shape, dict):
                errors.append("missing_receipt_approval_shape")
            elif (
                approval_shape.get("raw_approval_text_included") is not False
                or approval_shape.get("raw_actor_id_included") is not False
            ):
                errors.append("unsafe_receipt_approval_shape")
            if metadata.get("report_safety") != L6_POSITIVE_AUTHORIZATION_REPORT_SAFETY:
                errors.append("unsafe_receipt_report_safety")
    else:
        if result.get("status") != L6_POSITIVE_AUTHORIZATION_DENIAL_STATUS:
            errors.append("unexpected_denial_status")
        if metadata is not None:
            errors.append("unexpected_positive_receipt_for_denial")
    held_surfaces = tuple(result.get("held_surfaces", ()))
    for surface in L6_POSITIVE_AUTHORIZATION_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
