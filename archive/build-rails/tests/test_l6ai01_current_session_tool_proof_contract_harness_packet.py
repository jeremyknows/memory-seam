from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ai01-current-session-tool-proof-contract-harness-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION"
RAIL_STARTING_SOURCE_FLOOR = "9c706d0b430f64e0b3ea9fd85b220f6abcb0c497"
PARENT_SUCCESSOR_COMMENT = "4654450317"
CONTRACT_AUTHORIZATION_COMMENT = "4654450209"
PROOF_APPROVAL_COMMENT = "4654450262"
OPERATION_CLASS = "L6AI_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"
NEXT_FRONTIER = "CURRENT_SESSION_PROOF_ALLOWED_FOR_ISSUE_322_ONLY"

HELD_COUNTER_TERMS = (
    "live_private_read_count=0",
    "source_card_read_count=0",
    "raw_private_content_count=0",
    "raw_source_text_count=0",
    "raw_approval_prose_count=0",
    "credential_auth_read_count=0",
    "discovery_query_count=0",
    "runtime_registry_consumed=false",
    "callback_invoked=false",
    "persistence_or_mutation_attempted=false",
    "activation_attempted=false",
    "write_attempted=false",
    "publication_or_gate_movement_attempted=false",
    "broad_allowed_attempted=false",
    "all held-surface counters zero",
)

RESIDUAL_HOLDS = (
    "#322 proof execution until the next tick selects #322 and revalidates live issue/approval/source-floor state",
    "any current-session proof beyond exactly one allowed no-live/report-safe proof under #322",
    "any denied request beyond exactly one out-of-scope denial under #322",
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials/auth/env/keychain/OAuth/auth-file reads",
    "discovery, workspace scans, family scans, broad recall, and index queries",
    "live/private reads",
    "source-card reads outside committed no-live fixture/surrogate proof",
    "Runtime Registry consumption",
    "callbacks/provider routes",
    "persistence, mutation, writes, delete, reindex, rollback execution, cache purge, and runtime cache mutation",
    "service/listener/startup/global activation and recursive cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
)

