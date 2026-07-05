from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6z05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#231 / PR #236 / source floor `07ef81810809a0249fef2fd58be99cc57bce1746`",
    "#232 / PR #237 / source floor `a71f9f78afd5e0d254719acaf70cad8219ad23e6`",
    "#233 / PR #238 / source floor `4a7b390fd1a82efd561fdebebd16c651e12117b4`",
    "#234 / PR #239 / source floor `3ae34ad66e6281be17307b203923d9ed2b9f43ea`",
    "#235 / this packet / final source floor after merge",
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


def test_l6z05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6z05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6z05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6Z.05 source-floor parent status and frontier reconciliation" in inventory
    assert "RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED" in inventory


def test_l6z05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_HOLD_RECONCILED_NO_LIVE_EXECUTED`",
        "Rail issue: #235",
        "Parent issue: #6",
        "Rail outcome: `HOLD_FOR_OPERATOR_EXACT_TARGET_REF_MATCH`",
        "Source floor entering slice: `3ae34ad66e6281be17307b203923d9ed2b9f43ea`",
        "Current reconciled source floor before this packet merge: `3ae34ad66e6281be17307b203923d9ed2b9f43ea` or later",
        "No live/private read executed in L6Z",
        "The L6Z rail ended in HOLD, not PASS and not FIX_BEFORE_NEXT_SOURCE",
    )
    for term in required_terms:
        assert term in text


def test_l6z05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#231 closed by exact target-ref approval packet" in text
    assert "#232 closed via target-ref mismatch deny-before-read HOLD" in text
    assert "#233 closed via receipt/redaction verifier" in text
    assert "#234 closed via usefulness/trust-boundary review" in text
    assert "#235 closes this reconciliation after merge and parent #6 receipt" in text


def test_l6z05_parent_status_and_live_outcome_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6Z completed its bounded issue-railed exact target-ref one-read retry path as a no-live HOLD",
        "named `descriptor:l6z/operator-proof` and `source-card:l6z/operator-proof`",
        "did not match the #231 executable report-safe refs `descriptor:l6z/report-safe-operator-preference-card` and `source-card:l6z/report-safe-operator-preference-card`",
        "Live/source outcome: no live/private read executed",
        "Verification status to report on #6 after this packet merges",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, activate services, change repository visibility, publish a package, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6z05_next_frontier_requires_fresh_issue_bound_approval():
    text = normalized(DOC)

    required_terms = (
        "Next exact frontier: `L6AA exact owner-approved target-ref live-read value proof rail`",
        "Another issue-bound approval is required before any future live/private read attempt",
        "fresh owner comment on the exact execution issue",
        "bind max one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation",
        "expire within <=12h",
        "`descriptor:l6aa/<report-safe-slug>` and `source-card:l6aa/<report-safe-slug>`",
        "explicitly rebind the carried-forward L6Z refs `descriptor:l6z/report-safe-operator-preference-card` and `source-card:l6z/report-safe-operator-preference-card`",
        "This packet does not create L6AA issues, does not approve them, and does not authorize another read by inertia from #231-#235",
    )
    for term in required_terms:
        assert term in text


def test_l6z05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
