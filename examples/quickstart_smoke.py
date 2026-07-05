#!/usr/bin/env python3
"""README-level quickstart smoke for Memory Seam.

This example uses only the committed synthetic-safe provider. It performs no
local source discovery, no network calls, no live/private reads, no service
startup, and no write/custody/reindex behavior.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_seam import (
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
    synthetic_safe_content_provider,
)


def build_quickstart_runtime() -> LocalReadOnlyRuntime:
    """Return an enabled in-process runtime backed by synthetic safe content."""

    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="synthetic-safe-content"),
        provider=synthetic_safe_content_provider(),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:quickstart",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def quickstart_context() -> dict[str, Any]:
    """Answer a safe project/memory context question from synthetic fixtures."""

    runtime = build_quickstart_runtime()
    return runtime.handle(
        RuntimeRequest(
            "GET",
            "/context?include=project,memory&mode=quickstart&agent=quickstart&read_receipt=metadata_only",
        )
    )


def quickstart_recall() -> dict[str, Any]:
    """Answer a safe runtime-boundary recall question from synthetic fixtures."""

    runtime = build_quickstart_runtime()
    return runtime.handle(
        RuntimeRequest(
            "GET",
            "/recall?query=runtime+identity+rollback&scope=wiki&n=2&read_receipt=metadata_only",
        )
    )


def compact_summary(response: dict[str, Any]) -> dict[str, Any]:
    """Render stable, README-friendly proof without leaking full envelopes."""

    body = dict(response.get("body") or {})
    return {
        "status_code": response.get("status_code"),
        "endpoint": body.get("endpoint"),
        "items": [item.get("title") for item in body.get("items", [])],
        "safe_posture": {
            "read_backend_called": body.get("read_backend_called"),
            "service_started": body.get("service_started"),
            "runtime_registry_consumed": body.get("runtime_registry_consumed"),
            "raw_fallback_used": body.get("raw_fallback_used"),
            "write_custody_or_reindex": body.get("write_custody_or_reindex"),
        },
        "receipt_verdict": (body.get("read_receipt") or {}).get("usefulness_shape", {}).get("verdict"),
    }


def main() -> int:
    payload = {
        "context": compact_summary(quickstart_context()),
        "recall": compact_summary(quickstart_recall()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
