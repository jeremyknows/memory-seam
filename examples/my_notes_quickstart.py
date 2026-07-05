#!/usr/bin/env python3
"""Run Memory Seam recall over a local folder of markdown notes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from examples.local_markdown_provider import LocalMarkdownProvider
from memory_seam import (
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)


DEMO_NOTES = {
    "memory-seam.md": """# Memory Seam onboarding

Memory Seam gives agents receipt-first recall over local markdown notes. The
runtime checks authority before the provider scans files.
""",
    "launch-plan.md": """# Launch plan

The launch demo should prove local notes can be searched without a service,
network call, or write-side index.
""",
    "recipes/pasta.md": """# Weeknight pasta

Tomato sauce, garlic, basil, and a short grocery list. This note should not win
for authority and receipt queries.
""",
}


def ensure_demo_notes(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for relative, content in DEMO_NOTES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def build_runtime(notes_root: Path) -> LocalReadOnlyRuntime:
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="local-markdown-demo"),
        provider=AdapterMemorySeamProvider(
            LocalMarkdownProvider(notes_root),
            provider_name="local-markdown-demo",
        ),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:local-notes-demo",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def run_recall(notes_root: Path, query: str = "authority receipt local notes") -> dict[str, Any]:
    runtime = build_runtime(notes_root)
    return runtime.handle(
        RuntimeRequest(
            "GET",
            f"/recall?query={query.replace(' ', '+')}&scope=wiki&n=3&read_receipt=metadata_only",
        )
    )


def compact_summary(response: dict[str, Any]) -> dict[str, Any]:
    body = dict(response.get("body") or {})
    return {
        "status_code": response.get("status_code"),
        "endpoint": body.get("endpoint"),
        "provider": body.get("provider"),
        "items": [
            {
                "title": item.get("title"),
                "path": item.get("path"),
                "snippet": item.get("snippet"),
            }
            for item in body.get("items", [])
        ],
        "safe_posture": {
            "read_backend_called": body.get("read_backend_called"),
            "service_started": body.get("service_started"),
            "runtime_registry_consumed": body.get("runtime_registry_consumed"),
            "raw_fallback_used": body.get("raw_fallback_used"),
            "write_custody_or_reindex": body.get("write_custody_or_reindex"),
        },
        "receipt_verdict": (body.get("read_receipt") or {}).get("usefulness_shape", {}).get("verdict"),
        "receipt_reason": (body.get("read_receipt") or {}).get("usefulness_shape", {}).get("reason_code"),
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    notes_root = Path(args[0]).expanduser() if args else ROOT / "demo-notes"
    if not args:
        ensure_demo_notes(notes_root)
    response = run_recall(notes_root)
    print(json.dumps(compact_summary(response), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
