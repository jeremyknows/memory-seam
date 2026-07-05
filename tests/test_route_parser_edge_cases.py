from __future__ import annotations

import pytest

from memory_seam.contracts import MAX_TIMEOUT_MS, MIN_TIMEOUT_MS
from memory_seam.receipts import read_receipt_enabled
from memory_seam.router import route_request


def route_with_captures(method: str, target: str):
    calls: dict[str, list] = {"health": [], "context": [], "recall": []}

    def health_handler():
        calls["health"].append({})
        return {"ok": True}

    def context_handler(**kwargs):
        calls["context"].append(kwargs)
        return {"endpoint": "context", "kwargs": kwargs}

    def recall_handler(query: str, **kwargs):
        calls["recall"].append({"query": query, **kwargs})
        return {"endpoint": "recall", "query": query, "kwargs": kwargs}

    response = route_request(
        method,
        target,
        health_handler=health_handler,
        context_handler=context_handler,
        recall_handler=recall_handler,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context", "recall"],
    )
    return response, calls


def test_repeated_query_params_use_first_value_and_preserve_csv_parsing():
    response, calls = route_with_captures(
        "GET",
        "/context?include=project,soul&include=wiki&mode=startup&mode=override&agent=sax&agent=watson",
    )

    assert response["status_code"] == 200
    kwargs = calls["context"][-1]
    assert kwargs["include"] == ["project", "soul"]
    assert kwargs["mode"] == "startup"
    assert kwargs["agent"] == "sax"


def test_empty_context_query_uses_documented_defaults():
    response, calls = route_with_captures("GET", "/context?")

    assert response["status_code"] == 200
    kwargs = calls["context"][-1]
    assert kwargs["include"] == []
    assert kwargs["mode"] == "startup"
    assert kwargs["agent"] is None
    assert kwargs["timeout_ms"] == 1500
    assert kwargs["include_read_receipt"] is False


@pytest.mark.parametrize(
    ("target", "expected_timeout"),
    [
        ("/context?timeout_ms=1", MIN_TIMEOUT_MS),
        (f"/context?timeout_ms={MAX_TIMEOUT_MS + 1000}", MAX_TIMEOUT_MS),
        ("/recall?query=runtime&timeout_ms=1", MIN_TIMEOUT_MS),
        (f"/recall?query=runtime&timeout_ms={MAX_TIMEOUT_MS + 1000}", MAX_TIMEOUT_MS),
    ],
)
def test_timeout_params_are_clamped_for_context_and_recall(target: str, expected_timeout: int):
    response, calls = route_with_captures("GET", target)

    assert response["status_code"] == 200
    called = calls["context"][-1] if calls["context"] else calls["recall"][-1]
    assert called["timeout_ms"] == expected_timeout


def test_unknown_route_returns_404_without_calling_handlers():
    response, calls = route_with_captures("GET", "/unknown?query=runtime")

    assert response["status_code"] == 404
    assert response["body"]["error"] == "route_not_found"
    assert calls == {"health": [], "context": [], "recall": []}


@pytest.mark.parametrize(
    ("method", "target"),
    [("POST", "/diary/append"), ("POST", "/wiki/publish"), ("POST", "/reindex")],
)
def test_explicit_write_like_routes_return_405_before_read_handlers(method: str, target: str):
    response, calls = route_with_captures(method, target)

    assert response["status_code"] == 405
    assert response["body"]["error"] == "write_like_route_unavailable"
    assert calls == {"health": [], "context": [], "recall": []}


@pytest.mark.parametrize("method", ["HEAD", "POST", "PUT", "PATCH", "DELETE"])
def test_non_get_read_route_returns_method_not_allowed_without_handlers(method: str):
    response, calls = route_with_captures(method, "/health")

    assert response["status_code"] == 405
    assert response["body"]["error"] == "method_not_allowed"
    assert calls == {"health": [], "context": [], "recall": []}


def test_bad_integer_query_param_returns_bad_request():
    response, calls = route_with_captures("GET", "/recall?query=runtime&n=not-an-int")

    assert response["status_code"] == 400
    assert response["body"]["error"] == "bad_request"
    assert calls == {"health": [], "context": [], "recall": []}
