from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_INVENTORY_COMPLETE_RUNTIME_INTEGRATION_STILL_HELD"
RAIL_STARTING_SOURCE_FLOOR = "b7fe89f752372de4f42d5f7e1084acad99c5ebf0"
PARENT_SUCCESSOR_COMMENT = "4653805965"
ISSUE_AUTHORIZATION_COMMENT = "4653805822"
HISTORICAL_SMOKE_APPROVAL_COMMENT = "4653350823"

L6AF_ANCHORS = (
    "L6AF.01 default-off adapter runtime-use approval packet (#291 / PR #296 / source floor `daf68ecd9e7cc55690bc70fdbbaf2d3707abd1f6`)",
    "L6AF.02 fixture-only default-off adapter runtime-use smoke (#292 / PR #297 / source floor `d995a5ac2c9dca2e571d8eb5fdb1009482031f06`)",
    "L6AF.03 runtime-use smoke value receipt and held-surface map (#293 / PR #298 / source floor `354dbe6baba18aaff9a6b609acd8f316d93c81d0`)",
    "L6AF.04 no-live trust-boundary review (#294 / PR #299 / source floor `02dcc439d32fdd464a84a919bfab52269d9afe21`)",
    "L6AF.05 source-floor parent status frontier reconciliation (#295 / PR #300 / source floor `b7fe89f752372de4f42d5f7e1084acad99c5ebf0`)",
)

BLOCKER_ROWS = (
    ("L6AF evidence inventory", "`PASS`"),
    ("Fixture-only runtime-use smoke", "`PASS_CONSUMED`"),
    ("Decision packet readiness", "`PASS_TO_L6AG_02`"),
    ("Runtime integration authority", "`HOLD`"),
    ("Additional adapter calls or runtime-use smokes", "`HOLD`"),
    ("Live/private reads and source-card reads", "`HOLD`"),
    ("Source discovery / broad recall / index query", "`HOLD`"),
    ("Runtime Registry / callbacks / provider routes", "`HOLD`"),
    ("Persistence / mutation / rollback execution", "`HOLD`"),
    ("Service/global activation and cron changes", "`HOLD`"),
    ("Publication / visibility / provider-prod-canary / Atlas Gate", "`HOLD`"),
    ("Broad `allowed=true` behavior", "`HOLD`"),
)

RESIDUAL_HOLDS = (
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval remains held",
    "runtime integration, adapter wiring, service routes, provider routes, callbacks, and activation remain held",
    "live/private reads and any source-card reads remain held",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material remain held",
    "source discovery, workspace scans, family scans, broad recall, and index queries remain held",
    "Runtime Registry consumption remains held",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation remain held",
    "service/listener/startup/global activation and recursive cron/schedule changes remain held",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement remain held",
    "broad `allowed=true` behavior remains held",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ag01_inventory_packet_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ag01-post-smoke-integration-evidence-inventory-blocker-map.md" in docs_index
    assert "tests/test_l6ag01_post_smoke_integration_evidence_inventory_blocker_map.py" in inventory
    assert "L6AG.01 post-smoke integration evidence inventory and blocker map" in inventory
    assert STATUS in inventory


def test_l6ag01_records_status_source_floor_and_authorization_anchors():
    text = normalized(DOC)

    required_terms = (
        "# L6AG.01 post-smoke integration evidence inventory and blocker map",
        f"Status: `{STATUS}`",
        "Rail issue: #301",
        "Parent issue: #6",
        "Blocked by: L6AF #291-#295 closed/PASS",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Parent successor comment: `{PARENT_SUCCESSOR_COMMENT}`",
        f"Issue-bound authorization comment: `{ISSUE_AUTHORIZATION_COMMENT}`",
        f"Historical runtime-use approval consumed by L6AF.02: #292 comment `{HISTORICAL_SMOKE_APPROVAL_COMMENT}`",
        "Verdict vocabulary: `PASS_INVENTORY_COMPLETE`, `FIX_BEFORE_DECISION_PACKET`, `HOLD_FOR_OWNER_DECISION`",
        "Verdict: `PASS_INVENTORY_COMPLETE`",
    )
    for term in required_terms:
        assert term in text


def test_l6ag01_inventories_l6af_artifacts_and_consumed_smoke():
    text = normalized(DOC)

    for anchor in L6AF_ANCHORS:
        assert anchor in text

    required_terms = (
        "operation class `L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE`",
        "consumed exactly one approved local fixture-only adapter import/call",
        "committed report-safe data and the committed default-off adapter module",
        "recorded the missing-approval denial, exact fixture positive label, zero guarded counters",
        "without another runtime-use smoke",
        "additional-smoke/live/read/callback/Registry/persistence/activation/Gate/broad-allow holds forward",
        "`RAIL_PASS_RECONCILED_FIXTURE_ONLY_RUNTIME_USE_SMOKE_CONSUMED`",
        "created no successor issue rail or cron change",
    )
    for term in required_terms:
        assert term in text


def test_l6ag01_preserves_public_metadata_only_no_runtime_boundary():
    text = normalized(DOC)

    required_terms = (
        "docs/tests/fixtures/public-metadata-only evidence inventory",
        "does not perform runtime integration",
        "execute another adapter call",
        "run another runtime-use smoke",
        "perform live/private reads",
        "read source cards",
        "consume Runtime Registry data",
        "invoke callbacks/provider routes",
        "persist or mutate state",
        "create or modify cron automation",
        "move provider/prod/canary/Gate or Atlas Gate state",
        "introduce broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ag01_distinguishes_smoke_evidence_from_integration_authority():
    text = normalized(DOC)

    required_terms = (
        "L6AF.02 consumed exactly one owner-approved local fixture-only adapter import/call under #292",
        "can preserve missing-approval denial behavior",
        "can keep all guarded held-surface counters at zero",
        "It does not prove that runtime integration is approved",
        "does not authorize another adapter call, runtime-use smoke, live/private read, source-card read",
        "#292 runtime-use approval is consumed historical evidence only and is not reusable",
        "parent successor comment `4653805965`",
        "issue-bound authorization comment `4653805822`",
        "source-floor advancement, copied wording, stale comments, labels, rail continuity, or this inventory PASS",
    )
    for term in required_terms:
        assert term in text


def test_l6ag01_blocker_map_labels_pass_consumed_and_hold_surfaces():
    text = normalized(DOC)

    assert "## Runtime-integration blocker map" in text
    for surface, label in BLOCKER_ROWS:
        assert surface in text
        assert label in text

    required_terms = (
        "`PASS_TO_L6AG_02`",
        "No L6AG.01 artifact, issue body, comment, PR merge, or source-floor advancement authorizes runtime integration or adapter wiring",
        "#292 approval is consumed; L6AG.01 has no approval for another adapter call or smoke",
        "Runtime Registry consumption and provider/backend/source-stat/source-read callbacks remain blocked",
        "No service/listener/startup/global config activation and no recursive cron/schedule modification are authorized",
    )
    for term in required_terms:
        assert term in text


def test_l6ag01_carries_residual_holds_and_next_issue():
    text = normalized(DOC)

    for hold in RESIDUAL_HOLDS:
        assert hold in text

    assert "Next open rail issue after #301: #302 `L6AG.02: runtime-integration-or-continued-hold decision packet`" in text
    assert "returns one of `PASS_INTEGRATION_PACKET_READY`, `FIX_BEFORE_INTEGRATION_PACKET`, or `HOLD_FOR_OWNER_DECISION`" in text
    assert "must not implement runtime integration, execute adapter calls, run another smoke" in text

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
