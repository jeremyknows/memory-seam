from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ae03-no-live-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
ADAPTER = REPO_ROOT / "src" / "memory_seam" / "l6ad_report_safe_source_card_value_adapter.py"

STATUS = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW_DEFAULT_OFF_ADAPTER"
VERDICT = "PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW"
NEXT_FRONTIER = "USE_PROOF_PACKET_AND_HELD_RUNTIME_MAP_ALLOWED_FOR_ISSUE_284_ONLY"
RAIL_STARTING_SOURCE_FLOOR = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
SOURCE_FLOOR_ENTERING_SLICE = "45a09f62df38180b429abfb408b80ab59c348a6d"
IMPLEMENTATION_MERGE_COMMIT = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
RECEIPT_REVIEW_MERGE_COMMIT = "45a09f62df38180b429abfb408b80ab59c348a6d"
CONSUMED_APPROVAL_COMMENT = "4652448584"
PREAUTH_COMMENT = "4652980909"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"

REVIEWED_SURFACES = (
    "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py",
    "tests/test_l6ad_report_safe_source_card_value_adapter.py",
    "tests/test_l6ae02_post_implementation_fixture_only_adapter_receipt_review.py",
    "docs/l6ae-default-off-adapter-implementation-receipt.md",
    "docs/l6ae02-post-implementation-fixture-only-adapter-receipt-review.md",
)

