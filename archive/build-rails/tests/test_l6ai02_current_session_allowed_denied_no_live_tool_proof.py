from __future__ import annotations

from pathlib import Path

from memory_seam.l6ai_current_session_tool_proof import (
    L6AI_ALLOWED_EVIDENCE_CLASS,
    L6AI_ALLOWED_LABEL,
    L6AI_ALLOWED_STATUS,
    L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID,
    L6AI_DENIED_EVIDENCE_CLASS,
    L6AI_DENIED_STATUS,
    L6AI_GUARDED_COUNTERS,
    L6AI_OPERATION_CLASS,
    L6AI_PARENT_SUCCESSOR_COMMENT_ID,
    L6AI_PROOF_APPROVAL_COMMENT_ID,
    L6AI_REPORT_SAFE_FIELDS,
    L6AI_REPOSITORY,
    L6AI_SOURCE_FLOOR,
    build_l6ai02_exact_approval_fixture,
    validate_l6ai02_report_safe_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ai02-current-session-allowed-denied-no-live-tool-proof.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_CURRENT_SESSION_NO_LIVE_REPORT_SAFE_TOOL_PROOF"
NEXT_FRONTIER = "CURRENT_SESSION_RECEIPT_AND_USEFULNESS_PACKET_FOR_ISSUE_323"
SOURCE_ENTERING_SLICE = "7b35141dce9d559add86ec31f1c5857a1fb435f0"

HELD_COUNTER_TERMS = (
    "`live_private_read_count` | `0`",
    "`source_card_read_count` | `0`",
    "`raw_private_content_count` | `0`",
    "`raw_source_text_count` | `0`",
    "`raw_approval_prose_count` | `0`",
    "`credential_auth_read_count` | `0`",
    "`discovery_query_count` | `0`",
    "`runtime_registry_read_count` | `0`",
    "`callback_invocation_count` | `0`",
    "`persistence_or_mutation_attempt_count` | `0`",
    "`activation_attempt_count` | `0`",
    "`write_attempt_count` | `0`",
    "`publication_or_gate_movement_attempt_count` | `0`",
    "`broad_allowed_attempt_count` | `0`",
    "all held-surface counters | zero",
)

FORBIDDEN_DOC_MARKERS = (
    "credential value",
    "oauth token",
    "keychain material",
    "auth-file secret",
    "source://",
    "platform-raw-id",
    "private absolute path",
    "raw prompt",
    "raw query",
    "query payload",
    "backend response",
    "private-correlation-ref",
    "raw private source text",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _literal_allowed_receipt() -> dict:
    return {
        "schema_version": "l6ai02-current-session-tool-proof-v1",
        "status": L6AI_ALLOWED_STATUS,
        "repo": L6AI_REPOSITORY,
        "parent_issue": 6,
        "rail_issue": 322,
        "source_floor": L6AI_SOURCE_FLOOR,
        "parent_successor_comment": L6AI_PARENT_SUCCESSOR_COMMENT_ID,
        "contract_authorization_comment": L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID,
        "proof_approval_comment": L6AI_PROOF_APPROVAL_COMMENT_ID,
        "operation_class": L6AI_OPERATION_CLASS,
        "evidence_class": L6AI_ALLOWED_EVIDENCE_CLASS,
        "allowed": L6AI_ALLOWED_LABEL,
        "current_session_tool_proof_count": 1,
        "denied_out_of_scope_request_count": 0,
        "denial_before_source_access": False,
        "artifact_paths": [
            "src/memory_seam/l6ai_current_session_tool_proof.py",
            "docs/l6ai02-current-session-allowed-denied-no-live-tool-proof.md",
            "tests/test_l6ai02_current_session_allowed_denied_no_live_tool_proof.py",
        ],
        "guarded_counters": {counter: 0 for counter in L6AI_GUARDED_COUNTERS},
        "runtime_registry_consumed": False,
        "callback_invoked": False,
        "persistence_or_mutation_attempted": False,
        "activation_attempted": False,
        "write_attempted": False,
        "publication_or_gate_movement_attempted": False,
        "broad_allowed_attempted": False,
        "held_surface_flags": {
            "live_private_reads": False,
            "source_card_reads": False,
            "runtime_registry_consumption": False,
            "callbacks_provider_routes": False,
            "broad_allowed_true_behavior": False,
        },
        "non_sensitive_value_metadata": {
            "value_class": "public_metadata_only",
            "tool_path": "current_session_memory_seam_shim",
            "no_live": True,
            "report_safe": True,
        },
    }


def test_l6ai02_artifacts_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ai02-current-session-allowed-denied-no-live-tool-proof.md" in docs_index
    assert "tests/test_l6ai02_current_session_allowed_denied_no_live_tool_proof.py" in inventory
    assert "L6AI.02 current-session allowed and denied no-live tool proof" in inventory
    assert STATUS in inventory


def test_l6ai02_records_issue_floor_approval_and_verdict() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AI.02 current-session allowed and denied no-live tool proof",
        f"Status: `{STATUS}`",
        "Rail issue: #322",
        "Parent issue: #6",
        "Depends on: #321 closed/PASS",
        "Roadmap step: 2 current-session tool proof",
        f"Rail starting source floor: `{L6AI_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_ENTERING_SLICE}`",
        f"Parent L6AI successor comment: `{L6AI_PARENT_SUCCESSOR_COMMENT_ID}`",
        f"Contract packet authorization: #321 comment `{L6AI_CONTRACT_AUTHORIZATION_COMMENT_ID}`",
        f"Proof approval consumed: #322 comment `{L6AI_PROOF_APPROVAL_COMMENT_ID}`",
        f"Operation class: `{L6AI_OPERATION_CLASS}`",
        "Proof executed at: `2026-06-08T23:39:37Z`",
        "Proof module: `src/memory_seam/l6ai_current_session_tool_proof.py`",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ai02_records_exact_allowed_and_denied_counts() -> None:
    text = normalized(DOC)

    required_terms = (
        "exactly two current-session Memory Seam tool/shim requests",
        "Exactly one allowed no-live/report-safe current-session tool proof",
        "Exactly one denied out-of-scope current-session request that denied before source access",
        f"`status` | `{L6AI_ALLOWED_STATUS}`",
        f"`evidence_class` | `{L6AI_ALLOWED_EVIDENCE_CLASS}`",
        f"`allowed` | `{L6AI_ALLOWED_LABEL}`",
        "`current_session_tool_proof_count` | `1`",
        "`denied_out_of_scope_request_count` | `0`",
        "`denial_before_source_access` | `false`",
        f"`status` | `{L6AI_DENIED_STATUS}`",
        f"`evidence_class` | `{L6AI_DENIED_EVIDENCE_CLASS}`",
        "`allowed` | `false`",
        "`current_session_tool_proof_count` | `0`",
        "`denied_out_of_scope_request_count` | `1`",
        "`denial_before_source_access` | `true`",
        "`request_values_echoed` | `false`",
    )
    for term in required_terms:
        assert term in text


def test_l6ai02_report_safe_boundaries_and_zero_guarded_counters() -> None:
    text = normalized(DOC)

    boundary_terms = (
        "committed report-safe/public metadata",
        "repo-local current-session shim",
        "did not read raw private content",
        "raw source text",
        "raw approval prose",
        "credentials/auth/env/keychain/OAuth/auth-file material",
        "live/private data",
        "Runtime Registry data",
        "backend/provider/callback routes",
        "did not perform discovery",
        "workspace scans",
        "family scans",
        "broad recall",
        "index queries",
        "persistence, mutation, write/delete/reindex/cache-purge/rollback execution",
        "service/listener/startup/global activation",
        "cron changes",
        "publication, visibility changes, provider/prod/canary/Gate movement, Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in boundary_terms:
        assert term in text

    for counter_term in HELD_COUNTER_TERMS:
        assert counter_term in text


def test_l6ai02_module_validation_contract_without_reexecuting_proof() -> None:
    approval = build_l6ai02_exact_approval_fixture()
    assert set(approval) >= {
        "repo",
        "rail_issue",
        "source_floor",
        "proof_approval_comment",
        "operation_class",
        "max_allowed_current_session_tool_proofs",
        "max_denied_out_of_scope_requests",
        "broad_allowed_true_authorized",
    }
    assert approval["max_allowed_current_session_tool_proofs"] == 1
    assert approval["max_denied_out_of_scope_requests"] == 1
    assert approval["broad_allowed_true_authorized"] is False

    literal_receipt = _literal_allowed_receipt()
    assert set(literal_receipt).issubset(L6AI_REPORT_SAFE_FIELDS)
    assert literal_receipt["allowed"] is not True
    assert validate_l6ai02_report_safe_receipt(literal_receipt) == []


def test_l6ai02_verification_residual_holds_and_next_issue() -> None:
    text = normalized(DOC)

    verification_terms = (
        "python -m pytest -q tests/test_l6ai02_current_session_allowed_denied_no_live_tool_proof.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    )
    for term in verification_terms:
        assert term in text

    residual_terms = (
        "any additional current-session tool proof beyond the single #322 allowed proof",
        "any additional out-of-scope denied request beyond the single #322 denial",
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
        "Next open rail issue after #322: #323 `L6AI.03: current-session tool proof receipt and usefulness packet`",
        "must not execute another current-session tool proof",
    )
    for term in residual_terms:
        assert term in text


def test_l6ai02_document_avoids_unsafe_echo_markers() -> None:
    lowered = DOC.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_DOC_MARKERS:
        assert marker not in lowered
