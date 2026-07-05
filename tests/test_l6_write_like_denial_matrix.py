from __future__ import annotations

import pytest

from memory_seam.receipts import read_receipt_enabled
from memory_seam.router import route_request
from memory_seam.runtime import LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest, StaticIdentityVerifier
from memory_seam.providers import NullMemorySeamProvider


PRIVATE_MARKERS = (
    "super-secret-token",
    "/private/source.md",
    "platform-id-12345",
    "custody-ref-raw-abc",
)


def route_with_write_spies(method: str, target: str, *, request_body: dict | None = None):
    counters = {
        "health": 0,
        "context": 0,
        "recall": 0,
        "provider_reads": 0,
        "source_stats": 0,
        "backend_reads": 0,
        "custody_callbacks": 0,
        "reindex_callbacks": 0,
        "write_custody_or_reindex": False,
    }

    def health_handler():  # pragma: no cover - denial cases must not call this
        counters["health"] += 1
        return {"ok": True, "write_custody_or_reindex": False}

    def context_handler(**kwargs):  # pragma: no cover - denial cases must not call this
        counters["context"] += 1
        counters["provider_reads"] += 1
        return {"endpoint": "context", "items": [], "read_backend_called": False, "write_custody_or_reindex": False}

    def recall_handler(query: str, **kwargs):  # pragma: no cover - denial cases must not call this
        counters["recall"] += 1
        counters["provider_reads"] += 1
        return {"endpoint": "recall", "items": [], "read_backend_called": False, "write_custody_or_reindex": False}

    response = route_request(
        method,
        target,
        health_handler=health_handler,
        context_handler=context_handler,
        recall_handler=recall_handler,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context", "wiki"],
        request_body=request_body,
    )
    return response, counters


@pytest.mark.parametrize("target", ["/write", "/delete", "/reindex"])
def test_post_write_delete_reindex_routes_deny_before_any_callbacks(target: str):
    response, counters = route_with_write_spies(
        "POST",
        target,
        request_body={"secret": "super-secret-token", "path": "/private/source.md"},
    )

    assert response["status_code"] == 405
    assert response["body"]["error"] == "write_like_route_unavailable"
    assert response["body"]["write_custody_or_reindex"] is False
    assert counters == {
        "health": 0,
        "context": 0,
        "recall": 0,
        "provider_reads": 0,
        "source_stats": 0,
        "backend_reads": 0,
        "custody_callbacks": 0,
        "reindex_callbacks": 0,
        "write_custody_or_reindex": False,
    }


@pytest.mark.parametrize(
    ("method", "target"),
    [("PATCH", "/context?include=project"), ("PUT", "/recall?query=memory"), ("DELETE", "/health")],
)
def test_unsupported_methods_on_read_routes_deny_without_reads(method: str, target: str):
    response, counters = route_with_write_spies(method, target)

    assert response["status_code"] == 405
    assert response["body"]["error"] == "method_not_allowed"
    assert response["body"]["read_backend_called"] is False
    assert response["body"]["source_stat_called"] is False
    assert response["body"]["write_custody_or_reindex"] is False
    assert counters["provider_reads"] == 0
    assert counters["source_stats"] == 0
    assert counters["backend_reads"] == 0
    assert counters["custody_callbacks"] == 0
    assert counters["reindex_callbacks"] == 0


@pytest.mark.parametrize(
    ("target", "payload"),
    [
        ("/context?include=project", {"custody_receipt": "custody-ref-raw-abc", "private_path": "/private/source.md"}),
        ("/context?include=project&action=delete", {"note": "super-secret-token"}),
        ("/recall?query=memory", {"operation": "reindex", "platform_id": "platform-id-12345"}),
        ("/recall?query=memory&custody=true", {"query": "do not echo this"}),
    ],
)
def test_custody_like_payloads_on_read_routes_deny_report_safely(target: str, payload: dict[str, str]):
    response, counters = route_with_write_spies("GET", target, request_body=payload)

    assert response["status_code"] == 405
    body = response["body"]
    assert body["error"] == "write_like_payload_unavailable"
    assert body["write_custody_or_reindex"] is False
    rendered = repr(body)
    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    assert counters["provider_reads"] == 0
    assert counters["source_stats"] == 0
    assert counters["backend_reads"] == 0
    assert counters["custody_callbacks"] == 0
    assert counters["reindex_callbacks"] == 0


class CountingProvider(NullMemorySeamProvider):
    def __init__(self):
        self.context_calls = 0
        self.recall_calls = 0

    def context(self, **kwargs):  # pragma: no cover - denial cases must not call this
        self.context_calls += 1
        return super().context(**kwargs)

    def recall(self, query, **kwargs):  # pragma: no cover - denial cases must not call this
        self.recall_calls += 1
        return super().recall(query, **kwargs)


@pytest.mark.parametrize(
    "runtime_request",
    [
        RuntimeRequest("POST", "/write", body={"secret": "super-secret-token"}),
        RuntimeRequest("POST", "/delete", body={"path": "/private/source.md"}),
        RuntimeRequest("POST", "/reindex", body={"platform_id": "platform-id-12345"}),
        RuntimeRequest("GET", "/context?include=project", body={"custody": "custody-ref-raw-abc"}),
        RuntimeRequest("GET", "/recall?query=memory&operation=write"),
    ],
)
def test_runtime_write_like_denials_happen_before_provider_backend_or_custody(runtime_request: RuntimeRequest):
    provider = CountingProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(subject="agent:example", allowed_scopes=frozenset({"context", "wiki"})),
    )

    response = runtime.handle(runtime_request)

    assert response["status_code"] == 405
    assert response["body"]["runtime"]["write_custody_or_reindex"] is False
    assert provider.context_calls == 0
    assert provider.recall_calls == 0
    rendered = repr(response["body"])
    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
