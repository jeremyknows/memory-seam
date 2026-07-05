# Changelog

Memory Seam uses this changelog as the stability ledger for public API, schema,
contract, and operator-facing behavior changes for the public Apache-2.0 source
package. Record merged changes here before tagging or publishing a package
artifact; do not use this file as authority to activate services, consume
Runtime Registry, perform live reads, or add write/custody/reindex behavior.

## v0.1.0

### Stability policy

- Public API changes include exported modules under `memory_seam`, documented
  contract dataclasses/protocols, CLI no-live smoke behavior, envelope schema
  snapshots, receipt fields, provider interfaces, and bridge fixture versions.
- Mark entries as **breaking**, **non-breaking**, or **documentation-only** so
  downstream adapters can decide when migration work is required.
- Breaking changes must include the affected surface, migration note, rollback
  note, and the issue/PR that introduced the change.
- Non-breaking changes should include the affected surface and the issue/PR that
  introduced the change.
- Documentation-only changes should call out when they do not alter package
  behavior or schema shape.

### Initial public release baseline

- **Non-breaking** — Initial no-live core package surface: contracts, policy,
  descriptors, provider protocols/null provider, receipts, router, testing
  helpers, and package import boundary.
- **Non-breaking** — Atlas Query bridge helper and versioned standalone fixture
  for downstream adapter migration without duplicating core contracts.
- **Non-breaking** — Default-off read-only runtime skeleton for synthetic
  `/health`, `/context`, and `/recall` envelopes, including denial-before-read
  behavior, metadata-only receipts, kill-switch/rollback contract tests, and
  safe source-card adapter interfaces.
- **Non-breaking** — Local packaging metadata, local wheel/install smoke, null
  and deterministic fake provider examples, and minimal no-live CLI smoke.
- **Documentation-only** — Public hygiene, docs taxonomy, release decision
  checklist, issue-railed autopilot template, Atlas Query migration guide, and
  private provenance quarantine guidance.
- **Documentation-only** — F10 package boundary and release-authority docs cleanup
  aligning README/docs/changelog/packaging on public v0.1.0 posture, no-live
  examples, downstream adapter ownership, and held runtime/write authority.

### Entry template for future PRs

```markdown
- **breaking|non-breaking|documentation-only** — Short summary.
  - Surface: exported API, schema snapshot, CLI, docs, packaging, or downstream
    fixture.
  - Migration: required downstream action, or `none`.
  - Rollback: safe rollback route, or `revert PR` when sufficient.
  - Evidence: issue #NN / PR #NN plus local and CI checks.
```

## Runtime boundary

This changelog records source package changes only. It does not authorize
service/listener activation, live source reads, Runtime Registry consumption,
provider/prod/canary authority changes, or write/custody/reindex work.
