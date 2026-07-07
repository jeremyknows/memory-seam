from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6u05-supervised-live-use-trust-boundary-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"
VERDICTS = ("PASS", "HOLD", "FIX_BEFORE_NEXT_SLICE")

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)

HELD_SURFACES = (
    "implementation of any supervised live-use adapter",
    "execution of live/private reads or unsupervised reads",
    "credential/auth/env/keychain/OAuth/auth-file reads",
    "source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, and source-read calls",
    "Runtime Registry consumption",
    "provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
    "mutation execution and any `allowed=true` result path",
    "write execution",
    "custody transfer and custody receipt persistence",
    "delete execution",
    "reindex execution",
    "rollback execution",
    "cache purge execution",
    "persistence/audit/custody records and cache mutation",
    "service/listener/startup/cron activation or recurring runner behavior",
    "global Hermes/MCP/client/runtime configuration mutation",
    "package publication and repository visibility changes",
    "provider/prod/canary authority and production-authoritative claims",
    "Atlas Gate movement",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6u05_trust_boundary_review_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6u05-supervised-live-use-trust-boundary-review.md" in docs_index
    assert "tests/test_l6u05_supervised_live_use_trust_boundary_review.py" in inventory
    assert "L6U.05 supervised live-use trust-boundary review" in inventory
    assert "PASS/HOLD/FIX_BEFORE_NEXT_SLICE" in inventory


def test_l6u05_is_docs_tests_only_no_execution_review():
    text = normalized(DOC)

    required_terms = [
        "Status: `TRUST_BOUNDARY_REVIEW_PACKET_ONLY`",
        "Review verdict: `PASS`",
        "Reviewed rail issues: #177, #178, #179, #180",
        "docs/tests-only, no-edit/no-execution trust-boundary review",
        "does not implement adapters, execute live/private reads",
        "read credentials",
        "discover sources",
        "consume Runtime Registry data",
        "call provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "activate services/listeners/startup/cron paths",
        "introduce any `allowed=true` path",
    ]
    for term in required_terms:
        assert term in text


def test_l6u05_verdict_vocabulary_only_and_pass_is_not_approval():
    text = normalized(DOC)

    assert "The review outcome vocabulary is exactly `PASS`, `HOLD`, or `FIX_BEFORE_NEXT_SLICE`." in text
    for verdict in VERDICTS:
        assert verdict in text

    required_terms = [
        "The PASS is not approval for implementation",
        "not approval for live/private reads",
        "not approval for provider/backend/source callbacks",
        "Any future proof still requires a fresh exact HITL approval packet",
        "This `PASS` only means the docs/tests preparation rail is internally coherent and boundary-preserving",
        "must not be treated as approval to implement behavior",
    ]
    for term in required_terms:
        assert term in text


def test_l6u05_summarizes_l6u01_through_l6u04_evidence():
    text = normalized(DOC)

    required_terms = [
        "L6U.01 adapter wiring map (#177)",
        "docs/l6u01-supervised-live-use-adapter-wiring-map.md",
        "tests/test_l6u01_supervised_live_use_adapter_wiring_map.py",
        "adapter-boundary-only, docs/tests-only, default-off, no-approval",
        "Atlas Query/Hermes adapters to depend downstream on Memory Seam",
        "L6U.02 supervised live-read approval packet (#178)",
        "docs/l6u02-supervised-live-read-approval-packet.md",
        "tests/test_l6u02_supervised_live_read_approval_packet.py",
        "HITL-only and future-only; the packet itself is not approval",
        "stale, variant, copied, mismatched, broadened",
        "L6U.03 local integration smoke design (#179)",
        "docs/l6u03-local-integration-smoke-design.md",
        "tests/test_l6u03_local_integration_smoke_design.py",
        "uses committed synthetic fixtures only",
        "`live_adapter_invoked=false`",
        "unsupported write/custody/delete/reindex/rollback/cache-purge behavior",
        "L6U.04 dogfood/use-proof prompt set (#180)",
        "docs/l6u04-dogfood-use-proof-prompt-set.md",
        "tests/test_l6u04_dogfood_use_proof_prompt_set.py",
        "source-card/descriptor citation",
        "explicit HOLD outcomes for degraded, too-redacted, unsafe, or ambiguous evidence",
    ]
    for term in required_terms:
        assert term in text


def test_l6u05_preserves_public_hygiene_and_report_safe_receipts():
    text = normalized(DOC)

    required_terms = [
        "Public hygiene: PASS.",
        "report-safe references and metadata-only descriptors",
        "exclude raw source content, private/raw content, secrets, credentials",
        "auth/env/keychain material",
        "OAuth material",
        "auth-file material",
        "source URIs",
        "raw prompts, raw queries, raw payload content, raw backend responses",
        "Runtime Registry references",
        "Report-safe receipts/results: PASS.",
        "public-safe fields such as status, operation class, prompt/smoke/reference identifiers",
        "guarded callback counters, live-private-read count, source-discovery count, Runtime Registry consumption count",
        "`live_adapter_invoked=false`",
        "do not persist audit/custody bodies or cache data",
    ]
    for term in required_terms:
        assert term in text

    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6u05_preserves_denial_before_callback_no_production_and_one_operation_bounds():
    text = normalized(DOC)

    required_terms = [
        "Denial before callback design: PASS.",
        "requires denial or HOLD before provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
        "Callback counters remain zero for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, and cache-purge families.",
        "No-production holds: PASS.",
        "One-operation bounds: PASS.",
        f"exactly one operation class, `{OPERATION_CLASS}`",
        "`max_operation_count=1`",
        "no write/custody/delete/reindex/rollback/cache-purge operation support",
    ]
    for term in required_terms:
        assert term in text


def test_l6u05_restates_all_residual_holds_and_no_allowed_true_path():
    text = normalized(DOC)

    assert "Residual holds restated" in text
    for surface in HELD_SURFACES:
        assert surface in text

    required_terms = [
        "No `allowed=true` path: PASS.",
        "introduces no approval recognition, no allowed result, no mutation execution, and no `allowed=true` path",
        "denied before callback when stale, variant, copied, mismatched, broadened, or requesting held authority",
        "Proceed no further autonomously after L6U.05.",
        "pause and ask Jeremy for an explicit future direction",
    ]
    for term in required_terms:
        assert term in text
