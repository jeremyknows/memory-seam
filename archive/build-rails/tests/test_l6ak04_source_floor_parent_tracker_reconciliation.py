from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ak04-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_REAL_READ_AUTH_BLOCKER_RETRY_HELD"
NEXT_FRONTIER = "STEP_3_RETRY_HELD_STEP_5_SERVICE_PROVIDER_AUTH_FRONTIER"
RAIL_STARTING_SOURCE_FLOOR = "95e7a7979ae092703da8f77c4d897f703348a308"
SOURCE_FLOOR_ENTERING_SLICE = "ab76964"
OPERATION_CLASS = "L6AK_REAL_READ_AUTH_BLOCKER_SOURCE_FLOOR_RECONCILIATION"
EVIDENCE_CLASS = "SUPERVISED_REAL_READ_AUTH_BLOCKER_PARENT_TRACKER_RECONCILIATION"

RAIL_ROWS = (
    "#341 | #345 | `407a80a` | `PASS_SAFE_403_RECEIPT_AUTH_BLOCKER_CAPTURED_NO_ITEMS_RETURNED`",
    "#342 | #346 | `5346907` | `PASS_ROUTE_AUDIENCE_AUTH_BINDING_DESIGNED_RETRY_STILL_HELD`",
    "#343 | #347 | `ab76964` | `PASS_NON_SECRET_AUTH_CONTRACT_SHIM_READY_RETRY_STILL_HELD`",
    "#344 | packet PR | pending merge handoff | `RAIL_PASS_RECONCILED_REAL_READ_AUTH_BLOCKER_RETRY_HELD`",
)

OUTCOME_TERMS = (
    "#341 recorded the already-performed bounded current-session Memory Seam MCP attempts",
    "recall returned `auth_status_code=403`, `degraded=true`, `items=[]`, and `wrong_route_audience`",
    "context health returned `auth_status_code=403`, `items=[]`, and `unauthorized_narrowing`",
    "#342 defined the non-secret identity, acting-for, agent, audience, scope, output-mode, freshness, and operation-count semantics",
    "#343 implemented a pure data-only route-audience/auth contract shim with typed metadata receipts",
    "Exact bindings can return `ready_for_exact_retry=true` only as readiness metadata while `read_authorized=false`, `retry_executed=false`",
    "No raw/private/source item content was returned by the real attempt",
    "No L6AK issue executed a retry after the safe 403 receipt",
)

TRACKER_TERMS = (
    "`current_floor_checked` should become the final #344 merged source floor",
    "Roadmap step 3 should become AUTH BLOCKER RECONCILED / RETRY HELD with L6AK #341-#344 closed, PRs #345-#348 merged",
    "parent #6 L6AK completion receipt comment ID",
    "The step 3 proof remains incomplete for raw value/usefulness because the real read returned safe 403 metadata only and no items",
    "exact supervised metadata read retry only if route-audience/service auth binding is actually ready and separately issue-bound",
    "otherwise keep Step 3 execution held and advance Step 5 service/provider auth",
    "Roadmap step 4 should remain HELD until a separately issue-bound fresh-agent proof exists",
    "Roadmap steps 5-8 should remain HELD unless separately issue-bound and approved",
)

RESIDUAL_HOLDS = (
    "any live read retry unless exact route-audience/service auth is ready and separately issue-bound",
    "any broader read, source discovery, broad recall, workspace/family scan, or index query",
    "any raw private content, raw source text, source-card body, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, auth-file material, source URI, platform raw ID, Runtime Registry payload, callback payload, provider payload, private correlation ref, or token-like value",
    "any persistence, custody, mutation, write, delete, reindex, cache purge, rollback execution, or runtime cache mutation",
    "any service/listener/startup/global activation or cron change",
    "any publication, visibility, provider/prod/canary/Gate movement, Atlas Gate movement, or broad `allowed=true` behavior",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ak04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ak04-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6ak04_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AK.04 source-floor parent tracker reconciliation" in inventory
    assert STATUS in inventory


def test_l6ak04_records_status_floor_scope_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AK.04 source-floor parent tracker reconciliation for real-read auth blocker",
        f"Status: `{STATUS}`",
        "Rail issue: #344",
        "Parent issue: #6",
        "Depends on: #341-#343 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read, auth blocker handoff toward step 5 service/provider auth",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Tracker reconciliation target: Atlas roadmap tracker for Memory Seam 8-step roadmap",
        f"Operation reconciled: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        "Verdict vocabulary: `RAIL_PASS_RECONCILED_REAL_READ_AUTH_BLOCKER_RETRY_HELD`, `FIX_AUTH_BLOCKER_RECONCILIATION_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_SERVICE_PROVIDER_AUTH_OR_EXACT_RETRY_AUTHORITY`.",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "performs no live read retry",
    ):
        assert term in text


def test_l6ak04_rail_anchors_and_auth_blocker_outcome() -> None:
    text = normalized(DOC)

    assert "Rail anchors" in text
    for row in RAIL_ROWS:
        assert row in text
    assert "Auth-blocker outcome" in text
    for term in OUTCOME_TERMS:
        assert term in text


def test_l6ak04_parent_and_tracker_reconciliation_requirements() -> None:
    text = normalized(DOC)

    for term in (
        "After #344 merges and closes, parent #6 should receive an L6AK completion receipt naming",
        "final #344 PR and source floor",
        "L6AK issue/PR anchors #341-#344 and #345-#348",
        "local verification commands and GitHub checks",
        "safe-403 outcome with `items=[]`, `wrong_route_audience`, and `unauthorized_narrowing`",
        "non-secret contract shim outcome with retry readiness metadata only, not read authorization",
        "tracker update confirming roadmap step 3 is AUTH BLOCKER RECONCILED / RETRY HELD",
        f"next frontier: `{NEXT_FRONTIER}`",
        "Atlas roadmap tracker file `2026-06-08-memory-seam-8-step-roadmap-tracker.md`",
    ):
        assert term in text
    for term in TRACKER_TERMS:
        assert term in text


def test_l6ak04_residual_holds_and_boundaries() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    for term in (
        "no broader recall",
        "no index query",
        "no source discovery",
        "no raw/private/source/auth/credential read",
        "no Runtime Registry consumption",
        "no callback/provider route invocation",
        "no persistence/mutation/write/delete/reindex/cache-purge/rollback",
        "no activation",
        "no cron change",
        "no publication/visibility change",
        "no provider/prod/canary/Gate movement",
        "no Atlas Gate movement",
        "no broad `allowed=true` behavior",
    ):
        assert term in text

    lowered = text.lower()
    for marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref value",
        "source://",
        "platform-raw-id value",
    ):
        assert marker not in lowered


def test_l6ak04_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6ak04_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
