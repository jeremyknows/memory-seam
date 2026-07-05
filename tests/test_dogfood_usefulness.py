from __future__ import annotations

from memory_seam.adapters import (
    DOGFOOD_USEFULNESS_STATUS,
    SAFE_DOGFOOD_ITEMS,
    SYNTHETIC_USEFULNESS_RUBRIC_VERSION,
    SourceAdapter,
    SyntheticSafeContentAdapter,
    score_synthetic_usefulness,
    synthetic_safe_content_provider,
)
from memory_seam.receipts import build_read_receipt, read_receipt_enabled
from memory_seam.router import route_request


def test_synthetic_adapter_satisfies_source_adapter_protocol():
    adapter = SyntheticSafeContentAdapter()
    assert isinstance(adapter, SourceAdapter)
    items = adapter.context_items(include=["project"], token_subject="agent:example")
    assert items
    rendered = repr(items)
    assert "/" + "Users" + "/" not in rendered
    assert "gho_" not in rendered
    assert "raw_fallback" not in rendered


def test_context_dogfood_question_is_answerable_from_safe_content():
    provider = synthetic_safe_content_provider()
    response = route_request(
        "GET",
        "/context?include=project,memory&mode=dogfood&agent=sax&read_receipt=metadata_only",
        health_handler=provider.health,
        context_handler=provider.context,
        recall_handler=provider.recall,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context:project", "context:memory"],
    )
    assert response["status_code"] == 200
    body = response["body"]
    assert body["dogfood_usefulness_status"] == DOGFOOD_USEFULNESS_STATUS
    assert body["raw_fallback_used"] is False
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["write_custody_or_reindex"] is False
    assert any("public source" in item["snippet"] for item in body["items"])
    receipt = build_read_receipt(endpoint="context", token_subject="agent:example", timeout_ms=body["timeout_ms"], envelope=body)
    assert receipt["usefulness_shape"]["verdict"] == "useful"
    assert receipt["usefulness_shape"]["task_answerable_from_safe_content"] is True
    assert receipt["reportable_artifacts"]["content_hashes"]


def test_recall_dogfood_question_answers_runtime_boundary_without_raw_fallback():
    provider = synthetic_safe_content_provider()
    response = route_request(
        "GET",
        "/recall?query=runtime+identity+rollback&scope=wiki&n=2&read_receipt=metadata_only",
        health_handler=provider.health,
        context_handler=provider.context,
        recall_handler=provider.recall,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["wiki"],
    )
    assert response["status_code"] == 200
    body = response["body"]
    assert body["scope_effective"] == ["wiki"]
    assert body["raw_fallback_used"] is False
    assert any("identity verification is explicit" in item["snippet"] for item in body["items"])
    receipt = build_read_receipt(endpoint="recall", token_subject="agent:example", timeout_ms=body["timeout_ms"], envelope=body)
    assert receipt["read_backend_called"] is True
    assert receipt["usefulness_shape"]["reason_code"] == "safe_context_sufficient"
    assert receipt["flight_record"]["outcome"] == "answered_from_safe_context"


def test_synthetic_usefulness_rubric_passes_answerable_safe_content():
    score = score_synthetic_usefulness(SAFE_DOGFOOD_ITEMS)

    assert score["schema"] == SYNTHETIC_USEFULNESS_RUBRIC_VERSION
    assert score["verdict"] == "PASS"
    assert score["answerable"] is True
    assert score["safe"] is True
    assert score["too_degraded"] is False
    assert score["redaction_survived"] is False
    assert score["reason_codes"] == ["safe_context_sufficient"]


def test_synthetic_usefulness_rubric_holds_on_truncated_redaction_survival():
    redacted_item = {
        **SAFE_DOGFOOD_ITEMS[0],
        "snippet": "[redacted-token] Synthetic no-live/read-only boundary remains reportable.",
        "redaction_applied": True,
        "redaction_labels": ["token"],
        "truncated": True,
    }

    score = score_synthetic_usefulness([redacted_item])

    assert score["verdict"] == "HOLD"
    assert score["answerable"] is True
    assert score["safe"] is True
    assert score["too_degraded"] is False
    assert score["redaction_survived"] is True
    assert "redaction_survived" in score["reason_codes"]
    assert "safe_content_truncated" in score["reason_codes"]


def test_allowed_receipt_rollback_shape_revoke_grant_is_none():
    # PRISM B-1 Finding 5: both ternary branches were identical, so every
    # allowed receipt carried revocation advice. Verify the fix: allowed
    # grant_decision must produce revoke_grant=None.
    envelope = {
        "items": [
            {
                "id": "item-1",
                "scope": "context",
                "source_tier": "source_card_safe_detail",
                "backend": "synthetic",
                "retrieval_backend": "metadata_only",
                "canonicality": "safe_fixture",
                "private_class": "reportable_synthetic",
                "snippet": "Safe content for the operator.",
                "include_family": "project",
                "redaction_applied": False,
                "redaction_labels": [],
                "truncated": False,
            }
        ],
        "degraded": False,
        "degraded_reasons": [],
        "partial": False,
        "backend_latency_ms": 5,
        "source_age_seconds": 10,
    }
    receipt = build_read_receipt(
        endpoint="context",
        token_subject="agent:example",
        timeout_ms=1500,
        envelope=envelope,
    )
    assert receipt["grant_decision"] == "allowed"
    assert receipt["rollback_shape"]["revoke_grant"] is None


def test_denied_receipt_rollback_shape_revoke_grant_equals_grant_id():
    # PRISM B-1 Finding 5 companion: denied grant_decision must still carry
    # the grant_id so the operator knows which grant to revoke.
    envelope = {
        "items": [],
        "degraded": True,
        "degraded_reasons": ["unknown_source_family"],
        "partial": True,
        "backend_latency_ms": 0,
        "source_age_seconds": 0,
    }
    receipt = build_read_receipt(
        endpoint="context",
        token_subject="agent:example",
        timeout_ms=1500,
        envelope=envelope,
    )
    assert receipt["grant_decision"] == "denied"
    grant_id = receipt["grant_id"]
    assert grant_id is not None
    assert receipt["rollback_shape"]["revoke_grant"] == grant_id


def test_synthetic_usefulness_rubric_fails_when_too_degraded_or_unsafe():
    degraded = score_synthetic_usefulness([], degraded_reasons=["gbrain_timeout"])
    unsafe_snippet = "/Us" + "ers/example/.env"
    unsafe = score_synthetic_usefulness([{**SAFE_DOGFOOD_ITEMS[0], "snippet": unsafe_snippet}])
    erased = score_synthetic_usefulness(
        [
            {
                **SAFE_DOGFOOD_ITEMS[0],
                "snippet": "[redacted-token] [redacted-private-path]",
                "redaction_applied": True,
            }
        ]
    )

    assert degraded["verdict"] == "FAIL"
    assert degraded["too_degraded"] is True
    assert "too_degraded" in degraded["reason_codes"]
    assert unsafe["verdict"] == "FAIL"
    assert unsafe["safe"] is False
    assert "unsafe_fragment_detected" in unsafe["reason_codes"]
    assert erased["verdict"] == "FAIL"
    assert erased["redaction_survived"] is False
    assert "redaction_erased_answer" in erased["reason_codes"]
