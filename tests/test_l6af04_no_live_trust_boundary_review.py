from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6af04-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
ADAPTER = REPO_ROOT / "src" / "memory_seam" / "l6ad_report_safe_source_card_value_adapter.py"

STATUS = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_FIXTURE_ONLY_RUNTIME_USE_SMOKE_RAIL"
VERDICT = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "SOURCE_FLOOR_PARENT_STATUS_RECONCILIATION_ALLOWED_FOR_ISSUE_295_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "f321708b1e8f708345194fc34c0d0968c620c03e"
SOURCE_FLOOR_ENTERING_SLICE = "354dbe6baba18aaff9a6b609acd8f316d93c81d0"
APPROVAL_PACKET_SOURCE_FLOOR = "daf68ecd9e7cc55690bc70fdbbaf2d3707abd1f6"
SMOKE_SOURCE_FLOOR = "d995a5ac2c9dca2e571d8eb5fdb1009482031f06"
VALUE_RECEIPT_SOURCE_FLOOR = "354dbe6baba18aaff9a6b609acd8f316d93c81d0"
PREP_AUTH_COMMENT = "4653350694"
RUNTIME_USE_APPROVAL_COMMENT = "4653350823"
OPERATION_CLASS = "L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE"

REVIEWED_SURFACES = (
    "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py",
    "tests/test_l6ad_report_safe_source_card_value_adapter.py",
    "tests/test_l6af01_default_off_adapter_runtime_use_approval_packet.py",
    "tests/test_l6af02_fixture_only_default_off_adapter_runtime_use_smoke.py",
    "tests/test_l6af03_runtime_use_smoke_value_receipt_held_surface_map.py",
    "docs/l6af01-default-off-adapter-runtime-use-approval-packet.md",
    "docs/l6af02-fixture-only-default-off-adapter-runtime-use-smoke.md",
    "docs/l6af03-runtime-use-smoke-value-receipt-held-surface-map.md",
)

CUSTODY_FINDINGS = (
    "runtime-use approval consumed by | #292 only",
    "approval comment reference | `4653350823`",
    "operation class | `L6AF_FIXTURE_ONLY_DEFAULT_OFF_ADAPTER_RUNTIME_USE_SMOKE`",
    "max runtime-use count | `1`",
    "actual runtime-use count reviewed | `1`",
    "additional runtime-use smoke in #293/#294 | `0`",
    "live/private reads invoked | `false`",
    "source-card reads invoked | `false`",
    "Runtime Registry consumed | `false`",
    "callbacks invoked | `false`",
    "persistence or mutation invoked | `false`",
    "service/listener/startup/global activation invoked | `false`",
    "cron changes invoked | `false`",
    "publication or visibility changes invoked | `false`",
    "provider/prod/canary/Gate movement invoked | `false`",
    "Atlas Gate movement invoked | `false`",
    "broad `allowed=true` created | `false`",
)

RESIDUAL_HOLDS = (
    "any additional runtime-use smoke or adapter call beyond #292's consumed one-smoke approval",
    "live/private reads and any source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks",
    "persistence, custody, mutation, audit writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, Gate movement, and Atlas Gate movement",
    "broad `allowed=true` behavior",
)

UNSAFE_REPORT_CLASSES = (
    "raw private content",
    "raw source text",
    "raw approval prose",
    "credentials",
    "auth material",
    "environment values",
    "keychain material",
    "OAuth material",
    "auth-file material",
    "private absolute paths",
    "source URIs",
    "platform IDs",
    "prompts",
    "queries",
    "payloads",
    "backend responses",
    "private correlation refs",
    "Runtime Registry handles",
    "provider handles",
    "secret values",
    "token-like values",
)

