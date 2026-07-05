from __future__ import annotations

from memory_seam.adapters import SourceCard, score_synthetic_usefulness
from memory_seam.receipts import build_read_receipt, read_receipt_enabled
from memory_seam.router import route_request


def route_with_spies(method: str, target: str, *, receipt_parser=read_receipt_enabled):
    calls: dict[str, int] = {
        "health": 0,
        "context": 0,
        "recall": 0,
        "provider_reads": 0,
        "source_stats": 0,
        "backend_reads": 0,
    }

    def health_handler():
        calls["health"] += 1
        return {"ok": True}

    def context_handler(**kwargs):
        calls["context"] += 1
        return {
            "endpoint": "context",
            "items": [],
            "degraded": False,
            "degraded_reasons": [],
            "read_backend_called": False,
            "raw_fallback_used": False,
            "kwargs": kwargs,
        }

    def recall_handler(query: str, **kwargs):
        calls["recall"] += 1
        return {
            "endpoint": "recall",
            "query": query,
            "items": [],
            "degraded": False,
            "degraded_reasons": [],
            "read_backend_called": False,
            "raw_fallback_used": False,
            "kwargs": kwargs,
        }

    response = route_request(
        method,
        target,
        health_handler=health_handler,
        context_handler=context_handler,
        recall_handler=recall_handler,
        read_receipt_enabled=receipt_parser,
        token_subject="agent:example",
        allowed_scopes=["context:project", "recall:wiki"],
    )
    return response, calls


def test_malformed_unknown_and_blank_read_receipt_values_do_not_enable_receipts():
    for value in ("", "raw", "metadata_only,raw", "true", "metadata only", "../../metadata_only"):
        response, calls = route_with_spies("GET", f"/context?include=project&read_receipt={value}")

        assert response["status_code"] == 200
        assert response["body"]["kwargs"]["include_read_receipt"] is False
        assert calls["provider_reads"] == 0
        assert calls["source_stats"] == 0
        assert calls["backend_reads"] == 0


def test_repeated_read_receipt_params_use_first_value_without_backend_side_effects():
    response, calls = route_with_spies(
        "GET",
        "/recall?query=runtime&read_receipt=raw&read_receipt=metadata_only",
    )

    assert response["status_code"] == 200
    assert response["body"]["kwargs"]["include_read_receipt"] is False
    assert calls["recall"] == 1
    assert calls["provider_reads"] == 0
    assert calls["source_stats"] == 0
    assert calls["backend_reads"] == 0

    response, calls = route_with_spies(
        "GET",
        "/recall?query=runtime&read_receipt=metadata_only&read_receipt=raw",
    )

    assert response["status_code"] == 200
    assert response["body"]["kwargs"]["include_read_receipt"] is True
    assert calls["recall"] == 1
    assert calls["provider_reads"] == 0
    assert calls["source_stats"] == 0
    assert calls["backend_reads"] == 0


def test_unexpected_endpoint_and_method_denials_happen_before_handlers_or_reads():
    for method, target, expected_status, expected_error in (
        ("GET", "/fly?query=runtime", 404, "route_not_found"),
        ("POST", "/context?include=project", 405, "method_not_allowed"),
        ("DELETE", "/recall?query=runtime", 405, "method_not_allowed"),
        ("POST", "/reindex?source=project", 405, "write_like_route_unavailable"),
    ):
        response, calls = route_with_spies(method, target)

        assert response["status_code"] == expected_status
        assert response["body"]["error"] == expected_error
        assert calls == {
            "health": 0,
            "context": 0,
            "recall": 0,
            "provider_reads": 0,
            "source_stats": 0,
            "backend_reads": 0,
        }


def test_bad_numeric_params_deny_before_recall_handler_or_reads():
    response, calls = route_with_spies("GET", "/recall?query=runtime&n=not-a-number")

    assert response["status_code"] == 400
    assert response["body"]["error"] == "bad_request"
    assert calls == {
        "health": 0,
        "context": 0,
        "recall": 0,
        "provider_reads": 0,
        "source_stats": 0,
        "backend_reads": 0,
    }


