from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aa05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#241 / PR #246 / source floor `169bcaf040277441f5f4b2a2e90f3f894817046d`",
    "#242 / PR #247 / source floor `4a01bf9b2ff8feec9c56b038bab5c7dbf2991241`",
    "#243 / PR #248 / source floor `4df614bec8c0a1523f2be177eed512b9c769d424`",
    "#244 / PR #249 / source floor `9879ec2740583ff7d0c4139d00806f02592cdaa9`",
    "#245 / this packet / final source floor after merge",
)

RESIDUAL_HOLDS = (
    "additional live/private reads remain held",
    "raw private content remains held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "credential/auth/env/keychain/OAuth/auth-file reads remain held",
    "provider/backend/source-stat/source-read callbacks remain held except the consumed exactly-one #242 report-safe source-card read path",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "mutation, rollback, and cache-purge execution remain held",
    "any broad `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aa05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aa05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6aa05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AA.05 source-floor parent status and frontier reconciliation" in inventory
    assert "RAIL_PASS_RECONCILED_ONE_REPORT_SAFE_SOURCE_CARD_READ" in inventory


def test_l6aa05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_PASS_RECONCILED_ONE_REPORT_SAFE_SOURCE_CARD_READ`",
        "Rail issue: #245",
        "Parent issue: #6",
        "Rail outcome: `PASS_CONTINUE_REPORT_SAFE_SOURCE_CARD_EVIDENCE`",
        "Source floor entering slice: `9879ec2740583ff7d0c4139d00806f02592cdaa9`",
        "Current reconciled source floor before this packet merge: `9879ec2740583ff7d0c4139d00806f02592cdaa9` or later",
        "Exactly one supervised report-safe source-card read executed in #242",
        "No live/private read executed in #241, #243, #244, or #245",
    )
    for term in required_terms:
        assert term in text


def test_l6aa05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#241 closed by exact target-ref packet" in text
    assert "#242 closed via owner-approved one-read PASS" in text
    assert "#243 closed via value-proof receipt hygiene verifier" in text
    assert "#244 closed via usefulness/trust-boundary review" in text
    assert "#245 closes this reconciliation after merge and parent #6 receipt" in text


def test_l6aa05_parent_status_and_live_outcome_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6AA completed its bounded issue-railed exact owner-approved target-ref live-read value proof as PASS",
        "#242 found the fresh issue-bound OWNER approval comment present, fresh, max-one-operation, and matching those exact refs",
        "descriptor:l6aa/report-safe-operator-preference-card",
        "source-card:l6aa/report-safe-operator-preference-card",
        "Preauthorization proof anchors carried through the rail: #6 comment `4649391691`; #215 comment `4649391836`",
        "issuecomment-4650524341",
        "Live/source outcome: exactly one report-safe source-card read executed in #242",
        "raw private source content was omitted",
        "Verification status to report on #6 after this packet merges",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, activate services, change repository visibility, publish a package, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6aa05_next_frontier_requires_fresh_issue_bound_approval():
    text = normalized(DOC)

    required_terms = (
        "Next exact issue-railed frontier: `L6AB report-safe source-card value comparison and stale-approval hardening review`",
        "Another issue-bound approval is required before any future live/private read attempt",
        "review/design-first unless Jeremy explicitly creates and authorizes a bounded execution issue",
        "fresh owner comment on the exact execution issue",
        "binds max one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation",
        "expiring within <=12h",
        "naming exact executable descriptor/source-card refs",
        "This packet does not create L6AB issues, does not approve them, does not schedule automation, and does not authorize another read by inertia from #241-#245",
    )
    for term in required_terms:
        assert term in text


def test_l6aa05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
