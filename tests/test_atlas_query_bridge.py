from __future__ import annotations

from memory_seam import (
    ATLAS_QUERY_BRIDGE_CONTRACT_COMPATIBILITY,
    ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR,
    ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA,
    ATLAS_QUERY_BRIDGE_CONTRACT_VERSION,
    ATLAS_QUERY_BRIDGE_STATUS,
    ATLAS_QUERY_HELD_SURFACES,
    ATLAS_QUERY_PROVIDER_METHODS,
    assert_atlas_query_bridge_contract,
    atlas_query_bridge_contract_fixture,
    atlas_query_bridge_plan,
    atlas_query_route_bridge,
)
from memory_seam.providers import NullMemorySeamProvider


def test_atlas_query_bridge_plan_is_report_safe_and_package_based():
    plan = atlas_query_bridge_plan()

    assert plan["status"] == ATLAS_QUERY_BRIDGE_STATUS
    assert plan["package_name"] == "memory-seam"
    assert plan["import_name"] == "memory_seam"
    assert plan["dependency_mode"] == "editable_or_path_install"
    rendered = repr(plan)
    assert "/" + "Users" + "/" not in rendered
    assert "runtime-registry" not in rendered
    assert "credential_or_keychain_read" in ATLAS_QUERY_HELD_SURFACES


def test_atlas_query_route_bridge_defaults_to_no_live_null_provider():
    bridge = atlas_query_route_bridge()
    response = bridge.route(
        "GET",
        "/context?include=project&mode=startup&agent=reference-agent&read_receipt=metadata_only",
        token_subject="agent:reference-agent",
        allowed_scopes=["context:project"],
    )

    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["provider"] == "atlas-query-unconfigured"
    assert body["include_requested"] == ["project"]
    assert body["read_receipt_requested"] is True
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["write_custody_or_reindex"] is False


def test_atlas_query_route_bridge_accepts_downstream_provider_without_core_duplication():
    provider = NullMemorySeamProvider(provider_name="reference-adapter")
    bridge = atlas_query_route_bridge(provider)
    response = bridge.route(
        "GET",
        "/recall?query=safe+bridge+fixture&scope=wiki&n=2",
        token_subject="agent:reference-agent",
        allowed_scopes=["wiki"],
    )

    assert response["status_code"] == 200
    assert response["body"]["provider"] == "reference-adapter"
    assert response["body"]["query"] == "safe bridge fixture"
    assert response["body"]["items"] == []


def test_atlas_query_route_bridge_keeps_write_like_routes_forbidden():
    response = atlas_query_route_bridge().route(
        "POST",
        "/diary/append",
        token_subject="agent:reference-agent",
        allowed_scopes=["wiki", "diary", "context"],
    )

    assert response["status_code"] == 405
    assert response["body"]["write_like_routes"] == "absent_or_404_405"


def test_atlas_query_bridge_contract_fixture_is_standalone_and_consumable():
    fixture = atlas_query_bridge_contract_fixture()

    assert fixture["schema_version"] == ATLAS_QUERY_BRIDGE_CONTRACT_VERSION
    assert fixture["schema"] == ATLAS_QUERY_BRIDGE_CONTRACT_SCHEMA
    assert fixture["schema_major"] == ATLAS_QUERY_BRIDGE_CONTRACT_MAJOR
    assert fixture["compatibility"] == ATLAS_QUERY_BRIDGE_CONTRACT_COMPATIBILITY
    assert fixture["consumer"] == "reference-adapter/atlas-query"
    assert fixture["provider_protocol"] == "MemorySeamProvider"
    assert fixture["required_provider_methods"] == list(ATLAS_QUERY_PROVIDER_METHODS)
    assert "assert_atlas_query_bridge_contract" in fixture["required_exports"]
    assert len(fixture["route_probes"]) == 4
    assert {probe["case"] for probe in fixture["route_probes"]} == {
        "health_null_provider",
        "context_metadata_only_project",
        "recall_empty_safe_fixture",
        "write_like_route_forbidden",
    }
    rendered = repr(fixture)
    assert "/" + "Users" + "/" not in rendered
    assert "runtime-registry" not in rendered
    assert "credential_or_keychain_read" in fixture["held_surfaces"]


def test_atlas_query_bridge_contract_fixture_versioning_is_explicit():
    fixture = atlas_query_bridge_contract_fixture()
    compatibility = fixture["compatibility"]

    assert fixture["schema_version"] == "atlas-query-bridge-contract/v1"
    assert fixture["schema_version"] == f"{fixture['schema']}/v{fixture['schema_major']}"
    assert compatibility["schema"] == fixture["schema"]
    assert compatibility["major"] == fixture["schema_major"]
    assert compatibility["version"] == fixture["schema_version"]
    assert compatibility["package_min_version"] == "0.1.0"
    assert compatibility["package_max_major"] == "0"
    assert compatibility["change_policy"] == "major_version_changes_require_downstream_adapter_review"


def test_atlas_query_bridge_contract_assertion_runs_no_live_null_probes():
    proof = assert_atlas_query_bridge_contract()

    assert proof["schema_version"] == ATLAS_QUERY_BRIDGE_CONTRACT_VERSION
    assert proof["status"] == ATLAS_QUERY_BRIDGE_STATUS
    assert proof["provider"] == "atlas-query-unconfigured"
    assert proof["held_surfaces_verified"] is True
    assert [probe["safe"] for probe in proof["probes"]] == [True, True, True, True]
    assert [probe["status_code"] for probe in proof["probes"]] == [200, 200, 200, 405]


def test_atlas_query_bridge_contract_assertion_accepts_downstream_provider_name():
    proof = assert_atlas_query_bridge_contract(NullMemorySeamProvider(provider_name="reference-adapter"))

    assert proof["provider"] == "reference-adapter"
    assert proof["held_surfaces_verified"] is True
