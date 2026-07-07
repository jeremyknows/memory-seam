from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ad02-implementation-or-hold-decision-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_UNHOLD_PACKET_READY_IMPLEMENTATION_NOT_APPROVED"
RAIL_STARTING_SOURCE_FLOOR = "f606ed18737d057f0b544503c2532935a9d6c258"
SOURCE_FLOOR_ENTERING_SLICE = "5d42de21671bb885433bc23d6f5aac9e2be094dc"
PARENT_SUCCESSOR_COMMENT = "4651958877"
DECISION = "PASS_UNHOLD_PACKET_READY"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ad02_decision_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ad02-implementation-or-hold-decision-packet.md" in docs_index
    assert "tests/test_l6ad02_implementation_or_hold_decision_packet.py" in inventory
    assert "L6AD.02 implementation-or-hold decision packet" in inventory
    assert STATUS in inventory


def test_l6ad02_records_status_source_floor_and_decision():
    text = normalized(DOC)

    required_terms = (
        "# L6AD.02 implementation-or-hold decision packet",
        f"Status: `{STATUS}`",
        "Rail issue: #272",
        "Parent issue: #6",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Issue-bound authorization: #272 owner-created issue body",
        "Prerequisite inventory: [`l6ad01-post-l6ac-evidence-inventory-blocker-map.md`](l6ad01-post-l6ac-evidence-inventory-blocker-map.md)",
        "Decision vocabulary: `PASS_UNHOLD_PACKET_READY`, `FIX_BEFORE_IMPLEMENTATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Decision: `{DECISION}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_preserves_docs_tests_only_no_execution_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests-only implementation-or-hold decision packet",
        "does not approve or perform implementation",
        "runtime execution, live/private reads, callbacks, persistence, activation, publication, provider/prod/canary movement, Atlas Gate movement, cron changes",
        "any broad `allowed=true` behavior",
        "The consumed #262 one-read approval remains historical evidence only",
        "not reusable by #272, this packet, issue closure, PR merge, labels, stale comments, copied wording, source-floor advancement, rail continuity, or the parent successor comment",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_decision_basis_cites_l6ac_and_l6ad01_evidence():
    text = normalized(DOC)

    required_terms = (
        "L6AC.02 (#262 / PR #267) consumed exactly one issue-bound owner-approved `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`",
        "`descriptor:l6ac/report-safe-operator-preference-card` and `source-card:l6ac/report-safe-operator-preference-card`",
        "returned report-safe metadata/value evidence only",
        "L6AC.03-L6AC.05 (#263-#265 / PR #268-#270)",
        "without another read or Gate movement",
        "L6AD.01 (#271 / PR #276) inventoried the post-L6AC evidence floor",
        "marked decision-packet readiness as `PASS_TO_L6AD_02`",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_names_future_issue_shape_without_current_approval():
    text = normalized(DOC)

    required_terms = (
        "Result: `PASS_UNHOLD_PACKET_READY` for a future exact owner-created implementation issue packet",
        "`NOT APPROVAL`: This result is not an implementation approval, not a live-read approval, not a runtime execution approval, and not permission to move Atlas Gate",
        "`NEXT`: The next L6AD rail issue is #273",
        "Future issue title shape:",
        "`L6AD.N: default-off report-safe source-card value adapter implementation slice`",
        f"{OPERATION_CLASS}",
        "Approval expires at <UTC timestamp>",
        "max one implementation slice",
        "allowed repo-relative files",
        "rollback/stop conditions",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_candidate_allowed_files_are_narrow_and_default_off():
    text = normalized(DOC)

    required_terms = (
        "This packet does not authorize editing these files for implementation now",
        "`src/memory_seam/l6ad_report_safe_source_card_value_adapter.py`",
        "no live/private read path and no callback/provider/Runtime Registry/persistence hooks",
        "`src/memory_seam/__init__.py`",
        "`tests/test_l6ad_report_safe_source_card_value_adapter.py`",
        "`docs/l6ad03-default-off-implementation-unhold-candidate-design.md`",
        "`docs/README.md` and `docs/contract-test-inventory.md`",
        "should not edit examples, CLI entry points, provider adapters, runtime registry code, service/startup files, cron schedules, packaging/release metadata, publication/visibility controls, or Atlas Gate files",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_required_future_tests_and_stop_conditions():
    text = normalized(DOC)

    required_terms = (
        "python -m pytest tests/test_l6ad_report_safe_source_card_value_adapter.py -q",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "missing, stale, copied, broadened, mismatched, expired, non-owner, callback-requesting, activation-requesting, publication-requesting, provider/prod/canary/Gate-moving, Runtime-Registry-consuming, persistence-requesting, mutation-requesting, and broad `allowed=true` variants deny before any held surface",
        "all guarded callback/source/provider/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge counters remain zero",
        "request for a live/private read or any second source-card read",
        "inability to keep the implementation default-off and fixture-only",
        "any failing targeted/full pytest, hygiene scan, whitespace diff check, or compileall gate",
    )
    for term in required_terms:
        assert term in text


def test_l6ad02_residual_holds_and_next_issue():
    text = normalized(DOC)

    residual_holds = (
        "implementation/runtime execution until a separate exact owner-created future issue approval exists",
        "any live/private read or additional source-card read beyond the consumed historical #262 read",
        "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads",
        "source discovery, workspace scans, family scans, broad recall, and index queries",
        "Runtime Registry consumption",
        "provider/backend/source-stat/source-read callbacks",
        "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
        "service/listener/startup/global activation and recursive cron/schedule changes",
        "publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for hold in residual_holds:
        assert hold in text

    assert "Next open rail issue after #272: #273 `L6AD.03: default-off implementation unhold candidate design and rollback plan`" in text
    assert "must remain docs/tests/design-only and must not implement code/runtime behavior or execute held surfaces" in text

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
