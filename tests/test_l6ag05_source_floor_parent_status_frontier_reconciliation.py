from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ag05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_RUNTIME_INTEGRATION_CONTINUED_HOLD"
RAIL_STARTING_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
SOURCE_FLOOR_ENTERING_SLICE = "f6ebc6de6f1df2b5aa85d7073153104eca540656"
PARENT_SUCCESSOR_COMMENT = "4653805965"
INVENTORY_AUTH_COMMENT = "4653805822"
DESIGN_AUTH_COMMENT = "4653805892"
HISTORICAL_SMOKE_APPROVAL_COMMENT = "4653350823"
HISTORICAL_SMOKE_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"
NEXT_FRONTIER = "OWNER_DECISION_FOR_EXACT_DEFAULT_OFF_RUNTIME_INTEGRATION_ISSUE_OR_CONTINUED_HOLD"

L6AG_ANCHORS = (
    "L6AG.01 (#301 / PR #306 / source floor `49688202b1fdde0231f417ca3077b544e20781a6`)",
    "L6AG.02 (#302 / PR #307 / source floor `1ff55c0056248162b7726f966f7a5a31e9a8241f`)",
    "L6AG.03 (#303 / PR #308 / source floor `f8a91ccd7bdefab08d7bca5a5784e34609e1bc10`)",
    "L6AG.04 (#304 / PR #309 / source floor `f6ebc6de6f1df2b5aa85d7073153104eca540656`)",
    "L6AG.05 (#305 / this packet)",
)

RESIDUAL_HOLDS = (
    "runtime integration and adapter wiring remain held",
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval remains held",
    "live/private reads and any source-card reads remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "callbacks/provider routes, provider/backend/source-stat/source-read callbacks remain held",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement remain held",
    "broad `allowed=true` behavior remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ag05_reconciliation_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ag05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ag05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AG.05 source-floor parent status frontier reconciliation" in inventory
    assert STATUS in inventory


def test_l6ag05_records_status_source_floor_parent_and_outcome() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AG.05 source-floor anchor, parent status, and next frontier reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #305",
        "Parent issue: #6",
        "Blocked by: #301-#304 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AG successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound inventory authorization: #301 comment `{INVENTORY_AUTH_COMMENT}`",
        f"Issue-bound design authorization: #303 comment `{DESIGN_AUTH_COMMENT}`",
        f"Historical runtime-use smoke approval consumed by L6AF.02: #292 comment `{HISTORICAL_SMOKE_APPROVAL_COMMENT}`",
        f"Historical runtime-use smoke final reconciliation: #295 / PR #300 / source floor `{HISTORICAL_SMOKE_SOURCE_FLOOR}`",
        f"Future operation class named only by #302/#303: `{OPERATION_CLASS}`",
        "Reconciliation vocabulary: `RAIL_PASS_RECONCILED`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        "Reconciliation: `RAIL_PASS_RECONCILED`",
        "Rail outcome: `POST_SMOKE_RUNTIME_INTEGRATION_DECISION_COMPLETE_RUNTIME_INTEGRATION_CONTINUED_HOLD`",
        "Parent #6 remains `OPEN` while this packet is prepared",
    )
    for term in required_terms:
        assert term in text


