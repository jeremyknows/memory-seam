#!/usr/bin/env python3
"""Local synthetic/no-production smoke for the L6P positive receipt skeleton.

This example uses only the committed report-safe fixture fields from
``memory_seam.positive_authorization_receipt``. It emits a stdout-only summary;
it does not persist receipts, discover sources, read live/private data, consume
Runtime Registry, invoke provider/backend/source/write/custody/delete/reindex/
rollback/cache-purge callbacks, activate services, publish, change visibility,
claim prod/canary authority, or move Atlas Gate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_seam.positive_authorization_receipt import (  # noqa: E402
    L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS,
    build_l6_positive_authorization_approval_context_fixture,
    run_positive_authorization_receipt_skeleton,
    validate_l6_positive_authorization_receipt_result,
)


SMOKE_INPUT: dict[str, Any] = {
    "operation_class": L6_POSITIVE_AUTHORIZATION_RECEIPT_SLICE,
    "approval_context": build_l6_positive_authorization_approval_context_fixture(),
}


def build_report_safe_smoke_summary() -> dict[str, Any]:
    """Run one synthetic operation and return a report-safe smoke summary."""

    result = run_positive_authorization_receipt_skeleton(
        SMOKE_INPUT["operation_class"],
        approval_context=SMOKE_INPUT["approval_context"],
    )
    validation_errors = validate_l6_positive_authorization_receipt_result(result)
    counters = result["counters"]
    persistent_counts_zero = (
        counters["persistent_receipt_count"] == 0
        and counters["durable_write_record_count"] == 0
        and counters["audit_persistence_count"] == 0
        and counters["cache_mutation_count"] == 0
    )
    guarded_counters_zero = all(counters[counter] == 0 for counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS)

    return {
        "smoke": "l6_positive_authorization_no_production",
        "synthetic_no_production_only": result["synthetic_no_production_only"],
        "status": result["status"],
        "recognized_positive_authorization": result["recognized_positive_authorization"],
        "operation_count": result["operation_count"],
        "max_operation_count": result["max_operation_count"],
        "allowed": result["allowed"],
        "mutation_attempted": result["mutation_attempted"],
        "mutation_supported": result["mutation_supported"],
        "allowed_result_count": counters["allowed_result_count"],
        "persistent_counts_zero": persistent_counts_zero,
        "guarded_counters_zero": guarded_counters_zero,
        "callbacks_invoked": result["callbacks_invoked"],
        "fixture_is_persistent": result["fixture_is_persistent"],
        "receipt_metadata_status": result["positive_authorization_receipt_metadata"]["status"],
        "validation_errors": validation_errors,
    }


def main() -> int:
    summary = build_report_safe_smoke_summary()
    print(json.dumps(summary, sort_keys=True))
    expected = (
        summary["status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
        and summary["recognized_positive_authorization"] is True
        and summary["operation_count"] == 1
        and summary["max_operation_count"] == 1
        and summary["allowed"] is False
        and summary["mutation_attempted"] is False
        and summary["mutation_supported"] is False
        and summary["allowed_result_count"] == 0
        and summary["persistent_counts_zero"] is True
        and summary["guarded_counters_zero"] is True
        and summary["callbacks_invoked"] is False
        and summary["fixture_is_persistent"] is False
        and summary["receipt_metadata_status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
        and summary["validation_errors"] == []
    )
    return 0 if expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
