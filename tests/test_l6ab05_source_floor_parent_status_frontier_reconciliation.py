from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ab05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#251 / PR #256 / source floor `fefcec6b2da56666558adc1e0bd673e8d54a550d`",
    "#252 / PR #257 / source floor `b12b820977ed3a9629fd9b0bcdb534fd39a2ad6c`",
    "#253 / PR #258 / source floor `813e24c59b8a60671240513723ba3f646fb35ab2`",
    "#254 / PR #259 / source floor `075ae45a22054789767eb53e86553fb4209775ab`",
    "#255 / this packet / final source floor after merge",
)

RESIDUAL_HOLDS = (
    "additional live/private reads remain held",
    "raw private content remains held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "credential/auth/env/keychain/OAuth/auth-file reads remain held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "Runtime Registry consumption remains held",
    "persistence, audit/custody writes, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "mutation, rollback, and cache-purge execution remain held",
    "any broad `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ab05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ab05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ab05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AB.05 source-floor parent status and frontier reconciliation" in inventory
    assert "RAIL_PASS_RECONCILED_NO_LIVE_READS" in inventory


def test_l6ab05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_PASS_RECONCILED_NO_LIVE_READS`",
        "Rail issue: #255",
        "Parent issue: #6",
        "Rail outcome: `PASS_CONTINUE_NO_LIVE_VALUE_COMPARISON_HARDENED`",
        "Source floor entering L6AB: `91761ed55889f4c5432b55c445e396e727a6be93` or later",
        "Current reconciled source floor before this packet merge: `075ae45a22054789767eb53e86553fb4209775ab` or later",
        "No live/private read executed anywhere in #251, #252, #253, #254, or #255",
        "#242 one-read PASS remains consumed historical evidence only",
    )
    for term in required_terms:
        assert term in text


def test_l6ab05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#251 closed by value comparison matrix" in text
    assert "#252 closed by stale approval fixture hardening" in text
    assert "#253 closed by value evidence UX packet" in text
    assert "#254 closed by no-live trust-boundary review" in text
    assert "#255 closes this reconciliation after merge and parent #6 receipt" in text


def test_l6ab05_parent_status_and_no_live_outcome_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6AB completed its bounded issue-railed review/design/test/docs-only value-comparison and stale-approval hardening rail as PASS",
        "#251 compared absent approval, missing target refs, mismatched target refs, and the exact-owner-approved #242 PASS evidence without executing a read",
        "#252 expanded stale approval hardening fixtures",
        "#253 placed the report-safe value headline and limits first",
        "#254 confirmed no live/private read, no callback, no standing approval, no broad `allowed=true` path, and no Gate movement",
        "Preauthorization proof anchors carried through the rail: #6 comment `4649391691`; #215 comment `4649391836`",
        "issuecomment-4651032970",
        "Live/source outcome: no live/private read executed in L6AB",
        "raw private source content was not read or recorded",
        "Verification status to report on #6 after this packet merges",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, activate services, change repository visibility, publish a package, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6ab05_next_frontier_requires_new_issue_bound_approval():
    text = normalized(DOC)

    required_terms = (
        "Next exact issue-railed frontier: `L6AC fresh owner-approved report-safe source-card read decision rail`",
        "Another issue-bound approval is required before any future live/private read attempt",
        "not created or approved by this packet",
        "only if Jeremy creates explicit issue rails and approval for that bounded frontier",
        "fresh owner comment on the exact execution issue",
        "binds max one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation",
        "expires within <=12h",
        "names exact executable descriptor/source-card refs",
        "treats prior #242 PASS as consumed historical evidence only",
        "This packet does not create L6AC issues, does not approve them, does not schedule automation, and does not authorize another read by inertia from #251-#255 or #242",
    )
    for term in required_terms:
        assert term in text


def test_l6ab05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
