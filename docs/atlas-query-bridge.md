# Atlas Query bridge plan (L2)

Memory Seam L2 moves Atlas Query toward consuming this repository as a normal Python package while keeping Atlas-specific runtime authority in the downstream reference adapter.

## Package boundary

- Core package: `memory-seam`, imported as `memory_seam`.
- Downstream adapter owner: `reference-adapter/atlas-query`.
- Dependency mode for local development: editable/path install from a Memory Seam checkout.
- No submodule and no duplicated core-contract source should be required once the downstream adapter imports this package.

## Memory Seam side now exposed

- `memory_seam.atlas_query_bridge_plan()` returns a report-safe package adoption contract.
- `memory_seam.atlas_query_route_bridge(provider=None)` returns a no-live route bridge over a `MemorySeamProvider`.
- The default bridge uses `NullMemorySeamProvider(provider_name="atlas-query-unconfigured")`, so import/route tests can run before Atlas Query wires its live-owned adapter.
- `memory_seam.atlas_query_bridge_contract_fixture()` returns a standalone `atlas-query-bridge-contract/v1` fixture/schema with explicit version metadata, required exports, provider protocol methods, no-live route probes, and held surfaces.
- `memory_seam.assert_atlas_query_bridge_contract(provider=None)` runs that fixture against the null provider or a downstream-owned provider and returns a metadata-only proof packet. It raises if a probe starts a service, consumes Runtime Registry, calls a read backend in the null path, or crosses write/custody/reindex boundaries.

## Contract fixture use

Atlas Query adapter tests can consume the fixture without importing Atlas runtime
state:

```python
from memory_seam import assert_atlas_query_bridge_contract

from atlas_query_memory_seam_adapter import AtlasQueryMemorySeamProvider


def test_memory_seam_package_bridge_contract():
    proof = assert_atlas_query_bridge_contract(AtlasQueryMemorySeamProvider())
    assert proof["schema_version"] == "atlas-query-bridge-contract/v1"
    assert proof["held_surfaces_verified"] is True
```

The fixture validates the package/provider seam only. It is not authority to
start services, read private/live sources, add Runtime Registry consumption, or move
provider/prod/canary gates.

## Fixture versioning

The bridge fixture is versioned independently from downstream Atlas runtime code
so reference adapter tests can assert compatibility without importing private
adapter state.

| Field | Current value | Meaning |
| --- | --- | --- |
| `schema` | `atlas-query-bridge-contract` | Stable fixture family name. |
| `schema_major` | `1` | Compatibility major for adapter assertions. |
| `schema_version` | `atlas-query-bridge-contract/v1` | Complete fixture identifier to pin in downstream tests. |
| `compatibility.package_min_version` | `0.1.0` | Earliest Memory Seam package version expected to expose this fixture. |
| `compatibility.package_max_major` | `0` | Package major accepted for this v1 fixture. |
| `compatibility.change_policy` | `major_version_changes_require_downstream_adapter_review` | Any fixture major bump needs explicit downstream adapter review before tests are repinned. |

Downstream adapter tests should pin `schema_version` and may additionally assert
`compatibility.version == schema_version`. Additive fields inside the same major
are allowed when they do not remove route probes, required exports, held
surfaces, or provider protocol methods. Removing or renaming those contract
surfaces requires a new major fixture version.

## Held surfaces

The package bridge must not start listeners, read credentials/keychain/env secrets, consume Runtime Registry at runtime, mutate client/runtime config, perform unsupervised/live/private source reads, add write custody/reindex, or move provider/prod/canary authority.

## Downstream migration sequence

1. Add a reference-adapter-only PR that imports `memory_seam` through an editable/path dependency in tests.
2. Wrap existing Atlas Query handler implementations in a `MemorySeamProvider` implementation downstream.
3. Run `assert_atlas_query_bridge_contract()` in adapter tests against that downstream provider.
4. Replace duplicated constants/router/protocol glue with imports from this package.
5. Keep existing client behavior and tests passing; any live-read or service activation remains separately held.