def test_source_card_redaction_survives_when_safe_summary_remains_answerable():
    card = SourceCard(
        card_id="source-card-redacted-safe-detail",
        include_family="project",
        source_tier="source_card_safe_detail",
        private_class="reportable_synthetic",
        canonicality="safe_fixture",
        retrieval_backend="metadata_only",
        title="Redacted safe-detail card",
        safe_summary="[redacted-private-path] Memory Seam remains no-live/read-only with held write custody.",
        redaction_applied=True,
        redaction_labels=("private_path",),
    ).to_safe_detail()

    assert card["redaction_applied"] is True
    assert card["redaction_labels"] == ["private_path"]
    assert "Memory Seam remains no-live/read-only" in card["safe_summary"]

    usefulness = score_synthetic_usefulness(
        [
            {
                "snippet": "[redacted-private-path] Memory Seam remains no-live/read-only with held write custody.",
                "redaction_applied": True,
                "redaction_labels": ["private_path"],
            }
        ]
    )
    assert usefulness["verdict"] == "PASS"
    assert usefulness["redaction_survived"] is True
    assert "redaction_survived" in usefulness["reason_codes"]


def test_read_receipt_withholds_content_artifacts_for_redacted_or_degraded_safe_detail():
    envelope = {
        "items": [
            {
                "scope": "context",
                "source_tier": "source_card_safe_detail",
                "backend": "synthetic_safe_content",
                "retrieval_backend": "metadata_only",
                "canonicality": "safe_fixture",
                "private_class": "reportable_synthetic",
                "snippet": "[redacted-token] Useful no-live project boundary summary survives.",
                "redaction_applied": True,
                "redaction_labels": ["token"],
                "truncated": False,
            }
        ],
        "include_requested": ["project"],
        "include_effective": ["project"],
        "degraded": True,
        "degraded_reasons": ["provider_unconfigured"],
        "partial": True,
        "read_backend_called": False,
        "raw_fallback_used": False,
    }

    receipt = build_read_receipt(
        endpoint="context",
        token_subject="agent:example",
        timeout_ms=1500,
        envelope=envelope,
    )

    assert receipt["grant_decision"] == "allowed"
    assert receipt["read_backend_called"] is True
    assert receipt["response_shape"]["degraded"] is True
    assert receipt["response_shape"]["degraded_reasons"] == ["provider_unconfigured"]
    assert receipt["safety_shape"]["redaction_labels"] == ["token"]
    assert receipt["reportable_artifacts"]["content_hashes"] == []
    assert receipt["reportable_artifacts"]["byte_counts"] == []
    assert receipt["reportable_artifacts"]["label_counts"]["degraded:provider_unconfigured"] == 1
    assert receipt["reportable_artifacts"]["label_counts"]["redaction:token"] == 1


def test_unsafe_reportable_fragments_remain_rejected_after_redaction_placeholder_allowlist():
    for unsafe_summary in (
        "Raw transcript marker raw_transcript must not pass.",
        "Token-like gho_example must not pass.",
        "/" + "Users" + "/example/private/source.md must not pass.",
    ):
        try:
            SourceCard(
                card_id="unsafe-card",
                include_family="project",
                source_tier="source_card_safe_detail",
                private_class="reportable_synthetic",
                canonicality="safe_fixture",
                retrieval_backend="metadata_only",
                title="Unsafe card",
                safe_summary=unsafe_summary,
                redaction_applied=True,
                redaction_labels=("private_path",),
            ).to_safe_detail()
        except ValueError as exc:
            assert "unsafe raw/private fragment" in str(exc)
        else:  # pragma: no cover - explicit guard failure message for this contract
            raise AssertionError("unsafe reportable fragment was accepted")
