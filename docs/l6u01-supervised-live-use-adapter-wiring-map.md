# L6U.01 supervised live-use adapter wiring map

Status: `DOCS_TESTS_ONLY_ADAPTER_BOUNDARY_MAP`
Parent: #6
Rail issue: #177
Source floor: `1299f4f` or later
Upstream packet: `docs/l6-supervised-live-use-next-rail-decision-packet.md`

This packet maps one future supervised live-use adapter boundary without implementing or executing any live/private read. It is documentation and contract-test evidence only. It is not approval, not a runtime adapter, not an activation path, and not a production/canary/provider authority grant.

## One future proof target

Future proof target: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.

The target is limited to one operator-approved, report-safe source-card/descriptor read-side proof in a later HITL-approved issue. L6U.01 does not select an actual private source, read raw content, discover sources, query indexes, perform broad recall, call source-stat/source-read APIs, consume Runtime Registry data, or recognize any approval. It only names the future target shape and does not recognize any approval, so later packets can bind exact approval requirements before any implementation or execution is considered.

## Adapter boundary map

Dependency direction:

- Memory Seam core remains standalone and does not import Atlas Query, Hermes, provider backends, Runtime Registry clients, workspace scanners, source readers, source-stat helpers, or downstream adapter modules.
- Any Atlas Query or Hermes adapter must live downstream and depend on Memory Seam contracts, not the reverse.
- The adapter boundary is default-off until a later issue supplies explicit HITL approval, implementation authority, and no-production/live-read limits.
- Denial and HOLD decisions must happen before any provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback family.

Future adapter inputs may contain only report-safe metadata fields shaped like:

```text
future_issue_ref: "#TBD"
proof_target: "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"
caller_subject_ref: "operator-approved-subject-ref"
acting_for_ref: "operator-approved-owner-ref"
audience: "memory-seam-supervised-live-use"
scope: "source-card-read-proof"
fixture_ref: "l6u01.synthetic.source-card.v1"
descriptor_ref: "descriptor.synthetic.report-safe.v1"
source_card_ref: "source-card.synthetic.report-safe.v1"
approval_ref: "future-hitl-approval-ref-required"
expiry_ref: "future-expiry-required"
```

These are reference strings only. They must not contain raw private source text, raw paths, credentials, tokens, auth material, platform IDs, raw query/payload content, private correlation references, or source-family discovery output.

## Allowed synthetic fixtures

Allowed committed synthetic fixtures for future tests are limited to metadata-only shapes:

- `l6u01.synthetic.source-card.v1` — safe source-card reference with title/classification/family labels and no body text.
- `descriptor.synthetic.report-safe.v1` — descriptor reference with subject/audience/scope labels and disabled-by-default posture.
- `caller.synthetic.operator-ref.v1` — caller identity reference with subject/acting-for/audience/scope strings only.
- `receipt.synthetic.zero-callback-counters.v1` — expected all-zero counter fixture for guarded callback families.

No fixture may include secrets, credentials, private paths, raw document content, raw prompt/query text, live source identifiers, OAuth/keychain/env material, or Runtime Registry references.

## Required report-safe source-card and descriptor shape

Any later proof must keep reportable artifacts to this kind of public-safe metadata:

- `source_card_ref`
- `descriptor_ref`
- `proof_target`
- `issue_ref`
- `caller_subject_ref`
- `acting_for_ref`
- `audience`
- `scope`
- `approval_ref`
- `expiry_ref`
- `status` with `HOLD`, `DENIED_BEFORE_CALLBACK`, or future review vocabulary supplied by a later issue
- `guarded_callback_counters` with every guarded family equal to `0`

The shape intentionally excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw query/payload content, private correlation references, backend response bodies, and Runtime Registry data.

## Guarded callback families that must remain zero

The L6U.01 boundary requires all of these counters to remain zero in docs/tests evidence and in any later denied/HOLD preflight path unless a separate exact HITL-approved issue narrows one family:

- `provider_callback_count=0`
- `backend_callback_count=0`
- `source_stat_callback_count=0`
- `source_read_callback_count=0`
- `write_callback_count=0`
- `custody_callback_count=0`
- `delete_callback_count=0`
- `reindex_callback_count=0`
- `rollback_callback_count=0`
- `cache_purge_callback_count=0`
- `runtime_registry_consumption_count=0`
- `source_discovery_count=0`
- `allowed_result_count=0`
- `persistence_record_count=0`
- `activation_count=0`

## Explicit held surfaces

L6U.01 preserves the full rail hold:

- no implementation or execution of live/private reads;
- no credentials, auth, env, keychain, OAuth, or auth-file reads;
- no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption;
- no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- no mutation execution, no `allowed=true` path, no write/custody/delete/reindex/rollback/cache-purge behavior, no persistence/audit/custody records, and no cache mutation;
- no service/listener/startup/cron activation, global Hermes/MCP/client/runtime config mutation, package publication, repository visibility change, provider/prod/canary authority, production authority, or Atlas Gate movement.

## Acceptance evidence

Companion tests prove this map is discoverable from the docs index and contract-test inventory, adapter-boundary-only, default-off, no-live, no-callback, no-source-discovery, Runtime-Registry-free, and limited to exactly one future proof target shape without raw private content or credentials.
