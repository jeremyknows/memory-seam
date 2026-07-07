from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6af01-default-off-adapter-runtime-use-approval-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_RUNTIME_USE_SMOKE_PACKET_READY_FIXTURE_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "f321708b1e8f708345194fc34c0d0968c620c03e"
PARENT_SUCCESSOR_COMMENT = "4653350950"
PREP_AUTHORIZATION_COMMENT = "4653350694"
RUNTIME_USE_APPROVAL_COMMENT = "4653350823"
APPROVAL_EXPIRY = "2026-06-09T08:41:15Z"
OPERATION_CLASS = "L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE"
TARGET_MODULE = "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6af01_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6af01-default-off-adapter-runtime-use-approval-packet.md" in docs_index
    assert "tests/test_l6af01_default_off_adapter_runtime_use_approval_packet.py" in inventory
    assert "L6AF.01 default-off adapter runtime-use approval packet" in inventory
    assert STATUS in inventory


def test_l6af01_records_status_source_floor_and_exact_binding():
    text = normalized(DOC)

    required_terms = (
        "# L6AF.01 default-off adapter runtime-use approval packet",
        f"Status: `{STATUS}`",
        "Rail issue: #291",
        "Parent issue: #6",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound prep authorization: #291 comment `{PREP_AUTHORIZATION_COMMENT}`",
        f"Future runtime-use smoke approval reference: #292 comment `{RUNTIME_USE_APPROVAL_COMMENT}`",
        f"Approval expiry ceiling: `{APPROVAL_EXPIRY}`",
        f"Operation class: `{OPERATION_CLASS}`",
        f"Target adapter module: `{TARGET_MODULE}`",
        "Exact future test/smoke issue: #292",
    )
    for term in required_terms:
        assert term in text


def test_l6af01_preserves_docs_tests_fixtures_only_non_execution_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests/fixtures-only approval packet",
        "It does not run the adapter",
        "approve any live/private read",
        "consume Runtime Registry data",
        "start services",
        "invoke callbacks",
        "persist or mutate state",
        "move provider/prod/canary surfaces",
        "move Atlas Gate",
        "broad `allowed=true` behavior",
        "`NOT EXECUTED HERE`: #291 remains docs/tests/fixtures-only",
        "does not reuse any historical source-card read authority",
    )
    for term in required_terms:
        assert term in text


def test_l6af01_names_exact_292_smoke_envelope():
    text = normalized(DOC)

    required_terms = (
        "#292 may execute at most one local fixture-only adapter runtime-use smoke",
        "repository: `jeremyknows/memory-seam`",
        "issue: #292 only",
        f"operation class: `{OPERATION_CLASS}`",
        f"module under test: `{TARGET_MODULE}`",
        f"approval reference: #292 comment `{RUNTIME_USE_APPROVAL_COMMENT}`",
        f"expiry ceiling: `{APPROVAL_EXPIRY}`",
        "max runtime-use smoke count: `1`",
        "inputs: committed fixture/report-safe metadata only",
        "outputs: report-safe metadata, booleans, status strings, counters, fixture refs, usefulness labels, and artifact paths only",
        "one narrow fixture-only adapter value label without broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6af01_requires_denial_variants_and_zero_held_surface_counters():
    text = normalized(DOC)

    required_terms = (
        "missing, stale, mismatched, broadened, expired, non-owner, callback-requesting, activation-requesting, publication-requesting, Runtime-Registry-consuming, provider/prod/canary/Gate-moving, persistence-requesting, mutation-requesting, or broad `allowed=true` variants deny before any held surface",
        "live/private read, additional source-card read, credential/auth/env/keychain/OAuth/auth-file read, source discovery, workspace/family scan, broad recall, index query, Runtime Registry, callback, provider/backend/source-stat/source-read, persistence, mutation, write, custody, delete, reindex, rollback, cache-purge, service activation, cron, publication, visibility, provider/prod/canary, Atlas Gate, and broad-allow counters remain zero",
    )
    for term in required_terms:
        assert term in text


def test_l6af01_stop_conditions_and_verification_gate():
    text = normalized(DOC)

    required_terms = (
        "approval missing, stale, expired, not owner-bound, issue-mismatched, operation-class-mismatched, or broader than the packet envelope",
        "any request for live/private reads, raw private content, raw source text, raw approval prose, additional source-card reads, or source-card refresh",
        "any credential/auth/env/keychain/OAuth/auth-file access",
        "source discovery, workspace scan, family scan, broad recall, index query, or Runtime Registry consumption",
        "provider/backend/source-stat/source-read callbacks or callback wiring",
        "persistence, mutation, write, custody, delete, reindex, rollback execution, cache purge, or audit/custody storage",
        "service/listener/startup/global activation or cron changes",
        "publication, visibility change, provider/prod/canary movement, Atlas Gate movement, or broad `allowed=true` behavior",
        "docs/l6af02-fixture-only-default-off-adapter-runtime-use-smoke.md",
        "tests/test_l6af02_fixture_only_default_off_adapter_runtime_use_smoke.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    )
    for term in required_terms:
        assert term in text


def test_l6af01_residual_holds_and_next_issue():
    text = normalized(DOC)

    residual_holds = (
        "#292 runtime-use smoke until the next tick selects #292 and revalidates live issue/approval/source-floor state",
        "any runtime-use smoke beyond exactly one local fixture-only adapter call under #292",
        "all live/private reads and any source-card read",
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

    assert "Next open rail issue after #291: #292 `L6AF.02: execute one fixture-only default-off adapter runtime-use smoke`" in text
    assert "may perform exactly one local fixture-only runtime-use smoke by importing/calling the committed adapter locally through tests or a committed proof harness" in text

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