FORBIDDEN_ADAPTER_MARKERS = (
    "import os",
    "import subprocess",
    "import requests",
    "import pathlib",
    "import sqlite3",
    "import http",
    "runtime registry client",
    "provider_callback(",
    "source_read_callback(",
    "open(",
    "Path(",
    "write_text(",
    "unlink(",
    "rmtree(",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6af04_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6af04-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6af04_no_live_trust_boundary_review.py" in inventory
    assert "L6AF.04 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6af04_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AF.04 no-live trust-boundary review for runtime-use smoke rail",
        f"Status: `{STATUS}`",
        "Rail issue: #294",
        "Parent issue: #6",
        "Depends on: #293 closed/PASS via PR #298",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed approval-packet PR: #296",
        "Reviewed runtime-use smoke PR: #297",
        "Reviewed value-receipt PR: #298",
        f"Approval-packet merge source floor: `{APPROVAL_PACKET_SOURCE_FLOOR}`",
        f"Runtime-use smoke merge source floor: `{SMOKE_SOURCE_FLOOR}`",
        f"Value-receipt merge source floor: `{VALUE_RECEIPT_SOURCE_FLOOR}`",
        f"Issue-bound prep authorization: #291 comment `{PREP_AUTH_COMMENT}`",
        f"Consumed runtime-use approval: #292 comment `{RUNTIME_USE_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_RECONCILIATION`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6af04_reviews_committed_surfaces_only_without_new_smoke() -> None:
    text = normalized(DOC)

    required_terms = (
        "inspected committed repository implementation/test/docs surfaces plus public issue/PR/source-floor metadata only",
        "did not execute an additional adapter runtime-use smoke",
        "did not perform a live/private read",
        "did not read a source card",
        "did not fetch or publish raw approval prose",
        "did not read credentials/auth/env/keychain/OAuth/auth-file material",
        "did not discover sources",
        "did not scan workspaces or families",
        "did not run broad recall or index queries",
        "did not consume Runtime Registry data",
        "did not invoke callbacks",
        "did not persist or mutate state",
        "did not activate a service/listener/startup/global path",
        "did not create or modify cron automation",
        "did not publish or change visibility",
        "did not move provider/prod/canary/Gate or Atlas Gate state",
        "did not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
    for surface in REVIEWED_SURFACES:
        assert f"`{surface}`" in text


def test_l6af04_fixture_only_runtime_use_custody_is_exactly_one_consumed_smoke() -> None:
    text = normalized(DOC)

    assert "Fixture-only runtime-use custody finding" in text
    for term in CUSTODY_FINDINGS:
        assert term in text
    for term in (
        "The rail stayed inside the exact #292 approval envelope",
        "only runtime-use smoke was one local fixture-only adapter import/call performed by the #292 test/proof surface",
        "committed report-safe metadata and the committed adapter module",
        "This #294 review is docs/tests/review scope only and performs no new adapter call",
        "approval is consumed historical authority for #292 only",
        "not reusable by #293, this #294 review, #295, parent #6",
        "future runtime use, live/private reads, service activation",
        "Atlas Gate movement, or broad `allowed=true` behavior",
    ):
        assert term in text


def test_l6af04_adapter_report_safety_and_no_broad_allowed_true() -> None:
    text = normalized(DOC)

    required_terms = (
        "fixture-only, default-off, report-safe module",
        "consumes caller-supplied approval and fixture mappings",
        "denies by default before adapter action",
        "rejects unsafe raw/private/source/credential/approval echoes before report output",
        "emits only status strings, safe refs, booleans, denial labels, narrow value labels, counts, and all-zero guarded counters",
        "positive fixture path is not a general allow path",
        "narrow non-boolean label `EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER`",
        "rail records broad `allowed=true` as false",
        "Denied paths keep `allowed=false`, `allowed_result_count=0`, `live_read_invoked=false`, and all guarded counters zero",
    )
    for term in required_terms:
        assert term in text

    assert "Reportable evidence in this review is limited" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text


def test_l6af04_runtime_registry_callback_persistence_and_activation_absent() -> None:
    text = normalized(DOC)

    required_terms = (
        "No Runtime Registry consumer",
        "registry handle",
        "provider callback",
        "backend callback",
        "source-stat callback",
        "source-read callback",
        "write/custody/delete/reindex/rollback/cache-purge callback",
        "persistence store",
        "mutation route",
        "audit/custody write",
        "cache mutation",
        "service/listener startup hook",
        "global activation path",
        "cron change",
        "publication route",
        "visibility change",
        "provider/prod/canary control",
        "Gate control",
        "Atlas Gate control",
        "The #292 smoke did not add runtime integration",
        "Rollback remains documentation-only; rollback execution and cache purge remain held",
    )
    for term in required_terms:
        assert term in text


def test_l6af04_names_next_blocker_and_residual_holds() -> None:
    text = normalized(DOC)

    for term in (
        "Next exact blocker: #295 source-floor anchor, parent status, and next frontier reconciliation",
        "#295 is docs/tests/reconciliation scope only",
        "may anchor #291-#295 PR/source floors and post the parent completion receipt after merge",
        "must not execute runtime use",
        "perform live/private reads",
        "read source cards",
        "fetch raw approval prose",
        "read credentials/auth/env/keychain/OAuth/auth-file material",
        "discover sources",
        "consume Runtime Registry data",
        "invoke callbacks",
        "persist or mutate state",
        "activate services/listeners/startup/global paths",
        "change crons",
        "publish or change visibility",
        "move provider/prod/canary/Gate or Atlas Gate state",
        "introduce broad `allowed=true` behavior",
        "Next open rail issue after #294: #295",
    ):
        assert term in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text


def test_l6af04_report_safe_doc_excludes_obvious_unsafe_examples() -> None:
    text = normalized(DOC).lower()

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    for marker in unsafe_example_markers:
        assert marker not in text


def test_l6af04_adapter_source_has_no_obvious_live_runtime_imports_or_io() -> None:
    adapter_source = ADAPTER.read_text(encoding="utf-8").lower()

    for marker in FORBIDDEN_ADAPTER_MARKERS:
        assert marker.lower() not in adapter_source
    assert 'allowed": "exact_fixture_only_report_safe_value_adapter"' in adapter_source
    assert 'allowed": true' not in adapter_source
    assert 'live_read_invoked": false' in adapter_source
