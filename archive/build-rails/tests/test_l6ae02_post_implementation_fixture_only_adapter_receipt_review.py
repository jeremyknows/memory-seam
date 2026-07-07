from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ae02-post-implementation-fixture-only-adapter-receipt-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_POST_IMPLEMENTATION_RECEIPT_REVIEW_FIXTURE_ONLY_DEFAULT_OFF"
VERDICT = "PASS_POST_IMPLEMENTATION_RECEIPT_REVIEW"
SOURCE_FLOOR = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
IMPLEMENTATION_PR = "#286"
IMPLEMENTATION_MERGE_COMMIT = "c21ed1cd82f74ff184143a2c1bea08ed22ad3262"
CONSUMED_APPROVAL_COMMENT = "4652448584"
OPERATION_CLASS = "L6AD_REPORT_SAFE_SOURCE_CARD_VALUE_ADAPTER_SKELETON"

ALLOWED_FILES = (
    "src/memory_seam/l6ad_report_safe_source_card_value_adapter.py",
    "tests/test_l6ad_report_safe_source_card_value_adapter.py",
    "docs/l6ae-default-off-adapter-implementation-receipt.md",
    "docs/README.md",
    "docs/contract-test-inventory.md",
)

HELD_COUNTER_TERMS = (
    "live/private reads and additional source-card reads",
    "raw private content and raw source text reads",
    "credential/auth/env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, and index queries",
    "Runtime Registry reads",
    "provider/backend/source-stat/source-read callbacks",
    "persistence, mutation, write/delete/reindex/cache-purge/rollback callbacks",
    "service/listener/startup/global activation and cron changes",
    "publication/visibility changes",
    "provider/prod/canary/Gate movement and Atlas Gate movement",
    "broad `allowed=true` results",
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


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ae02_review_doc_is_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ae02-post-implementation-fixture-only-adapter-receipt-review.md" in docs_index
    assert "tests/test_l6ae02_post_implementation_fixture_only_adapter_receipt_review.py" in inventory
    assert "L6AE.02 post-implementation fixture-only adapter receipt review" in inventory
    assert STATUS in inventory


def test_l6ae02_records_status_source_floor_and_review_scope() -> None:
    text = normalized(DOC)

    required_terms = (
        "# L6AE.02 post-implementation fixture-only adapter receipt review",
        f"Status: `{STATUS}`",
        "Rail issue: #282",
        "Parent issue: #6",
        "Depends on: #281 closed/PASS via PR #286",
        f"Starting source floor for resumed rail: `{SOURCE_FLOOR}`",
        f"Source floor entering slice: `{SOURCE_FLOOR}`",
        f"Reviewed implementation PR: {IMPLEMENTATION_PR}",
        f"Reviewed implementation merge commit: `{IMPLEMENTATION_MERGE_COMMIT}`",
        f"Issue-bound approval consumed: #281 comment `{CONSUMED_APPROVAL_COMMENT}`",
        f"Operation class reviewed: `{OPERATION_CLASS}`",
        f"Verdict: `{VERDICT}`",
    )
    for term in required_terms:
        assert term in text


def test_l6ae02_verifies_allowed_file_envelope_only() -> None:
    text = normalized(DOC)

    for path in ALLOWED_FILES:
        assert f"`{path}`" in text
    assert "`src/memory_seam/__init__.py` as permitted but not substantively changed" in text
    assert "No runtime service, provider, Runtime Registry, Gate, cron, persistence, source discovery, credential, environment, keychain, OAuth, auth-file, publication, visibility, rollback-execution, cache, index, or production-control files were added or modified" in text


def test_l6ae02_verifies_fixture_only_default_off_and_report_safe_output() -> None:
    text = normalized(DOC)

    required_terms = (
        "stayed inside the exact fixture-only/default-off/report-safe envelope",
        "default-off unless caller-supplied approval metadata exactly matches",
        "max slices `1`",
        "every held-surface flag false",
        "accepts caller-supplied fixture metadata only",
        "does not fetch GitHub approval text",
        "does not fetch GitHub approval text, inspect local/private source files, read credentials, read auth/env/keychain/OAuth/auth-file material",
        "Reportable PASS output is limited to schema/status strings, public descriptor/source-card fixture refs, usefulness label, issue/source-floor/operation metadata, fixture/default-off/report-safe/metadata-only booleans",
        "a narrow non-boolean allowed label",
        "Denied output keeps `allowed=false`, `allowed_result_count=0`, `live_read_invoked=false`, and all guarded counters at zero",
        "output validator rejects broad `allowed=true`",
    )
    for term in required_terms:
        assert term in text


def test_l6ae02_all_held_surface_counters_remain_zero() -> None:
    text = normalized(DOC)

    assert "All held-surface counters remain zero" in text
    for term in HELD_COUNTER_TERMS:
        assert term in text


def test_l6ae02_confirms_281_approval_consumed_once_not_standing_authority() -> None:
    text = normalized(DOC)

    required_terms = (
        "The #281 issue-bound approval was consumed exactly once by the merged #286 implementation slice",
        "cannot be reused by this #282 review",
        "parent #6 continuity",
        "source-floor advancement",
        "#283-#285 follow-up reviews",
        "future implementation work",
        "runtime activation",
        "live/private reads",
        "Atlas Gate movement",
        "broad `allowed=true` behavior",
    )
    for term in required_terms:
        assert term in text


def test_l6ae02_preserves_residual_holds_and_avoids_raw_private_examples() -> None:
    text = normalized(DOC)

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
