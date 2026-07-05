from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6u04-dogfood-use-proof-prompt-set.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"

HOLD_OUTCOMES = (
    "HOLD_DEGRADED_EVIDENCE",
    "HOLD_TOO_REDACTED",
    "HOLD_UNSAFE_EVIDENCE",
    "HOLD_AMBIGUOUS_EVIDENCE",
)

FORBIDDEN_HELD_SURFACES = (
    "no prompt execution against live/private sources",
    "no implementation or execution of live/private reads",
    "no credentials, auth, env, keychain, OAuth, or auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption",
    "no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
    "no mutation execution, no `allowed=true` path",
    "no persistence/audit/custody records",
    "no cache mutation",
    "no service/listener/startup/cron activation",
    "no global Hermes/MCP/client/runtime config mutation",
    "no package publication",
    "no repository visibility change",
    "no provider/prod/canary authority",
    "no production authority",
    "no Atlas Gate movement",
)

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


def test_l6u04_prompt_set_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6u04-dogfood-use-proof-prompt-set.md" in docs_index
    assert "tests/test_l6u04_dogfood_use_proof_prompt_set.py" in inventory
    assert "L6U.04 dogfood/use-proof prompt set" in inventory
    assert OPERATION_CLASS in inventory


def test_l6u04_is_docs_tests_only_future_only_and_not_execution():
    text = normalized(DOC)

    required_terms = [
        "Status: `REPORT_SAFE_DOGFOOD_PROMPT_SET_NOT_EXECUTION`",
        "documentation and contract-test evidence only",
        "does not execute prompts",
        "does not execute prompts, implement adapters, perform live/private reads",
        "future-only, HITL-only, and not approval",
        "This packet itself is future-only, HITL-only, and not approval to connect to private sources.",
    ]
    for term in required_terms:
        assert term in text


def test_l6u04_names_exactly_one_future_proof_target():
    text = normalized(DOC)

    assert f"Future dogfood target: `{OPERATION_CLASS}`." in text
    assert text.count("Future dogfood target:") == 1
    assert "limited to exactly one future proof target and exactly one supervised read-side operation class" in text
    assert "max-one-operation limit described by L6U.02" in text


def test_l6u04_prompts_are_report_safe_and_request_no_private_content_or_credentials():
    text = normalized(DOC)

    for prompt_id in (
        "Prompt A — answerability from source card",
        "Prompt B — current-truth continuity check",
        "Prompt C — boundary-aware degraded handling",
    ):
        assert prompt_id in text

    required_safety_terms = [
        "templates only",
        "must not be executed by this packet",
        "report-safe references, never raw private content, secrets, source paths, source URIs",
        "Required citation: `source_card_ref`",
        "Required citation: `descriptor_ref`",
        "Required fallback stance: `fallback_avoided=true` unless the answer is HOLD",
        "Forbidden prompt inputs and outputs: raw source content, private/raw content, secrets, credentials",
        "raw prompts, raw queries, raw payload content",
    ]
    for term in required_safety_terms:
        assert term in text

    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6u04_requires_source_card_citation_fallback_avoidance_and_public_hygiene():
    text = normalized(DOC)

    required_terms = [
        "Cite the source-card reference",
        "Cite the descriptor reference",
        "fallback_avoided=true",
        "Citation",
        "Fallback avoidance",
        "Public-safe prompt inputs",
        "public_hygiene_result",
        "metadata-only and public-safe",
    ]
    for term in required_terms:
        assert term in text


def test_l6u04_has_explicit_hold_outcomes_for_degraded_redacted_unsafe_ambiguous_evidence():
    text = normalized(DOC)

    for hold in HOLD_OUTCOMES:
        assert hold in text

    required_terms = [
        "return HOLD if the descriptor is degraded, too redacted, unsafe, ambiguous, or missing",
        "return HOLD if the evidence is degraded, too redacted, unsafe, ambiguous, stale, or mismatched",
        "If any boundary would be needed, return HOLD",
        "A useful-looking answer that requires raw content, credentials, source discovery, broad recall, callbacks, Runtime Registry consumption, production authority, provider/prod/canary authority, activation, publication, or Atlas Gate movement is a HOLD",
    ]
    for term in required_terms:
        assert term in text


def test_l6u04_rubric_prioritizes_usefulness_without_weakening_boundaries():
    text = normalized(DOC)

    rubric_dimensions = (
        "Answerability",
        "Citation",
        "Fallback avoidance",
        "Boundary preservation",
        "Operator value",
    )
    for dimension in rubric_dimensions:
        assert dimension in text

    required_terms = [
        "The rubric prioritizes usefulness only when source and privacy boundaries remain unchanged.",
        "without weakening any held boundary",
        "accepted/held/next-action or bounded orientation result",
        "using metadata-only evidence",
        "no-live, no-callback, no-production, no-activation, no-publication, no-provider/prod/canary, and no-Gate holds",
    ]
    for term in required_terms:
        assert term in text


def test_l6u04_result_shape_is_report_safe_no_live_no_callback_no_registry():
    text = normalized(DOC)

    public_fields = (
        "status",
        "operation_class",
        "prompt_id",
        "source_card_ref",
        "descriptor_ref",
        "citation_present",
        "fallback_avoided",
        "public_hygiene_result",
        "guarded_callback_counters",
        "live_private_read_count",
        "source_discovery_count",
        "runtime_registry_consumption_count",
    )
    for field in public_fields:
        assert f"`{field}`" in text

    required_terms = [
        "all guarded callback families fixed at zero",
        "`live_private_read_count`: `0`",
        "`source_discovery_count`: `0`",
        "`runtime_registry_consumption_count`: `0`",
        "must not echo raw prompts, raw private content, source paths, source URIs, credentials",
        "source discovery results, broad recall output, or private correlation references",
    ]
    for term in required_terms:
        assert term in text


def test_l6u04_preserves_no_live_no_callback_no_production_holds():
    text = normalized(DOC)

    for surface in FORBIDDEN_HELD_SURFACES:
        assert surface in text

    assert "no Runtime Registry consumption" in text
    assert "no service/listener/startup/cron activation" in text
    assert "no package publication" in text
    assert "no provider/prod/canary authority" in text
    assert "no Atlas Gate movement" in text
