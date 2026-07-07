"""Synthetic denial-before-mutation harness for L6S.04 tests.

This helper is test infrastructure only. It never calls provider, backend,
source-stat, source-read, write, custody, reindex, rollback, cache-purge,
audit-persistence, activation, Runtime Registry, credential, or live/private
source surfaces. It records a denied preflight result and proves every guarded
callback counter stays at zero.
"""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

L6_DENIAL_BEFORE_MUTATION_STATUS = "denied_before_mutation_harness_non_executing"
L6_DENIAL_BEFORE_MUTATION_AUTHORITY = "held_until_exact_jeremy_approval"
L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION = "l6-denial-before-mutation-harness-v1"
L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES = (
    "write_intent",
    "custody_receipt_persistence",
    "delete",
    "reindex",
    "rollback",
    "cache_purge",
)
L6_DENIAL_BEFORE_MUTATION_CALLBACKS = (
    "provider_callback",
    "backend_callback",
    "source_stat_callback",
    "source_read_callback",
    "write_callback",
    "custody_callback",
    "delete_callback",
    "reindex_callback",
    "rollback_callback",
    "cache_purge_callback",
    "audit_persistence_callback",
    "runtime_registry_callback",
    "activation_callback",
)
L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES = (
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
L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY = {
    "raw_private_text": False,
    "credentials_or_auth_material": False,
    "private_paths": False,
    "raw_platform_ids": False,
    "raw_query_payloads": False,
    "raw_payload_content": False,
    "private_correlation_refs": False,
}


@dataclass(frozen=True)
class SyntheticCallbackHarness:
    """Callback bundle whose callbacks would fail if denial order regressed."""

    callbacks: dict[str, Callable[[], None]]
    counters: dict[str, int]

    @classmethod
    def build(cls) -> "SyntheticCallbackHarness":
        counters = {name: 0 for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}

        def make_callback(name: str) -> Callable[[], None]:
            def callback() -> None:
                counters[name] += 1
                raise AssertionError(f"unexpected_callback_invoked:{name}")

            return callback

        callbacks = {name: make_callback(name) for name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS}
        return cls(callbacks=callbacks, counters=counters)


L6_DENIAL_BEFORE_MUTATION_FIXTURE: dict[str, Any] = {
    "schema_version": L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION,
    "status": L6_DENIAL_BEFORE_MUTATION_STATUS,
    "authority": L6_DENIAL_BEFORE_MUTATION_AUTHORITY,
    "operation_classes": L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES,
    "guarded_callbacks": L6_DENIAL_BEFORE_MUTATION_CALLBACKS,
    "preflight_result": "denied_before_mutation",
    "mutation_possible": False,
    "callback_invocation_allowed": False,
    "synthetic_only": True,
    "runtime_route": {
        "supported": False,
        "registered": False,
        "executable": False,
        "authority": L6_DENIAL_BEFORE_MUTATION_AUTHORITY,
    },
    "held_surfaces": L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES,
    "report_safety": L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY,
}


def build_l6_denial_before_mutation_fixture() -> dict[str, Any]:
    """Return a copied synthetic fixture with no execution authority."""

    return deepcopy(L6_DENIAL_BEFORE_MUTATION_FIXTURE)


def run_denied_before_mutation_preflight(
    operation_class: str,
    harness: SyntheticCallbackHarness | None = None,
) -> dict[str, Any]:
    """Return a denied result without invoking any guarded callback.

    The function intentionally performs only input classification and counter
    copying. It does not call entries from ``harness.callbacks`` on either known
    or unknown operation classes.
    """

    harness = harness or SyntheticCallbackHarness.build()
    known_operation = operation_class in L6_DENIAL_BEFORE_MUTATION_OPERATION_CLASSES
    denial_reason = "held_surface_preflight_denied" if known_operation else "unknown_operation_class_denied"
    return {
        "schema_version": L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION,
        "status": L6_DENIAL_BEFORE_MUTATION_STATUS,
        "operation_class": operation_class if known_operation else "unknown_operation_class",
        "allowed": False,
        "denied_before_mutation": True,
        "denial_reason": denial_reason,
        "callbacks_invoked": False,
        "counters": deepcopy(harness.counters),
        "held_surfaces": L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES,
        "report_safety": deepcopy(L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY),
    }


def validate_l6_denial_before_mutation_result(result: dict[str, Any]) -> list[str]:
    """Return report-safe error codes for denied-before-mutation proof output."""

    errors: list[str] = []
    if result.get("schema_version") != L6_DENIAL_BEFORE_MUTATION_SCHEMA_VERSION:
        errors.append("unexpected_schema_version")
    if result.get("status") != L6_DENIAL_BEFORE_MUTATION_STATUS:
        errors.append("unexpected_status")
    if result.get("allowed") is not False:
        errors.append("allowed_not_false")
    if result.get("denied_before_mutation") is not True:
        errors.append("denied_before_mutation_not_true")
    if result.get("callbacks_invoked") is not False:
        errors.append("callbacks_invoked_not_false")
    counters = result.get("counters")
    if not isinstance(counters, dict):
        errors.append("missing_counters")
    else:
        for callback_name in L6_DENIAL_BEFORE_MUTATION_CALLBACKS:
            if counters.get(callback_name) != 0:
                errors.append(f"nonzero_counter_{callback_name}")
    report_safety = result.get("report_safety")
    if report_safety != L6_DENIAL_BEFORE_MUTATION_REPORT_SAFETY:
        errors.append("unsafe_report_safety_flag")
    held_surfaces = tuple(result.get("held_surfaces", ()))
    for surface in L6_DENIAL_BEFORE_MUTATION_HELD_SURFACES:
        if surface not in held_surfaces:
            errors.append(f"missing_held_surface_{surface}")
    return errors
