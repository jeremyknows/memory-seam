# Memory Seam

Memory Seam is a portable, no-live memory-boundary core for agent memory systems.

It provides the package boundary, contracts, policy helpers, descriptors, receipts, provider protocols, and synthetic examples needed to evaluate memory access behavior without connecting to live systems.

## Public release status

- Public v0.1.0 source package under Apache-2.0.
- Scope: no-live/read-only core package.
- Included now: contracts, policy, descriptors, provider protocols/null provider, receipts, router, testing helpers, downstream bridge helpers, a default-off read-only runtime skeleton, and synthetic source adapter/usefulness proofs.
- Not included: live adapter implementation, service/listener activation, credentials, runtime registry consumption, unsupervised reads, writes/custody/reindex, provider/prod/canary authority, or package publication automation.
- The repository is designed so package use does not require private source decks, local operator paths, live services, credentials, or production checkouts.

## Operator quickstart

Use this path when evaluating Memory Seam from a fresh clone or from a local
wheel/install artifact. The quickstart stays fully synthetic: it does not start a service, discover
local sources, call a network, consume Runtime Registry, read private/live data,
fall back to raw reads, publish packages, or perform write/custody/reindex
behavior.

### 1. Clone and install locally

```bash
git clone https://github.com/jeremyknows/memory-seam.git
cd memory-seam
python -m pip install -e .
```

If you already have a local wheel from `docs/packaging.md`, install that wheel in
a temporary environment instead of publishing it:

```bash
python -m pip install dist/memory_seam-*.whl
```

### 2. Run the no-live context/recall smoke

```bash
python examples/quickstart_smoke.py
```

The example builds `LocalReadOnlyRuntime` with `synthetic_safe_content_provider()`
and `StaticIdentityVerifier`, then sends one `/context` request and one `/recall`
request. Both requests ask for metadata-only receipts and only read committed
synthetic fixtures.

Expected shape:

```json
{
  "context": {
    "endpoint": "context",
    "items": ["Memory Seam project boundary", "Default-off runtime answer"],
    "receipt_verdict": "useful",
    "safe_posture": {
      "raw_fallback_used": false,
      "read_backend_called": false,
      "runtime_registry_consumed": false,
      "service_started": false,
      "write_custody_or_reindex": false
    },
    "status_code": 200
  },
  "recall": {
    "endpoint": "recall",
    "items": ["Default-off runtime answer"],
    "receipt_verdict": "useful",
    "safe_posture": {
      "raw_fallback_used": false,
      "read_backend_called": false,
      "runtime_registry_consumed": false,
      "service_started": false,
      "write_custody_or_reindex": false
    },
    "status_code": 200
  }
}
```

### 3. Inspect null and fake provider examples

```bash
python examples/null_and_fake_providers.py
```

The null-provider example shows the safe unconfigured envelope with no items and
`provider_unconfigured`. The fake-provider example shows how downstream adapter
work can start with committed, deterministic fixtures before any live provider
exists. Both examples route through the public provider protocol and assert the
same no-live posture: no backend read, no service start, no Runtime Registry
consumption, no raw fallback, and no write/custody/reindex behavior.

### 4. Run the local verification gate

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
```

Packaging metadata and local build smoke instructions live in
`docs/packaging.md`. Publication to a package registry is a separate maintainer
decision; this repository does not automate registry upload.

## Development

```bash
python -m pip install -e .
pytest -q
```

## Package layout

```text
src/memory_seam/
  adapters.py
  contracts.py
  policy.py
  descriptors.py
  providers.py
  receipts.py
  router.py
  atlas_query_bridge.py
  runtime.py
  testing.py
```

Start with `docs/README.md` for the documentation taxonomy across public package
docs, runtime/contracts notes, downstream adapter notes, and examples.

Key package-boundary docs:

- See `CHANGELOG.md` for the API/schema stability ledger and future PR entry template.
- `docs/package-boundary.md` — no-live, downstream-adapter, and release-authority alignment checklist.
- `docs/atlas-query-bridge.md` and `docs/atlas-query-migration.md` — downstream adapter bridge/migration guidance without reversing dependencies into core.
- `docs/adapter-import-boundary.md` — compatibility rule: adapters may import Memory Seam package surfaces, but Memory Seam core must not import downstream adapter/runtime/service code.
- `docs/default-off-runtime.md`, `docs/envelope-schema-snapshots.md`, `docs/schema-contracts.md`, and `docs/policy-semantics-decision-note.md` — runtime/schema/policy contract notes.
- `docs/f2-verifier-packet.md`, `docs/f3-manual-pull-dogfood.md`, `docs/f3-source-card-usefulness-proof.md`, `docs/f3-verifier-packet.md`, `docs/no-service-identity-semantics.md`, and `docs/f4-verifier-packet.md` — verifier, dogfood, usefulness, and identity packets with preserved holds.
- `docs/public-private-hygiene-inventory.md` — public/private hygiene inventory covering public surfaces, scanner target classes, safe exceptions, and omitted private planning material.
