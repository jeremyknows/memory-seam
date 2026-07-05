from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aj05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_SUPERVISED_REAL_READ_PREP_READY_EXECUTION_HELD"
NEXT_FRONTIER = "STEP_3_EXECUTION_HELD_FOR_FRESH_EXACT_SOURCE_QUERY_OUTPUT_APPROVAL"
RAIL_STARTING_SOURCE_FLOOR = "e7b3e67c438891be00f4001d9cfff72026ebe4d3"
SOURCE_FLOOR_ENTERING_SLICE = "d9b94b7d73140eb00ef1426ea2cff8a2e13bc72e"
PARENT_SUCCESSOR_PREP_COMMENT = "4654676210"
SCAFFOLD_AUTH_COMMENT = "4654676115"
DENIAL_HARNESS_PREAUTH_COMMENT = "4654676162"
OPERATION_CLASS = "L6AJ_SUPERVISED_REAL_READ_PREP_RECONCILIATION"
EVIDENCE_CLASS = "SUPERVISED_REAL_READ_PREP_SOURCE_FLOOR_PARENT_TRACKER_RECONCILIATION"

RAIL_ROWS = (
    "#331 | #336 | `55c3fec203ba0398347cdc441dbb2be36cf290ca` | `PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION`",
    "#332 | #337 | `435c352b03a8ac41d109ec1105b86e1626a65af1` | `PASS_DENIAL_BEFORE_READ_FIXTURE_HARNESS_READY_NO_LIVE_READ`",
    "#333 | #338 | `1d96bb793b50a6146496c1dba28c3d80b7015ed7` | `PASS_REPORT_SAFE_SOURCE_QUERY_OUTPUT_ENVELOPE_READY_NO_EXECUTION`",
    "#334 | #339 | `d9b94b7d73140eb00ef1426ea2cff8a2e13bc72e` | `PASS_PREP_TRUST_BOUNDARY_REVIEW_EXECUTION_STILL_HELD`",
    "#335 | packet PR | pending merge handoff | `RAIL_PASS_RECONCILED_SUPERVISED_REAL_READ_PREP_READY_EXECUTION_HELD`",
)

PREP_OUTCOME_TERMS = (
    "#331 defines exact future approval packet semantics for one supervised real read and one denied out-of-scope request before source access",
    "#332 adds a no-live fixture-only denial-before-read harness with inert spies/counters and fail-closed receipt posture",
    "#333 defines a report-safe synthetic source/query/output envelope and forbids raw/private/source/approval/credential echo fields",
    "#334 records trust-boundary PASS, required stop-before-read conditions, and reconciliation-only handoff to #335",
    "All L6AJ prep artifacts preserve zero guarded counters",
    "No L6AJ issue authorizes execution",
    "supervised real-read execution remains held pending a future fresh owner-created execution issue/comment",
)

TRACKER_TERMS = (
    "current_floor_checked` should become the final #335 merged source floor",
    "Roadmap step 3 should become PREP READY / EXECUTION HELD with L6AJ #331-#335 closed",
    "PRs #336-#340 merged",
    "parent #6 L6AJ completion receipt comment ID",
    "Roadmap step 3 execution proof remains incomplete until a fresh exact owner-approved source/query/output packet authorizes one supervised real read plus one denied out-of-scope request before source access",
    "Roadmap step 4 should remain HELD until a separately issue-bound fresh-agent proof exists",
    "Roadmap steps 5-8 should remain HELD unless separately issue-bound and approved",
)

RESIDUAL_HOLDS = (
    "supervised real-read execution until a fresh exact owner-created execution issue/comment binds source, query, output, operation count, denied-request count, expiry, report-safe receipt fields, and stop conditions",
    "any live/private read",
    "any source-card read",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks and provider routes",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
    "new-agent proof until a separate fresh-session/fresh-profile issue-bound proof is created and approved",
    "service/provider auth, canary/fleet activation, write custody, and Gate movement until separate exact rails and approvals exist",
)

UNSAFE_REPORT_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials",
    "auth material",
    "environment values",
    "keychain material",
    "OAuth material",
    "auth-file material",
    "private absolute paths",
    "source URIs",
    "platform IDs",
    "prompts",
    "queries",
    "payloads",
    "backend responses",
    "private correlation refs",
    "Runtime Registry handles",
    "provider handles",
    "secret values",
    "token-like values",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aj05_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aj05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6aj05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AJ.05 source-floor parent tracker reconciliation" in inventory
    assert STATUS in inventory


def test_l6aj05_records_status_floor_scope_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AJ.05 source-floor parent tracker reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #335",
        "Parent issue: #6",
        "Depends on: #331-#334 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AJ successor prep comment: `{PARENT_SUCCESSOR_PREP_COMMENT}`",
        f"Prior scaffold authorization reference: #331 comment `{SCAFFOLD_AUTH_COMMENT}`",
        f"Prior denial harness preauthorization reference: #332 comment `{DENIAL_HARNESS_PREAUTH_COMMENT}`",
        "Closeout comments: #331 `4654717500`, #332 `4654794469`, #333 `4654872366`, #334 `4654929247`",
        "Tracker reconciliation target: Atlas roadmap tracker for Memory Seam 8-step roadmap",
        f"Operation reconciled: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        "Verdict vocabulary: `RAIL_PASS_RECONCILED_SUPERVISED_REAL_READ_PREP_READY_EXECUTION_HELD`, `FIX_PREP_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_EXACT_OWNER_EXECUTION_APPROVAL`",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "consumes only committed L6AJ docs/tests/modules, public issue/PR/source-floor metadata, and the Atlas roadmap tracker state",
        "performs no supervised real read",
    ):
        assert term in text


def test_l6aj05_rail_anchors_and_prep_ready_outcome() -> None:
    text = normalized(DOC)

    assert "Rail anchors" in text
    for row in RAIL_ROWS:
        assert row in text
    assert "Prep-ready outcome" in text
    for term in PREP_OUTCOME_TERMS:
        assert term in text


def test_l6aj05_parent_and_tracker_reconciliation_instructions() -> None:
    text = normalized(DOC)

    for term in (
        "Parent #6 should receive an L6AJ completion receipt after #335 merges and closes",
        "final PR/source floor for #335",
        "verification commands and GitHub checks",
        "prep-ready outcome `RAIL_PASS_RECONCILED_SUPERVISED_REAL_READ_PREP_READY_EXECUTION_HELD`",
        "tracker update confirming roadmap step 3 is PREP READY / EXECUTION HELD",
        f"next frontier: `{NEXT_FRONTIER}`",
        "does not create successor issues",
        "update cron jobs",
        "authorize a supervised real read",
        "authorize a new-agent proof",
    ):
        assert term in text
    for term in TRACKER_TERMS:
        assert term in text


def test_l6aj05_residual_holds_and_report_safe_boundaries() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text
    assert "Report-safe boundaries" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text

    lowered = text.lower()
    for marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    ):
        assert marker not in lowered


def test_l6aj05_verification_and_final_closeout_constraints() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6aj05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "After PR merge and #335 closeout, post the parent #6 L6AJ completion receipt",
        "Do not create successor issues",
        "Do not create or update cron jobs",
        "Do not execute any supervised real read, additional prep proof, denied request, or source access",
        "Do not move publication, provider/prod/canary/Gate, or Atlas Gate state",
    ):
        assert term in text
