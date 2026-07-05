from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ai05-source-floor-parent-tracker-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_CURRENT_SESSION_TOOL_PROOF_STEP_2_COMPLETE"
VERDICT = "RAIL_PASS_RECONCILED_CURRENT_SESSION_TOOL_PROOF"
NEXT_FRONTIER = "STEP_3_SUPERVISED_REAL_READ_HELD_FOR_FRESH_EXACT_APPROVAL"
RAIL_STARTING_SOURCE_FLOOR = "9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"
SOURCE_FLOOR_ENTERING_SLICE = "0a1794046cd02938a4a74a6ee339b836a5e49d7a"
PARENT_SUCCESSOR_COMMENT = "4654450317"
OPERATION_CLASS = "L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"

RAIL_ROWS = (
    "#321 | #326 | `7b35141dce9d559add86ec31f1c5857a1fb435f0` | `PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION`",
    "#322 | #327 | `a52a5503f12520b7dbe6d5d963d5a2d8dfd30452` | `PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`",
    "#323 | #328 | `324d1fcdb7233881f3c8db307a2866600423bc5e` | `PASS_RECEIPT_USEFULNESS_PACKET_NO_ADDITIONAL_PROOF`",
    "#324 | #329 | `0a1794046cd02938a4a74a6ee339b836a5e49d7a` | `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_CURRENT_SESSION_TOOL_PROOF`",
    "#325 | packet PR | pending merge handoff | `RAIL_PASS_RECONCILED_CURRENT_SESSION_TOOL_PROOF`",
)

PROOF_OUTCOME_TERMS = (
    "exactly one allowed no-live/report-safe current-session Memory Seam shim proof occurred in #322",
    "exactly one denied out-of-scope current-session request occurred in #322",
    "the denied request stopped before source access",
    "source floor, evidence class, status/denial labels, booleans, counts, zero held-surface counters",
    "all held-surface counters remained zero",
    "Runtime Registry consumption, callback/provider routes, persistence/mutation, activation, writes, publication/Gate movement, and broad `allowed=true` behavior remained false",
    "#323 and #324 consumed the #322 receipt as historical evidence only",
)

TRACKER_TERMS = (
    "current_floor_checked` should become the final #325 merged source floor",
    "Roadmap step 2 should become COMPLETE with L6AI #321-#325 closed",
    "PRs #326-#330 merged",
    "#322 current-session proof outcome",
    "Roadmap step 3 should remain HELD until fresh exact source/query/output approval exists",
    "Roadmap steps 4-8 should remain HELD unless separately issue-bound and approved",
)

RESIDUAL_HOLDS = (
    "any additional current-session tool proof beyond #322's consumed one allowed proof",
    "any additional out-of-scope denied request beyond #322's consumed one denial",
    "live/private reads and source-card reads outside committed no-live fixture/surrogate proof",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks and provider routes",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
    "step 3 supervised real read until a fresh exact source/query/output approval exists",
    "step 4 new-agent proof until a separate fresh-session/fresh-profile issue-bound proof is created and approved",
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


def test_l6ai05_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ai05-source-floor-parent-tracker-reconciliation.md" in docs_index
    assert "tests/test_l6ai05_source_floor_parent_tracker_reconciliation.py" in inventory
    assert "L6AI.05 source-floor parent status tracker reconciliation" in inventory
    assert STATUS in inventory


def test_l6ai05_records_status_floor_scope_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AI.05 source-floor parent status tracker reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #325",
        "Parent issue: #6",
        "Depends on: #324 closed/PASS via PR #329",
        "Roadmap step: 2 current-session tool proof",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AI successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Contract packet authorization: #321 comment `4654450209`",
        "Proof approval consumed by #322: #322 comment `4654450262`",
        "Closeout comments: #321 `4654484717`, #322 `4654551378`, #323 `4654616454`, #324 `4654637779`",
        "Tracker reconciliation target: Atlas roadmap tracker for Memory Seam 8-step roadmap",
        f"Operation reconciled: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `RAIL_PASS_RECONCILED_CURRENT_SESSION_TOOL_PROOF`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "consumes only committed L6AI docs/tests/module surfaces, public issue/PR/source-floor metadata, and the Atlas roadmap tracker state",
        "performs no additional current-session tool proof",
        "no additional denied out-of-scope request",
    ):
        assert term in text


def test_l6ai05_rail_anchors_and_current_session_outcome() -> None:
    text = normalized(DOC)

    assert "Rail anchors" in text
    for row in RAIL_ROWS:
        assert row in text
    assert "Current-session proof outcome" in text
    for term in PROOF_OUTCOME_TERMS:
        assert term in text


def test_l6ai05_parent_and_tracker_reconciliation_instructions() -> None:
    text = normalized(DOC)

    for term in (
        "Parent #6 should receive an L6AI completion receipt after #325 merges and closes",
        "final PR/source floor for #325",
        "verification commands and GitHub checks",
        "current-session proof outcome `PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`",
        "tracker update confirming roadmap step 2 complete",
        "next frontier: `STEP_3_SUPERVISED_REAL_READ_HELD_FOR_FRESH_EXACT_APPROVAL`",
        "does not create successor issues",
        "update cron jobs",
        "authorize a supervised real read",
        "authorize a new-agent proof",
    ):
        assert term in text
    for term in TRACKER_TERMS:
        assert term in text


def test_l6ai05_residual_holds_and_report_safe_boundaries() -> None:
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


def test_l6ai05_verification_and_final_closeout_constraints() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6ai05_source_floor_parent_tracker_reconciliation.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "After PR merge and #325 closeout, post the parent #6 L6AI completion receipt",
        "Do not create successor issues",
        "Do not create or update cron jobs",
        "Do not execute another proof/read/denial surface",
        "Do not move publication, provider/prod/canary/Gate, or Atlas Gate state",
    ):
        assert term in text
