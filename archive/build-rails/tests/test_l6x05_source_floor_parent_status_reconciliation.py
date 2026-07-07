from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6x05-source-floor-parent-status-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#211 / PR #216 / source floor `3f1066897cd11c5b312eff9351e16b7ffbb17082`",
    "#212 / PR #217 / source floor `1348a4b55fc52ca065a54ad8b3d57e0ccc333a9d`",
    "#213 / PR #218 / source floor `3313620ba2ea7f9aff778e8cab9bc64cf764554d`",
    "#214 / PR #219 / source floor `b85924f7a925440e6283c0ebe71299c5b52db01e`",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "credential/auth/env/keychain/OAuth/auth-file reads remain held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "mutation, rollback, and cache-purge execution remain held",
    "any `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6x05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6x05-source-floor-parent-status-reconciliation.md" in docs_index
    assert "tests/test_l6x05_source_floor_parent_status_reconciliation.py" in inventory
    assert "L6X.05 source-floor anchor and parent status reconciliation" in inventory
    assert "RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED" in inventory


def test_l6x05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED`",
        "Rail issue: #215",
        "Parent issue: #6",
        "Rail outcome: `HOLD_FOR_ANCHOR_RECONCILE`",
        "Current reconciled source floor: `b85924f7a925440e6283c0ebe71299c5b52db01e` or later",
        "No live/private read executed in L6X",
        "The rail ended in HOLD, not PASS and not FIX_BEFORE_NEXT_SOURCE",
    )
    for term in required_terms:
        assert term in text


def test_l6x05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#211 closed" in text
    assert "#212 closed via absent-approval HOLD" in text
    assert "#213 closed via receipt verifier" in text
    assert "#214 closed via frontier review" in text


def test_l6x05_parent_status_and_next_blocker_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6X completed its bounded one-read approval/attempt rail as a no-live HOLD because exact owner approval was absent on #212",
        "Next blocker: any future supervised report-safe source-card live read requires a fresh exact owner approval comment and a new bounded issue rail",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6x05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
