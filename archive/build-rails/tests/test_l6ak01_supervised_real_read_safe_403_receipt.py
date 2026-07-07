from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6ak01-supervised-real-read-safe-403-receipt.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

STATUS = "PASS_SAFE_403_RECEIPT_AUTH_BLOCKER_CAPTURED_NO_ITEMS_RETURNED"
NEXT_FRONTIER = "STEP_5_SERVICE_PROVIDER_ROUTE_AUDIENCE_AUTH_BINDING_BEFORE_EXACT_RETRY"
RAIL_STARTING_SOURCE_FLOOR = "95e7a7979ae092703da8f77c4d897f703348a308"
OPERATION_CLASS = "L6AK_SUPERVISED_REAL_READ_SAFE_403_RECEIPT"
EVIDENCE_CLASS = "SUPERVISED_REAL_READ_EXECUTION_ATTEMPT_METADATA_ONLY_AUTH_BLOCKER"
RECALL_QUERY_LABEL = (
    "Memory Seam supervised metadata-only real-source read readiness source floor held "
    "surfaces denial-before-read"
)

SAFE_RECEIPT_TERMS = (
    "report-safe authorization blocker before returning any source items",
    "status codes, degraded booleans, denial labels, item counts, and next-frontier classification only",
    "does not include raw private content, raw source text, source-card text, source discovery output, credentials, auth secrets, environment values, callback/provider payloads, Runtime Registry payloads, persistence state, or private source identifiers",
)

BOUNDARY_TERMS = (
    "performs no retry",
    "no broader recall",
    "no index query",
    "no workspace scan",
    "no family scan",
    "no source discovery",
    "no source-card read",
    "no raw private content read",
    "no raw source text read",
    "no raw approval prose read",
    "no credential read",
    "no auth secret read",
    "no environment read",
    "no keychain read",
    "no OAuth read",
    "no auth-file read",
    "no Runtime Registry consumption",
    "no provider/backend/source-stat/source-read callback invocation",
    "no persistence",
    "no mutation",
    "no write",
    "no delete",
    "no reindex",
    "no cache purge",
    "no rollback execution",
    "no runtime cache mutation",
    "no service/listener/startup/global activation",
    "no cron change",
    "no publication",
    "no visibility change",
    "no provider/prod/canary/Gate movement",
    "no Atlas Gate movement",
    "no broad `allowed=true` behavior",
)

FORBIDDEN_REPORT_MARKERS = (
    "oauth token",
    "credential value",
    "auth-file secret",
    "private-correlation-ref",
    "source://",
    "platform-raw-id",
    "runtime registry payload value",
    "provider payload body value",
    "callback payload body value",
    "raw item body",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6ak01_doc_and_inventory_are_discoverable() -> None:
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6ak01-supervised-real-read-safe-403-receipt.md" in docs_index
    assert "tests/test_l6ak01_supervised_real_read_safe_403_receipt.py" in inventory
    assert "L6AK.01 supervised real-read execution attempt safe 403 receipt" in inventory
    assert STATUS in inventory


def test_l6ak01_records_issue_floor_operation_and_verdict() -> None:
    text = normalized(DOC)

    for term in (
        "# L6AK.01 supervised real-read execution attempt safe 403 receipt",
        f"Status: `{STATUS}`",
        "Rail issue: #341",
        "Parent issue: #6",
        "Roadmap step: 3 supervised real read with denial-before-read",
        f"Rail starting source floor: `{RAIL_STARTING_SOURCE_FLOOR}`",
        "Prior prep rail: L6AJ #331-#335 / PR #336-#340",
        "Jeremy explicitly authorized continuing toward real reads/writes in Discord",
        f"Operation class: `{OPERATION_CLASS}`",
        f"Evidence class: `{EVIDENCE_CLASS}`",
        "Verdict vocabulary: `PASS_SAFE_403_RECEIPT_AUTH_BLOCKER_CAPTURED_NO_ITEMS_RETURNED`, `BLOCKED_AUTH_ROUTE_AUDIENCE_BEFORE_ITEMS`, `ESCALATE_FOR_OWNER_BOUNDARY`.",
        f"Verdict: `{STATUS}`",
        f"Next-frontier classification: `{NEXT_FRONTIER}`",
    ):
        assert term in text

    for term in SAFE_RECEIPT_TERMS:
        assert term in text


def test_l6ak01_attempt_receipt_is_metadata_only_and_denied_before_items() -> None:
    text = normalized(DOC)

    for term in (
        "Attempt receipt",
        "`atlas-query MCP memory_seam_recall`",
        "`atlas-query MCP memory_seam_context`",
        "`sax`",
        "`wiki`",
        "`health`",
        "`turn`",
        f"`{RECALL_QUERY_LABEL}`",
        "`degraded=true`, `auth_status_code=403`",
        "`wrong_route_audience`",
        "`unauthorized_narrowing`",
        "Both attempts returned `items=[]`",
        "No raw/private/source item body was returned, inspected, copied, summarized, cached, persisted, or transformed.",
    ):
        assert term in text


def test_l6ak01_boundary_preserves_strict_no_retry_no_secret_no_mutation_posture() -> None:
    text = normalized(DOC)

    for term in BOUNDARY_TERMS:
        assert term in text

    lowered = text.lower()
    for marker in FORBIDDEN_REPORT_MARKERS:
        assert marker not in lowered


def test_l6ak01_auth_blocker_points_to_exact_route_audience_contract() -> None:
    text = normalized(DOC)

    for term in (
        "safe denial happened before any items were returned",
        "exact route-audience/service auth binding work rather than broader read permission or source expansion",
        "`wrong_route_audience` means the recall path did not have the exact audience binding required for Sax's supervised metadata-only read attempt",
        "`unauthorized_narrowing` means the context health path could not narrow into the requested report-safe turn/health view for Sax under the current auth posture",
        "`items=[]` and `auth_status_code=403` keep the rail in denial-before-read posture",
        "define and test non-secret `identity_subject`, `acting_for`, `agent`, `audience`, `scope`, output-mode, and stale/broadened-request semantics before any exact supervised retry",
    ):
        assert term in text


def test_l6ak01_retry_capability_matrix_keeps_retry_blocked_until_auth_binding() -> None:
    text = normalized(DOC)

    for term in (
        "Retry capability matrix",
        "Same agent `sax` | required",
        "Same scope `wiki` for recall | required",
        "Same query label or an owner-approved exact replacement | required",
        "Metadata-only/report-safe output | required",
        "Route audience binding implemented and verified | blocked pending #342/#343",
        "Denial-before-read for wrong audience or unauthorized narrowing | required",
        "Raw/private item output | forbidden",
        "Broader recall, source discovery, or index query | forbidden",
        "Persistence, mutation, write, delete, reindex, cache purge, rollback | forbidden",
        "Service activation, provider/prod/canary/Gate, Atlas Gate movement | forbidden",
    ):
        assert term in text


def test_l6ak01_closeout_and_verification_gate() -> None:
    text = normalized(DOC)

    for term in (
        "#341 should close after this receipt and its verifier merge",
        "The next open unblocked issue is #342, limited to docs/tests for route-audience auth binding semantics",
        "No live read retry is authorized by #341",
        "python -m pytest -q tests/test_l6ak01_supervised_real_read_safe_403_receipt.py",
        "python -m pytest -q",
        "python scripts/public_hygiene_scan.py",
        "git diff --check",
        "python -m compileall -q src tests examples",
    ):
        assert term in text
