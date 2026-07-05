# Adapter import-boundary compatibility

Memory Seam stays a portable core package. Downstream adapter code may depend on Memory Seam, but Memory Seam must not import downstream adapter modules, Atlas runtime modules, service wiring, Runtime Registry clients, credential helpers, or private source discovery code.

This note complements [`downstream-integration-smoke-plan.md`](downstream-integration-smoke-plan.md). The smoke plan is the executable downstream proof surface; this note defines the package boundary that the smoke is expected to preserve.

## Direction of dependency

Allowed dependency direction:

```text
downstream adapter wrapper -> memory_seam package -> Python standard library
```

Disallowed dependency direction:

```text
memory_seam package -> downstream adapter wrapper
memory_seam package -> Atlas runtime/service wiring
memory_seam package -> Runtime Registry/runtime clients
memory_seam package -> credential/auth/keychain/env readers
memory_seam package -> live/private source discovery or raw file readers
```

The core package may expose protocols, fixtures, route helpers, receipts, descriptors, policy helpers, synthetic providers, and default-off runtime helpers. Adapter implementation remains downstream and should import those public surfaces instead of copying core contracts into an adapter checkout.

## Core import contract

The `src/memory_seam` package must remain importable from a clean downstream checkout after a local editable install or private wheel install. Importing Memory Seam must not require:

- an Atlas checkout;
- FastMCP/Hermes service wiring;
- Runtime Registry configuration;
- credentials, auth files, environment secrets, keychains, or OAuth state;
- private source roots or source discovery;
- a service/listener process;
- write, custody, reindex, or thread-retirement authority.

The repository test suite enforces this with an AST-based import-boundary check over every committed core module. The check allows only relative `memory_seam` imports and Python standard-library imports unless a future review explicitly adds a public package dependency to `pyproject.toml`.

## Downstream compatibility expectation

Downstream adapter wrappers should prove compatibility by running the no-mutation smoke in [`downstream-integration-smoke-plan.md`](downstream-integration-smoke-plan.md):

1. install Memory Seam locally or from a private wheel artifact;
2. import public package surfaces such as `route_request`, `provider_handlers`, `NullMemorySeamProvider`, and `synthetic_safe_content_provider`;
3. exercise synthetic `/context`, `/recall`, and `/health` routes only;
4. assert safe-posture fields stay false for service start, Runtime Registry consumption, and write/custody/reindex behavior;
5. roll back only temporary environments or disposable checkouts.

Do not add submodules, pinned production clones, global client configuration, service activation, or live adapter wiring to prove this boundary.

## Public artifact hygiene

Issue and PR artifacts for this boundary should use sanitized placeholders such as `<DOWNSTREAM_CHECKOUT>` and synthetic route payloads. Do not include raw private source text, credentials, auth material, platform IDs, private absolute paths, raw operator queries, or private correlation references.
