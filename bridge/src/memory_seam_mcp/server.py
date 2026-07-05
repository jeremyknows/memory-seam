"""MCP stdio bridge for Memory Seam local markdown reads."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlencode

from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version

from memory_seam_mcp import BRIDGE_VERSION, COMPATIBLE_CORE
from memory_seam.adapters import AdapterMemorySeamProvider
from memory_seam.contracts import MAX_QUERY_CHARS as CORE_MAX_QUERY_CHARS
from memory_seam.contracts import MAX_RECALL_N as CORE_MAX_RECALL_N
from memory_seam.local_adapters.markdown import LocalMarkdownAdapter
from memory_seam.runtime import LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest, StaticIdentityVerifier

BRIDGE_NAME = "memory-seam-mcp"
BRIDGE_STATUS = "user_started_stdio_bridge"
PROVIDER_NAME = "local-markdown-mcp"
AGENT_SUBJECT = "agent:memory-seam-mcp"
READ_RECEIPT_QUERY_VALUE = "metadata_only"

SAFE_POSTURE_KEYS = (
    "read_backend_called",
    "service_started",
    "runtime_registry_consumed",
    "raw_fallback_used",
    "write_custody_or_reindex",
)
CORE_DISTRIBUTION = "memory-seam"
CORE_MODULE = "memory_seam"
ALLOW_INCOMPATIBLE_ENV = "MEMORY_SEAM_MCP_ALLOW_INCOMPATIBLE"
MAX_QUERY_CHARS = CORE_MAX_QUERY_CHARS
MAX_QUERY_TERMS = 100
MIN_RECALL_N = 1
MAX_RECALL_N = CORE_MAX_RECALL_N
QUERY_TERM_RE = re.compile(r"\S+")


@dataclass(frozen=True)
class BridgeConfig:
    root: Path
    adapter: str = "markdown"


def build_runtime(root: str | Path) -> LocalReadOnlyRuntime:
    """Build the in-process, read-only local markdown runtime."""

    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name=PROVIDER_NAME),
        provider=AdapterMemorySeamProvider(
            LocalMarkdownAdapter(root),
            provider_name=PROVIDER_NAME,
        ),
        identity_verifier=StaticIdentityVerifier(
            subject=AGENT_SUBJECT,
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def check_core_compatibility() -> None:
    """Fail when the installed core is outside the declared bridge range."""

    core_version = _installed_core_version()
    compatible = _version_satisfies(core_version, COMPATIBLE_CORE)
    if compatible:
        return
    message = (
        f"{BRIDGE_NAME}: installed {CORE_DISTRIBUTION} {core_version} is outside "
        f"bridge {BRIDGE_VERSION} compatible core range {COMPATIBLE_CORE}"
    )
    if os.environ.get(ALLOW_INCOMPATIBLE_ENV) == "1":
        print(f"WARNING: {message}; continuing because {ALLOW_INCOMPATIBLE_ENV}=1", file=sys.stderr)
        return
    raise RuntimeError(f"{message}; set {ALLOW_INCOMPATIBLE_ENV}=1 to override intentionally")


def _installed_core_version() -> str:
    try:
        return metadata.version(CORE_DISTRIBUTION)
    except metadata.PackageNotFoundError:
        module = __import__(CORE_MODULE)
        return str(getattr(module, "__version__", "0.0.0"))


def _version_satisfies(version: str, spec: str) -> bool:
    try:
        return Version(version) in SpecifierSet(spec)
    except InvalidVersion as exc:
        raise RuntimeError(f"{BRIDGE_NAME}: installed {CORE_DISTRIBUTION} version is invalid: {version}") from exc


def memory_seam_health_envelope(runtime: LocalReadOnlyRuntime) -> dict[str, Any]:
    """Return runtime health with bridge posture metadata."""

    return _with_bridge_posture(runtime.handle(RuntimeRequest("GET", "/health")))


def memory_seam_context_envelope(
    runtime: LocalReadOnlyRuntime,
    *,
    include: list[str] | None = None,
) -> dict[str, Any]:
    """Return the full Memory Seam context envelope."""

    include_value = ",".join(include or ["memory"])
    target = "/context?" + urlencode(
        {
            "include": include_value,
            "mode": "startup",
            "agent": AGENT_SUBJECT,
            "read_receipt": READ_RECEIPT_QUERY_VALUE,
        }
    )
    return _with_bridge_posture(runtime.handle(RuntimeRequest("GET", target)))


def memory_seam_recall_envelope(
    runtime: LocalReadOnlyRuntime,
    *,
    query: Any,
    n: Any = 5,
) -> dict[str, Any]:
    """Return the full Memory Seam recall envelope."""

    validation = _validate_recall_input(query=query, n=n)
    if validation["error"] is not None:
        return _bridge_error_envelope(400, validation["error"], validation["message"])
    safe_query = validation["query"]
    safe_n = validation["n"]
    target = "/recall?" + urlencode(
        {
            "query": safe_query,
            "scope": "wiki",
            "n": safe_n,
            "agent": AGENT_SUBJECT,
            "read_receipt": READ_RECEIPT_QUERY_VALUE,
        }
    )
    return _with_bridge_posture(runtime.handle(RuntimeRequest("GET", target)))


def _validate_recall_input(*, query: Any, n: Any) -> dict[str, Any]:
    if not isinstance(query, str):
        return _validation_error("invalid_query_type", "query must be a string")
    if len(query) > MAX_QUERY_CHARS:
        return _validation_error(
            "query_too_long",
            f"query must be {MAX_QUERY_CHARS} characters or fewer",
        )
    term_count = len(QUERY_TERM_RE.findall(query.strip()))
    if term_count > MAX_QUERY_TERMS:
        return _validation_error(
            "query_too_many_terms",
            f"query must contain {MAX_QUERY_TERMS} terms or fewer",
        )
    if isinstance(n, bool) or not isinstance(n, int):
        return _validation_error("invalid_n_type", "n must be an integer")
    return {"query": query, "n": min(max(n, MIN_RECALL_N), MAX_RECALL_N), "error": None, "message": None}


def _validation_error(error: str, message: str) -> dict[str, Any]:
    return {"query": "", "n": 0, "error": error, "message": message}


def _bridge_error_envelope(status_code: int, error: str, message: str) -> dict[str, Any]:
    return _with_bridge_posture(
        {
            "status_code": status_code,
            "body": {
                "endpoint": "recall",
                "error": error,
                "message": message,
                "contract_status": "bridge_input_rejected",
            },
        }
    )


def _with_bridge_posture(envelope: dict[str, Any]) -> dict[str, Any]:
    body = dict(envelope.get("body") or {})
    bridge = {
        "name": BRIDGE_NAME,
        "status": BRIDGE_STATUS,
        "transport": "stdio",
        "user_started": True,
        "socket_bound": False,
        "daemon": False,
        "auto_start": False,
        "credential_reads": False,
        "global_config_mutation": False,
        "read_only": True,
    }
    return {
        **envelope,
        "body": body,
        "bridge": bridge,
        "safe_posture": _safe_posture(body),
    }


def _safe_posture(body: dict[str, Any]) -> dict[str, bool]:
    return {key: bool(body.get(key)) for key in SAFE_POSTURE_KEYS}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memory-seam-mcp",
        description="User-started MCP stdio bridge for Memory Seam local markdown reads.",
    )
    parser.add_argument(
        "--root",
        "--notes",
        dest="root",
        default=os.environ.get("MEMORY_SEAM_ROOT"),
        help="Local notes folder to read (--notes is an accepted alias). May also be set with MEMORY_SEAM_ROOT.",
    )
    parser.add_argument(
        "--adapter",
        choices=("markdown",),
        default=os.environ.get("MEMORY_SEAM_ADAPTER", "markdown"),
        help="Local adapter to use. Only markdown is supported.",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print report-safe bridge config and exit without starting MCP stdio.",
    )
    return parser


def parse_config(argv: Sequence[str] | None = None) -> tuple[BridgeConfig, bool]:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.root:
        parser.error("--root or MEMORY_SEAM_ROOT is required")
    return BridgeConfig(root=Path(args.root).expanduser(), adapter=args.adapter), bool(args.print_config)


def run_stdio_bridge(config: BridgeConfig) -> int:
    """Run the FastMCP stdio bridge."""

    from mcp.server.fastmcp import FastMCP  # noqa: PLC0415

    runtime = build_runtime(config.root)
    server = FastMCP(BRIDGE_NAME)

    @server.tool(name="memory_seam_health", description="Memory Seam local markdown health envelope.")
    def memory_seam_health() -> dict[str, Any]:
        return memory_seam_health_envelope(runtime)

    @server.tool(name="memory_seam_context", description="Memory Seam local markdown context envelope.")
    def memory_seam_context(include: list[str] | None = None) -> dict[str, Any]:
        return memory_seam_context_envelope(runtime, include=include)

    @server.tool(name="memory_seam_recall", description="Memory Seam local markdown recall envelope.")
    def memory_seam_recall(query: Any, n: Any = 5) -> dict[str, Any]:
        return memory_seam_recall_envelope(runtime, query=query, n=n)

    server.run()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    config, print_config = parse_config(argv)
    check_core_compatibility()
    if print_config:
        payload = {
            "bridge": BRIDGE_NAME,
            "status": BRIDGE_STATUS,
            "root": str(config.root),
            "adapter": config.adapter,
            "transport": "stdio",
            "socket_bound": False,
            "daemon": False,
            "auto_start": False,
            "credential_reads": False,
            "global_config_mutation": False,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    return run_stdio_bridge(config)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
