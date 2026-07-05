from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ag03-default-off-integration-candidate-design-rollback-plan.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_DESIGN_PACKET_READY_RUNTIME_INTEGRATION_NOT_APPROVED"
RESULT = "PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_CANDIDATE_READY_RUNTIME_INTEGRATION_NOT_APPROVED"
RAIL_STARTING_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
SOURCE_FLOOR_ENTERING_SLICE = "1ff55c0056248162b7726f966f7a5a31e9a8241f"
PARENT_SUCCESSOR_COMMENT = "4653805965"
AUTH_COMMENT = "4653805892"
HISTORICAL_SMOKE_APPROVAL_COMMENT = "4653350823"
OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

RESIDUAL_HOLDS = (
    "runtime integration and adapter wiring until a separate exact owner-created future runtime-integration issue approval exists",
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval",
    "live/private reads and any source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks and provider routes",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and recursive cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ag03_design_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ag03-default-off-integration-candidate-design-rollback-plan.md" in docs_index
    assert "tests/test_l6ag03_default_off_integration_candidate_design_rollback_plan.py" in inventory
    assert "L6AG.03 default-off integration candidate design and rollback plan" in inventory
    assert STATUS in inventory


def test_l6ag03_records_status_source_floor_and_authorization():
    text = normalized(DOC)

    required_terms = (
        "# L6AG.03 default-off integration candidate design and rollback plan",
        f"Status: `{STATUS}`",
        "Rail issue: #303",
        "Parent issue: #6",
        "Blocked by: #301-#302 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound design authorization: #303 owner-created issue body and owner comment `{AUTH_COMMENT}`",
        "Prerequisite decision packet: [`l6ag02-runtime-integration-or-continued-hold-decision-packet.md`](l6ag02-runtime-integration-or-continued-hold-decision-packet.md)",
        f"Historical runtime-use smoke approval consumed by L6AF.02: #292 comment `{HISTORICAL_SMOKE_APPROVAL_COMMENT}`",
        "Decision vocabulary: `PASS_DESIGN_PACKET_READY`, `FIX_BEFORE_DESIGN_PACKET`, `HOLD_FOR_OWNER_DECISION`",
        "Decision: `PASS_DESIGN_PACKET_READY`",
        f"Result: `{RESULT}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_preserves_design_only_no_runtime_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests/design-only default-off runtime-integration candidate and rollback/stop-condition plan",
        "does not implement runtime integration",
        "wire adapters into runtime routes",
        "execute another adapter call or smoke",
        "perform live/private reads",
        "read source cards",
        "read credentials/auth/env/keychain/OAuth/auth-file material",
        "perform source discovery/workspace/family scans/broad recall/index queries",
        "consume Runtime Registry data",
        "invoke callbacks/provider routes",
        "persist or mutate state",
        "activate services/listeners/startup/global routes",
        "create or modify cron automation",
        "move provider/prod/canary/Gate or Atlas Gate state",
        "introduce broad `allowed=true` behavior",
        "`NOT APPROVAL`: This packet is not runtime-integration authority",
        "The historical #292 fixture-only adapter runtime-use smoke is evidence only; it is consumed and cannot authorize another call, smoke, or integration path",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_names_future_candidate_and_allowed_file_envelope():
    text = normalized(DOC)

    required_terms = (
        "`L6AG.N: default-off report-safe adapter runtime-integration slice`",
        f"`{OPERATION_CLASS}`",
        "`src/memory_seam/l6ag_default_off_runtime_integration.py` — new module containing a default-off runtime-integration shim",
        "`src/memory_seam/__init__.py` — optional export only if the future issue requires an importable package symbol",
        "`tests/test_l6ag_default_off_runtime_integration.py` — targeted unit contract",
        "`docs/l6ag-future-default-off-runtime-integration-receipt.md` — optional future receipt",
        "`docs/README.md` — discoverability row only",
        "`docs/contract-test-inventory.md` — contract inventory row only",
        "Explicitly excluded unless a separate later owner approval narrows and authorizes them",
        "examples, CLI entry points, release/package publishing files, cron/schedule files, service/listener/startup files, provider adapters, Runtime Registry code",
        "Atlas Gate files, and any Atlas Gate movement hooks",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_defines_future_approval_contract_and_denials():
    text = normalized(DOC)

    required_terms = (
        "explicit approval contract object or function parameter rather than reading credentials, environment values, keychain material, OAuth material, auth files, GitHub comments, issue text, Runtime Registry state",
        "repository: `jeremyknows/memory-seam`",
        "actor association: `OWNER`",
        f"operation class: `{OPERATION_CLASS}`",
        "max operation count: exactly one integration slice and zero extra runtime-use smokes unless separately and exactly approved",
        "Deny before any adapter action, provider route, Runtime Registry read, callback, persistence, activation, live/private read, source-card read, source discovery, cron change, Gate movement, or broad allow result",
        "approval is missing, stale, copied from prior issue, expired, broadened, mismatched to repo/issue/source-floor/operation/files, non-owner",
        "permits another smoke, permits any held surface, requests callbacks, requests Runtime Registry, requests persistence/mutation",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_fixture_live_input_boundary_and_report_safe_output_contract():
    text = normalized(DOC)

    required_terms = (
        "Future implementation inputs should be limited to committed fixture/report-safe values",
        "public descriptor reference string",
        "public adapter value reference string or already-safe value label",
        "integer max-operation and guarded held-surface counters",
        "Live/private inputs remain held",
        "The future integration output should contain only",
        "`DENIED_DEFAULT_OFF`, `PASS_DEFAULT_OFF_RUNTIME_INTEGRATION_FIXTURE_ONLY`, or `HOLD_FOR_OWNER_DECISION`",
        "integer counters for `integration_slice_count`, `runtime_use_smoke_count`, provider/backend/source-stat/source-read/callback/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge/service/cron/publication/Gate families",
        "The future output must never include raw private content, raw source text, raw approval prose",
        "broad `allowed=true` as an authorization result",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_future_approval_wording_is_inert_documentation():
    text = normalized(DOC)

    required_terms = (
        "A future runtime-integration issue should use this exact approval sentence shape",
        f"{OPERATION_CLASS}",
        "Scope is limited to source floor <source_floor_after_l6ag03_and_prerequisites>, repository jeremyknows/memory-seam, and these repo-relative files only: <exact_file_list>",
        "max operation count",
        "No additional runtime-use smoke or adapter call beyond what this exact issue separately names",
        "No live/private reads, source-card reads, raw private content, raw source text, raw approval prose",
        "This wording is inert documentation in #303",
        "L6AG.03 itself is not approval",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_future_tests_rollback_and_stop_conditions():
    text = normalized(DOC)

    required_terms = (
        "A future implementation issue must add `tests/test_l6ag_default_off_runtime_integration.py`",
        "missing approval denies with `DENIED_DEFAULT_OFF` and all guarded counters zero",
        "stale source floor, stale issue number, copied prior rail wording, broadened file envelope, expired UTC window, mismatched operation class, mismatched repository, non-owner actor, max-operation count greater than one",
        "exact valid fixture-only approval returns report-safe metadata and labels only, with `integration_slice_count=1` and `runtime_use_smoke_count=0`",
        "all provider/backend/source-stat/source-read/callback/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge/service/cron/publication/Gate counters remain zero",
        "`live_adapter_invoked=false`, `callback_invoked=false`, `registry_consumed=false`, `persistence_attempted=false`, `activation_attempted=false`, and `broad_allowed_attempted=false`",
        "python -m pytest tests/test_l6ag_default_off_runtime_integration.py -q",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
        "Rollback must be limited to the future runtime-integration PR",
        "Rollback execution itself remains held in L6AG.03",
        "Stop and hold for owner decision",
        "cannot remain fixture-only, report-safe, default-off, denial-before-callback, and no-live by default",
    )
    for term in required_terms:
        assert term in text


def test_l6ag03_residual_holds_and_next_issue():
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #303: #304 `L6AG.04: no-live trust-boundary review for post-smoke integration rail`" in text
    assert "#304 should review #301-#303 no-live artifacts" in text
    assert "confirm #292 approval remains consumed and not reusable" in text

    unsafe_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
