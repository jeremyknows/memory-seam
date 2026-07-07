from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ai03-current-session-tool-proof-receipt-usefulness-packet.md"
PROOF_DOC = REPO_ROOT / "docs" / "l6ai02-current-session-allowed-denied-no-live-tool-proof.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_RECEIPT_USEFULNESS_PACKET_NO_ADDITIONAL_PROOF"
VERDICT = "PASS_RECEIPT_USEFULNESS_PACKET"
NEXT_FRONTIER = "NO_LIVE_TRUST_BOUNDARY_REVIEW_ALLOWED_FOR_ISSUE_324_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"
SOURCE_FLOOR_ENTERING_SLICE = "a52a5503f12520b7dbe6d5d963d5a2d8dfd30452"
CONTRACT_PACKET_SOURCE_FLOOR = "7b35141dce9d559add86ec31f1c5857a1fb435f0"
PROOF_SOURCE_FLOOR = "a52a5503f12520b7dbe6d5d963d5a2d8dfd30452"
PARENT_SUCCESSOR_COMMENT = "4654450317"
CONTRACT_AUTH_COMMENT = "4654450209"
PROOF_APPROVAL_COMMENT = "4654450262"
OPERATION_CLASS = "L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"

RECEIPT_TERMS = (
    "allowed status | `PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`",
    "allowed evidence class | `CURRENT_SESSION_TOOL_SHIM_NO_LIVE_REPORT_SAFE`",
    "allowed label | `EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF`",
    "allowed proof count | `1`",
    "denied status | `DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST`",
    "denied evidence class | `CURRENT_SESSION_DENIAL_BEFORE_SOURCE_ACCESS`",
    "denied request count | `1`",
    "denied before source access | `true`",
    "broad `allowed=true` | `false`",
    "Runtime Registry consumed | `false`",
    "callbacks invoked | `false`",
    "persistence or mutation invoked | `false`",
    "activation invoked | `false`",
    "writes invoked | `false`",
    "publication or Gate movement invoked | `false`",
    "guarded counters | all zero",
)

USEFULNESS_TERMS = (
    "Can the current session reach a Memory Seam tool/shim path?",
    "one exact current-session shim proof returned `CURRENT_SESSION_TOOL_SHIM_NO_LIVE_REPORT_SAFE`",
    "Can the path return report-safe metadata useful to an operator?",
    "source floor, evidence class, status labels, counts, booleans, zero counters, artifact paths, and public IDs",
    "Can out-of-scope requests fail closed?",
    "`DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST` with `denial_before_source_access=true`",
    "Did held surfaces remain quiet?",
    "Does the result move roadmap step 2 forward?",
    "Step 3 supervised real read remains held until a fresh exact source/query/output approval exists",
)

HELD_SURFACES = (
    "Additional current-session tool proof",
    "Additional denied out-of-scope request",
    "Live/private reads and source-card reads",
    "Source discovery / workspace-family scan / broad recall / index query",
    "Runtime Registry",
    "Callback/provider/backend routes",
    "Persistence / mutation / write / rollback / cache purge",
    "Service/listener/startup/global activation",
    "Credentials/auth/env/keychain/OAuth/auth files",
    "Publication / visibility / provider-prod-canary / Gate / Atlas Gate",
    "Broad `allowed=true`",
    "Cron / automation",
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


def test_l6ai03_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ai03-current-session-tool-proof-receipt-usefulness-packet.md" in docs_index
    assert "tests/test_l6ai03_current_session_tool_proof_receipt_usefulness_packet.py" in inventory
    assert "L6AI.03 current-session tool proof receipt and usefulness packet" in inventory
    assert STATUS in inventory


def test_l6ai03_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AI.03 current-session tool proof receipt and usefulness packet",
        f"Status: `{STATUS}`",
        "Rail issue: #323",
        "Parent issue: #6",
        "Depends on: #322 closed/PASS via PR #327",
        "Roadmap step: 2 current-session tool proof",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Contract packet PR/source floor: #326 `{CONTRACT_PACKET_SOURCE_FLOOR}`",
        f"Current-session proof PR/source floor: #327 `{PROOF_SOURCE_FLOOR}`",
        f"Parent L6AI successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Contract packet authorization: #321 comment `{CONTRACT_AUTH_COMMENT}`",
        f"Proof approval consumed by #322: #322 comment `{PROOF_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Reviewed proof artifact: `docs/l6ai02-current-session-allowed-denied-no-live-tool-proof.md`",
        "Reviewed proof module: `src/memory_seam/l6ai_current_session_tool_proof.py`",
        "Reviewed proof test: `tests/test_l6ai02_current_session_allowed_denied_no_live_tool_proof.py`",
        "Verdict vocabulary: `PASS_RECEIPT_USEFULNESS_PACKET`, `FIX_BEFORE_TRUST_BOUNDARY_REVIEW`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
        "docs/tests/review scope only",
        "performs no additional current-session tool proof",
        "no additional denied out-of-scope request",
    )
    for term in required_terms:
        assert term in text


