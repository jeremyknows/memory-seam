"""Synthetic no-production smoke for the L6 write-intent preflight gate.

The smoke exercises exactly one committed synthetic ``write intent`` request and
prints report-safe denial output. It does not execute writes, custody transfer,
delete, reindex, rollback, cache purge, provider/backend/source callbacks,
source discovery, live reads, Runtime Registry access, services, credentials, or
configuration mutation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from memory_seam.write_intent_preflight_gate import (
    L6_WRITE_INTENT_GUARDED_COUNTERS,
    L6_WRITE_INTENT_OPERATION_CLASS,
    WriteIntentPreflightCallbackHarness,
    build_l6_write_intent_approval_context_fixture,
    run_write_intent_preflight_gate,
    validate_l6_write_intent_preflight_gate_result,
)

SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST: dict[str, Any] = {
    "operation_class": L6_WRITE_INTENT_OPERATION_CLASS,
    "synthetic_operation_count": 1,
    "production": False,
    "payload_included": False,
    "source_read_requested": False,
    "credential_read_requested": False,
}


def run_synthetic_write_intent_preflight_smoke() -> dict[str, Any]:
    """Run the local no-production write-intent preflight smoke.

    The function returns a compact public-safe summary. Guarded counters are
    copied from the synthetic harness after the gate denies; if any callback is
    accidentally invoked, the harness would increment and fail before this
    summary can satisfy tests.
    """

    harness = WriteIntentPreflightCallbackHarness.build()
    result = run_write_intent_preflight_gate(
        SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST["operation_class"],
        harness,
        build_l6_write_intent_approval_context_fixture(),
    )
    validation_errors = validate_l6_write_intent_preflight_gate_result(result)
    guarded_counters_zero = all(harness.counters[counter] == 0 for counter in L6_WRITE_INTENT_GUARDED_COUNTERS)
    metadata = result["denial_receipt_metadata"]
    return {
        "smoke": "l6_write_intent_preflight_no_production",
        "request": dict(SYNTHETIC_WRITE_INTENT_SMOKE_REQUEST),
        "allowed": result["allowed"],
        "denied_before_callback": result["denied_before_callback"],
        "callbacks_invoked": result["callbacks_invoked"],
        "denial_reason": result["denial_reason"],
        "operation_class": result["operation_class"],
        "operation_count": result["operation_count"],
        "guarded_counters_zero": guarded_counters_zero,
        "guarded_counters": dict(harness.counters),
        "receipt": {
            "schema_version": metadata["schema_version"],
            "emitted_for": metadata["emitted_for"],
            "operation_class": metadata["operation_class"],
            "denial_reason_code": metadata["denial_reason_code"],
            "counter_summary": dict(metadata["counter_summary"]),
        },
        "validation_errors": validation_errors,
        "report_safe": True,
        "production_executed": False,
    }


def main() -> None:
    print(json.dumps(run_synthetic_write_intent_preflight_smoke(), sort_keys=True))


if __name__ == "__main__":
    main()