RESIDUAL_HOLDS = (
    "live/private reads and any additional source-card reads",
    "raw private content, raw source text, raw approval prose, credentials, auth material, environment values, keychain material, OAuth material, and auth-file material",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read callbacks",
    "persistence, mutation, audit/custody writes, write/delete/reindex/cache-purge, rollback execution, and cache mutation",
    "service/listener/startup/global activation and cron/schedule changes",
    "publication, visibility changes, provider/prod/canary authority, and Atlas Gate movement",
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
    "source locations",
    "platform identifiers",
    "private absolute paths",
    "prompt/query/payload bodies",
    "backend responses",
    "private correlation references",
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


def test_l6ae03_review_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ae03-no-live-trust-boundary-review.md" in docs_index
    assert "tests/test_l6ae03_no_live_trust_boundary_review.py" in inventory
    assert "L6AE.03 no-live trust-boundary review" in inventory
    assert STATUS in inventory


def test_l6ae03_records_status_source_floor_and_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AE.03 no-live trust-boundary review for default-off adapter implementation",
        f"Status: `{STATUS}`",
        "Rail issue: #283",
        "Parent issue: #6",
        "Depends on: #282 closed/PASS via PR #287",
        f"Starting source floor for resumed rail: `{RAIL_STARTING_SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR_ENTERING_SLICE}`",
        "Reviewed implementation PR: #286",
        "Reviewed receipt-review PR: #287",
        f"Implementation merge commit: `{IMPLEMENTATION_MERGE_COMMIT}`",
        f"Receipt-review merge commit: `{RECEIPT_REVIEW_MERGE_COMMIT}`",
        f"Issue-bound approval consumed by implementation: #281 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Issue-bound preauthorization for this review: #283 comment `{PREAUTH_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        "Verdict vocabulary: `PASS_NO_LIVE_TRUST_BOUNDARY_REVIEW`, `FIX_BEFORE_USE_PROOF`, `HOLD_FOR_OWNER_DECISION`",
        f"Verdict: `{VERDICT}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ae03_reviews_committed_implementation_and_receipt_surfaces_only() -> None:
    text = normalized(DOC)

    required_terms = (
        "inspected committed repository implementation/test/docs surfaces plus public issue/PR/source-floor metadata only",
        "did not perform a live/private source read",
        "did not fetch approval prose",
        "did not read credentials/auth/env/keychain/OAuth/auth-file material",
        "did not consume Runtime Registry data",
        "did not call providers or callbacks",
        "did not persist or mutate state",
        "did not activate a service",
        "did not publish or change visibility",
        "did not move provider/prod/canary/Gate or Atlas Gate",
        "did not create broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text
    for surface in REVIEWED_SURFACES:
        assert f"`{surface}`" in text


def test_l6ae03_confirms_no_live_private_read_path_or_broad_allowed_true() -> None:
    text = normalized(DOC)

    required_terms = (
        "The reviewed adapter has no source-card read path and no local/private source inspection path",
        "approval and fixture builders return static report-safe metadata",
        "adaptation function consumes caller-supplied mappings and returns a report-safe dictionary",
        "does not import or invoke GitHub clients, source readers, file/path scanners",
        "environment readers, keychain/OAuth/auth-file readers, Runtime Registry clients",
        "provider/backend/source-stat/source-read callbacks",
        "service/listener startup hooks",
        "persistence stores",
        "mutation/write/delete/reindex/cache-purge routines",
        "Atlas Gate controls",
        "positive path is not broad `allowed=true`",
        "narrow non-boolean label `EXACT_FIXTURE_ONLY_REPORT_SAFE_VALUE_ADAPTER`",
        "Denied paths keep `allowed=false`, `allowed_result_count=0`, `live_read_invoked=false`, and all guarded counters zero",
    )
    for term in required_terms:
        assert term in text


def test_l6ae03_runtime_registry_callback_persistence_and_activation_remain_absent() -> None:
    text = normalized(DOC)

    required_terms = (
        "No Runtime Registry consumption exists in the reviewed implementation, tests, or receipt docs",
        "There is no callback route for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, cache purge",
        "does not persist approvals, receipts, counters, outputs, or audit/custody state",
        "does not mutate indexes, caches, files, global config, cron schedules, services, providers, production/canary state, or Gate state",
        "Rollback remains documentation-only; rollback execution and cache purge remain held",
    )
    for term in required_terms:
        assert term in text


def test_l6ae03_approval_custody_and_stale_authority_resistance() -> None:
    text = normalized(DOC)

    required_terms = (
        "The #281 owner approval is consumed historical authority for PR #286 only",
        "not reusable by #282, this #283 review, #284, #285, parent #6",
        "merge events, issue closure, labels, source-floor advancement",
        "copied comments, stale/broadened/expired/mismatched/non-owner approval metadata",
        "future implementation work, runtime activation, live/private reads",
        "Atlas Gate movement, or broad `allowed=true` behavior",
        "denies before adapter action if approval metadata is missing, stale, copied, broadened, expired, non-owner",
        "mismatched to repository `jeremyknows/memory-seam`, issue `281`",
        f"operation class `{OPERATION_CLASS}`",
        "source floor `972cc3026cd1a2629679778143de0eafe7b3b921`",
        f"approval comment `{CONSUMED_APPROVAL_COMMENT}`",
        "max slices `1`",
        "exact file envelope",
        "any held-surface authorization flag",
        "This #283 review does not refresh, extend, or replace that approval",
    )
    for term in required_terms:
        assert term in text


def test_l6ae03_report_safe_redaction_and_residual_holds() -> None:
    text = normalized(DOC)

    assert "Report-safe redaction finding" in text
    assert "expose only status/schema strings" in text
    for unsafe_class in UNSAFE_REPORT_CLASSES:
        assert unsafe_class in text
    for hold in RESIDUAL_HOLDS:
        assert hold in text

    unsafe_example_markers = (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref",
        "source://",
        "platform-raw-id",
    )
    lowered = text.lower()
    for marker in unsafe_example_markers:
        assert marker not in lowered


def test_l6ae03_names_next_blocker_and_limits_issue_284_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "Next exact blocker: #284 adapter use-proof packet and held-runtime map",
        "committed fixture/default-off adapter evidence only",
        "must not activate runtime use",
        "perform live/private reads",
        "fetch private/raw source material",
        "fetch credentials/auth/env/keychain/OAuth/auth-file material",
        "consume Runtime Registry",
        "create callbacks",
        "persist or mutate state",
        "publish or change visibility",
        "move provider/prod/canary/Gate or Atlas Gate",
        "execute rollback/cache purge",
        "create/change cron automation",
        "introduce broad `allowed=true` behavior",
        "Next open rail issue after #283: #284",
    )
    for term in required_terms:
        assert term in text


def test_l6ae03_adapter_source_has_no_obvious_live_runtime_imports_or_io() -> None:
    adapter_source = ADAPTER.read_text(encoding="utf-8").lower()

    for marker in FORBIDDEN_ADAPTER_MARKERS:
        assert marker.lower() not in adapter_source
    assert 'allowed": "exact_fixture_only_report_safe_value_adapter"' in adapter_source
    assert 'allowed": true' not in adapter_source
    assert 'live_read_invoked": false' in adapter_source
