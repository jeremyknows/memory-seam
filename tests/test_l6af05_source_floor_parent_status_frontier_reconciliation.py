from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6af05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_FIXTURE_ONLY_RUNTIME_USE_SMOKE_CONSUMED"
RAIL_STARTING_SOURCE_FLOOR = "f321708b1e8f708345194fc34c0d0968c620c03e"
SOURCE_FLOOR_ENTERING_SLICE = "02dcc439d32fdd464a84a919bfab52269d9afe21"
PARENT_SUCCESSOR_COMMENT = "4653350950"
PREP_AUTH_COMMENT = "4653350694"
RUNTIME_USE_APPROVAL_COMMENT = "4653350823"
APPROVAL_EXPIRY = "2026-06-09T08:41:15Z"
OPERATION_CLASS = "L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE"
NEXT_FRONTIER = "OWNER_DECISION_FOR_POST_SMOKE_RUNTIME_INTEGRATION_OR_CONTINUED_HOLD"

L6AF_ANCHORS = (
    "L6AF.01 (#291 / PR #296 / source floor `daf68ecd9e7cc55690bc70fdbbaf2d3707abd1f6`)",
    "L6AF.02 (#292 / PR #297 / source floor `d995a5ac2c9dca2e571d8eb5fdb1009482031f06`)",
    "L6AF.03 (#293 / PR #298 / source floor `354dbe6baba18aaff9a6b609acd8f316d93c81d0`)",
    "L6AF.04 (#294 / PR #299 / source floor `02dcc439d32fdd464a84a919bfab52269d9afe21`)",
    "L6AF.05 (#295 / this packet)",
)

RESIDUAL_HOLDS = (
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval remains held",
    "live/private reads and any source-card reads remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "provider/backend/source-stat/source-read callbacks remain held",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement remain held",
    "broad `allowed=true` behavior remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6af05_reconciliation_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6af05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6af05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AF.05 source-floor parent status frontier reconciliation" in inventory
    assert STATUS in inventory


def test_l6af05_records_status_source_floor_parent_and_outcome() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AF.05 source-floor anchor, parent status, and next frontier reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #295",
        "Parent issue: #6",
        "Blocked by: #291-#294 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound prep authorization: #291 comment `{PREP_AUTH_COMMENT}`",
        f"Consumed runtime-use smoke approval: #292 comment `{RUNTIME_USE_APPROVAL_COMMENT}`",
        f"Runtime-use approval expiry ceiling: `{APPROVAL_EXPIRY}`",
        f"Operation class consumed by #292: `{OPERATION_CLASS}`",
        "Reconciliation vocabulary: `RAIL_PASS_RECONCILED`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        "Reconciliation: `RAIL_PASS_RECONCILED`",
        "Rail outcome: `FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE_CONSUMED_RUNTIME_HELD`",
        "Parent #6 remains `OPEN` while this packet is prepared",
    )
    for term in required_terms:
        assert term in text


def test_l6af05_lists_all_l6af_prs_source_floors_and_scope() -> None:
    text = normalized(DOC)

    for anchor in L6AF_ANCHORS:
        assert anchor in text

    required_terms = (
        "default-off adapter runtime-use approval packet",
        "fixture-only default-off adapter runtime-use smoke",
        "runtime-use smoke value receipt and held-surface map",
        "no-live trust-boundary review for runtime-use smoke rail",
        "source-floor anchor, parent status, residual holds, and next-frontier reconciliation",
        "creates no successor issues, no successor cron jobs, no runtime activation, no additional smoke, and no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6af05_confirms_one_consumed_smoke_without_runtime_expansion() -> None:
    text = normalized(DOC)

    required_terms = (
        "Finding: `PASS_TO_PARENT_RECEIPT_WITH_ONE_FIXTURE_ONLY_RUNTIME_USE_SMOKE_CONSUMED_RUNTIME_HELD`",
        "#291-#294 are closed/PASS and #295 can close after this packet merges and verification passes",
        "completed the exact fixture-only default-off adapter runtime-use smoke rail",
        "did execute exactly one approved local fixture-only adapter import/call in #292",
        "committed report-safe metadata and the committed adapter module",
        "did not perform live/private reads",
        "did not read source cards",
        "did not call providers/backends/source-stat/source-read callbacks",
        "did not consume Runtime Registry data",
        "did not persist/mutate/cache/write/delete/reindex/rollback",
        "did not activate services/listeners/startup/global routes",
        "did not create or modify cron automation",
        "did not authorize a broad allowed path",
    )
    for term in required_terms:
        assert term in text


def test_l6af05_preserves_consumed_runtime_use_authority_and_report_safety() -> None:
    text = normalized(DOC)

    required_terms = (
        "Runtime-use custody conclusion",
        "The #292 approval is fully consumed historical authority for one local fixture-only runtime-use smoke only",
        "not reusable by #293, #294, this #295 reconciliation, parent #6 status comments",
        "future runtime use, live/private reads, service activation",
        "Atlas Gate movement, or broad `allowed=true` behavior",
        "Reportable evidence from the consumed smoke is limited to repo-relative artifact paths",
        "public issue/PR numbers",
        "safe descriptor/source-card fixture refs",
        "schema/status/denial labels, booleans, zero guarded counters",
        "It excludes raw private content, raw source text, raw approval prose, credentials",
        "Runtime Registry handles, provider handles, secret values, and token-like values",
    )
    for term in required_terms:
        assert term in text


def test_l6af05_names_next_frontier_without_creating_successor_rail() -> None:
    text = normalized(DOC)

    required_terms = (
        f"Next exact frontier: `{NEXT_FRONTIER}`",
        "separate exact owner-created issue rail",
        "freshly binds repository `jeremyknows/memory-seam`, issue number",
        "operation class, owner actor association, unexpired UTC approval window",
        "exact repo-relative files, exact fixture-only or explicitly approved live/source-card inputs",
        "max operation count, denial-before-callback behavior",
        "L6AF.05 does not create that rail and does not approve additional runtime use",
        "continued HOLD: no additional runtime-use smoke, no live/private reads",
        "no Runtime Registry consumption, no callbacks, no persistence/mutation",
        "no publication/provider/prod/canary/Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6af05_residual_holds_parent_receipt_template_and_hygiene() -> None:
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    required_terms = (
        "Parent receipt template after merge",
        "L6AF rail: #291-#295 all closed",
        "final PR and merge source floor for #295",
        "artifacts: `docs/l6af01-default-off-adapter-runtime-use-approval-packet.md`",
        "`docs/l6af05-source-floor-parent-status-frontier-reconciliation.md`",
        "tests: `tests/test_l6af01_default_off_adapter_runtime_use_approval_packet.py`",
        "`tests/test_l6af05_source_floor_parent_status_frontier_reconciliation.py`",
        "targeted pytest, full `python -m pytest -q`, `python scripts/public_hygiene_scan.py`, `git diff --check`, `python -m compileall -q src tests examples`, and GitHub checks",
        f"outcome: `{STATUS}`",
        f"next exact frontier: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text

    unsafe_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_markers:
        assert marker not in lowered
