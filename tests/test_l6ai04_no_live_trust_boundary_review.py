from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ai04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_CURRENT_SESSION_TOOL_PROOF"
VERDICT = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "SOURCE_FLOOR_PARENT_TRACKER_RECONCILIATION_ALLOWED_FOR_ISSUE_325_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"
SOURCE_FLOOR_ENTERING_SLICE = "324d1fcdb7233881f3c8db307a2866600423bc5e"
PROOF_APPROVAL_COMMENT = "4654450262"
ISSUE_323_CLOSEOUT_COMMENT = "4654616454"
OPERATION_CLASS = "L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"

EVIDENCE_ROWS = (
    "#321 | #326 / `7b35141dce9d559add86ec31f1c5857a1fb435f0` | Contract/harness packet",
    "#322 | #327 / `a52a5503f12520b7dbe6d5d963d5a2d8dfd30452` | Current-session tool proof receipt",
    "#323 | #328 / `324d1fcdb7233881f3c8db307a2866600423bc5e` | Receipt/usefulness packet",
)

TRUST_FINDINGS = (
    "Approval custody stayed narrow",
    "#322 consumed #322 comment `4654450262` once",
    "Allowed output stayed non-broad",
    "`EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF`, not boolean `allowed=true`",
    "Denied path failed before source access",
    "`DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST` with `denial_before_source_access=true`",
    "Held-surface counters stayed zero",
    "Report-safe output stayed bounded",
    "Roadmap value is real but scoped",
)

REVIEW_DIMENSIONS = (
    "Exact operation binding | PASS",
    "Max-one proof custody | PASS",
    "Denial before source access | PASS",
    "Report-safe metadata | PASS",
    "Raw/private/source/approval hygiene | PASS",
    "Credentials/auth/env/keychain/OAuth/auth-file boundary | PASS",
    "Discovery/scan/recall/index boundary | PASS",
    "Runtime Registry/callback/provider boundary | PASS",
    "Persistence/mutation/write/activation boundary | PASS",
    "Publication/provider/prod/canary/Gate/Atlas Gate boundary | PASS",
    "Broad `allowed=true` boundary | PASS",
    "Next issue readiness | PASS",
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


def test_l6ai04_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ai04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ai04_no_live_trust_boundary_review.py" in inventory
    assert "L6AI.04 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ai04_records_status_floor_scope_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AI.04 no-live trust-boundary review for current-session tool proof",
        f"Status: `{STATUS}`",
        "Rail issue: #324",
        "Parent issue: #6",
        "Depends on: #323 closed/PASS via PR #328",
        "Roadmap step: 2 current-session tool proof",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Contract packet PR/source floor: #326 `7b35141dce9d559add86ec31f1c5857a1fb435f0`",
        "Current-session proof PR/source floor: #327 `a52a5503f12520b7dbe6d5d963d5a2d8dfd30452`",
        "Receipt/usefulness PR/source floor: #328 `324d1fcdb7233881f3c8db307a2866600423bc5e`",
        f"Proof approval consumed by #322: #322 comment `{PROOF_APPROVAL_COMMENT}`",
        f"Issue #323 closeout comment: `{ISSUE_323_CLOSEOUT_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "consumes only committed L6AI docs/tests/module surfaces and public issue/PR/source-floor metadata",
        "performs no additional current-session tool proof",
        "no additional denied out-of-scope request",
    ):
        assert term in text


def test_l6ai04_evidence_review_and_trust_findings() -> None:
    text = normalized(DOC)

    assert "Evidence reviewed" in text
    for row in EVIDENCE_ROWS:
        assert row in text
    for term in TRUST_FINDINGS:
        assert term in text
    for term in (
        "#323 and #324 did not refresh, extend, reuse, or reinterpret that approval as standing authority",
        "request_values_echoed=false",
        "no source-card/live/private source access",
        "public issue/PR/comment IDs, source floors, repo-relative artifact paths",
        "does not prove supervised live read readiness, fresh-agent usability, service/provider auth, canary/fleet activation, write custody, publication, or Gate readiness",
    ):
        assert term in text


def test_l6ai04_pass_fix_hold_review_table() -> None:
    text = normalized(DOC)

    assert "PASS/FIX/HOLD review table" in text
    for dimension in REVIEW_DIMENSIONS:
        assert dimension in text
    assert "#325 may reconcile source floor, parent status, tracker state, and next frontier" in text
    assert "without executing new proof/read surfaces" in text


def test_l6ai04_residual_holds_and_report_safe_boundaries() -> None:
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


def test_l6ai04_verification_and_next_issue_bounds() -> None:
    text = normalized(DOC)

    for term in (
        "python -m pytest -q tests/test_l6ai04_no_live_trust_boundary_review.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "Next open rail issue after #324: #325",
        "#325 may update the Atlas roadmap tracker",
        "must not create successor issues or cron jobs",
        "must not execute another current-session proof",
        "another denied request",
        "live/private read",
        "source-card read outside committed no-live fixture/surrogate proof",
        "callback/provider route",
        "Runtime Registry consumption",
        "persistence/mutation",
        "write/delete/reindex/cache-purge/rollback execution",
        "activation",
        "publication/provider/prod/canary/Gate movement",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    ):
        assert term in text
