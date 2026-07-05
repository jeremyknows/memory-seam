"""Minimal no-live CLI for Memory Seam synthetic smoke checks."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .adapters import synthetic_safe_content_provider
from .providers import provider_handlers
from .receipts import read_receipt_enabled
from .router import route_request

CLI_STATUS = "minimal_no_live_synthetic_smoke_cli"
CLI_HELD_SURFACES = (
    "daemon_or_listener",
    "live_source_reads",
    "runtime_registry_consumption",
    "global_config_mutation",
    "write_like_routes",
    "custody_or_reindex",
)


def no_live_response(endpoint: str, *, include: str, mode: str, agent: str | None, query: str, scope: str, n: int) -> dict[str, Any]:
    """Route one health/context/recall smoke request through committed fixtures only."""

    provider = synthetic_safe_content_provider()
    if endpoint == "health":
        target = "/health"
    elif endpoint == "context":
        target = f"/context?include={include}&mode={mode}"
        if agent:
            target += f"&agent={agent}"
    elif endpoint == "recall":
        target = f"/recall?query={query}&scope={scope}&n={n}"
        if agent:
            target += f"&agent={agent}"
    else:  # Defensive: argparse prevents this branch for CLI calls.
        raise ValueError(f"unsupported no-live CLI endpoint: {endpoint}")

    response = route_request(
        "GET",
        target,
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject=agent,
        allowed_scopes=["context", "wiki", "diary"],
    )
    body = dict(response.get("body") or {})
    body["cli"] = {
        "status": CLI_STATUS,
        "synthetic_fixtures_only": True,
        "service_started": False,
        "live_source_reads": False,
        "runtime_registry_consumed": False,
        "write_like_routes_available": False,
        "write_custody_or_reindex": False,
        "held_surfaces": list(CLI_HELD_SURFACES),
    }
    return {**response, "body": body}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memory-seam",
        description="Run no-live Memory Seam smoke checks against committed synthetic fixtures only.",
    )
    subparsers = parser.add_subparsers(dest="endpoint", required=True)

    health = subparsers.add_parser("health", help="emit synthetic provider health JSON")
    health.set_defaults(include="project", mode="startup", agent=None, query="", scope="wiki", n=5)

    context = subparsers.add_parser("context", help="emit synthetic context JSON")
    context.add_argument("--include", default="project", choices=("project", "memory", "project,memory"))
    context.add_argument("--mode", default="startup")
    context.add_argument("--agent", default="agent:memory-seam-cli")
    context.set_defaults(query="", scope="wiki", n=5)

    recall = subparsers.add_parser("recall", help="emit synthetic recall JSON")
    recall.add_argument("--query", default="runtime boundary")
    recall.add_argument("--scope", default="wiki", choices=("wiki", "diary", "context", "all"))
    recall.add_argument("--n", default=5, type=int)
    recall.add_argument("--agent", default="agent:memory-seam-cli")
    recall.set_defaults(include="project", mode="startup")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = no_live_response(
        args.endpoint,
        include=args.include,
        mode=args.mode,
        agent=args.agent,
        query=args.query,
        scope=args.scope,
        n=args.n,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if int(payload.get("status_code", 1)) < 400 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = ["CLI_HELD_SURFACES", "CLI_STATUS", "build_parser", "main", "no_live_response"]
