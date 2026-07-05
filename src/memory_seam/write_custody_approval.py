"""Metadata-only ownership and approval fixtures for future L6 write/custody slices.

This module defines public-safe schema fixtures only. It does not implement,
authorize, or execute writes, custody transfer, delete, reindex, rollback, cache
purge, provider/backend calls, source discovery, live/private reads, recurring
runners, services, listeners, cron/startup activation, Runtime Registry
consumption, global configuration mutation, publication, visibility changes, or
Atlas Gate movement.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

L6_WRITE_CUSTODY_APPROVAL_STATUS = "schema_fixture_implementation_held"
L6_WRITE_CUSTODY_APPROVAL_SCHEMA_VERSION = "l6-write-custody-approval-v1"
L6_WRITE_CUSTODY_APPROVAL_REQUIRED_FIELDS = (
    "schema_version",
    "status",
    "approval_ref",
    "approval_phrase_ref",
    "approval_issue",
    "operation_class",
    "custody_owner_role",
    "approver_role",
    "actor_binding",
    "expires_at",
    "max_operation_count",
    "approval_state",
    "report_safe_reference",
    "side_effects",
    "held_surfaces",
    "report_safety",
)
L6_WRITE_CUSTODY_OPERATION_CLASSES = (
    "write_intent",
    "custody_receipt_persistence",
    "delete_intent",
    "reindex_intent",
    "rollback_intent",
    "cache_purge_intent",
)
L6_WRITE_CUSTODY_REQUIRED_APPROVAL_FIELDS = (
    "approval_phrase_ref",
    "approval_issue",
    "operation_class",
    "custody_owner_role",
    "approver_role",
    "actor_binding",
    "expires_at",
    "max_operation_count",
    "report_safe_reference",
)
L6_WRITE_CUSTODY_HELD_SURFACES = (
    "write_execution",
    "custody_transfer",
    "delete_execution",
    "reindex_execution",
    "rollback_execution",
    "cache_purge_execution",
    "provider_backend_calls",
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
_SAFE_SIDE_EFFECTS = {
    "write_callbacks": 0,
    "custody_callbacks": 0,
    "delete_callbacks": 0,
    "reindex_callbacks": 0,
    "rollback_callbacks": 0,
    "cache_purge_callbacks": 0,
    "provider_calls": 0,
    "backend_calls": 0,
    "source_discovery_calls": 0,
    "source_stat_calls": 0,
    "source_read_calls": 0,
    "runtime_registry_reads": 0,
    "activation_callbacks": 0,
}
_REPORT_SAFETY = {
    "raw_private_text": False,
    "credentials_or_auth_material": False,
    "private_paths": False,
    "raw_platform_ids": False,
    "raw_query_payloads": False,
    "raw_payload_content": False,
    "private_correlation_refs": False,
}


def _fixture(*, approval_ref: str, operation_class: str, max_operation_count: int) -> dict[str, Any]:
    return {
        "schema_version": L6_WRITE_CUSTODY_APPROVAL_SCHEMA_VERSION,
        "status": L6_WRITE_CUSTODY_APPROVAL_STATUS,
        "approval_ref": approval_ref,
        "approval_phrase_ref": "exact-future-approval-phrase-required",
        "approval_issue": "future-issue-number-required",
        "operation_class": operation_class,
        "custody_owner_role": "named_memory_custody_owner_required",
        "approver_role": "jeremy_exact_human_approver_required",
        "actor_binding": "named_actor_and_acting_for_subject_required",
        "expires_at": "future_expiry_timestamp_required",
        "max_operation_count": max_operation_count,
        "approval_state": "not_approved_schema_only",
        "report_safe_reference": "approval-reference-public-safe-redacted-link",
        "side_effects": deepcopy(_SAFE_SIDE_EFFECTS),
        "held_surfaces": L6_WRITE_CUSTODY_HELD_SURFACES,
        "report_safety": deepcopy(_REPORT_SAFETY),
    }


L6_WRITE_CUSTODY_APPROVAL_FIXTURES: tuple[dict[str, Any], ...] = tuple(
    _fixture(
        approval_ref=f"approval-fixture-{operation_class.replace('_', '-')}",
        operation_class=operation_class,
        max_operation_count=1,
    )
    for operation_class in L6_WRITE_CUSTODY_OPERATION_CLASSES
)


def build_l6_write_custody_approval_fixtures() -> tuple[dict[str, Any], ...]:
    """Return deep-copied approval fixtures without authorizing execution."""

    return deepcopy(L6_WRITE_CUSTODY_APPROVAL_FIXTURES)


def validate_l6_write_custody_approval_fixture(fixture: dict[str, Any]) -> list[str]:
    """Return report-safe validation errors for an L6 approval schema fixture."""

    errors: list[str] = []
    for field in L6_WRITE_CUSTODY_APPROVAL_REQUIRED_FIELDS:
        if field not in fixture:
            errors.append(f"missing_{field}")
    if fixture.get("schema_version") != L6_WRITE_CUSTODY_APPROVAL_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if fixture.get("status") != L6_WRITE_CUSTODY_APPROVAL_STATUS:
        errors.append("unexpected_status")
    if fixture.get("operation_class") not in L6_WRITE_CUSTODY_OPERATION_CLASSES:
        errors.append("unexpected_operation_class")
    if fixture.get("approval_state") != "not_approved_schema_only":
        errors.append("unexpected_approval_state")
    for field in L6_WRITE_CUSTODY_REQUIRED_APPROVAL_FIELDS:
        value = fixture.get(field)
        if value in (None, ""):
            errors.append(f"missing_required_approval_field_{field}")
    max_operation_count = fixture.get("max_operation_count")
    if not isinstance(max_operation_count, int) or max_operation_count < 1:
        errors.append("invalid_max_operation_count")
    side_effects = fixture.get("side_effects")
    if not isinstance(side_effects, dict):
        errors.append("missing_side_effect_counters")
    elif side_effects != _SAFE_SIDE_EFFECTS:
        errors.append("nonzero_side_effect_counter")
    report_safety = fixture.get("report_safety")
    if not isinstance(report_safety, dict):
        errors.append("missing_report_safety_flags")
    elif report_safety != _REPORT_SAFETY:
        errors.append("unsafe_report_safety_flag")
    held_surfaces = tuple(fixture.get("held_surfaces", ()))
    for surface in L6_WRITE_CUSTODY_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