def test_l6ai03_packages_prior_receipt_without_rerunning_proof() -> None:
    text = normalized(DOC)
    proof_text = normalized(PROOF_DOC)

    assert "Status: `PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF`" in proof_text
    assert "Proof approval consumed: #322 comment `4654450262`" in proof_text
    assert "`denied_out_of_scope_request_count` | `1`" in proof_text

    assert "Report-safe receipt from #322" in text
    assert "#323 packages that result without rerunning it" in text
    for term in RECEIPT_TERMS:
        assert term in text
    for term in (
        "The useful result is control-plane evidence",
        "active Sax/current-session lane can exercise a Memory Seam tool/shim path",
        "narrow non-boolean allowed label",
        "reject one out-of-scope request before source access",
        "not a live source-card value proof",
        "not a broad recall proof",
        "not runtime activation",
        "not provider/backend routing",
        "not standing authority for another proof",
    ):
        assert term in text


def test_l6ai03_usefulness_assessment_records_value_and_limits() -> None:
    text = normalized(DOC)

    assert "Usefulness assessment" in text
    for term in USEFULNESS_TERMS:
        assert term in text
    for term in (
        "It returned no raw private content, no raw source text, no prompt/query/payload material, and no live source value",
        "It proves only the exact single denial requested by #322",
        "it is not a broad denial matrix for all future sessions",
        "Future held-surface use still needs separate exact owner approval and issue-bound tests",
    ):
        assert term in text


def test_l6ai03_held_surface_map_and_residual_holds() -> None:
    text = normalized(DOC)

    assert "Held-surface map after #323" in text
    for surface in HELD_SURFACES:
        assert surface in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text
    for term in (
        "Any second proof, broader proof, or different tool path requires fresh exact owner approval",
        "Additional denial exercises remain held unless separately scoped",
        "Any supervised real read requires fresh exact source/query/output approval",
        "fixture/surrogate proof",
        "denial-before-registry proof",
        "denial-before-callback behavior",
        "Human release/Gate authority remains required",
        "General allow semantics remain held",
        "Automation changes remain held",
    ):
        assert term in text


def test_l6ai03_report_safe_boundaries_verification_and_next_blocker() -> None:
    text = normalized(DOC)

    assert "Report-safe boundaries" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_example_markers:
        assert marker not in lowered

    for term in (
        "python -m pytest -q tests/test_l6ai03_current_session_tool_proof_receipt_usefulness_packet.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "Next open rail issue after #323: #324",
        "#324 is docs/tests/review scope only",
        "does not authorize an additional current-session tool proof",
        "another denied request",
        "live/private read",
        "source-card read outside committed no-live fixture/surrogate proof",
        "callback/provider route",
        "Runtime Registry consumption",
        "persistence/mutation",
        "write/delete/reindex/cache-purge/rollback execution",
        "activation",
        "cron change",
        "publication/provider/prod/canary/Gate movement",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    ):
        assert term in text
