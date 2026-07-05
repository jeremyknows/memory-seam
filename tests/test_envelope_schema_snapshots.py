from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memory_seam import (
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
    synthetic_safe_content_provider,
)

SNAPSHOT_PATH = Path(__file__).resolve().parent / "fixtures" / "envelope_schema_snapshots_v0.json"


def structural_json_shape(value: Any) -> Any:
    """Return a deterministic JSON-schema-like shape without volatile values."""

    if isinstance(value, dict):
        return {str(key): structural_json_shape(inner) for key, inner in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple)):
        return [structural_json_shape(inner) for inner in value]
    if isinstance(value, (set, frozenset)):
        return [structural_json_shape(inner) for inner in sorted(value)]
    if value is None:
        return "<null>"
    if isinstance(value, bool):
        return "<bool>"
    if isinstance(value, int):
        return "<int>"
    if isinstance(value, float):
        return "<float>"
    if isinstance(value, str):
        return "<str>"
    return f"<{type(value).__name__}>"


def snapshot_runtime() -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="synthetic-safe-content"),
        provider=synthetic_safe_content_provider(),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:snapshot",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def current_envelope_schema_snapshots() -> dict[str, Any]:
    runtime = snapshot_runtime()
    return {
        "schema_version": "memory_seam_envelope_schema_snapshots_v0",
        "snapshot_kind": "structural_json_shape",
        "health": structural_json_shape(runtime.handle(RuntimeRequest("GET", "/health"))),
        "context": structural_json_shape(
            runtime.handle(
                RuntimeRequest(
                    "GET",
                    "/context?include=project,memory&mode=snapshot&agent=snapshot&timeout_ms=250&read_receipt=metadata_only",
                )
            )
        ),
        "recall": structural_json_shape(
            runtime.handle(
                RuntimeRequest(
                    "GET",
                    "/recall?query=runtime+identity+rollback&scope=wiki&n=2&timeout_ms=250&read_receipt=metadata_only",
                )
            )
        ),
    }


def test_health_context_and_recall_envelope_schema_snapshots_do_not_drift():
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert current_envelope_schema_snapshots() == expected


def test_schema_snapshots_pin_runtime_and_read_receipt_shapes():
    snapshots = current_envelope_schema_snapshots()
    for name in ("health", "context", "recall"):
        assert snapshots[name]["status_code"] == "<int>"
        assert snapshots[name]["headers"] == {"content-type": "<str>"}
        assert "runtime" in snapshots[name]["body"]
        assert snapshots[name]["body"]["runtime"]["schema"] == "<str>"
        assert snapshots[name]["body"]["runtime"]["rollback"]["disable_runtime"] == "<bool>"

    for name in ("context", "recall"):
        body = snapshots[name]["body"]
        assert body["read_receipt"]["receipt_id"] == "<str>"
        assert body["read_receipt"]["mode"] == "<str>"
        assert body["read_receipt"]["audit_shape"]["schema"] == "<str>"
        assert body["read_receipt"]["rollback_shape"]["cache_purge_required"] == "<bool>"
        assert body["read_backend_called"] == "<bool>"
        assert body["live_backend_called"] == "<bool>"
        assert body["service_started"] == "<bool>"
        assert body["runtime_registry_consumed"] == "<bool>"
        assert body["write_custody_or_reindex"] == "<bool>"
