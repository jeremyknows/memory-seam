# Contributing

Memory Seam is a standalone, no-live memory-boundary package. Contributions should keep the package portable and should not depend on local worktrees, production checkouts, service processes, credentials, or client configuration.

## Safe contribution lanes

Safe changes include:

- package contracts and pure helpers;
- tests, fixtures, and synthetic examples;
- documentation and release-readiness hardening;
- adapter contract fixtures that downstream projects can import without runtime side effects;
- packaging metadata and CI improvements.

## Held surfaces

Do not add or activate:

- package publication automation;
- persistent services, listeners, daemons, or MCP/client config mutation;
- credential, keychain, token, or environment-secret reads;
- Runtime Registry consumption at runtime;
- unsupervised/live/private source reads;
- write, custody, reindex, provider, production, canary, or gate authority.

Design-only notes for held surfaces are acceptable when they clearly state that no live read or write behavior is implemented.

## Local verification

Run the core proof set before proposing a change:

```bash
pytest -q
python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py
python scripts/public_hygiene_scan.py
git diff --check
```

If a change modifies packaging or examples, also run the relevant example entry point, such as:

```bash
python examples/quickstart_smoke.py
```

## Documentation hygiene

User-facing docs should describe current package behavior and explicit non-goals. Do not add host-local paths, private source-deck references, raw identifiers, credentials, or private provenance to the public package surface.
