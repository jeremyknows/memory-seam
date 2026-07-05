from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ag02-runtime-integration-or-continued-hold-decision-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_INTEGRATION_PACKET_READY_RUNTIME_INTEGRATION_NOT_APPROVED"
RAIL_STARTING_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
SOURCE_FLOOR_ENTERING_SLICE = "49688202b1fdde0231f417ca3077b544e20781a6"
PARENT_SUCCESSOR_COMMENT = "4653805965"
HISTORICAL_SMOKE_APPROVAL_COMMENT = "4653350823"
FUTURE_OPERATION_CLASS = "L6AG_DEFAULT_OFF_REPORT_SAFE_ADAPTER_RUNTIME_INTEGRATION_SLICE"

NO_APPROVAL_BY_INERTIA_ANCHORS = (
    "#292 approval comment `4653350823` after its one fixture-only runtime-use smoke was consumed",
    "#295 source-floor reconciliation, PR #300 merge, or source floor `b7fe89f752372de4f42d5f7e1084acad99c5ebf0`",
    "parent successor comment `4653805965`",
    "#301 inventory authorization comment `4653805822`",
    "#301 closeout, PR #306 merge, or source floor `49688202b1fdde0231f417ca3077b544e20781a6`",
    "#302 issue creation, labels, title, closure, this PASS decision, copied wording, stale comments, rail continuity, or future source-floor advancement",
)

RESIDUAL_HOLDS = (
    "runtime integration and adapter wiring until a separate exact owner-created future issue approval exists",
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval",
    "live/private reads and any source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
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


def test_l6ag02_decision_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ag02-runtime-integration-or-continued-hold-decision-packet.md" in docs_index
    assert "tests/test_l6ag02_runtime_integration_or_continued_hold_decision_packet.py" in inventory
    assert "L6AG.02 runtime-integration-or-continued-hold decision packet" in inventory
    assert STATUS in inventory


def test_l6ag02_records_status_source_floor_and_prerequisites():
    text = normalized(DOC)

    required_terms = (
        "# L6AG.02 runtime-integration-or-continued-hold decision packet",
        f"Status: `{STATUS}`",
        "Rail issue: #302",
        "Parent issue: #6",
        "Blocked by: #301 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        "Prerequisite inventory: [`l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md`](l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md)",
        f"Historical runtime-use smoke approval consumed by L6AF.02: #292 comment `{HISTORICAL_SMOKE_APPROVAL_COMMENT}`",
        "Decision vocabulary: `PASS_INTEGRATION_PACKET_READY`, `FIX_BEFORE_INTEGRATION_PACKET`, `HOLD_FOR_OWNER_DECISION`",
        "Decision: `PASS_INTEGRATION_PACKET_READY`",
    )
    for term in required_terms:
        assert term in text


def test_l6ag02_preserves_docs_tests_public_metadata_only_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests/fixtures/public-metadata-only decision packet",
        "does not implement runtime integration",
        "execute another adapter call",
        "run another smoke",
        "perform live/private reads",
        "read source cards",
        "inspect raw private content/source text/approval prose",
        "read credentials/auth/env/keychain/OAuth/auth-file material",
        "consume Runtime Registry data",
        "invoke callbacks/provider routes",
        "persist or mutate state",
        "activate services/listeners/startup/global routes",
        "create or modify cron automation",
        "move provider/prod/canary/Gate or Atlas Gate state",
        "introduce broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ag02_decision_basis_uses_consumed_smoke_as_history_only():
    text = normalized(DOC)

    required_terms = (
        "L6AG.01 (#301 / PR #306 / source floor `49688202b1fdde0231f417ca3077b544e20781a6`)",
        "`PASS_INVENTORY_COMPLETE_RUNTIME_INTEGRATION_STILL_HELD`",
        "L6AF.02 (#292 / PR #297 / source floor `d995a5ac2c9dca2e571d8eb5fdb1009482031f06`)",
        "consumed exactly one approved local fixture-only adapter import/call",
        "operation class `L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE`",
        "L6AF.03-L6AF.05 (#293-#295 / PR #298-#300)",
        "without another runtime-use smoke or adapter call",
        "did not authorize runtime integration, another smoke, live/private reads, Runtime Registry consumption, callbacks",
    )
    for term in required_terms:
        assert term in text


def test_l6ag02_records_not_approval_and_no_approval_by_inertia():
    text = normalized(DOC)

    assert "Result: `PASS_INTEGRATION_PACKET_READY` for a future exact issue-bound runtime-integration candidate path" in text
    assert "`NOT APPROVAL`: This result is not runtime-integration approval" in text
    assert "not permission for another adapter call or smoke" in text
    assert "not Runtime Registry/callback/provider-route approval" in text

    for anchor in NO_APPROVAL_BY_INERTIA_ANCHORS:
        assert anchor in text

    assert "None of the following can authorize runtime integration, another adapter call, another smoke" in text
    assert "broad `allowed=true` behavior" in text


def test_l6ag02_names_future_operation_class_without_approving_it():
    text = normalized(DOC)

    required_terms = (
        "Future runtime-integration issue title shape:",
        "`L6AG.N: default-off report-safe adapter runtime-integration slice`",
        "Candidate future operation class:",
        f"`{FUTURE_OPERATION_CLASS}`",
        "This operation class is named only for a later separate issue-bound owner approval packet",
        "It is not approved by L6AG.02",
        "max one implementation slice and zero extra runtime-use smokes unless separately approved",
        "denial-before-callback/provider-route/Runtime-Registry/persistence/activation behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ag02_defines_candidate_file_envelope_tests_and_stop_conditions():
    text = normalized(DOC)

    required_terms = (
        "`src/memory_seam/l6ag_default_off_runtime_integration.py`",
        "`tests/test_l6ag_default_off_runtime_integration.py`",
        "`docs/l6ag03-default-off-integration-candidate-design-rollback-plan.md`",
        "A later runtime-integration issue should not edit examples, CLIs, provider adapters, Runtime Registry internals",
        "python -m pytest tests/test_l6ag_default_off_runtime_integration.py -q",
        "missing, stale, copied, broadened, mismatched, expired, non-owner",
        "all guarded source/provider/callback/registry/persistence/mutation/write/custody/delete/reindex/rollback/cache-purge/service/cron/publication/Gate counters remain zero",
        "Stop immediately and hold for owner decision",
        "inability to keep the future integration default-off, report-safe, denial-before-callback, and no-live by default",
    )
    for term in required_terms:
        assert term in text


def test_l6ag02_carries_residual_holds_and_next_issue():
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #302: #303 `L6AG.03: default-off integration candidate design and rollback plan`" in text
    assert "preauthorization comment `4653805892`" in text
    assert "must not implement runtime integration, execute another adapter call or smoke" in text

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
