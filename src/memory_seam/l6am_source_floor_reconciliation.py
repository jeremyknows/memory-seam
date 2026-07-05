from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from memory_seam.l6al_service_auth_contract import zero_l6al03_guarded_counters
from memory_seam.l6am_next_use_proof_decision import L6AM03_STATUS
from memory_seam.l6am_supervised_metadata_retry_packet import (
    L6AM01_PARENT_ISSUE,
    L6AM01_RAIL_STARTING_SOURCE_FLOOR,
    L6AM01_REPOSITORY,
)
from memory_seam.l6am_supervised_metadata_retry_receipt import L6AM02_BLOCKER_CLASSIFICATION

L6AM04_SCHEMA_VERSION = "l6am04-source-floor-parent-tracker-reconciliation-v1"
L6AM04_RAIL_ISSUE = 360
L6AM04_STATUS = "RAIL_RECONCILED_AUTH_UNBLOCK_PACKET_READY_RETRY_HELD"
L6AM04_FINAL_SOURCE_FLOOR = "7a8bc869d9a9263854262a324d803c58cb325dd0"
L6AM04_ACTIVE_FINAL_POKE_ID = "16b4859012da"
L6AM04_ACTIVE_WRITER_ID = "ae4fa822720a"
L6AM04_OVERNIGHT_METRONOME_POKE_ID = "98fbff368dfb"
L6AM04_TRACKER_REF = "atlas/sax/data/memory-seam-8-step-roadmap-tracker"
L6AM04_TRACKER_UPDATE_STATE = "TRACKER_UPDATE_PACKET_PREPARED_EXTERNAL_WRITE_HELD_BY_CRON_BOUNDARY"
L6AM04_DISPATCH_POKE_STATE = "EXISTING_CONDITIONAL_FINAL_POKE_REFERENCED_NO_NEW_CRON_CREATED"

L6AM04_RAIL_EVIDENCE = (
    {
        "issue": 357,
        "pr": 366,
        "merge_commit": "d03ed73cc5b9d872946fa24e2f0ebc46ec549693",
        "status": "PASS_EXACT_SUPERVISED_METADATA_RETRY_PACKET_READY",
    },
    {
        "issue": 358,
        "pr": 367,
        "merge_commit": "8930ac7cb632a1b385beaca16572c674b2885096",
        "status": "PASS_SUPERVISED_METADATA_RETRY_SAFE_DENIAL_CAPTURED",
    },
    {
        "issue": 359,
        "pr": 368,
        "merge_commit": L6AM04_FINAL_SOURCE_FLOOR,
        "status": L6AM03_STATUS,
    },
)

L6AM04_VERIFICATION = (
    "python -m pytest -q tests/test_l6am04_source_floor_reconciliation.py",
    "python -m pytest -q",
    "python scripts/public_hygiene_scan.py",
    "git diff --check",
    "python -m compileall -q src tests examples",
)

L6AM04_RESIDUAL_HOLDS = (
    "no_live_read_retry",
    "no_secret_env_keychain_oauth_auth_file_reads",
    "no_raw_private_source_auth_provider_callback_payloads",
    "no_source_discovery_or_broad_recall_index_query",
    "no_runtime_registry_consumption",
    "no_service_activation",
    "no_provider_prod_canary_gate_movement",
    "no_write_mutation_persistence",
    "no_broad_allowed_true_behavior",
    "no_new_cron_created_inside_cron_run",
)


def build_l6am04_reconciliation_receipt() -> dict[str, Any]:
    return {
        "schema_version": L6AM04_SCHEMA_VERSION,
        "repo": L6AM01_REPOSITORY,
        "parent_issue": L6AM01_PARENT_ISSUE,
        "rail_issue": L6AM04_RAIL_ISSUE,
        "rail_starting_source_floor": L6AM01_RAIL_STARTING_SOURCE_FLOOR,
        "final_source_floor": L6AM04_FINAL_SOURCE_FLOOR,
        "status": L6AM04_STATUS,
        "rail_evidence": [dict(item) for item in L6AM04_RAIL_EVIDENCE],
        "retry_outcome": {
            "auth_status_code": 403,
            "degraded_reason": "wrong_route_audience",
            "item_count": 0,
            "blocker_classification": L6AM02_BLOCKER_CLASSIFICATION,
        },
        "next_frontier": "fresh operator/service auth binding for exact metadata recall before current-session or fresh-agent proof",
        "tracker_ref": L6AM04_TRACKER_REF,
        "tracker_update_state": L6AM04_TRACKER_UPDATE_STATE,
        "tracker_update_summary": (
            "Step 3 becomes AUTH UNBLOCK PACKET READY / RETRY HELD after L6AM #357-#360; "
            "Step 4 remains HELD until safe metadata returns; Step 5 repo-side auth contract remains ready but runtime binding is missing."
        ),
        "dispatch_poke_state": L6AM04_DISPATCH_POKE_STATE,
        "active_writer_id": L6AM04_ACTIVE_WRITER_ID,
        "active_final_poke_id": L6AM04_ACTIVE_FINAL_POKE_ID,
        "overnight_metronome_poke_id": L6AM04_OVERNIGHT_METRONOME_POKE_ID,
        "verification_commands": list(L6AM04_VERIFICATION),
        "residual_holds": list(L6AM04_RESIDUAL_HOLDS),
        "guarded_counters": zero_l6al03_guarded_counters(),
    }


def assert_l6am04_reconciliation_report_safe(receipt: Mapping[str, Any]) -> None:
    if receipt.get("status") != L6AM04_STATUS:
        raise AssertionError("L6AM.04 reconciliation status mismatch")
    if receipt.get("final_source_floor") != L6AM04_FINAL_SOURCE_FLOOR:
        raise AssertionError("final source floor must be pinned")
    retry_outcome = receipt.get("retry_outcome")
    if not isinstance(retry_outcome, Mapping):
        raise AssertionError("retry outcome must be report-safe metadata")
    if retry_outcome.get("auth_status_code") != 403 or retry_outcome.get("item_count") != 0:
        raise AssertionError("reconciliation must preserve the safe 403 empty retry outcome")
    if receipt.get("tracker_update_state") != L6AM04_TRACKER_UPDATE_STATE:
        raise AssertionError("tracker write must remain boundary-labeled")
    if receipt.get("dispatch_poke_state") != L6AM04_DISPATCH_POKE_STATE:
        raise AssertionError("cron run must reference existing poke without creating a new cron")
    counters = receipt.get("guarded_counters")
    if not isinstance(counters, Mapping) or any(value != 0 for value in counters.values()):
        raise AssertionError("reconciliation must keep guarded counters zero")
