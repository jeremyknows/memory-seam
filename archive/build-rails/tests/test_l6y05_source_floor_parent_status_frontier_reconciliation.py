from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6y05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#221 / PR #226 / source floor `b268ce0a064629c823a14d3f68563607a14019b4`",
    "#222 / PR #227 / source floor `f86eab3e16147b2aa2a2b77a7bf75608b6ddffde`",
    "#223 / PR #228 / source floor `1a5029c639b4a599739aa97873ad6a58e9dd0ad1`",
    "#224 / PR #229 / source floor `25d561f7a5088ac46323f2e68485205c7c76b30c`",
    "#225 / this packet / final source floor after merge",
)

RESIDUAL_HOLDS = (
    "live/private reads remain held",
    "raw private content remains held",
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


def test_l6y05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6y05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6y05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6Y.05 source-floor parent status and frontier reconciliation" in inventory
    assert "RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED" in inventory


def test_l6y05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED`",
        "Rail issue: #225",
        "Parent issue: #6",
        "Rail outcome: `HOLD_FOR_OPERATOR_EXACT_TARGET_REFS`",
        "Source floor entering slice: `25d561f7a5088ac46323f2e68485205c7c76b30c`",
        "Current reconciled source floor before this packet merge: `25d561f7a5088ac46323f2e68485205c7c76b30c` or later",
        "No live/private read executed in L6Y",
        "The L6Y rail ended in HOLD, not PASS and not FIX_BEFORE_NEXT_SOURCE",
    )
    for term in required_terms:
        assert term in text


def test_l6y05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#221 closed by binding packet" in text
    assert "#222 closed via approval-mismatch deny-before-read HOLD" in text
    assert "#223 closed via receipt hygiene verifier" in text
    assert "#224 closed via usefulness/redaction review" in text
    assert "#225 closes this reconciliation after merge and parent #6 receipt" in text


def test_l6y05_parent_status_and_live_outcome_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6Y completed its bounded issue-railed preauthorized one-read path as a no-live HOLD",
        "did not provide executable report-safe `descriptor:l6y/<report-safe-slug>` and `source-card:l6y/<report-safe-slug>` target refs",
        "Live/source outcome: no live/private read executed",
        "Verification status to report on #6 after this packet merges",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, activate services, change repository visibility, publish a package, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6y05_next_frontier_requires_fresh_issue_bound_approval():
    text = normalized(DOC)

    required_terms = (
        "Next exact frontier: `L6Z exact target-ref approval and one-read retry rail`",
        "Another issue-bound approval is required before any future live/private read attempt",
        "fresh owner comment on the exact execution issue",
        "bind max one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation",
        "expire within <=12h",
        "`descriptor:l6z/<report-safe-slug>` and `source-card:l6z/<report-safe-slug>`",
        "This packet does not create the L6Z issues, does not approve them, and does not authorize another read by inertia from #221-#225",
    )
    for term in required_terms:
        assert term in text


def test_l6y05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
