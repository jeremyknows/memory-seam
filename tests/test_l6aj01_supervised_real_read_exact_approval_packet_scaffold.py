from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6aj01-supervised-real-read-exact-approval-packet-scaffold.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION"
RAIL_STARTING_SOURCE_FLOOR = "e7b3e67c438891be00f4001d9cfff72026ebe4d3"
PARENT_SUCCESSOR_PREP_COMMENT = "4654676210"
SCAFFOLD_AUTHORIZATION_COMMENT = "4654676115"
DENIAL_HARNESS_PREAUTH_COMMENT = "4654676162"
OPERATION_CLASS = "L6AJ_SUPERVISED_REAL_READ_EXACT_APPROVAL_PREP"
NEXT_FRONTIER = "DENIAL_BEFORE_READ_FIXTURE_HARNESS_ONLY_FOR_ISSUE_332"

APPROVAL_FIELDS = (
    "`repo`",
    "`parent_issue`",
    "`execution_issue`",
    "`owner_actor_association`",
    "`source_identifier_class`",
    "`query_or_prompt_constraints`",
    "`output_constraints`",
    "`max_operation_count`",
    "`evidence_class`",
    "`approval_comment_id`",
    "`expiry_window`",
    "`denial_before_read_requirement`",
    "`rollback_stop_conditions`",
    "`residual_holds`",
)

HELD_COUNTER_TERMS = (
    "raw_private_content_count=0",
    "raw_source_text_count=0",
    "raw_approval_prose_count=0",
    "credential_auth_read_count=0",
    "source_discovery_count=0",
    "runtime_registry_consumed=false",
    "callback_invoked=false",
    "persistence_or_mutation_attempted=false",
    "activation_attempted=false",
    "write_attempted=false",
    "publication_or_gate_movement_attempted=false",
    "broad_allowed_attempted=false",
    "all non-approved held-surface counters zero",
)

