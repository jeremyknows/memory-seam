from __future__ import annotations

import memory_seam
from memory_seam import (
    MemorySeamProvider,
    NullMemorySeamProvider,
    provider_handlers,
    read_receipt_enabled,
    route_request,
)


def test_public_api_exports_core_provider_contracts():
    exported = set(memory_seam.__all__)
    expected = {
        "CONTRACT_STATUS",
        "ContextProvider",
        "HealthProvider",
        "MemorySeamProvider",
        "NullMemorySeamProvider",
        "RecallProvider",
        "provider_handlers",
        "route_request",
        "SubjectPolicy",
        "ContextSourceDescriptor",
        "build_read_receipt",
        "build_runtime_audit_receipt",
    }
    assert expected <= exported
    for name in expected:
        assert getattr(memory_seam, name)


def test_null_provider_satisfies_runtime_protocol_without_live_reads():
    provider = NullMemorySeamProvider()
    assert isinstance(provider, MemorySeamProvider)

    health = provider.health()
    assert health["provider"] == "null"
    assert health["read_backend_called"] is False
    assert health["service_started"] is False
    assert health["runtime_registry_consumed"] is False
    assert health["write_custody_or_reindex"] is False


def test_route_request_can_use_provider_handlers_for_context_schema():
    provider = NullMemorySeamProvider()
    response = route_request(
        "GET",
        "/context?include=project&mode=startup&agent=reference-agent&read_receipt=metadata_only",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:reference-agent",
        allowed_scopes=["context:project"],
    )

    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["include_requested"] == ["project"]
    assert body["items"] == []
    assert body["degraded_reasons"] == ["provider_unconfigured"]
    assert body["read_receipt_requested"] is True
    assert body["read_backend_called"] is False


def test_route_request_can_use_provider_handlers_for_recall_schema():
    provider = NullMemorySeamProvider(provider_name="test-null")
    response = route_request(
        "GET",
        "/recall?query=safe+synthetic+question&scope=wiki&n=3&timeout_ms=900",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:reference-agent",
        allowed_scopes=["wiki"],
    )

    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "recall"
    assert body["provider"] == "test-null"
    assert body["query"] == "safe synthetic question"
    assert body["scope_requested"] == "wiki"
    assert body["n"] == 3
    assert body["items"] == []
    assert body["read_backend_called"] is False
