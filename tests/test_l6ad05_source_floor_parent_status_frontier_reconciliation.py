from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ad05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_OWNER_DECISION_HOLD"
RAIL_STARTING_SOURCE_FLOOR = "f606ed18737d057f0b544503c2532935a9d6c258"
SOURCE_FLOOR_ENTERING_SLICE = "dd76ab99c9d3dedef405d0bc1742738d2c3e242a"
PARENT_SUCCESSOR_COMMENT = "4651958877"
NEXT_FRONTIER = "OWNER_DECISION_FOR_EXACT_DEFAULT_OFF_IMPLEMENTATION_ISSUE_OR_CONTINUED_HOLD"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"

L6AD_ANCHORS = (
    "L6AD.01 (#271 / PR #276 / source floor `5d42de21671bb885433bc23d6f5aac9e2be094dc`)",
    "L6AD.02 (#272 / PR #277 / source floor `5157d40a5903ba54129b61ad5c8417df467300c8`)",
    "L6AD.03 (#273 / PR #278 / source floor `6c4c1b8bb27c09d099c62dc84139b03a4f6f4abd`)",
    "L6AD.04 (#274 / PR #279 / source floor `dd76ab99c9d3dedef405d0bc1742738d2c3e242a`)",
    "L6AD.05 (#275 / this packet)",
)

RESIDUAL_HOLDS = (
    "implementation/runtime execution remains held until a separate exact owner-created future implementation issue approval exists",
    "live/private reads and any additional source-card read beyond the consumed historical #262 evidence remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement remain held",
    "broad `allowed=true` behavior remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ad05_reconciliation_doc_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ad05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ad05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AD.05 source-floor parent status frontier reconciliation" in inventory
    assert STATUS in inventory


def test_l6ad05_records_status_source_floor_parent_and_outcome():
    text = normalized(DOC)

    required_terms = (
        "# L6AD.05 source-floor anchor, parent status, and next frontier reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #275",
        "Parent issue: #6",
        "Blocked by: #271-#274 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Reconciliation vocabulary: `RAIL_PASS_RECONCILED`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        "Reconciliation: `RAIL_PASS_RECONCILED`",
        "Rail outcome: `OWNER_DECISION_HOLD_FOR_IMPLEMENTATION_AUTHORITY`",
        "Parent #6 remains `OPEN` while this packet is prepared",
    )
    for term in required_terms:
        assert term in text


def test_l6ad05_lists_all_l6ad_prs_source_floors_and_scope():
    text = normalized(DOC)

    for anchor in L6AD_ANCHORS:
        assert anchor in text

    required_terms = (
        "post-L6AC evidence inventory and implementation blocker map",
        "implementation-or-hold decision packet",
        "default-off implementation unhold candidate design and rollback plan",
        "no-live trust-boundary review",
        "source-floor anchor, parent status, residual holds, and next-frontier reconciliation",
        "creates no successor issues, no successor cron jobs, no runtime activation, and no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ad05_confirms_completion_without_implementation_or_new_read():
    text = normalized(DOC)

    required_terms = (
        "Finding: `PASS_TO_PARENT_RECEIPT_WITH_OWNER_DECISION_HOLD`",
        "#271-#274 are closed/PASS and #275 can close after this packet merges and verification passes",
        "L6AD completed as a docs/tests-only implementation-or-hold rail",
        "did not implement the candidate adapter",
        "did not create `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py`",
        "did not export a runtime symbol",
        "did not execute held surfaces",
        "did not authorize a broad allowed path",
        "does not approve implementation, runtime execution, another source-card read",
    )
    for term in required_terms:
        assert term in text


def test_l6ad05_names_next_frontier_as_owner_decision_hold():
    text = normalized(DOC)

    required_terms = (
        f"Next exact frontier: `{NEXT_FRONTIER}`",
        "separate exact owner-created implementation issue",
        "freshly binds repository `jeremyknows/memory-seam`, issue number",
        f"operation class `{OPERATION_CLASS}`",
        "unexpired UTC approval window",
        "max one implementation slice",
        "exact repo-relative files, fixture-only inputs, report-safe outputs",
        "L6AD.05 does not create that issue and does not approve it",
        "continued HOLD: no implementation/runtime execution, no additional read",
        "no Runtime Registry consumption, no callbacks, no persistence/mutation",
        "no publication/provider/prod/canary/Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ad05_preserves_consumed_262_boundary_and_residual_holds():
    text = normalized(DOC)

    required_terms = (
        "The #262 one-read approval remains consumed historical evidence only",
        "approved exactly one L6AC `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        "`descriptor:l6ac/report-safe-operator-preference-card` and `source-card:l6ac/report-safe-operator-preference-card`",
        "that one read completed before L6AD began",
        "not reusable by this #275 reconciliation",
        "source-floor advancement, copied approval templates, exact future approval wording in #273, or any future implementation issue",
    )
    for term in required_terms:
        assert term in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text


def test_l6ad05_parent_receipt_template_and_report_hygiene():
    text = normalized(DOC)

    required_terms = (
        "Parent receipt template after merge",
        "L6AD rail: #271-#275 all closed",
        "final PR and merge source floor for #275",
        "artifact: `docs/l6ad05-source-floor-parent-status-frontier-reconciliation.md`",
        "test: `tests/test_l6ad05_source_floor_parent_status_frontier_reconciliation.py`",
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
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
