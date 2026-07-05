from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ac05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

MERGED_ARTIFACTS = (
    "#261 / PR #266 / source floor `ca81a18fbba9603f5f35a8fa57410963e028c904`",
    "#262 / PR #267 / source floor `e954c2e37e7c643dbde71e3f8d371c4aee04011c`",
    "#263 / PR #268 / source floor `734fe3a05158d8412b5d27d8c2998b6afcd4678c`",
    "#264 / PR #269 / source floor `6f627ac73d26fceb60be5eb61de47ee7ad7043ed`",
    "#265 / this packet / final source floor after merge",
)

RESIDUAL_HOLDS = (
    "additional live/private reads remain held beyond the consumed single #262 PASS receipt",
    "raw private content, raw source text, and raw approval prose remain held",
    "credentials/auth/env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "callbacks and provider/backend/source-stat/source-read routes remain held outside the consumed #262 receipt",
    "persistence, audit/custody writes, mutation, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/cron activation and global runtime config mutation remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "implementation unhold remains held pending a separate owner-created issue rail",
    "a second read remains held",
    "any broad `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ac05_reconciliation_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ac05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ac05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AC.05 source-floor parent status and frontier reconciliation" in inventory
    assert "RAIL_PASS_RECONCILED_ONE_REPORT_SAFE_READ" in inventory


def test_l6ac05_records_rail_outcome_and_current_floor():
    text = normalized(DOC)

    required_terms = (
        "Status: `RAIL_PASS_RECONCILED_ONE_REPORT_SAFE_READ`",
        "Rail issue: #265",
        "Parent issue: #6",
        "Rail outcome: `PASS_FRESH_OWNER_APPROVED_ONE_REPORT_SAFE_SOURCE_CARD_READ_RECONCILED`",
        "Source floor entering L6AC: `67a1a78db2b7adca0048497cce61412de13032f1` or later",
        "Current reconciled source floor before this packet merge: `6f627ac73d26fceb60be5eb61de47ee7ad7043ed` or later",
        "No live/private read executed in #261, #263, #264, or #265",
        "#262 executed exactly one approved read and no second read",
        "#262 approval is consumed and is not reusable",
    )
    for term in required_terms:
        assert term in text


def test_l6ac05_lists_merged_artifacts_and_issue_closure_chain():
    text = normalized(DOC)

    for artifact in MERGED_ARTIFACTS:
        assert artifact in text
    assert "#261 closed by fresh owner-approved packet" in text
    assert "#262 closed by one-read receipt" in text
    assert "#263 closed by value/usefulness evidence packet" in text
    assert "#264 closed by no-live trust-boundary review" in text
    assert "#265 closes this reconciliation after merge and parent #6 receipt" in text


def test_l6ac05_parent_status_and_one_read_outcome_are_explicit():
    text = normalized(DOC)

    required_terms = (
        "Parent #6 status note: L6AC completed its bounded issue-railed fresh owner-approved report-safe source-card read decision rail as PASS",
        "#261 anchored the source floor `67a1a78db2b7adca0048497cce61412de13032f1`",
        "parent successor comment `4651509390`",
        "issue-bound prep comment `4651509094`",
        "exact max-one read approval comment `4651509226`",
        "#262 verified the exact owner approval and matching executable refs before executing exactly one report-safe source-card read",
        "#263 converted the receipt into report-safe value/usefulness evidence without another read",
        "#264 confirmed max-one custody, consumed approval, stale approval resistance, report-safe redaction posture, no standing approval, and no Gate movement",
        "Live/source outcome: exactly one live/private source-card read occurred in L6AC, only in #262",
        "Raw private source content was not recorded",
        "Verification status to report on #6 after this packet merges",
        "This reconciliation does not create successor issues, schedule automation, move Atlas Gate, activate services, change repository visibility, publish a package, authorize another read, or imply release/publication readiness",
    )
    for term in required_terms:
        assert term in text


def test_l6ac05_next_frontier_requires_owner_created_issue_rail():
    text = normalized(DOC)

    required_terms = (
        "Next exact issue-railed frontier: `owner-created post-L6AC implementation-or-hold decision rail`",
        "not created, scheduled, approved, or authorized by this packet",
        "Jeremy must explicitly create any successor issues and any future approval",
        "future live/private read, source discovery, implementation unhold, provider/prod/canary movement, Runtime Registry use, persistence/mutation, publication, service activation, or Atlas Gate movement remains blocked",
        "separate fresh owner comment on the exact execution issue",
        "binds max one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` operation",
        "expires within <=12h",
        "names exact executable descriptor/source-card refs",
        "treats #262 PASS as consumed historical evidence only",
        "missing, stale, copied, broadened, expired, mismatched, unsafe, non-owner, second-read, missing-ref, unsafe-output, or broad-allow variants",
    )
    for term in required_terms:
        assert term in text


def test_l6ac05_preserves_all_residual_holds():
    text = normalized(DOC)

    for held in RESIDUAL_HOLDS:
        assert held in text
