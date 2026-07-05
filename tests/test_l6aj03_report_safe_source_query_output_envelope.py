from __future__ import annotations

from pathlib import Path

from memory_seam.l6aj_report_safe_envelope import (
    L6AJ03_EVIDENCE_CLASS,
    L6AJ03_NEXT_FRONTIER,
    L6AJ03_OPERATION_CLASS,
    L6AJ03_RAIL_STARTING_SOURCE_FLOOR,
    L6AJ03_SOURCE_FLOOR_ENTERING_SLICE,
    L6AJ03_STATUS,
    build_l6aj03_output_contract,
    build_l6aj03_report_safe_envelope_fixture,
    build_l6aj03_synthetic_query_binding,
    build_l6aj03_synthetic_source_binding,
    validate_l6aj03_source_query_output_envelope,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aj03-report-safe-source-query-output-envelope.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PARENT_SUCCESSOR_PREP_COMMENT = "4654676210"
SCAFFOLD_AUTH_COMMENT = "4654676115"
DENIAL_HARNESS_PREAUTH_COMMENT = "4654676162"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6aj03_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aj03-report-safe-source-query-output-envelope.md" in docs_index
    assert "tests/test_l6aj03_report_safe_source_query_output_envelope.py" in inventory
    assert "L6AJ.03 report-safe source/query/output envelope" in inventory
    assert L6AJ03_STATUS in inventory


def test_l6aj03_doc_records_issue_floor_dependencies_and_verdict() -> None:
    text = normalized(DOC)
    required_terms = (
        "# L6AJ.03 report-safe source/query/output envelope for future supervised real read",
        f"Status: `{L6AJ03_STATUS}`",
        "Rail issue: #333",
        "Parent issue: #6",
        "Depends on: #331-#332 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{L6AJ03_RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{L6AJ03_SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent L6AJ successor prep comment: `{PARENT_SUCCESSOR_PREP_COMMENT}`",
        f"Prior scaffold authorization reference: #331 comment `{SCAFFOLD_AUTH_COMMENT}`",
        f"Prior denial harness preauthorization reference: #332 comment `{DENIAL_HARNESS_PREAUTH_COMMENT}`",
        f"Operation class: `{L6AJ03_OPERATION_CLASS}`",
        f"Evidence class: `{L6AJ03_EVIDENCE_CLASS}`",
        "Verdict vocabulary: `PASS_REPORT_SAFE_SOURCE_QUERY_OUTPUT_ENVELOPE_READY_NO_EXECUTION`, `FIX_BEFORE_TRUST_BOUNDARY_REVIEW`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{L6AJ03_STATUS}`",
        "Next open rail issue after #333: #334 `L6AJ.04: supervised real-read prep trust-boundary and stop-condition review`.",
    )
    for term in required_terms:
        assert term in text


def test_l6aj03_doc_preserves_no_live_no_source_boundary() -> None:
    text = normalized(DOC)
    required_terms = (
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
    )
    for term in required_terms:
        assert term in text


def test_l6aj03_fixture_uses_synthetic_public_metadata_bindings_only() -> None:
    source = build_l6aj03_synthetic_source_binding()
    query = build_l6aj03_synthetic_query_binding()

    assert source["source_binding_ref"] == "synthetic-public-metadata-source-binding:l6aj03"
    assert source["source_binding_kind"] == "synthetic_fixture_reference"
    assert source["source_access_mode"] == "no_live_no_source_card_no_discovery"
    assert source["fixture_only"] is True
    assert query["query_binding_ref"] == "synthetic-public-metadata-query-binding:l6aj03"
    assert query["max_query_count"] == 1
    assert query["denied_out_of_scope_request_count"] == 1
    assert query["fixture_only"] is True

    combined = str(source) + str(query)
    assert "source://" not in combined
    assert "platform-raw-id" not in combined
    assert "raw query" not in combined.lower()


def test_l6aj03_output_contract_names_allowed_classes_and_forbidden_raw_fields() -> None:
    contract = build_l6aj03_output_contract()

    assert contract["report_safe_only"] is True
    assert contract["unsafe_echo_rejected"] is True
    assert contract["fixture_only"] is True
    assert "raw_private_content" in contract["forbidden_output_fields"]
    assert "raw_source_text" in contract["forbidden_output_fields"]
    assert "credential_value" in contract["forbidden_output_fields"]
    assert "runtime_registry_payload" in contract["forbidden_output_fields"]
    assert "callback_payload" in contract["forbidden_output_fields"]
    assert "allowed_true_broad_result" in contract["forbidden_output_fields"]
    assert "zero_guarded_counter" in contract["safe_value_classes"]
    assert "synthetic_descriptor_or_source_card_ref" in contract["safe_value_classes"]


def test_l6aj03_envelope_fixture_is_held_no_execution_and_valid_report_safe() -> None:
    envelope = build_l6aj03_report_safe_envelope_fixture()

    assert envelope["status"] == L6AJ03_STATUS
    assert envelope["repo"] == "jeremyknows/memory-seam"
    assert envelope["parent_issue"] == 6
    assert envelope["rail_issue"] == 333
    assert envelope["operation_class"] == L6AJ03_OPERATION_CLASS
    assert envelope["allowed"] is False
    assert envelope["supervised_real_read_execution_authorized"] is False
    assert envelope["supervised_real_read_count"] == 0
    assert envelope["denied_out_of_scope_request_count"] == 0
    assert envelope["denial_before_read_required"] is True
    assert all(value == 0 for value in envelope["guarded_counters"].values())
    assert all(value is False for value in envelope["held_surface_flags"].values())
    assert envelope["next_frontier"] == L6AJ03_NEXT_FRONTIER
    assert validate_l6aj03_source_query_output_envelope(envelope) == []


def test_l6aj03_validator_rejects_unsafe_fields_allowed_true_nonzero_counter_and_echo() -> None:
    envelope = build_l6aj03_report_safe_envelope_fixture()

    extra = dict(envelope, raw_private_content="redacted-but-still-forbidden")
    assert any(error.startswith("UNSAFE_EXTRA_FIELDS") for error in validate_l6aj03_source_query_output_envelope(extra))

    broad = dict(envelope, allowed=True)
    assert "BROAD_ALLOWED_TRUE" in validate_l6aj03_source_query_output_envelope(broad)

    executing = dict(envelope, supervised_real_read_execution_authorized=True)
    assert "EXECUTION_AUTHORIZED_IN_PREP_ENVELOPE" in validate_l6aj03_source_query_output_envelope(executing)

    nonzero = dict(envelope)
    nonzero["guarded_counters"] = dict(envelope["guarded_counters"], live_private_read_count=1)
    assert "NON_ZERO_GUARDED_COUNTER" in validate_l6aj03_source_query_output_envelope(nonzero)

    unsafe = dict(envelope)
    unsafe["output_contract"] = dict(envelope["output_contract"], required_redaction_posture="oauth token")
    assert "UNSAFE_ECHO_MARKER" in validate_l6aj03_source_query_output_envelope(unsafe)


def test_l6aj03_doc_names_future_approval_binding_and_residual_holds() -> None:
    text = normalized(DOC)
    required_terms = (
        "A later owner-created execution issue/comment must separately bind all of the following before any supervised real read can be attempted",
        "one exact source binding ref plus one exact source descriptor/source-card ref or equivalent future source ref",
        "one exact query binding ref, intent label, and output purpose",
        "max one supervised real-read operation",
        "exactly one denied out-of-scope request before source access",
        "Absent any one of these bindings, the future path must deny before read.",
        "#334 may review #331-#333 prep artifacts only",
        "supervised real-read execution remains held pending a future exact owner-created execution issue/comment binding source/query/output and operation count",
        "Residual holds: supervised real-read execution",
        "credentials/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry consumption",
        "real callbacks/provider routes",
        "publication/provider/prod/canary/Gate movement and Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
