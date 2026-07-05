from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAP = REPO_ROOT / "ROADMAP.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
FRONTIER = REPO_ROOT / "docs" / "l6-next-implementation-slice-frontier-packet.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6i07_roadmap_records_current_l5_l6_completion_without_unholding_runtime_surfaces():
    text = normalized(ROADMAP)

    required_terms = [
        "L5 — Unsupervised read ladder",
        "Completed evidence now:",
        "no-source-read local tick contract and supervised one-read packet/receipt",
        "post-read verifier and default-off bounded runner shape",
        "one-tick canary decision packet that remains no-execution/no-activation",
        "unsupervised/live/private reads beyond the committed supervised metadata-card evidence",
        "L6 — Write custody companion",
        "L6S planning packets for ownership/approval, rollback/audit, operation-class fixtures, denied-before-mutation harness, trust-boundary review, and first implementation-slice decision packet",
        "L6I.01-L6I.04 approved implementation of the default-off synthetic write-intent preflight gate skeleton only",
        "L6I.05 trust-boundary review and L6I.06 frontier packet",
        "current implementation proves no-production denial-before-callback behavior",
        "report-safe denial metadata, stale/mismatched approval denial hardening, and a local synthetic smoke path",
    ]
    for term in required_terms:
        assert term in text


def test_l6i07_roadmap_names_post_l6ar_fleet_adoption_contract_frontier_as_current():
    """ROADMAP must name the CURRENT frontier explicitly and not regress to a stale one.

    History: this test originally asserted the L6I.06-era frontier wording
    (`SPLIT_AGAIN_DOCS_TESTS_ONLY` plus the L6I.06 frontier packet reference).
    The 2026-06-09 L6AR synthesis moved the frontier: the recommended next work
    is a human-reviewed fleet-adoption contract followed by the smallest
    read-only pilot. The assertions below track that frontier while preserving the original
    protective intent — a future ROADMAP edit that silently reverts to a
    superseded frontier, or that smuggles in an implementation approval
    phrase, must fail here.
    """
    text = normalized(ROADMAP)

    frontier_start = text.index("Current frontier:")
    after_frontier = text[frontier_start:]
    frontier_section = after_frontier[: after_frontier.index("Still held:")]

    current_frontier_terms = [
        "docs/l6ar05-source-floor-parent-tracker-reconciliation.md",
        "human-reviewed fleet-adoption contract",
        "smallest read-only pilot",
        "historical bounded evidence, not standing authority",
    ]
    for term in current_frontier_terms:
        assert term in frontier_section

    stale_frontier_markers = [
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "l6-next-implementation-slice-frontier-packet.md",
    ]
    for marker in stale_frontier_markers:
        assert marker not in frontier_section

    assert "I approve Memory Seam to implement" not in text


def test_l6i07_roadmap_preserves_positive_authorization_and_custody_holds():
    text = normalized(ROADMAP)

    held_terms = [
        "Still held:",
        "any code path returning `allowed=true`",
        "write execution",
        "custody transfer or custody receipt persistence",
        "delete",
        "reindex",
        "rollback",
        "cache purge",
        "provider/backend/source-stat/source-read callbacks",
        "positive allowed runtime paths",
        "persistence",
        "live/private source reads",
        "source discovery",
        "credential/auth/keychain/env reads",
        "Runtime Registry consumption",
        "global runtime configuration mutation",
        "service/listener/startup/cron activation",
        "provider/prod/canary authority",
        "publication",
        "repository visibility changes",
        "Atlas Gate movement",
        "production-authoritative claims",
    ]
    for term in held_terms:
        assert term in text


def test_l6i07_frontier_refresh_is_discoverable_and_tied_to_source_truth():
    docs_index = normalized(DOCS_INDEX)
    frontier = normalized(FRONTIER)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "../ROADMAP.md#l6--write-custody-companion" in docs_index
    assert "current L6 OSS-track frontier refresh through L6I.06" in docs_index
    assert "docs/tests-only positive-authorization prep tranche" in docs_index
    assert "l6-next-implementation-slice-frontier-packet.md" in docs_index
    assert "Recommendation: `SPLIT_AGAIN_DOCS_TESTS_ONLY`" in frontier
    assert "tests/test_l6_next_implementation_slice_frontier_packet.py" in inventory


def test_l6i07_public_artifacts_remain_report_safe():
    combined = " ".join(
        normalized(path)
        for path in (ROADMAP, DOCS_INDEX, FRONTIER)
    )

    allowed_public_terms = [
        "public issue numbers",
        "repository file names",
        "synthetic operation-class names",
        "boolean/counter facts",
        "safe status strings",
    ]
    for term in allowed_public_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
