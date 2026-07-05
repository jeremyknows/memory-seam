from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ah05-source-floor-parent-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_DEFAULT_OFF_RUNTIME_INTEGRATION_IMPLEMENTED_HELD_ACTIVATION"
RAIL_STARTING_SOURCE_FLOOR = "df8e034cd0d53c675212b6f7aa594abd4bd272d3"
SOURCE_FLOOR_ENTERING_SLICE = "f75c4d38ed178e67bb3cdde9fbb5e2c825863dae"
PARENT_SUCCESSOR_COMMENT = "4654131206"
IMPLEMENTATION_APPROVAL_COMMENT = "4654131093"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"
NEXT_FRONTIER = "OWNER_DECISION_FOR_DEFAULT_OFF_RUNTIME_INTEGRATION_ACTIVATION_OR_CONTINUED_HOLD"

L6AH_ANCHORS = (
    "L6AH.01 (#311 / PR #316 / source floor `365dd286566ad3d1a1c34bd7752ad7fa4f41b483`)",
    "L6AH.02 (#312 / PR #317 / source floor `91538337422bffc46ca4a53540fcf728f669f8cf`)",
    "L6AH.03 (#313 / PR #318 / source floor `8399a037adf09a07a2074f055a03a8b595b8c577`)",
    "L6AH.04 (#314 / PR #319 / source floor `f75c4d38ed178e67bb3cdde9fbb5e2c825863dae`)",
    "L6AH.05 (#315 / this packet)",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "source-card reads remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "callbacks/provider routes, provider/backend/source-stat/source-read callbacks remain held",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement remain held",
    "additional adapter calls or runtime-use smokes beyond this rail's committed fixture-only integration proof remain held unless separately exact-approved",
    "broad `allowed=true` behavior remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ah05_reconciliation_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ah05-source-floor-parent-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ah05_source_floor_parent_frontier_reconciliation.py" in inventory
    assert "L6AH.05 source-floor parent status frontier reconciliation" in inventory
    assert STATUS in inventory


def test_l6ah05_records_status_source_floor_parent_and_outcome() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AH.05 source-floor anchor, parent status, and next frontier reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #315",
        "Parent issue: #6",
        "Blocked by: #311-#314 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AH successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Implementation approval consumed by L6AH.01: #311 comment `{IMPLEMENTATION_APPROVAL_COMMENT}`",
        f"Operation class implemented: `{OPERATION_CLASS}`",
        "Reconciliation vocabulary: `RAIL_PASS_RECONCILED`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        "Reconciliation: `RAIL_PASS_RECONCILED`",
        "Rail outcome: `DEFAULT_OFF_RUNTIME_INTEGRATION_IMPLEMENTED_WITH_ACTIVATION_HELD`",
        "Parent #6 remains `OPEN` while this packet is prepared",
        f"Next exact frontier: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ah05_lists_all_l6ah_prs_source_floors_and_scope() -> None:
    text = normalized(DOC)

    for anchor in L6AH_ANCHORS:
        assert anchor in text
    for term in (
        "exact default-off runtime-integration implementation slice",
        "post-implementation fixture-only integration receipt review",
        "no-live trust-boundary review for integration implementation rail",
        "integration use-proof packet and held-activation map",
        "source-floor anchor, parent status, residual holds, parent completion receipt template, and next-frontier reconciliation",
        "creates no successor issues, no successor cron jobs, no runtime activation, no additional runtime-use smoke, no additional adapter call, and no Atlas Gate movement",
    ):
        assert term in text


def test_l6ah05_confirms_public_metadata_only_and_no_held_surface_execution() -> None:
    text = normalized(DOC)

    required_terms = (
        "docs/tests/public-metadata-only reconciliation",
        "does not implement another runtime integration",
        "does not execute another runtime-use smoke or adapter call",
        "does not perform live/private reads",
        "does not read source cards",
        "does not fetch or publish raw approval prose",
        "does not read credentials/auth/env/keychain/OAuth/auth-file material",
        "does not discover sources",
        "does not scan workspaces or families",
        "does not run broad recall or index queries",
        "does not consume Runtime Registry data",
        "does not invoke callbacks or provider routes",
        "does not persist or mutate state",
        "does not write/delete/reindex/cache-purge",
        "does not execute rollback",
        "does not activate a service/listener/startup/global path",
        "does not create or modify cron automation",
        "does not publish or change visibility",
        "does not move provider/prod/canary/Gate or Atlas Gate state",
        "does not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ah05_completion_finding_and_consumed_approval_boundary() -> None:
    text = normalized(DOC)

    required_terms = (
        "Finding: `PASS_TO_PARENT_RECEIPT_WITH_DEFAULT_OFF_RUNTIME_INTEGRATION_IMPLEMENTED_AND_ACTIVATION_HELD`",
        "#311-#314 are closed/PASS and #315 can close after this packet merges and verification passes",
        "completed the exact default-off runtime-integration implementation rail",
        "implemented one narrow fixture-only/report-safe runtime-integration seam in #311",
        "The rail did not activate runtime use",
        "did not call adapters beyond the committed fixture-only integration function proof",
        "The #311 approval is fully consumed historical authority for one implementation slice only",
        "not reusable by #312, #313, #314, this #315 reconciliation, parent #6 status comments",
        "future activation, future live/private reads, source-card reads, additional adapter calls or runtime-use smokes",
        "Runtime Registry consumption, callbacks/provider routes, persistence/mutation, cron changes",
        "Atlas Gate movement, or broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ah05_names_next_frontier_without_creating_successor_rail() -> None:
    text = normalized(DOC)

    required_terms = (
        f"Next exact frontier: `{NEXT_FRONTIER}`",
        "separate exact owner-created issue rail",
        "freshly binds repository `jeremyknows/memory-seam`, issue number",
        "operation class, owner actor association, unexpired UTC approval window",
        "exact repo-relative files, exact fixture-only or explicitly approved live/source-card inputs",
        "max operation count, denial-before-callback behavior",
        "verification gates, rollback/stop conditions, and residual held surfaces",
        "L6AH.05 does not create that rail and does not approve activation",
        "continued HOLD: no service/global activation, no live/private read, no source-card read",
        "no Runtime Registry consumption, no callbacks/provider routes, no persistence/mutation",
        "no publication/provider/prod/canary/Gate movement, no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ah05_residual_holds_parent_receipt_template_and_hygiene() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    required_terms = (
        "Parent receipt template after merge",
        "L6AH completion receipt — bounded default-off runtime-integration implementation rail reconciled",
        "Rail: #311-#315 all closed",
        "Final PR: #TBD",
        "Final merge/source floor: #TBD",
        "Consumed implementation approval: #311 comment `4654131093`",
        "artifacts:",
        "`src/memory_seam/l6ag_default_off_runtime_integration.py`",
        "`docs/l6ah05-source-floor-parent-frontier-reconciliation.md`",
        "tests:",
        "`tests/test_l6ag_default_off_runtime_integration.py`",
        "`tests/test_l6ah05_source_floor_parent_frontier_reconciliation.py`",
        "targeted pytest, full `python -m pytest -q`, `python scripts/public_hygiene_scan.py`, `git diff --check`, `python -m compileall -q src tests examples`, and GitHub checks",
        f"Outcome: `{STATUS}`",
        f"Next exact frontier: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text

    unsafe_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
