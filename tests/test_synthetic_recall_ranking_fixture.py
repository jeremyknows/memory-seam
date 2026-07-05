from __future__ import annotations

from memory_seam.adapters import (
    SAFE_DOGFOOD_ITEMS,
    SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION,
    SyntheticSafeContentAdapter,
    rank_synthetic_recall_items,
)


def test_synthetic_recall_ranking_orders_by_query_relevance_then_stable_tiebreak():
    items = (
        {
            "id": "zeta-runtime",
            "scope": "wiki",
            "title": "Runtime rollback note",
            "snippet": "Runtime rollback keeps identity checks explicit.",
        },
        {
            "id": "alpha-runtime",
            "scope": "wiki",
            "title": "Runtime identity rollback",
            "snippet": "Runtime identity rollback proof is metadata-only.",
        },
        {
            "id": "project-boundary",
            "scope": "context",
            "title": "Project boundary",
            "snippet": "Synthetic no-live/read-only boundary remains reportable.",
        },
    )

    ranked = rank_synthetic_recall_items(items, "runtime identity rollback", n=3)

    assert ranked["schema"] == SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION
    assert ranked["raw_fallback_used"] is False
    assert ranked["read_backend_called"] is False
    assert ranked["service_started"] is False
    assert ranked["runtime_registry_consumed"] is False
    assert ranked["write_custody_or_reindex"] is False
    assert [item["id"] for item in ranked["items"]] == ["alpha-runtime", "zeta-runtime"]
    assert ranked["items"][0]["ranking_score"] > ranked["items"][1]["ranking_score"]
    assert ranked["items"][0]["ranking_reason"] == "term_match"


def test_synthetic_recall_ranking_tiebreaks_deterministically_by_title():
    items = (
        {"id": "b", "scope": "wiki", "title": "Zulu rollback", "snippet": "rollback"},
        {"id": "a", "scope": "wiki", "title": "Alpha rollback", "snippet": "rollback"},
    )

    first = rank_synthetic_recall_items(items, "rollback", n=2)
    second = rank_synthetic_recall_items(tuple(reversed(items)), "rollback", n=2)

    assert [item["id"] for item in first["items"]] == ["a", "b"]
    assert [item["id"] for item in second["items"]] == ["a", "b"]


def test_synthetic_adapter_recall_uses_ranking_fixture_and_limits_results():
    adapter = SyntheticSafeContentAdapter(items=SAFE_DOGFOOD_ITEMS)

    results = adapter.recall_items("runtime identity rollback", scope="wiki", token_subject="agent:example", n=1)

    assert len(results) == 1
    assert results[0]["id"] == "safe-dogfood-runtime-answer"
    assert "ranking_score" not in results[0]
    assert "ranking_reason" not in results[0]


def test_synthetic_recall_ranking_reports_degraded_empty_result_without_live_fallback():
    ranked = rank_synthetic_recall_items(SAFE_DOGFOOD_ITEMS, "nonexistent-topic", n=2)

    assert ranked["items"] == []
    assert ranked["item_count"] == 0
    assert ranked["degraded"] is False
    assert ranked["degraded_reasons"] == []
    assert ranked["raw_fallback_used"] is False
    assert ranked["read_backend_called"] is False
