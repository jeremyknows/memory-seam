# L3 default-off read-only runtime

Memory Seam's L3 runtime surface is an in-process skeleton, not a service. It is
built to prove runtime posture while keeping every high-blast-radius surface held
until a later explicit activation decision.

## Defaults

- `ReadOnlyRuntimeConfig.enabled` defaults to `False`.
- `LocalReadOnlyRuntime.handle(...)` denies reads while disabled before calling a
  provider.
- The default `DenyAllIdentityVerifier` denies reads even when the runtime is
  explicitly enabled.
- The bundled provider remains `NullMemorySeamProvider`, which performs no live
  source reads.
- No listener is started and no persistent audit sink is opened.

## Held surfaces

The runtime reports these held surfaces in health and per-request runtime
receipts:

- service start
- listener activation
- Runtime Registry consumption
- persistent audit sinks
- global config mutation
- write custody or reindex behavior

## Identity verifier

Adapters must provide an `IdentityVerifier` implementation that returns an
`IdentityDecision` with the subject, scopes, and optional `acting_for` boundary.
The skeleton does not infer identity from request query strings and does not
widen authority on its own.

`StaticIdentityVerifier` exists only for tests and explicit local demos. It does
not perform network, credential, keychain, Runtime Registry, or platform lookups.

## Audit and rollback receipts

The runtime returns metadata-only receipts:

- `memory_seam_runtime_receipt_v0` records runtime decision, held surfaces,
  no-service/no-registry/no-write posture, and the local rollback handle
  (`disable_runtime: true`). It includes a nested
  `memory_seam_runtime_audit_receipt_v0` return-value receipt with stable
  version fields, opaque subject/source refs, and explicit false markers for raw
  content, source paths, credential refs, raw subject labels, and persistence.
- If a routed context/recall request asks for `read_receipt=metadata_only`, the
  existing `build_read_receipt(...)` path attaches audit and rollback shapes to
  the response envelope without persisting content or source paths.

## Kill switch

`ReadOnlyRuntimeConfig.kill_switch` can deny all reads before identity or provider
execution when `ContextReadKillSwitch.disable_all` is set. Family/descriptor kill
switch decisions stay in the lower-level context source policy layer; this L3
wrapper only owns the coarse runtime-off brake.

## Non-goals for this layer

L3 does not start/install services, register MCP tools, mutate Hermes/global
config, read from private live sources unsupervised, consume Runtime Registry at
runtime, publish packages, or introduce writes/custody/reindex execution.
