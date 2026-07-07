# Documentation index

This index keeps Memory Seam docs sorted by audience and release boundary.
Public-facing docs should be usable without private provenance, source-deck
access, local operator paths, Runtime Registry access, live reads, services,
package publication, or write/custody behavior.

**Note on scope (2026-07):** this index used to also carry ~130 build-rail
decision packets (the `l6aa`...`l6ar`, `l6x`/`l6y`/`l6z` chain) — receipted,
issue-bound process artifacts from construction that were never wired into
the installed package. Those moved to
[`../archive/build-rails/`](../archive/build-rails/README.md), preserved for
provenance but out of the way of anyone evaluating or using the package. The
docs below are what's left: architecture, the public package surface, the
shipped (if currently gated/held) write-custody and positive-authorization
modules, and deployment patterns.

## Architecture Decision Records

Accepted decisions that shape the seam's design and deployment posture. Each ADR records the context, the chosen option, and the consequences.

- [`adr/0001-fleet-read-privacy-open-within-fleet.md`](adr/0001-fleet-read-privacy-open-within-fleet.md) — ADR 0001: fleet read privacy is open-within-fleet with walls by exception, not the default.
- [`adr/0002-write-autonomy-ceiling-class-ladder.md`](adr/0002-write-autonomy-ceiling-class-ladder.md) — ADR 0002: write-autonomy ceiling is a per-class evidence-earned ladder; dangerous domains (credentials, auth, runbooks) are human-reviewed permanently.
- [`adr/0003-credentials-values-ban-pointer-as-pattern.md`](adr/0003-credentials-values-ban-pointer-as-pattern.md) — ADR 0003: credential values are banned permanently; pointer custody is documented as an OSS deployment pattern, not a core feature.
- [`adr/0004-unsupervised-reads-general-with-kill-switch.md`](adr/0004-unsupervised-reads-general-with-kill-switch.md) — ADR 0004: scheduled/unsupervised reads are general for Fleet Adoption Contract adopters, governed by a fire-tested kill switch and weekly telemetry review.

## Public package docs

Use these when evaluating or contributing to the standalone package surface:

