# Package boundary and runtime authority

## Verdict

**Package-boundary docs cleanup PASS — package-facing docs align on public v0.1.0 source release, no-live behavior, downstream adapter ownership, and held runtime/write authority.**

This note is documentation-only. It does not authorize package publication automation, service/listener activation, credential/auth/env/keychain reads, Runtime Registry consumption, live/private source reads, source discovery, unsupervised reads, writes/custody/reindex behavior, provider/prod/canary authority, or production authority changes.

## Current package boundary

Memory Seam is a public Apache-2.0 Python source package for a portable no-live/read-only memory boundary core. The package includes:

- contracts, policy, descriptors, provider protocols/null provider, receipts, router, testing helpers, and the default-off read-only runtime skeleton;
- synthetic examples and test fixtures that prove context/recall behavior without live sources;
- a package-local Atlas Query bridge helper that defines downstream adapter contract shape without importing downstream runtime or service code.

The package does not include and must not imply:

- live adapter implementations or private source discovery;
- service/listener startup or global client/runtime configuration mutation;
- credential, auth store, environment secret, keychain, OAuth, or auth-file reads;
- Runtime Registry runtime consumption;
- unsupervised reads, scheduled/startup activation, canaries, provider/prod authority, writes, custody, reindex, or package publication automation.

## Adapter downstream rule

Downstream adapters may import Memory Seam package surfaces. Memory Seam core must not import downstream adapter, runtime, service, or private implementation code. Adapter docs may describe package-import targets, synthetic smoke checks, rollback, and held live/runtime/write surfaces, but they must not turn downstream adapter wiring into package-core authority.

## Documentation alignment checklist

Use this checklist when editing README, docs, changelog, or packaging material:

1. **State public source release first.** The repository is a v0.1.0 Apache-2.0 source release.
2. **Say local build/install for registry-neutral checks.** Wheel and source distribution commands are local smoke checks unless a maintainer explicitly publishes a registry artifact.
3. **Keep examples synthetic.** Examples and fixtures must not discover local sources, read private/live data, start services, call networks, consume Runtime Registry, or perform writes/custody/reindex behavior.
4. **Preserve adapter direction.** Downstream adapters depend on Memory Seam; Memory Seam core does not depend on downstream adapters.
5. **Keep runtime authority explicit.** Package publication, registry upload, service activation, and provider/prod/canary use remain explicit maintainer decisions.
6. **Sanitize public artifacts.** Public issue/PR/docs text must avoid raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, and private correlation refs.

## Focused verifier

Focused command for this issue:

```bash
pytest -q tests/test_package_boundary_docs_cleanup.py tests/test_docs_taxonomy.py tests/test_readme_operator_quickstart.py tests/test_atlas_query_migration_guide.py
```

Required full gate before merge:

```bash
pytest -q
python scripts/public_hygiene_scan.py
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
git diff --check
```

## Trust-boundary evidence

This issue changes documentation only and does not add executable denial paths that can materialize source/provider/file/stat/backend reads. Existing denial-before-read and identity negative-path coverage remains in the F2/F3/F4 tests, where denied routes assert zero provider/backend/read/stat calls or equivalent monkeypatch/spy evidence before materialization. The docs cleanup records boundaries and does not widen authority.

## Next issue pointer

After this docs cleanup lands and passes local verification, remaining runtime/write authority changes still require explicit maintainer review.