RESIDUAL_HOLDS = (
    "supervised real-read execution until a future exact owner-created execution issue/comment binds source/query/output and operation count",
    "#332 denial-before-read harness execution until the next tick selects #332 and revalidates live issue/approval/source-floor state",
    "any live/private read",
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials/auth/env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "source-card reads",
    "Runtime Registry consumption",
    "real callbacks/provider routes",
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


def test_l6aj01_packet_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6aj01-supervised-real-read-exact-approval-packet-scaffold.md" in docs_index
    assert "tests/test_l6aj01_supervised_real_read_exact_approval_packet_scaffold.py" in inventory
    assert "L6AJ.01 supervised real-read exact approval packet scaffold" in inventory
    assert STATUS in inventory


def test_l6aj01_records_status_source_floor_and_exact_binding() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AJ.01 supervised real-read exact approval packet scaffold",
        f"Status: `{STATUS}`",
        "Rail issue: #331",
        "Parent issue: #6",
        "Depends on: L6AI #321-#325 closed/PASS",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Parent L6AJ successor prep comment: `{PARENT_SUCCESSOR_PREP_COMMENT}`",
        f"Issue-bound scaffold authorization: #331 comment `{SCAFFOLD_AUTHORIZATION_COMMENT}`",
        f"Future denial harness preauthorization reference: #332 comment `{DENIAL_HARNESS_PREAUTH_COMMENT}`",
        f"Operation class candidate: `{OPERATION_CLASS}`",
        "Exact future execution issue: none present; execution remains held",
        "Verdict vocabulary: `PASS_APPROVAL_PACKET_SCAFFOLD_READY_NO_EXECUTION`, `FIX_BEFORE_DENIAL_HARNESS`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6aj01_preserves_non_execution_public_metadata_boundary() -> None:
    text = normalized(DOC)

    required_terms = (
        "docs/tests/fixtures/public-metadata-only",
        "does not execute a supervised real read",
        "perform a live/private read",
        "read raw private content",
        "read raw source text",
        "read raw approval prose",
        "read a source card",
        "perform source discovery",
        "run workspace/family scans",
        "run broad recall or index queries",
        "read credentials/auth/env/keychain/OAuth/auth-file material",
        "consume Runtime Registry data",
        "invoke real callbacks/provider routes",
        "persist or mutate state",
        "write/delete/reindex/cache-purge/rollback execute",
        "activate service/listener/startup/global paths",
        "change cron automation",
        "move provider/prod/canary/Gate or Atlas Gate surfaces",
        "create broad `allowed=true` behavior",
        "repo name, source floor, parent issue, rail issue numbers, public comment IDs, operation-class labels, evidence classes, status labels, booleans, zero held-surface counters, issue/PR refs, and repo-relative artifact paths",
    )
    for term in required_terms:
        assert term in text


def test_l6aj01_defines_exact_future_approval_fields_without_approval() -> None:
    text = normalized(DOC)

    assert "No executable approval exists in #331" in text
    assert "A later owner-created issue/comment would have to bind all fields below before any supervised real read can execute" in text
    for field in APPROVAL_FIELDS:
        assert field in text

    required_terms = (
        "exactly `jeremyknows/memory-seam`",
        "one exact future owner-created issue number, not #331",
        "OWNER only",
        "one explicit report-safe source identifier class, with executable refs supplied by that future issue only",
        "report-safe intent label and output constraints only; raw prompt/query text remains held",
        "exactly `1` allowed supervised real read and exactly `1` denied out-of-scope request before read, if separately approved",
        "fresh exact owner comment ID on the future execution issue",
        "stale, missing, copied, or expired approval denies before read",
        "The future approval must be issue-bound, fresh, non-copied, non-stale, owner-authored, max-one-operation, and narrow",
        "Merge events, labels, issue closure, source-floor advancement, parent comments, copied wording, unrelated comments, or this scaffold PASS must not authorize execution",
    )
    for term in required_terms:
        assert term in text


def test_l6aj01_requires_report_safe_receipts_and_zero_held_surfaces() -> None:
    text = normalized(DOC)

    required_terms = (
        "`status=\"PASS_SUPERVISED_REAL_READ_REPORT_SAFE_ONE_OPERATION\"`",
        "`evidence_class=\"SUPERVISED_REAL_READ_REPORT_SAFE_ONE_OPERATION\"`",
        "`allowed=\"EXACT_SUPERVISED_REAL_READ_ONE_OPERATION\"`, never boolean `allowed=true`",
        "`supervised_real_read_count=1`",
        "`denied_out_of_scope_request_count=0`",
        "`denial_before_read=false`",
        "`status=\"DENIED_BEFORE_READ_OUT_OF_SCOPE_SUPERVISED_REAL_READ_REQUEST\"`",
        "`operation_class` equal to the future approved operation class or `UNAPPROVED_SUPERVISED_REAL_READ_REQUEST`",
        "`evidence_class=\"SUPERVISED_REAL_READ_DENIAL_BEFORE_READ\"`",
        "`allowed=false`",
        "`supervised_real_read_count=0`",
        "`denied_out_of_scope_request_count=1`",
        "`denial_before_read=true`",
        "The denial receipt must not echo unsafe request details",
    )
    for term in required_terms:
        assert term in text

    for counter_term in HELD_COUNTER_TERMS:
        assert counter_term in text


def test_l6aj01_denial_before_read_stop_and_rollback_conditions() -> None:
    text = normalized(DOC)

    required_terms = (
        "deny before source access",
        "missing exact approval fields",
        "raw private content",
        "raw source text",
        "raw approval prose",
        "credentials/auth/env/keychain/OAuth/auth-file reads",
        "source discovery",
        "workspace scans",
        "family scans",
        "broad recall",
        "index queries",
        "source-card reads outside exact future approval",
        "Runtime Registry consumption",
        "real callbacks/provider routes",
        "persistence/mutation/write/delete/reindex/cache-purge/rollback execution",
        "service/global activation",
        "cron changes",
        "publication/provider/prod/canary/Gate/Atlas Gate movement",
        "more than the exact approved operation count",
        "Denial-before-read must occur before source-card access, provider/backend/source-stat/source-read callbacks, live adapter invocation, Runtime Registry lookup, persistence, mutation, cache mutation, rollback execution, activation, publication, or Gate movement",
        "Rollback is limited to stopping before the held surface is touched and reporting the safe HOLD",
        "#331 authorizes no rollback execution, cache purge, persistence write, mutation, or cleanup callback",
    )
    for term in required_terms:
        assert term in text


def test_l6aj01_verification_gate_residual_holds_and_next_issue() -> None:
    text = normalized(DOC)

    verification_terms = (
        "python -m pytest -q tests/test_l6aj01_supervised_real_read_exact_approval_packet_scaffold.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    )
    for term in verification_terms:
        assert term in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #331: #332 `L6AJ.02: denial-before-read fixture harness for supervised real-read prep`" in text
    assert "#332 may produce only a no-live fixture-only denial-before-read harness with inert spies/counters and no source access" in text
    assert "#332 must not execute a supervised real read or invoke real callbacks/provider routes" in text

    lowered = text.lower()
    for marker in UNSAFE_MARKERS:
        assert marker not in lowered
