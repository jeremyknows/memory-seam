"""Metadata-only operation-class schema fixtures for future L6 write/custody slices.

This module defines public-safe schema fixtures only. It does not implement,
authorize, simulate, activate, schedule, or execute writes, custody transfer,
delete, reindex, rollback, cache purge, provider/backend calls, source
discovery, live/private reads, recurring runners, services, listeners,
cron/startup activation, Runtime Registry consumption, global configuration
mutation, publication, visibility changes, Atlas Gate movement, or production
authoritative behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS = "schema_fixture_implementation_held"
L6_WRITE_CUSTODY_OPERATION_CLASS_SCHEMA_VERSION = "l6-write-custody-operation-classes-v1"
L6_WRITE_CUSTODY_OPERATION_CLASS_REQUIRED_FIELDS = (
    "schema_version",
    "status",
    "operation_class",
    "custody_owner_role",
    "max_operation_count",
    "timeout_ref",
    "rollback_ref",
    "approval_ref",
    "runtime_route",
    "denied_before_mutation",
    "no_op_only",
    "side_effects",
    "held_surfaces",
    "report_safety",
)
L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES = (
    "write_intent",
    "custody_receipt_persistence",
    "delete",
    "reindex",
    "rollback",
    "cache_purge",
)
L6_WRITE_CUSTODY_OPERATION_CLASS_HELD_SURFACES = (
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
    "audit_persistence_callbacks": 0,
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


def _fixture(operation_class: str) -> dict[str, Any]:
    return {
        "schema_version": L6_WRITE_CUSTODY_OPERATION_CLASS_SCHEMA_VERSION,
        "status": L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS,
        "operation_class": operation_class,
        "custody_owner_role": "named_memory_custody_owner_required",
        "max_operation_count": 1,
        "timeout_ref": "future_slice_timeout_required_before_execution",
        "rollback_ref": "l6s-02-rollback-audit-plan-public-safe-fixture",
        "approval_ref": "l6s-01-approval-model-public-safe-reference-required",
        "runtime_route": {
            "supported": False,
            "registered": False,
            "executable": False,
            "authority": "held_until_exact_jeremy_approval",
        },
        "denied_before_mutation": True,
        "no_op_only": True,
        "side_effects": deepcopy(_SAFE_SIDE_EFFECTS),
        "held_surfaces": L6_WRITE_CUSTODY_OPERATION_CLASS_HELD_SURFACES,
        "report_safety": deepcopy(_REPORT_SAFETY),
    }


L6_WRITE_CUSTODY_OPERATION_CLASS_FIXTURES: tuple[dict[str, Any], ...] = tuple(
    _fixture(operation_class) for operation_class in L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES
)


def build_l6_write_custody_operation_class_fixtures() -> tuple[dict[str, Any], ...]:
    """Return deep-copied operation-class fixtures without mutation authority."""

    return deepcopy(L6_WRITE_CUSTODY_OPERATION_CLASS_FIXTURES)


def validate_l6_write_custody_operation_class_fixture(fixture: dict[str, Any]) -> list[str]:
    """Return report-safe validation errors for an L6 operation-class fixture."""

    errors: list[str] = []
    for field in L6_WRITE_CUSTODY_OPERATION_CLASS_REQUIRED_FIELDS:
        if field not in fixture:
            errors.append(f"missing_{field}")
    if fixture.get("schema_version") != L6_WRITE_CUSTODY_OPERATION_CLASS_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if fixture.get("status") != L6_WRITE_CUSTODY_OPERATION_CLASS_STATUS:
        errors.append("unexpected_status")
    if fixture.get("operation_class") not in L6_WRITE_CUSTODY_OPERATION_CLASS_NAMES:
        errors.append("unexpected_operation_class")
    if not isinstance(fixture.get("custody_owner_role"), str) or not fixture.get("custody_owner_role"):
        errors.append("missing_custody_owner_role")
    max_operation_count = fixture.get("max_operation_count")
    if not isinstance(max_operation_count, int) or max_operation_count < 1:
        errors.append("invalid_max_operation_count")
    for ref_field in ("timeout_ref", "rollback_ref", "approval_ref"):
        if not isinstance(fixture.get(ref_field), str) or not fixture.get(ref_field):
            errors.append(f"missing_{ref_field}")
    runtime_route = fixture.get("runtime_route")
    if not isinstance(runtime_route, dict):
        errors.append("missing_runtime_route")
    elif any(runtime_route.get(key) for key in ("supported", "registered", "executable")):
        errors.append("runtime_route_not_held")
    if fixture.get("denied_before_mutation") is not True:
        errors.append("denied_before_mutation_not_true")
    if fixture.get("no_op_only") is not True:
        errors.append("no_op_only_not_true")
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
    for surface in L6_WRITE_CUSTODY_OPERATION_CLASS_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
