from __future__ import annotations

import pytest

from memory_seam.adapters import (
    SAFE_SOURCE_CARD_ADAPTER_STATUS,
    SourceCardAdapter,
    SyntheticSourceCardAdapter,
    assert_source_card_is_report_safe,
    synthetic_safe_content_provider,
)
from memory_seam.receipts import build_read_receipt, read_receipt_enabled
from memory_seam.router import route_request


def test_synthetic_source_card_adapter_returns_sanitized_metadata_only_cards():
    adapter = SyntheticSourceCardAdapter()

    assert isinstance(adapter, SourceCardAdapter)
    cards = adapter.source_cards(include=["project", "memory"], token_subject="agent:example")

    assert {card["include_family"] for card in cards} == {"project", "memory"}
    rendered = repr(cards)
    assert "/" + "Users" + "/" not in rendered
    assert "session.jsonl" not in rendered
    assert "raw_transcript" not in rendered
    assert "content" not in cards[0]
    assert all(card["retrieval_backend"] == "metadata_only" for card in cards)
    assert all(card["safe_summary"] for card in cards)


def test_source_card_safety_guard_rejects_raw_paths_and_content_fields():
    with pytest.raises(ValueError, match="unsafe fields"):
        assert_source_card_is_report_safe(
            {
                "card_id": "bad-content",
                "include_family": "project",
                "safe_summary": "summary",
                "content": "raw private transcript text",
            }
        )

    with pytest.raises(ValueError, match="unsafe raw/private fragment"):
        assert_source_card_is_report_safe(
            {
                "card_id": "bad-path",
                "include_family": "project",
                "safe_summary": "summary",
                "title": "/" + "Users" + "/watson/private/source.md",
            }
        )


def test_context_envelope_carries_source_cards_into_usefulness_receipt_without_live_reads():
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
    assert body["source_card_adapter_status"] == SAFE_SOURCE_CARD_ADAPTER_STATUS
    assert body["source_card_adapter"] == "synthetic-source-card"
    assert {card["card_id"] for card in body["source_cards"]} == {
        "source-card-project-boundary",
        "source-card-runtime-answer",
    }
    assert body["read_backend_called"] is False
    assert body["raw_fallback_used"] is False
    assert "/" + "Users" + "/" not in repr(body["source_cards"])

    receipt = build_read_receipt(endpoint="context", token_subject="agent:example", timeout_ms=body["timeout_ms"], envelope=body)
    assert receipt["usefulness_shape"]["task_answerable_from_safe_content"] is True
    assert receipt["reportable_artifacts"]["content_hashes"]
