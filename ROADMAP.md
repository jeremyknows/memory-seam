# Memory Seam standalone development path

This repo is the portable public-track home for Memory Seam. Downstream adapters
remain reference integrations, but core package development should happen here
first whenever possible.

## Layer sequence

### L0 — Standalone core hygiene

Goal: make the extracted no-live core independently testable and package-shaped.

Done now:
- `src/memory_seam/` contains contracts, policy, descriptors, receipts, router, testing helpers.
- `pytest -q` passes in a clean clone.
- Public package docs are kept independent of private source decks and
  deployment-specific operator notes.

Next:
- add CI for Python versions;
- add public hygiene scan before making repo public;
- keep private provenance outside the public source tree.

### L1 — Core API hardening

Goal: stabilize import names and public interfaces before adapters depend on them.

Work:
- define `memory_seam` public API surface;
- add provider protocol interfaces;
- pin route/envelope schemas;
- add denial-before-read contract tests independent of Atlas fixtures.

### L2 — Adapter bridge

Goal: let Atlas Query consume the standalone package without re-coupling the core to downstream adapter implementation code.

Work:
- keep Atlas Query as reference adapter;
- use a normal package dependency/path install during development, not a downstream adapter submodule;
- preserve existing Atlas Query behavior while removing duplicated core code.

### L3 — Read-only local runtime product

Goal: package a boring, default-off read-only runtime around the core.

Work:
- local process/server design;
- real identity/auth verifier interface;
- metadata-only audit receipts;
- kill switch / rollback;
- no credentials or live/private reads without explicit approval.

### L4 — Dogfood and source adapters

Goal: prove the seam is useful in normal agent work.

Work:
- source-card and exact-path adapters;
- bounded filesystem/provider protocols;
- Atlas dogfood via adapter bridge;
- usefulness tests that answer real operator questions without raw fallback.

### L5 — Unsupervised read ladder

Goal: only after L3/L4 are boring.

Completed evidence now:
- no-source-read local tick contract and supervised one-read packet/receipt;
- post-read verifier and default-off bounded runner shape;
- one-tick canary decision packet that remains no-execution/no-activation.

Still held:
- unsupervised/live/private reads beyond the committed supervised metadata-card evidence;
- source discovery, credential/auth/keychain/env reads, Runtime Registry consumption,
  global runtime configuration mutation, service/listener/startup/cron activation,
  recurring canary authority, provider/prod/canary authority, publication, and Gate
  movement.

### L6 — Write custody companion

Goal: writes are a companion custody layer, not a prerequisite for the read-seam product.

Completed evidence now:
- L6S planning packets for ownership/approval, rollback/audit, operation-class
  fixtures, denied-before-mutation harness, trust-boundary review, and first
  implementation-slice decision packet;
- L6I.01-L6I.04 approved implementation of the default-off synthetic
  write-intent preflight gate skeleton only;
- L6I.05 trust-boundary review and L6I.06 frontier packet recording that the
  current implementation proves no-production denial-before-callback behavior,
  report-safe denial metadata, stale/mismatched approval denial hardening, and a
  local synthetic smoke path.

Current frontier:
- `docs/l6ar05-source-floor-parent-tracker-reconciliation.md` records the latest tactical rail closure: L6AR is reconciled and intentionally created no successor issue, no cron mutation, no second attempt, and no Gate/provider/write movement.
- The recommended next work is a human-reviewed fleet-adoption contract followed by the smallest read-only pilot, not another blind metadata retry.
- Update 2026-06-09: the `unauthorized_narrowing` root cause behind the #412 zero-item receipt was fixed upstream in the reference adapter; a live wiki-scope recall through the adapter now returns relevant, provenance-tagged items with `degraded: false`. Read-side usefulness is demonstrated at the adapter layer; remaining work is identity-bound fleet consumption and eval-vs-baseline, not zero-items investigation.
- Older L6 positive-authorization, supervised source-card, runtime-integration, and auth-repair rails remain historical bounded evidence, not standing authority.

Still held:
- any code path returning `allowed=true`;
- write execution, custody transfer or custody receipt persistence, delete,
  reindex, rollback, cache purge, provider/backend/source-stat/source-read
  callbacks, positive allowed runtime paths, persistence, live/private source
  reads, source discovery, credential/auth/keychain/env reads, Runtime Registry
  consumption, global runtime configuration mutation, service/listener/startup/cron
  activation, provider/prod/canary authority, publication, repository visibility
  changes, Atlas Gate movement, and production-authoritative claims.

## Current authority boundary

Allowed in this repo now:
- package/code/test/docs work for no-live/read-only core;
- CI/package hygiene;
- source-package repository operations;
- PRs/merges in this repo when tests and scans pass.

Held:
- registry publication until explicit maintainer review;
- persistent service/listener activation;
- credential/auth/keychain/env secret reads;
- Runtime Registry runtime consumption;
- unsupervised/live/private reads;
- writes/custody/reindex;
- provider/prod/canary/Gate movement in Atlas.
