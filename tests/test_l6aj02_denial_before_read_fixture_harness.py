from __future__ import annotations

from pathlib import Path

from memory_seam.l6aj_denial_before_read_harness import (
    L6AJ_DENIED_EVIDENCE_CLASS,
    L6AJ_DENIED_STATUS,
    L6AJ_OPERATION_CLASS,
    L6AJ_RAIL_STARTING_SOURCE_FLOOR,
    L6AJ_SOURCE_FLOOR_ENTERING_SLICE,
    L6AJ_STATUS,
    attempt_l6aj02_allowed_supervised_real_read,
    build_l6aj02_harness_preauthorization_fixture,
    deny_l6aj02_out_of_scope_supervised_real_read_request,
    preauthorization_allows_l6aj02_denial_harness,
    validate_l6aj02_report_safe_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aj02-denial-before-read-fixture-harness.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PREAUTH_COMMENT = "4654676162"
SCAFFOLD_AUTH_COMMENT = "4654676115"
PARENT_SUCCESSOR_PREP_COMMENT = "4654676210"
NEXT_FRONTIER = "REPORT_SAFE_SOURCE_QUERY_OUTPUT_ENVELOPE_FOR_ISSUE_333"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aj02_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aj02-denial-before-read-fixture-harness.md" in docs_index
    assert "tests/test_l6aj02_denial_before_read_fixture_harness.py" in inventory
    assert "L6AJ.02 denial-before-read fixture harness" in inventory
    assert L6AJ_STATUS in inventory


def test_l6aj02_records_issue_floor_preauth_and_scope() -> None:
    text = normalized(DOC)
    required_terms = (
        "# L6AJ.02 denial-before-read fixture harness for supervised real-read prep",
        f"Status: `{L6AJ_STATUS}`",
        "Rail issue: #332",
        "Parent issue: #6",
        "Depends on: #331 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{L6AJ_RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{L6AJ_SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AJ successor prep comment: `{PARENT_SUCCESSOR_PREP_COMMENT}`",
        f"Consumed no-live harness preauthorization: #332 comment `{PREAUTH_COMMENT}`",
        f"Prior scaffold authorization reference: #331 comment `{SCAFFOLD_AUTH_COMMENT}`",
        f"Operation class: `{L6AJ_OPERATION_CLASS}`",
        "Exact future supervised real-read execution approval: none present; execution remains held",
        "Verdict vocabulary: `PASS_DENIAL_BEFORE_READ_FIXTURE_HARNESS_READY_NO_LIVE_READ`, `FIX_BEFORE_ENVELOPE`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{L6AJ_STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6aj02_doc_preserves_no_live_fixture_only_boundary() -> None:
    text = normalized(DOC)
    required_terms = (
        "no-live fixture-only denial-before-read harness",
        "inert spies/counters only",
        "does not execute a supervised real read",
        "does not perform a live/private read",
        "does not read source cards",
        "does not read raw private content/source text/approval prose",
        "does not read credentials/auth/env/keychain/OAuth/auth-file material",
        "does not perform source discovery, workspace scans, family scans, broad recall, or index queries",
        "does not consume Runtime Registry data",
        "does not invoke real callbacks/provider routes",
        "does not persist, mutate, write, delete, reindex, cache-purge, rollback execute, or mutate runtime cache",
        "does not activate service/listener/startup/global paths",
        "does not change cron automation",
        "does not publish, change visibility, move provider/prod/canary/Gate surfaces, or move Atlas Gate",
        "does not create broad `allowed=true` behavior",
        "Only request key names are inspected; request values are not echoed",
    )
    for term in required_terms:
        assert term in text


def test_l6aj02_exact_preauthorization_fixture_is_narrow_and_non_executing() -> None:
    approval = build_l6aj02_harness_preauthorization_fixture()

    assert preauthorization_allows_l6aj02_denial_harness(approval)
    assert approval["repo"] == "jeremyknows/memory-seam"
    assert approval["rail_issue"] == 332
    assert approval["parent_issue"] == 6
    assert approval["denial_harness_preauthorization_comment"] == PREAUTH_COMMENT
    assert approval["max_denied_out_of_scope_requests"] == 1
    assert approval["supervised_real_read_execution_authorized"] is False
    assert approval["source_card_reads_authorized"] is False
    assert approval["callbacks_or_provider_routes_authorized"] is False
    assert approval["broad_allowed_true_authorized"] is False

    broadened = dict(approval, supervised_real_read_execution_authorized=True)
    assert not preauthorization_allows_l6aj02_denial_harness(broadened)
    stale = dict(approval, source_floor="stale-floor")
    assert not preauthorization_allows_l6aj02_denial_harness(stale)
    missing = dict(approval)
    missing.pop("denial_harness_preauthorization_comment")
    assert not preauthorization_allows_l6aj02_denial_harness(missing)


def test_l6aj02_denies_out_of_scope_request_before_source_access_with_zero_counters() -> None:
    approval = build_l6aj02_harness_preauthorization_fixture()
    receipt = deny_l6aj02_out_of_scope_supervised_real_read_request(
        {
            "raw_private_source_text": "do-not-echo-this-value",
            "runtime_registry": "do-not-touch",
            "provider_route": "do-not-call",
        },
        approval,
    )

    assert receipt["status"] == L6AJ_DENIED_STATUS
    assert receipt["evidence_class"] == L6AJ_DENIED_EVIDENCE_CLASS
    assert receipt["allowed"] is False
    assert receipt["supervised_real_read_count"] == 0
    assert receipt["denied_out_of_scope_request_count"] == 1
    assert receipt["denial_before_read"] is True
    assert receipt["source_access_attempted"] is False
    assert receipt["source_card_access_attempted"] is False
    assert receipt["live_adapter_invoked"] is False
    assert receipt["runtime_registry_consumed"] is False
    assert receipt["provider_route_invoked"] is False
    assert receipt["callback_invoked"] is False
    assert receipt["non_sensitive_value_metadata"]["request_values_echoed"] is False
    assert receipt["non_sensitive_value_metadata"]["out_of_scope_request_detected"] is True
    assert receipt["non_sensitive_value_metadata"]["preauthorization_fixture_matched"] is True
    assert all(value == 0 for value in receipt["guarded_counters"].values())
    assert all(value is False for value in receipt["held_surface_flags"].values())
    assert validate_l6aj02_report_safe_receipt(receipt) == []
    assert "do-not-echo-this-value" not in str(receipt)


def test_l6aj02_allowed_real_read_path_fails_closed_without_execution() -> None:
    approval = build_l6aj02_harness_preauthorization_fixture()
    receipt = attempt_l6aj02_allowed_supervised_real_read(approval)

    assert receipt["status"] == "HELD_SUPERVISED_REAL_READ_EXECUTION_NOT_AUTHORIZED"
    assert receipt["allowed"] is False
    assert receipt["supervised_real_read_count"] == 0
    assert receipt["denied_out_of_scope_request_count"] == 0
    assert receipt["denial_before_read"] is True
    assert receipt["source_access_attempted"] is False
    assert receipt["source_card_access_attempted"] is False
    assert receipt["live_adapter_invoked"] is False
    assert receipt["non_sensitive_value_metadata"]["execution_approval_present"] is False
    assert validate_l6aj02_report_safe_receipt(receipt) == []


def test_l6aj02_report_safe_validator_rejects_broad_allowed_nonzero_counters_and_unsafe_echo() -> None:
    receipt = deny_l6aj02_out_of_scope_supervised_real_read_request(
        {"source_card_read": "not echoed"},
        build_l6aj02_harness_preauthorization_fixture(),
    )
    broad = dict(receipt, allowed=True)
    assert "BROAD_ALLOWED_TRUE" in validate_l6aj02_report_safe_receipt(broad)

    nonzero = dict(receipt)
    nonzero["guarded_counters"] = dict(receipt["guarded_counters"], live_private_read_count=1)
    assert "NON_ZERO_GUARDED_COUNTER" in validate_l6aj02_report_safe_receipt(nonzero)

    unsafe = dict(receipt, non_sensitive_value_metadata={"unsafe": "oauth token"})
    assert "UNSAFE_ECHO_MARKER" in validate_l6aj02_report_safe_receipt(unsafe)


def test_l6aj02_doc_names_next_issue_and_residual_holds() -> None:
    text = normalized(DOC)
    required_terms = (
        "Next open rail issue after #332: #333 `L6AJ.03: report-safe source/query/output envelope for future supervised real read`.",
        "#333 may produce only a report-safe source/query/output envelope for future use",
        "supervised real-read execution remains held pending a future exact owner-created execution issue/comment binding source/query/output and operation count",
        "any live/private read",
        "raw private content/source text/approval prose",
        "credentials/auth/env/keychain/OAuth/auth-file reads",
        "source discovery/workspace/family scans/broad recall/index queries",
        "source-card reads",
        "Runtime Registry consumption",
        "real callbacks/provider routes",
        "persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
        "service/listener/startup/global activation",
        "cron/schedule changes",
        "publication/provider/prod/canary/Gate movement and Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
