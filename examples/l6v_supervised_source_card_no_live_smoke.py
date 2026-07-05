#!/usr/bin/env python3
"""Local no-live smoke for the L6V supervised source-card proof preflight.

This example exercises exactly one recognized, issue-bound, committed synthetic
``SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`` preflight. It emits a compact
stdout-only JSON summary and does not read live/private sources, discover sources,
read credentials, consume Runtime Registry data, invoke callbacks, persist
receipts, mutate caches, activate services/listeners/startup/cron paths, publish,
change visibility, claim provider/prod/canary authority, move Atlas Gate, execute
mutations, or create an ``allowed=true`` route.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_seam.supervised_source_card_preflight import (  # noqa: E402
    L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS,
    L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS,
    build_l6v_supervised_source_card_approval_context_fixture,
    run_l6v_supervised_source_card_preflight,
    validate_l6v_supervised_source_card_preflight_result,
)


SMOKE_INPUT: dict[str, Any] = {
    "issue_ref": "#190",
    "operation_class": L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    "approval_context": build_l6v_supervised_source_card_approval_context_fixture(),
}


def build_report_safe_smoke_summary() -> dict[str, Any]:
    """Run one synthetic preflight and return a report-safe stdout summary."""

    result = run_l6v_supervised_source_card_preflight(
        SMOKE_INPUT["approval_context"],
        operation_class=SMOKE_INPUT["operation_class"],
    )
    validation_errors = validate_l6v_supervised_source_card_preflight_result(result)
    counters = result["counters"]
    guarded_counters_zero = all(counters[counter] == 0 for counter in L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS)

    return {
        "smoke": "l6v_supervised_source_card_no_live",
        "issue_ref": SMOKE_INPUT["issue_ref"],
        "preflight_issue_ref": result["issue_ref"],
        "source_floor": result["source_floor"],
        "upstream_packet": result["upstream_packet"],
        "operation_class": result["operation_class"],
        "status": result["status"],
        "status_detail": result["status_detail"],
        "recognized_operation": result["recognized_operation"],
        "preflight_ready": result["preflight_ready"],
        "operation_count": result["operation_count"],
        "max_operation_count": result["max_operation_count"],
        "descriptor_ref": result["descriptor_ref"],
        "source_card_ref": result["source_card_ref"],
        "metadata_only": result["receipt"]["metadata_only"],
        "non_persistent": result["receipt"]["non_persistent"],
        "allowed": result["allowed"],
        "allowed_result_count": result["allowed_result_count"],
        "allowed_true_route_present": result["allowed_true_route_present"],
        "callbacks_invoked": result["callbacks_invoked"],
        "live_adapter_invoked": result["live_adapter_invoked"],
        "mutation_attempted": result["mutation_attempted"],
        "persistence_attempted": result["persistence_attempted"],
        "guarded_counters_zero": guarded_counters_zero,
        "counters": {counter: counters[counter] for counter in L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS},
        "approval_denial_codes": tuple(result["approval_denial_codes"]),
        "validation_errors": validation_errors,
    }


def main() -> int:
    summary = build_report_safe_smoke_summary()
    print(json.dumps(summary, sort_keys=True))
    expected = (
        summary["status"] == L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS
        and summary["recognized_operation"] is True
        and summary["preflight_ready"] is True
        and summary["operation_count"] == 1
        and summary["max_operation_count"] == 1
        and summary["metadata_only"] is True
        and summary["non_persistent"] is True
        and summary["allowed"] is False
        and summary["allowed_result_count"] == 0
        and summary["allowed_true_route_present"] is False
        and summary["callbacks_invoked"] is False
        and summary["live_adapter_invoked"] is False
        and summary["mutation_attempted"] is False
        and summary["persistence_attempted"] is False
        and summary["guarded_counters_zero"] is True
        and summary["approval_denial_codes"] == ()
        and summary["validation_errors"] == []
    )
    return 0 if expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
