from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ae05-source-floor-parent-status-frontier-reconciliation.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_RECONCILED_DEFAULT_OFF_ADAPTER_IMPLEMENTED"
RAIL_STARTING_SOURCE_FLOOR = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
SOURCE_FLOOR_ENTERING_SLICE = "944e34f68fc2ecccb52c2b57f8c7059bd81482bb"
PARENT_SUCCESSOR_COMMENT = "4652448783"
IMPLEMENTATION_APPROVAL_COMMENT = "4652448584"
RECONCILIATION_PREAUTH_COMMENT = "4652981285"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"
NEXT_FRONTIER = "OWNER_DECISION_FOR_DEFAULT_OFF_ADAPTER_RUNTIME_USE_OR_CONTINUED_HOLD"

L6AE_ANCHORS = (
    "L6AE.01 (#281 / PR #286 / source floor `c21ed1cd82f74ff184143a2c1bea08ed22ad3262`)",
    "L6AE.02 (#282 / PR #287 / source floor `45a09f62df38180b429abfb408b80ab59c348a6d`)",
    "L6AE.03 (#283 / PR #288 / source floor `0797449e29fd2296d994a27a3337bde234af2ffa`)",
    "L6AE.04 (#284 / PR #289 / source floor `944e34f68fc2ecccb52c2b57f8c7059bd81482bb`)",
    "L6AE.05 (#285 / this packet)",
)

RESIDUAL_HOLDS = (
    "live/private reads and any additional source-card read remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, env/keychain/OAuth/auth-file reads remain held",
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


def test_l6ae05_reconciliation_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ae05-source-floor-parent-status-frontier-reconciliation.md" in docs_index
    assert "tests/test_l6ae05_source_floor_parent_status_frontier_reconciliation.py" in inventory
    assert "L6AE.05 source-floor parent status frontier reconciliation" in inventory
    assert STATUS in inventory


def test_l6ae05_records_status_source_floor_parent_and_outcome() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AE.05 source-floor anchor, parent status, and next frontier reconciliation",
        f"Status: `{STATUS}`",
        "Rail issue: #285",
        "Parent issue: #6",
        "Blocked by: #281-#284 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound implementation approval consumed: #281 comment `{IMPLEMENTATION_APPROVAL_COMMENT}`",
        f"Issue-bound reconciliation preauthorization: #285 comment `{RECONCILIATION_PREAUTH_COMMENT}`",
        f"Operation class implemented: `{OPERATION_CLASS}`",
        "Reconciliation vocabulary: `RAIL_PASS_RECONCILED`, `FIX_BEFORE_PARENT_RECEIPT`, `HOLD_FOR_OWNER_DECISION`",
        "Reconciliation: `RAIL_PASS_RECONCILED`",
        "Rail outcome: `DEFAULT_OFF_FIXTURE_ONLY_ADAPTER_IMPLEMENTED_RUNTIME_HELD`",
        "Parent #6 remains `OPEN` while this packet is prepared",
    )
    for term in required_terms:
        assert term in text


def test_l6ae05_lists_all_l6ae_prs_source_floors_and_scope() -> None:
    text = normalized(DOC)

    for anchor in L6AE_ANCHORS:
        assert anchor in text

    required_terms = (
        "default-off report-safe source-card value adapter implementation slice",
        "post-implementation fixture-only adapter receipt review",
        "no-live trust-boundary review",
        "adapter use-proof packet and held-runtime map",
        "source-floor anchor, parent status, residual holds, and next-frontier reconciliation",
        "creates no successor issues, no successor cron jobs, no runtime activation, and no Atlas Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ae05_confirms_default_off_adapter_completion_without_runtime_activation() -> None:
    text = normalized(DOC)

    required_terms = (
        "Finding: `PASS_TO_PARENT_RECEIPT_WITH_DEFAULT_OFF_ADAPTER_IMPLEMENTED_RUNTIME_HELD`",
        "#281-#284 are closed/PASS and #285 can close after this packet merges and verification passes",
        "L6AE completed the exact default-off implementation rail",
        "The rail did create the narrow adapter module and tests approved by #281",
        "did not wire the adapter into runtime operation",
        "did not execute live/private reads",
        "did not call providers/backends/source-stat/source-read callbacks",
        "did not consume Runtime Registry data",
        "did not persist/mutate/cache/write/delete/reindex/rollback",
        "did not activate services/listeners/startup/global routes",
        "did not authorize a broad allowed path",
    )
    for term in required_terms:
        assert term in text


def test_l6ae05_names_next_frontier_without_creating_successor_rail() -> None:
    text = normalized(DOC)

    required_terms = (
        f"Next exact frontier: `{NEXT_FRONTIER}`",
        "separate exact owner-created issue rail",
        "freshly binds repository `jeremyknows/memory-seam`, issue number",
        "operation class or runtime-use operation class",
        "owner actor association",
        "unexpired UTC approval window",
        "exact repo-relative files, fixture-only or explicitly approved source-card inputs",
        "denial-before-callback behavior",
        "L6AE.05 does not create that rail and does not approve runtime use",
        "continued HOLD: no live/private reads, no runtime integration",
        "no publication/provider/prod/canary/Gate movement",
    )
    for term in required_terms:
        assert term in text


def test_l6ae05_preserves_consumed_approvals_evidence_and_residual_holds() -> None:
    text = normalized(DOC)

    required_terms = (
        "The #281 implementation approval remains consumed historical evidence only",
        f"approved exactly one fixture-only implementation slice for operation `{OPERATION_CLASS}`",
        "bounded to the #281 approved repo-relative file envelope",
        "expiring at `2026-06-09T07:01:56Z`",
        "not reusable by this #285 reconciliation",
        "future runtime-use packets, or any future live/private read or provider callback",
        "The earlier #262 and #267 source-card read evidence remains historical and consumed",
        "uses only committed report-safe fixture metadata and public source-floor/issue/PR anchors",
        "does not perform another read or publish raw private content",
    )
    for term in required_terms:
        assert term in text

    for hold in RESIDUAL_HOLDS:
        assert hold in text


def test_l6ae05_parent_receipt_template_and_report_hygiene() -> None:
    text = normalized(DOC)

    required_terms = (
        "Parent receipt template after merge",
        "L6AE rail: #281-#285 all closed",
        "final PR and merge source floor for #285",
        "artifacts: `src/memory_seam/l6ad_report_safe_source_card_value_adapter.py`",
        "`docs/l6ae05-source-floor-parent-status-frontier-reconciliation.md`",
        "tests: `tests/test_l6ae01_report_safe_source_card_value_adapter.py`",
        "`tests/test_l6ae05_source_floor_parent_status_frontier_reconciliation.py`",
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
