from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6al04-readiness-decision.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "RAIL_PASS_AUTH_CONTRACT_READY_RUNTIME_RETRY_AUTH_HELD"
DECISION = "AUTH_CONTRACT_READY_RUNTIME_RETRY_AUTH_HELD"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6al04_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6al04-readiness-decision.md" in docs_index
    assert "tests/test_l6al04_readiness_decision.py" in inventory
    assert "L6AL.04 supervised metadata read retry readiness decision" in inventory
    assert STATUS in inventory


def test_decision_records_auth_contract_ready_but_runtime_retry_auth_held() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AL.04 supervised metadata read retry readiness decision",
        f"Status: `{STATUS}`",
        "Rail issue: #352",
        "Parent issue: #6",
        "Depends on: L6AL.01-L6AL.03 closed/PASS",
        "Decision source floor entering slice: `a5c87db`",
        f"Decision: `{DECISION}`.",
        "not enough to open a live/private exact supervised metadata read retry from this rail",
        "must not verify external runtime/service/provider configuration",
        "The prior L6AK Step 3 raw usefulness proof remains incomplete",
        "`auth_status_code=403`, `items=[]`, `wrong_route_audience`, and `unauthorized_narrowing`",
    ):
        assert term in text


def test_decision_consumes_l6al_evidence_and_preserves_contract_readiness() -> None:
    text = normalized(DOC)

    for term in (
        "#349 / #353",
        "`PASS_CAPABILITY_MATRIX_READY_RETRY_STILL_HELD`",
        "#350 / #354",
        "`PASS_PROVIDER_AUTH_READINESS_FIXTURE_READY_RETRY_STILL_HELD`",
        "#351 / #355",
        "`PASS_MINIMAL_SERVICE_AUTH_CONTRACT_READY_RETRY_STILL_HELD`",
        "`AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY`",
        "`AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE`",
        "wrong route audience",
        "unauthorized narrowing",
        "missing/mismatched identity",
        "readiness remains metadata-only and does not authorize or execute a read",
        "zero source/callback/provider/secret/Registry counters",
    ):
        assert term in text


def test_blocker_and_next_packet_require_fresh_operator_service_auth_binding() -> None:
    text = normalized(DOC)

    for term in (
        "This blocker is service/operator configuration readiness, not repo contract absence.",
        "exact service/provider identity binding for the selected endpoint audience",
        "assurance that the service route will use the exact Memory Seam audience and will not fall back across endpoints",
        "a fresh issue-bound retry packet naming source/query/output/denial cases and stop conditions",
        "Do not open this as an executable retry until the blocker above is satisfied.",
        "Title: `L6AM.01: exact supervised metadata read retry after service auth binding`",
        "Depends on: L6AL #349-#352 closed/PASS and a fresh operator/service auth-binding approval comment.",
        "one max-one metadata-only supervised Memory Seam retry",
        "Required denial cases: `wrong_route_audience`, `unauthorized_narrowing`",
        "service/provider binding missing",
        "Runtime Registry requested",
        "broad `allowed=true`",
    ):
        assert term in text


def test_parent_tracker_update_and_verification_gate_are_explicit() -> None:
    text = normalized(DOC)

    for term in (
        "L6AL #349-#352 closed/PASS, PRs #353-#356 merged.",
        "Roadmap step 5 state: `AUTH CONTRACT READY / RUNTIME RETRY AUTH HELD`.",
        "Roadmap step 3 state remains `AUTH BLOCKER RECONCILED / RAW USEFULNESS PROOF INCOMPLETE / RETRY HELD`",
        "Next frontier: operator/service auth binding handoff or L6AM exact retry packet only after fresh service-auth binding approval.",
        "python -m pytest -q tests/test_l6al04_readiness_decision.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text


def test_decision_preserves_strict_no_live_no_secret_no_activation_boundaries() -> None:
    text = normalized(DOC)

    for hold in (
        "no live/private read retry",
        "no secret/env/keychain/OAuth/auth-file/credential reads",
        "no source discovery",
        "no broad recall/index queries",
        "no Runtime Registry consumption",
        "no provider callback invocation",
        "no provider route execution",
        "no service activation",
        "no cron changes",
        "no persistence/mutation/write/delete/reindex/rollback/cache-purge",
        "no publication/visibility/provider/prod/canary/Gate movement",
        "no Atlas Gate movement",
        "no broad `allowed=true` behavior",
    ):
        assert hold in text

    lowered = text.lower()
    for marker in (
        "oauth token",
        "credential value",
        "auth-file secret",
        "private-correlation-ref value",
        "source://",
        "platform-raw-id value",
    ):
        assert marker not in lowered
