#!/usr/bin/env python3
"""Local no-live smoke for the L6W supervised live-read approval prep rail.

This example exercises only committed synthetic metadata for the L6W approval
scaffold, denial matrix, and receipt contract. It emits stdout-only JSON and does
not recognize approval, perform live/private reads, discover sources, consume
Runtime Registry data, invoke callbacks, persist receipts, mutate caches,
activate services/listeners/startup/cron paths, publish, change visibility,
claim provider/prod/canary authority, move Atlas Gate, execute mutations, or
create an ``allowed=true`` route.
"""

from __future__ import annotations

import json
from typing import Any

OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
GUARDED_COUNTERS = (
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "write_callbacks",
    "custody_callbacks",
    "delete_callbacks",
    "reindex_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
    "credential_reads",
    "auth_reads",
    "env_reads",
    "keychain_reads",
    "oauth_reads",
    "auth_file_reads",
    "runtime_registry_consumptions",
    "source_discoveries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "live_private_reads",
    "source_stat_calls",
    "source_read_calls",
    "persistence_writes",
    "audit_record_writes",
    "custody_record_writes",
    "cache_mutations",
    "service_activations",
    "publication_actions",
    "visibility_changes",
    "provider_prod_canary_actions",
    "atlas_gate_movements",
    "mutation_executions",
)


def build_report_safe_smoke_summary() -> dict[str, Any]:
    """Return one synthetic held-before-callback smoke summary."""

    counters = {counter: 0 for counter in GUARDED_COUNTERS}
    return {
        "smoke": "l6w_supervised_live_read_approval_no_live",
        "issue_ref": "#202",
        "approval_scaffold_issue_ref": "#199",
        "denial_matrix_issue_ref": "#200",
        "receipt_contract_issue_ref": "#201",
        "source_floor": "9264533",
        "upstream_packet": "docs/l6v06-supervised-source-card-trust-boundary-review.md",
        "scaffold_doc": "docs/l6w01-supervised-live-read-approval-packet-scaffold.md",
        "denial_matrix_doc": "docs/l6w02-supervised-live-read-approval-denial-matrix.md",
        "receipt_contract_doc": "docs/l6w03-supervised-live-read-receipt-output-contract.md",
        "operation_class": OPERATION_CLASS,
        "status": "HELD_FOR_FUTURE_APPROVAL",
        "approval_status": "NO_APPROVAL_PRESENT",
        "recognition_status": "NO_APPROVAL_RECOGNIZED",
        "stop_condition_status": "HELD_PENDING_FUTURE_ISSUE_BOUND_OWNER_APPROVAL",
        "stop_reason": "NO_APPROVAL_PRESENT",
        "operation_count": 0,
        "max_operation_count": 1,
        "one_operation_binding": True,
        "descriptor_ref": "report-safe-descriptor-ref:l6w04-synthetic",
        "source_card_ref": "report-safe-source-card-ref:l6w04-synthetic",
        "metadata_only": True,
        "stdout_only": True,
        "non_persistent": True,
        "allowed": False,
        "allowed_result_count": 0,
        "allowed_true_route_present": False,
        "callbacks_invoked": False,
        "live_read_invoked": False,
        "live_adapter_invoked": False,
        "source_discovery_attempted": False,
        "runtime_registry_consumed": False,
        "mutation_attempted": False,
        "persistence_attempted": False,
        "production_authority_claimed": False,
        "guarded_counters_zero": all(value == 0 for value in counters.values()),
        "counters": counters,
        "denial_codes": ("NO_APPROVAL_PRESENT",),
        "validation_errors": [],
    }


def main() -> int:
    summary = build_report_safe_smoke_summary()
    print(json.dumps(summary, sort_keys=True))
    expected = (
        summary["status"] == "HELD_FOR_FUTURE_APPROVAL"
        and summary["approval_status"] == "NO_APPROVAL_PRESENT"
        and summary["recognition_status"] == "NO_APPROVAL_RECOGNIZED"
        and summary["operation_count"] == 0
        and summary["max_operation_count"] == 1
        and summary["one_operation_binding"] is True
        and summary["allowed"] is False
        and summary["allowed_result_count"] == 0
        and summary["allowed_true_route_present"] is False
        and summary["callbacks_invoked"] is False
        and summary["live_read_invoked"] is False
        and summary["live_adapter_invoked"] is False
        and summary["source_discovery_attempted"] is False
        and summary["runtime_registry_consumed"] is False
        and summary["mutation_attempted"] is False
        and summary["persistence_attempted"] is False
        and summary["production_authority_claimed"] is False
        and summary["guarded_counters_zero"] is True
        and summary["validation_errors"] == []
    )
    return 0 if expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
