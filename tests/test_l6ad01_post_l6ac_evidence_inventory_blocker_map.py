from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ad01-post-l6ac-evidence-inventory-blocker-map.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_INVENTORY_COMPLETE_IMPLEMENTATION_STILL_HELD"
RAIL_STARTING_SOURCE_FLOOR = "f606ed18737d057f0b544503c2532935a9d6c258"
PARENT_SUCCESSOR_COMMENT = "4651958877"
ISSUE_AUTHORIZATION_COMMENT = "4651958544"

L6AC_ANCHORS = (
    "L6AC.01 fresh owner-approved source-card read approval packet (#261 / PR #266 / source floor `ca81a18fbba9603f5f35a8fa57410963e028c904`)",
    "L6AC.02 owner-approved one-read receipt (#262 / PR #267 / source floor `e954c2e37e7c643dbde71e3f8d371c4aee04011c`)",
    "L6AC.03 report-safe value/usefulness evidence packet (#263 / PR #268 / source floor `734fe3a05158d8412b5d27d8c2998b6afcd4678c`)",
    "L6AC.04 no-live trust-boundary review (#264 / PR #269 / source floor `6f627ac73d26fceb60be5eb61de47ee7ad7043ed`)",
    "L6AC.05 source-floor parent status and frontier reconciliation (#265 / PR #270 / source floor `f606ed18737d057f0b544503c2532935a9d6c258`)",
)

BLOCKER_ROWS = (
    ("L6AC evidence inventory", "`PASS`"),
    ("Report-safe value proof", "`PASS`"),
    ("Decision packet readiness", "`PASS_TO_L6AD_02`"),
    ("Future implementation authority", "`HOLD`"),
    ("Additional source-card reads", "`HOLD`"),
    ("Source discovery / broad recall / index query", "`HOLD`"),
    ("Runtime Registry / callbacks / provider routes", "`HOLD`"),
    ("Persistence / mutation / rollback execution", "`HOLD`"),
    ("Service/global activation and cron changes", "`HOLD`"),
    ("Publication / visibility / provider-prod-canary / Atlas Gate", "`HOLD`"),
    ("Broad `allowed=true` behavior", "`HOLD`"),
)

RESIDUAL_HOLDS = (
    "live/private reads remain held beyond the already-consumed single #262 report-safe source-card read",
    "raw private content, raw source text, and raw approval prose remain held",
    "credentials/auth/env/keychain/OAuth/auth-file reads remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "callbacks and provider/backend/source-stat/source-read routes remain held outside the consumed #262 receipt",
    "persistence, audit/custody writes, mutation, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held",
    "implementation/runtime execution remains held pending a separate exact owner-created implementation authority",
    "a second read remains held",
    "any broad `allowed=true` route remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ad01_inventory_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ad01-post-l6ac-evidence-inventory-blocker-map.md" in docs_index
    assert "tests/test_l6ad01_post_l6ac_evidence_inventory_blocker_map.py" in inventory
    assert "L6AD.01 post-L6AC evidence inventory and implementation blocker map" in inventory
    assert STATUS in inventory


def test_l6ad01_records_status_source_floor_and_authorization_anchors():
    text = normalized(DOC)

    required_terms = (
        "# L6AD.01 post-L6AC evidence inventory and implementation blocker map",
        f"Status: `{STATUS}`",
        "Rail issue: #271",
        "Parent issue: #6",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound authorization comment: `{ISSUE_AUTHORIZATION_COMMENT}`",
        "Verdict vocabulary: `PASS_INVENTORY_COMPLETE`, `FIX_BEFORE_DECISION_PACKET`, `HOLD_FOR_OWNER_DECISION`",
        "Verdict: `PASS_INVENTORY_COMPLETE`",
    )
    for term in required_terms:
        assert term in text


def test_l6ad01_inventories_l6ac_artifacts_and_one_consumed_read():
    text = normalized(DOC)

    for anchor in L6AC_ANCHORS:
        assert anchor in text

    required_terms = (
        "exact executable refs `descriptor:l6ac/report-safe-operator-preference-card` and `source-card:l6ac/report-safe-operator-preference-card`",
        "#262 approval comment `4651509226`",
        "executed exactly one `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        "emitted report-safe metadata/value evidence only",
        "consumed the #262 approval",
        "without another live/private read",
        "L6AC as PASS with exactly one consumed #262 report-safe read",
    )
    for term in required_terms:
        assert term in text


def test_l6ad01_preserves_no_live_no_runtime_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests-only evidence inventory",
        "does not implement runtime behavior",
        "execute held surfaces",
        "authorize another source-card read",
        "No additional source-card read, live/private read, source discovery, workspace scan, family scan, broad recall, index query",
        "credential/auth/env/keychain/OAuth/auth-file read",
        "Runtime Registry consumption",
        "persistence, mutation, write/delete/reindex/cache-purge",
        "service/global activation",
        "provider/prod/canary movement, Atlas Gate movement, or broad `allowed=true` route occurred in L6AD.01",
    )
    for term in required_terms:
        assert term in text


def test_l6ad01_distinguishes_value_proof_from_implementation_authority():
    text = normalized(DOC)

    required_terms = (
        "one approved report-safe source-card read in #262 produced metadata/value output",
        "useful enough to justify an implementation-or-hold decision packet",
        "It does not prove that implementation is now approved",
        "does not authorize another read, broad source access, live/private content exposure, source discovery, callbacks, Runtime Registry use, persistence, mutation",
        "#262 one-read approval is consumed historical evidence only and is not reusable",
        "parent successor comment `4651958877`",
        "issue-bound authorization comment `4651958544`",
        "source-floor advancement, copied wording, stale comments, labels, rail continuity, or this inventory PASS",
    )
    for term in required_terms:
        assert term in text


def test_l6ad01_blocker_map_labels_pass_and_hold_surfaces():
    text = normalized(DOC)

    assert "## Implementation blocker map" in text
    for surface, label in BLOCKER_ROWS:
        assert surface in text
        assert label in text

    required_terms = (
        "`PASS_TO_L6AD_02`",
        "No L6AD.01 artifact, issue body, comment, PR merge, or source-floor advancement authorizes implementation/runtime behavior",
        "#262 approval is consumed",
        "Runtime Registry consumption and provider/backend/source-stat/source-read callbacks remain blocked",
        "No service/listener/startup/global config activation and no recursive cron/schedule modification are authorized",
    )
    for term in required_terms:
        assert term in text


def test_l6ad01_carries_residual_holds_and_next_issue():
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #271: #272 `L6AD.02: implementation-or-hold decision packet`" in text
    assert "returns one of `PASS_UNHOLD_PACKET_READY`, `FIX_BEFORE_IMPLEMENTATION`, or `HOLD_FOR_OWNER_DECISION`" in text
    assert "must not implement runtime behavior or execute held surfaces" in text

    unsafe_markers = (
        "raw private source text",
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
