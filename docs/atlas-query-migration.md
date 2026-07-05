# Atlas Query package migration guide

This guide is the reference adapter migration path for consuming the standalone Memory Seam package. It keeps Atlas Query runtime ownership downstream while replacing duplicated core seam contracts with imports from this repository.

## Target dependency shape

Use a normal Python dependency, not a Git submodule and not a pinned production checkout path.

Allowed local development forms:

```text
memory-seam @ file:///path/to/memory-seam
-e /path/to/memory-seam
```

Allowed packaged form:

```text
memory-seam==0.1.0
```

Held forms:

```text
git submodule add <memory-seam-url>
PYTHONPATH=/local/production/reference-adapter/vendor/memory-seam
import copied_memory_seam_contracts
```

A downstream Atlas Query PR should prove the package can be imported in tests with `python -m pip install -e /path/to/memory-seam` or an equivalent package dependency. Production service dependencies remain adapter-owned; this guide does not authorize service activation or production pinning.

## Target imports

Prefer package imports from `memory_seam` for stable boundary types and bridge helpers:

```python
from memory_seam import (
    MemorySeamProvider,
    NullMemorySeamProvider,
    RuntimeRequest,
    assert_atlas_query_bridge_contract,
    atlas_query_bridge_contract_fixture,
    atlas_query_bridge_plan,
    atlas_query_route_bridge,
    route_request,
)
```

If a narrower import is clearer in adapter code, import from the package modules without reaching into private paths:

```python
from memory_seam.atlas_query_bridge import assert_atlas_query_bridge_contract
from memory_seam.providers import MemorySeamProvider
from memory_seam.router import route_request
```

Do not copy constants, route parsing glue, provider protocols, or receipt/router shapes into the reference adapter once this dependency is available. Downstream code may keep Atlas-specific handlers, client wiring, source discovery, and live-read permissions in the adapter.

## Adapter boundary

The downstream reference adapter owns the Atlas Query adapter implementation. Memory Seam owns only the no-live core contract and bridge assertion helpers.

Downstream adapter shape:

```python
from memory_seam import MemorySeamProvider, atlas_query_route_bridge


class AtlasQueryMemorySeamProvider:
    provider_name = "atlas-query"

    def health(self):
        ...  # report-safe adapter metadata

    def context(self, request):
        ...  # call existing Atlas Query handler under existing downstream gates

    def recall(self, request):
        ...  # call existing Atlas Query handler under existing downstream gates


bridge = atlas_query_route_bridge(AtlasQueryMemorySeamProvider())
```

The adapter must preserve existing Atlas Query authority. The package bridge must not start listeners, read credentials/keychain/env secrets, consume Runtime Registry at runtime, mutate client/runtime config, perform unsupervised/private/live source reads in package import tests, add write/custody/reindex behavior, or move provider/prod/canary authority.

## Migration sequence

1. Add a reference-adapter-only test dependency on the local Memory Seam package path, editable install, or package artifact.
2. Replace duplicated protocol/router/receipt constants with the target imports above.
3. Wrap existing Atlas Query handler behavior in a downstream `MemorySeamProvider` implementation; keep all live backend access behind current Atlas Query gates.
4. Add a no-live downstream test that runs `assert_atlas_query_bridge_contract(AtlasQueryMemorySeamProvider())` against synthetic/null-safe handler paths.
5. Keep current client behavior tests green without starting a new service from Memory Seam.
6. Remove any temporary import shims after the package dependency proves stable.

## Rollback plan

Rollback is dependency-level and adapter-local:

1. Remove the Memory Seam path/editable dependency from the downstream test or package configuration.
2. Revert the adapter PR that swapped duplicated glue for `memory_seam` imports.
3. Restore the previous Atlas Query-local contract definitions from the downstream branch history if needed.
4. Leave the standalone Memory Seam repository untouched; no submodule cleanup, production checkout cleanup, service stop, Runtime Registry mutation, and no package unpublish step should be required.

A successful rollback should return Atlas Query to its previous downstream-only implementation without changing global client/runtime config and without deleting the Memory Seam repository.

## Acceptance smoke

Use this in the downstream adapter test suite after wiring the provider:

```python
from memory_seam import assert_atlas_query_bridge_contract

from atlas_query_memory_seam_adapter import AtlasQueryMemorySeamProvider


def test_memory_seam_package_bridge_contract():
    proof = assert_atlas_query_bridge_contract(AtlasQueryMemorySeamProvider())
    assert proof["held_surfaces_verified"] is True
```

The proof packet is metadata-only. It verifies the route/provider seam, not live source usefulness, service readiness, production canary behavior, or write custody.