def test_l6ag05_lists_all_l6ag_prs_source_floors_and_scope() -> None:
    text = normalized(DOC)

    for anchor in L6AG_ANCHORS:
        assert anchor in text

    required_terms = (
        "post-smoke integration evidence inventory and blocker map",
        "runtime-integration-or-continued-hold decision packet",
        "default-off integration candidate design and rollback plan",
        "no-live trust-boundary review for post-smoke integration rail",
        "source-floor anchor, parent status, residual holds, parent completion receipt template, and next-frontier reconciliation",
        "creates no successor issues, no successor cron jobs, no runtime activation, no additional smoke, and no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ag05_confirms_public_metadata_only_and_no_held_surface_execution() -> None:
    text = normalized(DOC)

    required_terms = (
        "docs/tests/public-metadata-only reconciliation",
        "does not implement runtime integration",
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


def test_l6ag05_completion_finding_and_runtime_integration_continued_hold() -> None:
    text = normalized(DOC)

    required_terms = (
        "Finding: `PASS_TO_PARENT_RECEIPT_WITH_RUNTIME_INTEGRATION_CONTINUED_HOLD`",
        "#301-#304 are closed/PASS and #305 can close after this packet merges and verification passes",
        "completed the post-smoke runtime-integration-or-continued-hold decision rail",
        "The rail did not execute runtime integration",
        "only runtime-use evidence remains the historical one approved local fixture-only adapter import/call consumed by L6AF.02",
        "The L6AG outcome is continued hold, not approval",
        "runtime integration, adapter wiring, additional smokes, additional adapter calls",
        "Runtime Registry consumption, callbacks/provider routes, persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
        "broad `allowed=true` behavior remain blocked unless a later exact owner-created issue rail separately authorizes a bounded operation",
    )
    for term in required_terms:
        assert term in text


def test_l6ag05_preserves_consumed_smoke_authority_and_report_safety() -> None:
    text = normalized(DOC)

    required_terms = (
        "Runtime-integration custody conclusion",
        "The #292 approval is fully consumed historical authority for one local fixture-only runtime-use smoke only",
        "not reusable by #293, #294, #295, #301, #302, #303, #304, this #305 reconciliation, parent #6 status comments",
        "future runtime integration, additional adapter calls, live/private reads",
        "Atlas Gate movement, or broad `allowed=true` behavior",
        f"`{OPERATION_CLASS}` remains a future exact issue-bound operation class candidate only",
        "The phrase is not approval, not an implementation, not activation, not a runtime route",
        "not a Runtime Registry consumer, not a callback path, not a persistence path, not a cron path, not a Gate movement, and not broad allow behavior",
        "Reportable evidence from L6AG is limited to repo-relative artifact paths",
        "public issue/PR numbers",
        "public source-floor commits",
        "public comment IDs",
        "verification command names, and residual hold labels",
        "It excludes raw private content, raw source text, raw approval prose, credentials",
        "Runtime Registry handles, provider handles, secret values, and token-like values",
    )
    for term in required_terms:
        assert term in text


def test_l6ag05_names_next_frontier_without_creating_successor_rail() -> None:
    text = normalized(DOC)

    required_terms = (
        f"Next exact frontier: `{NEXT_FRONTIER}`",
        "separate exact owner-created issue rail",
        "freshly binds repository `jeremyknows/memory-seam`, issue number",
        "operation class, owner actor association, unexpired UTC approval window",
        "exact repo-relative files, exact fixture-only or explicitly approved live/source-card inputs",
        "max operation count, denial-before-callback behavior",
        "verification gates, and residual held surfaces",
        "L6AG.05 does not create that rail and does not approve runtime integration",
        "continued HOLD: no runtime integration, no adapter wiring, no additional runtime-use smoke",
        "no Runtime Registry consumption, no callbacks/provider routes, no persistence/mutation",
        "no publication/provider/prod/canary/Gate movement, no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ag05_residual_holds_parent_receipt_template_and_hygiene() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    required_terms = (
        "Parent receipt template after merge",
        "L6AG rail: #301-#305 all closed",
        "final PR and merge source floor for #305",
        "artifacts: `docs/l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md`",
        "`docs/l6ag05-source-floor-parent-status-frontier-reconciliation.md`",
        "tests: `tests/test_l6ag01_post_smoke_integration_evidence_inventory_blocker_map.py`",
        "`tests/test_l6ag05_source_floor_parent_status_frontier_reconciliation.py`",
        "targeted pytest, full `python -m pytest -q`, `python scripts/public_hygiene_scan.py`, `git diff --check`, `python -m compileall -q src tests examples`, and GitHub checks",
        f"outcome: `{STATUS}`",
        f"next exact frontier: `{NEXT_FRONTIER}`",
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