UNSAFE_MARKERS = (
    "oauth token",
    "credential value",
    "auth-file secret",
    "private-correlation-ref",
    "source://",
    "raw private source text",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ai01_packet_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ai01-current-session-tool-proof-contract-harness-packet.md" in docs_index
    assert "tests/test_l6ai01_current_session_tool_proof_contract_harness_packet.py" in inventory
    assert "L6AI.01 current-session tool proof contract and harness packet" in inventory
    assert STATUS in inventory


def test_l6ai01_records_status_source_floor_and_exact_binding() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AI.01 current-session tool proof contract and harness packet",
        f"Status: `{STATUS}`",
        "Rail issue: #321",
        "Parent issue: #6",
        "Depends on: L6AH #311-#315 closed/PASS",
        "Roadmap step: 2 current-session tool proof",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Parent L6AI successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound contract authorization: #321 comment `{CONTRACT_AUTHORIZATION_COMMENT}`",
        f"Future proof approval reference: #322 comment `{PROOF_APPROVAL_COMMENT}`",
        f"Operation class: `{OPERATION_CLASS}`",
        "Exact future proof issue: #322",
        "Verdict vocabulary: `PASS_CONTRACT_PACKET_READY_NO_PROOF_EXECUTION`, `FIX_BEFORE_PROOF`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ai01_preserves_non_execution_public_metadata_boundary() -> None:
    text = normalized(DOC)

    required_terms = (
        "docs/tests/fixtures/public-metadata-only",
        "does not execute the current-session proof",
        "invoke a live/private read",
        "read a source card",
        "consume Runtime Registry data",
        "invoke callbacks/provider routes",
        "persist or mutate runtime state",
        "start services",
        "activate global behavior",
        "change cron automation",
        "publish or change visibility",
        "move provider/prod/canary/Gate/Atlas Gate surfaces",
        "execute writes",
        "broad `allowed=true` behavior",
        "source floor, parent issue, rail issue numbers, public comment IDs, operation-class labels, evidence classes, status labels, booleans, zero held-surface counters, and repo-relative artifact paths",
    )
    for term in required_terms:
        assert term in text


def test_l6ai01_binds_exact_future_allowed_and_denied_proof_counts() -> None:
    text = normalized(DOC)

    required_terms = (
        "#322 may execute exactly two current-session requests under the #322 approval, and no more",
        "One allowed no-live/report-safe current-session Memory Seam tool/shim proof",
        "One denied out-of-scope current-session request that denies before source access",
        "repository `jeremyknows/memory-seam`",
        f"bind source floor `{RAIL_STARTING_SOURCE_FLOOR}`",
        "The allowed proof is not a broad allow route",
        "`allowed=\"EXACT_NO_LIVE_CURRENT_SESSION_TOOL_PROOF\"`",
        "never boolean `allowed=true`",
        "`current_session_tool_proof_count=1`",
        "`denied_out_of_scope_request_count=0`",
        "`status=\"DENIED_BEFORE_SOURCE_ACCESS_OUT_OF_SCOPE_CURRENT_SESSION_REQUEST\"`",
        "`current_session_tool_proof_count=0`",
        "`denied_out_of_scope_request_count=1`",
        "`denial_before_source_access=true`",
    )
    for term in required_terms:
        assert term in text


def test_l6ai01_requires_report_safe_harness_fields_and_zero_held_surfaces() -> None:
    text = normalized(DOC)

    required_terms = (
        "`repo`",
        "`rail_issue`",
        "`parent_issue`",
        "`source_floor`",
        "`parent_successor_comment`",
        "`contract_authorization_comment`",
        "`proof_approval_comment`",
        "`operation_class`",
        "`evidence_class`",
        "`artifact_paths`",
        "`guarded_counters`",
        "`held_surface_flags`",
        "safe labels only",
        "repo-relative docs/tests paths only",
        "integer zero values only unless the exact proof count or denied count is the one authorized operation",
        "booleans proving held surfaces were not touched",
    )
    for term in required_terms:
        assert term in text

    for counter_term in HELD_COUNTER_TERMS:
        assert counter_term in text


def test_l6ai01_denial_before_source_access_and_stop_conditions() -> None:
    text = normalized(DOC)

    required_terms = (
        "denies before source access",
        "raw private content",
        "raw source text",
        "raw approval prose",
        "credentials/auth/env/keychain/OAuth/auth-file reads",
        "discovery/workspace/family scans",
        "broad recall",
        "index queries",
        "live/private reads",
        "source-card reads outside committed no-live fixture/surrogate proof",
        "Runtime Registry consumption",
        "callbacks/provider routes",
        "persistence/runtime mutation/write/delete/reindex/cache-purge/rollback execution",
        "service/global activation",
        "cron changes",
        "publication/provider/prod/canary/Gate/Atlas Gate movement",
        "more than one allowed proof",
        "more than one denied request",
        "The denial receipt must not echo unsafe request details",
    )
    for term in required_terms:
        assert term in text


def test_l6ai01_verification_gate_residual_holds_and_next_issue() -> None:
    text = normalized(DOC)

    verification_terms = (
        "python -m pytest -q tests/test_l6ai01_current_session_tool_proof_contract_harness_packet.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    )
    for term in verification_terms:
        assert term in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #321: #322 `L6AI.02: execute current-session allowed and denied no-live tool proof`" in text
    assert "may perform exactly one allowed no-live/report-safe current-session Memory Seam tool/shim proof and exactly one denied out-of-scope current-session request only after rechecking source floor, issue state, approval comment, and parent/tracker context" in text

    lowered = text.lower()
    for marker in UNSAFE_MARKERS:
        assert marker not in lowered