- [`../README.md`](../README.md) — package scope, current status, operator quickstart, local verification, and module layout.
- [`../CHANGELOG.md`](../CHANGELOG.md) — API/schema stability ledger, v0.1.0 public release baseline, and future PR entry template.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — safe contribution lanes, held surfaces, local checks, and documentation hygiene.
- [`../SECURITY.md`](../SECURITY.md) — security boundary and private vulnerability reporting posture.
- [`../ROADMAP.md`](../ROADMAP.md) — staged no-live development ladder and held future authority.
- [`public-hygiene.md`](public-hygiene.md) — public hygiene scanner purpose, quarantine rules, and generated-cache exclusions.
- [`public-private-hygiene-inventory.md`](public-private-hygiene-inventory.md) — public/private hygiene inventory naming public surfaces, scanner target classes, safe exceptions, and omitted private planning material.
- [`package-boundary.md`](package-boundary.md) — package-boundary alignment note for the public no-live release, downstream adapter ownership, and held runtime/write authority.
- [`packaging.md`](packaging.md) — local build/install smoke and package metadata boundaries.
- [`issue-railed-autopilot.md`](issue-railed-autopilot.md) — reusable bounded autopilot template, issue rails, hard holds, and final harvest checklist.
- [`l4-closure-review.md`](l4-closure-review.md) — L4 closure packet with issue/PR evidence, verifier commands, residual holds, and next-lane recommendation.
- [`f2-verifier-packet.md`](f2-verifier-packet.md) — F2 verifier packet with issue/PR evidence, local verifier commands, residual holds, and the supervised F3 unlock decision.
- [`f3-manual-pull-dogfood.md`](f3-manual-pull-dogfood.md) — supervised no-live source-card-first context/recall dogfood harness, commands, expected output, and held authority.
- [`librarian-dogfood.md`](librarian-dogfood.md) — in-process memory-librarian template-package dogfood runner covering doctor, health/context, five receipted recalls, hostile-note data handling, draft separation, and deterministic reports.
- [`f3-source-card-usefulness-proof.md`](f3-source-card-usefulness-proof.md) — source-card usefulness proof packet with PASS/HOLD/FAIL outcomes, safe source-card IDs, fallback avoidance, and held no-live surfaces.
- [`f3-verifier-packet.md`](f3-verifier-packet.md) — F3 supervised-pull verifier packet with issue/PR evidence, no-live trust-boundary finding, residual holds, and the F4 no-service identity unlock decision.
- [`no-service-identity-semantics.md`](no-service-identity-semantics.md) — F4 no-service identity semantics for caller subject, acting-for, audience/scope, descriptor subject, query/body mismatch, and held service/live/write authority.
- [`f4-verifier-packet.md`](f4-verifier-packet.md) — F4 no-service identity verifier packet with issue/PR evidence, denial-before-read identity proof, preserved service holds, and the F10 hygiene-prep unlock decision.
- [`l5-idle-tick-contract.md`](l5-idle-tick-contract.md) — L5.01 metadata-only idle tick contract proving wake/check behavior without source/provider/file/stat/backend access or activation.
- [`l5-supervised-source-grant-packet.md`](l5-supervised-source-grant-packet.md) — L5 supervised source-grant decision packet for exactly one future human-approved metadata-only project-doc source-card read while execution remains held.
- [`l5-supervised-one-read-runbook.md`](l5-supervised-one-read-runbook.md) — L5.04 dry-run/no-exec runbook and helper command shape for the future #105 one-read gate, preserving held live-read, source-discovery, service, Runtime Registry, global-config, write/custody, provider/prod/canary, publication, and Gate surfaces.
- [`l5-supervised-one-read-receipt.md`](l5-supervised-one-read-receipt.md) — L5.05 report-safe receipt for the one approved supervised metadata-only source-card read, including posture counters, usefulness verdict, stop conditions, rollback, and preserved write/custody/Gate holds.
- [`l5-post-read-verifier.md`](l5-post-read-verifier.md) — L5.06 no-live post-read verifier for usefulness classification, public/private hygiene failure, and held-posture counter checks without additional reads.
- [`l5-bounded-runner.md`](l5-bounded-runner.md) — L5.07 default-off bounded runner shape for finite approved metadata-only ticks with expiry, anti-recursion, denial/error stops, and no activation.
- [`l5-supervised-canary-one-tick-unhold-packet.md`](l5-supervised-canary-one-tick-unhold-packet.md) — L5.08 no-execution one-tick bounded-runner canary packet with exact future approval phrase, expiry, stop conditions, rollback, and preserved activation/write/Gate holds.
- [`l6-write-intent-threat-model.md`](l6-write-intent-threat-model.md) — L6.01 write-intent threat model and custody boundary defining non-goals, future approval/audit requirements, rollback expectations, and current unsupported write/custody/reindex surfaces without adding implementation.
- [`l6-write-custody-approval-model.md`](l6-write-custody-approval-model.md) — L6S.01 non-executing write/custody ownership and approval model naming custody owner, approver, actor binding, expiry, max-operation-count, operation-class, and report-safe approval reference requirements while implementation remains held.
- [`l6-write-custody-rollback-audit-plan.md`](l6-write-custody-rollback-audit-plan.md) — L6S.02 non-executing rollback/audit plan for one future write/custody slice naming required rollback shape, audit fields, stop conditions, timeout, and failure modes while runtime mutation remains unsupported.
- [`l6-write-custody-operation-class-fixtures.md`](l6-write-custody-operation-class-fixtures.md) — L6S.03 non-executing operation-class fixtures for write intent, custody receipt persistence, delete, reindex, rollback, and cache purge with owner/count/timeout/rollback/approval references while runtime routes remain denied/no-op.
- [`l6-write-intent-preflight-gate.md`](l6-write-intent-preflight-gate.md) — L6I.01/L6I.02/L6I.03/L6I.04 approved default-off synthetic write-intent preflight gate skeleton denying before provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks with report-safe denial receipt metadata, stale/mismatched approval denial hardening, and a local no-production smoke path.
- [`../ROADMAP.md`](../ROADMAP.md#l6--write-custody-companion) — current L6 OSS-track frontier refresh through L6I.06, naming the docs/tests-only positive-authorization prep tranche and preserving all write/custody/runtime/source/publication/Gate holds.
- [`l6v01-supervised-source-card-preflight.md`](l6v01-supervised-source-card-preflight.md) — L6V.01/L6V.02/L6V.03 approved default-off synthetic/no-live supervised source-card proof preflight skeleton, stale/variant denial matrix, and report-safe descriptor fixture proof for issue #187/#188/#189, recognizing only one report-safe `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF` approval shape with `max_operation_count=1`, emitting metadata-only non-persistent held/ready receipts, and validating committed synthetic descriptor/source-card fixtures before report output while callbacks, live/private reads, source discovery, credentials, Runtime Registry, persistence, activation, publication, production authority, external gate movement, broadened/copied/unrelated approvals, raw content/paths/URIs/tokens/platform IDs/payloads/correlation refs, and any `allowed=true` route remain held.

## Runtime, contracts, and schema notes

Use these for the default-off core behavior and contract snapshots:

- [`default-off-runtime.md`](default-off-runtime.md) — in-process read-only runtime skeleton and explicit no-live posture.
- [`envelope-schema-snapshots.md`](envelope-schema-snapshots.md) — pinned health/context/recall envelope shapes.
- [`schema-contracts.md`](schema-contracts.md) — portable descriptor, grant/control-plane, receipt/source-floor, degraded/no-live, and disclosure-label contract.
- [`policy-semantics-decision-note.md`](policy-semantics-decision-note.md) — F2 policy semantics decision for subject/include, descriptor/grant intersection, source-floor labels, denial reasons, and held authority.
- [`contract-test-inventory.md`](contract-test-inventory.md) — test-to-invariant map and missing coverage candidates.
- [`route-parser-contract.md`](route-parser-contract.md) — no-live router query/method/path edge-case contract.
- [`memory-expansion.md`](memory-expansion.md) — operator-facing boundary between profile memory, session artifacts, read-only seam context, and future write custody.

## Adapter and downstream migration notes

Use these for downstream bridge work that imports Memory Seam without duplicating core contracts or activating live services:

- [`atlas-query-bridge.md`](atlas-query-bridge.md) — standalone reference adapter contract fixture and bridge boundaries.
- [`atlas-query-migration.md`](atlas-query-migration.md) — reference/example adapter migration guide, rollback plan, and no-submodule/no-pinned-production-checkout rule.
- [`adapter-import-boundary.md`](adapter-import-boundary.md) — adapter import-boundary compatibility note for downstream wrappers that depend on the package without reversing the dependency into core.
- [`adapter-certification.md`](adapter-certification.md) — adapter protocol v0.2 certification bar, including path/redaction/cap/posture requirements and the reusable pytest helper.
- [`downstream-integration-smoke-plan.md`](downstream-integration-smoke-plan.md) — no-mutation downstream package import, synthetic context/recall smoke, expected output, rollback, and held authority plan.

## Examples

Runnable no-live examples live outside `docs/` so they can be exercised by tests and local operators:

- [`../examples/quickstart_smoke.py`](../examples/quickstart_smoke.py) — synthetic context/recall quickstart smoke.
- [`../examples/manual_pull_dogfood.py`](../examples/manual_pull_dogfood.py) — compact supervised manual-pull source-card/context/recall proof over committed synthetic fixtures only.
- [`../examples/null_and_fake_providers.py`](../examples/null_and_fake_providers.py) — null-provider and deterministic fake-provider examples.
- [`../examples/write_intent_preflight_smoke.py`](../examples/write_intent_preflight_smoke.py) — local synthetic no-production write-intent preflight denial smoke that emits report-safe JSON and preserves zero guarded counters.
- [`../examples/l6_positive_authorization_no_production_smoke.py`](../examples/l6_positive_authorization_no_production_smoke.py) — local synthetic positive-authorization smoke that emits a report-safe stdout-only held receipt summary without mutation, persistence, callbacks, source access, activation, publication, provider/prod/canary authority, or Gate movement.
- [`../examples/l6v_supervised_source_card_no_live_smoke.py`](../examples/l6v_supervised_source_card_no_live_smoke.py) — local synthetic supervised source-card proof smoke that emits report-safe stdout-only JSON with all guarded counters at zero and no live adapter, callback, persistence, production, or Gate behavior.

## Deployment patterns

Guides for extending the seam in specific deployment scenarios. These describe use of existing core machinery and carry no new package code.

- [`patterns/sensitive-pointer-family.md`](patterns/sensitive-pointer-family.md) — ADR 0003 consequence: how a multi-user deployment would add a deny-first `sensitive_pointer` source family using the existing descriptor registry, grant matrix, `private_class` labeling, and receipts; when to use it and when not to.

## Omitted Internal Material

Internal planning and provenance documents are maintained privately and omitted
from this repository.

Token-like strings, host-private paths, raw platform IDs, private issue-comment
URLs, and deployment-specific provenance must stay out of public source
artifacts.
