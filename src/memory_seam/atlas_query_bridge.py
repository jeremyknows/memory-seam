"""Atlas Query bridge helpers for package-based Memory Seam adoption.

The bridge in this module is deliberately adapter-only. It gives Atlas Query a
small import target that can be consumed from an editable/path dependency while
adapter-owned backends stay downstream. It does not discover local paths, start
services, read runtime registries, mutate client config, or perform live source
reads by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .policy import policy
from .providers import MemorySeamProvider, NullMemorySeamProvider, provider_handlers
from .receipts import read_receipt_enabled
from .router import route_request

ATLAS_QUERY_BRIDGE_STATUS = "adapter_bridge_package_dependency_ready"
ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA = "atlas-query-bridge-contract"
ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR = 1
ATLAS_QUERY_BRIDGE_CONTRACT_VERSION = f"{ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA}/v{ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR}"
ATLAS_QUERY_BRIDGE_CONTRACT_COMPATIBILITY = {
    "schema": ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA,
    "major": ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR,
    "version": ATLAS_QUERY_BRIDGE_CONTRACT_VERSION,
    "package_min_version": "0.1.0",
    "package_max_major": "0",
    "change_policy": "major_version_changes_require_downstream_adapter_review",
}
ATLAS_QUERY_HELD_SURFACES = (
    "service_start_or_listener",
    "runtime_registry_consumption",
    "mcp_client_config_mutation",
    "credential_or_keychain_read",
    "unsupervised_live_source_read",
    "write_custody_or_reindex",
    "provider_prod_canary_authority",
)
ATLAS_QUERY_REQUIRED_EXPORTS = (
    "MemorySeamProvider",
    "NullMemorySeamProvider",
    "provider_handlers",
    "route_request",
    "atlas_query_route_bridge",
    "atlas_query_bridge_contract_fixture",
    "assert_atlas_query_bridge_contract",
)
ATLAS_QUERY_PROVIDER_METHODS = ("health", "context", "recall")
ATLAS_QUERY_ROUTE_PROBES = (
    {
        "case": "health_null_provider",
        "method": "GET",
        "target": "/health",
        "expected_status_code": 200,
        "expected_endpoint": "health",
        "expected_provider": "atlas-query-unconfigured",
    },
    {
        "case": "context_metadata_only_project",
        "method": "GET",
        "target": "/context?include=project&mode=startup&agent=reference-agent&read_receipt=metadata_only",
        "token_subject": "agent:reference-agent",
        "allowed_scopes": ("context:project",),
        "expected_status_code": 200,
        "expected_endpoint": "context",
        "expected_provider": "atlas-query-unconfigured",
    },
    {
        "case": "recall_empty_safe_fixture",
        "method": "GET",
        "target": "/recall?query=safe+bridge+fixture&scope=wiki&n=2",
        "token_subject": "agent:reference-agent",
        "allowed_scopes": ("wiki",),
        "expected_status_code": 200,
        "expected_endpoint": "recall",
        "expected_provider": "atlas-query-unconfigured",
    },
    {
        "case": "write_like_route_forbidden",
        "method": "POST",
        "target": "/diary/append",
        "token_subject": "agent:reference-agent",
        "allowed_scopes": ("wiki", "diary", "context"),
        "expected_status_code": 405,
        "expected_error": "write_like_route_unavailable",
    },
)


@dataclass(frozen=True)
class AtlasQueryBridgePlan:
    """Report-safe package adoption contract for downstream Atlas Query code."""

    package_name: str = "memory-seam"
    import_name: str = "memory_seam"
    dependency_mode: str = "editable_or_path_install"
    adapter_owner: str = "reference-adapter/atlas-query"
    core_owner: str = "memory-seam/src/memory_seam"
    status: str = ATLAS_QUERY_BRIDGE_STATUS
    held_surfaces: tuple[str, ...] = ATLAS_QUERY_HELD_SURFACES

    def as_dict(self) -> dict[str, Any]:
        return {
            "package_name": self.package_name,
            "import_name": self.import_name,
            "dependency_mode": self.dependency_mode,
            "adapter_owner": self.adapter_owner,
            "core_owner": self.core_owner,
            "status": self.status,
            "held_surfaces": list(self.held_surfaces),
        }


@dataclass(frozen=True)
class AtlasQueryBridgeContractFixture:
    """Static bridge contract fixture for downstream Atlas Query adapter tests.

    The fixture is intentionally self-contained data plus no-live route probes.
    It is safe for downstream adapter tests to import because it does not
    discover local paths, read runtime registries, start services, or call live
    backends. Downstream code should satisfy this fixture by adapting its owned
    provider implementation to the ``MemorySeamProvider`` protocol.
    """

    schema_version: str = ATLAS_QUERY_BRIDGE_CONTRACT_VERSION
    schema: str = ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA
    schema_major: int = ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR
    consumer: str = "reference-adapter/atlas-query"
    package_name: str = "memory-seam"
    import_name: str = "memory_seam"
    status: str = ATLAS_QUERY_BRIDGE_STATUS
    provider_protocol: str = "MemorySeamProvider"
    required_provider_methods: tuple[str, ...] = ATLAS_QUERY_PROVIDER_METHODS
    required_exports: tuple[str, ...] = ATLAS_QUERY_REQUIRED_EXPORTS
    route_probes: tuple[dict[str, Any], ...] = ATLAS_QUERY_ROUTE_PROBES
    held_surfaces: tuple[str, ...] = ATLAS_QUERY_HELD_SURFACES

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "schema": self.schema,
            "schema_major": self.schema_major,
            "compatibility": dict(ATLAS_QUERY_BRIDGE_CONTRACT_COMPATIBILITY),
            "consumer": self.consumer,
            "package_name": self.package_name,
            "import_name": self.import_name,
            "status": self.status,
            "provider_protocol": self.provider_protocol,
            "required_provider_methods": list(self.required_provider_methods),
            "required_exports": list(self.required_exports),
            "route_probes": [
                {key: list(value) if isinstance(value, tuple) else value for key, value in probe.items()}
                for probe in self.route_probes
            ],
            "held_surfaces": list(self.held_surfaces),
        }


@dataclass(frozen=True)
class AtlasQueryRouteBridge:
    """Tiny route adapter Atlas Query can wrap around its provider implementation."""

    provider: MemorySeamProvider = NullMemorySeamProvider(provider_name="atlas-query-unconfigured")

    def route(
        self,
        method: str,
        target: str,
        *,
        token_subject: str | None = None,
        allowed_scopes: Iterable[str] | None = None,
        acting_for: str | None = None,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
    ) -> dict[str, Any]:
        subject_policy = policy(token_subject, allowed_scopes, acting_for=acting_for)
        return route_request(
            method,
            target,
            **provider_handlers(self.provider),
            read_receipt_enabled=read_receipt_enabled,
            token_subject=subject_policy.token_subject,
            allowed_scopes=subject_policy.allowed_scopes,
            acting_for=subject_policy.acting_for,
            context_sources=context_sources,
            context_source_allowlist=context_source_allowlist,
        )


def _assert_probe_safe(response_body: dict[str, Any]) -> None:
    for key in ("read_backend_called", "service_started", "runtime_registry_consumed", "write_custody_or_reindex"):
        if response_body.get(key) is True:
            raise AssertionError(f"bridge contract probe violated held surface: {key}")


def atlas_query_bridge_plan() -> dict[str, Any]:
    """Return the report-safe L2 bridge plan without touching Atlas runtime state."""

    return AtlasQueryBridgePlan().as_dict()


def atlas_query_bridge_contract_fixture() -> dict[str, Any]:
    """Return the static Atlas Query bridge contract fixture/schema."""

    return AtlasQueryBridgeContractFixture().as_dict()


def atlas_query_route_bridge(provider: MemorySeamProvider | None = None) -> AtlasQueryRouteBridge:
    """Build an Atlas Query route bridge, defaulting to the no-live null provider."""

    return AtlasQueryRouteBridge(provider=provider or NullMemorySeamProvider(provider_name="atlas-query-unconfigured"))


def assert_atlas_query_bridge_contract(provider: MemorySeamProvider | None = None) -> dict[str, Any]:
    """Run the no-live bridge contract probes against a provider.

    This is a downstream-friendly smoke assertion helper: Atlas Query can pass
    its adapter-owned provider here, while the default remains the bundled null
    provider. The helper returns a metadata-only proof packet and raises
    ``AssertionError`` if the adapter breaks the bridge contract.
    """

    fixture = atlas_query_bridge_contract_fixture()
    bridge = atlas_query_route_bridge(provider)
    results: list[dict[str, Any]] = []
    for probe in fixture["route_probes"]:
        response = bridge.route(
            probe["method"],
            probe["target"],
            token_subject=probe.get("token_subject"),
            allowed_scopes=probe.get("allowed_scopes"),
        )
        if response["status_code"] != probe["expected_status_code"]:
            raise AssertionError(
                f"{probe['case']} status {response['status_code']} != {probe['expected_status_code']}"
            )
        body = response["body"]
        expected_endpoint = probe.get("expected_endpoint")
        if expected_endpoint is not None and body.get("endpoint") != expected_endpoint:
            raise AssertionError(f"{probe['case']} endpoint {body.get('endpoint')} != {expected_endpoint}")
        expected_error = probe.get("expected_error")
        if expected_error is not None and body.get("error") != expected_error:
            raise AssertionError(f"{probe['case']} error {body.get('error')} != {expected_error}")
        expected_provider = probe.get("expected_provider")
        if provider is None and expected_provider is not None and body.get("provider") != expected_provider:
            raise AssertionError(f"{probe['case']} provider {body.get('provider')} != {expected_provider}")
        _assert_probe_safe(body)
        results.append({"case": probe["case"], "status_code": response["status_code"], "safe": True})
    return {
        "schema_version": fixture["schema_version"],
        "status": fixture["status"],
        "provider": getattr(bridge.provider, "provider_name", bridge.provider.__class__.__name__),
        "probes": results,
        "held_surfaces_verified": True,
    }


__all__ = [
    "ATLAS_QUERY_BRIDGE_CONTRACT_VERSION",
    "ATLAS_QUERY_BRIDGE_CONTRACT_COMPATIBILITY",
    "ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR",
    "ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA",
    "ATLAS_QUERY_BRIDGE_STATUS",
    "ATLAS_QUERY_HELD_SURFACES",
    "ATLAS_QUERY_PROVIDER_METHODS",
    "ATLAS_QUERY_REQUIRED_EXPORTS",
    "ATLAS_QUERY_ROUTE_PROBES",
    "AtlasQueryBridgeContractFixture",
    "AtlasQueryBridgePlan",
    "AtlasQueryRouteBridge",
    "assert_atlas_query_bridge_contract",
    "atlas_query_bridge_contract_fixture",
    "atlas_query_bridge_plan",
    "atlas_query_route_bridge",
]
