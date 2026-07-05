# L6U.03 local integration smoke design

Status: `LOCAL_ONLY_SYNTHETIC_SMOKE_DESIGN_NOT_IMPLEMENTATION`

Parent: #6  
Issue: #179  
Source floor: `1299f4f` or later on `origin/main`  
Upstream packet: `docs/l6-supervised-live-use-next-rail-decision-packet.md`  
Prerequisites: L6U.01 closed/PASS adapter wiring map and L6U.02 packet shape available

This packet designs one future local integration smoke for the supervised live-use rail. It is documentation and contract-test evidence only. It does not implement an adapter, execute a live/private read, discover sources, read credentials, call provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, consume Runtime Registry data, persist receipts, mutate caches, activate services, publish packages, change repository visibility, claim provider/prod/canary authority, move Atlas Gate, or recognize any approval.

## One future smoke target

Future smoke target: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.

The smoke is limited to exactly one future proof target and exactly one local smoke operation over committed synthetic fixtures. It imports a future downstream adapter/wrapper boundary only after a later exact HITL-approved implementation issue exists. Until then, this design is default-off and non-executable.

The smoke goal is narrow: prove local import/wiring and report formatting can be exercised with committed synthetic fixture data while callback counters remain zero and stdout remains public-safe. It is not a live-read proof, not approval to connect to private sources, and not authority to start listeners or scheduled jobs.

## Synthetic-only input set

Allowed future fixture family: `tests/fixtures/l6u03_synthetic_source_card_read_smoke.json`.

The fixture shape may contain only report-safe placeholders:

- `fixture_id`: stable synthetic fixture reference.
- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.
- `source_card_ref`: report-safe synthetic source-card reference.
- `descriptor_ref`: report-safe synthetic descriptor reference.
- `caller_subject_ref`: report-safe caller subject reference.
- `acting_for_ref`: report-safe acting-for / owner reference.
- `approval_packet_ref`: report-safe pointer to the L6U.02 packet shape, not approval.
- `expected_public_receipt_ref`: report-safe expected receipt reference.
- `guarded_callback_counters`: all guarded callback families fixed at zero.

The fixture must exclude raw source content, source path, source URI, credential material, raw platform identifiers, raw prompt/query text, raw payload content, private correlation references, backend response bodies, Runtime Registry data, persistence record bodies, audit/custody record bodies, environment variable values, OAuth material, keychain material, and auth-file content. In short: it excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw prompt/query text, raw payload content, private correlation references.

## Local no-live smoke flow

A later approved local smoke may use this sequence only if it remains committed-fixture-only and default-off:

1. Load the committed synthetic fixture by repository-relative path only.
2. Validate `operation_class == SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.
3. Validate `synthetic_fixture_only=true`, `local_only=true`, `default_off=true`, and `live_adapter_invoked=false`.
4. Validate all source discovery and Runtime Registry counters are zero before any adapter import boundary is touched.
5. Import only a local downstream adapter/wrapper boundary that depends on Memory Seam; Memory Seam core must not import downstream Atlas Query, Hermes, provider, backend, source, or Runtime Registry modules.
6. Produce a stdout-only public-safe smoke summary with references, booleans, and zero counters only.
7. Exit with `HOLD_NO_LIVE_ADAPTER` if any requested input attempts source discovery, credential reads, live/private reads, callbacks, activation, publication, provider/prod/canary authority, production authority, Atlas Gate movement, persistence, cache mutation, or write/custody/delete/reindex/rollback/cache-purge behavior.

No step may perform a live/private read, source discovery, workspace scan, family scan, broad recall, index query, source-stat call, source-read call, provider/backend callback, Runtime Registry lookup, credential/auth/env/keychain/OAuth/auth-file read, mutation execution, persistence/audit/custody record write, cache mutation, service/listener/startup/cron activation, global Hermes/MCP/client/runtime config mutation, package publication, visibility change, provider/prod/canary movement, production movement, or Atlas Gate movement.

## Required public stdout shape

The future stdout report must be JSON or line-oriented metadata with only these report-safe fields:

- `status`: `HOLD_NO_LIVE_ADAPTER` or `LOCAL_SYNTHETIC_SMOKE_DESIGNED`.
- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.
- `fixture_id`.
- `source_card_ref`.
- `descriptor_ref`.
- `caller_subject_ref`.
- `acting_for_ref`.
- `local_only`: `true`.
- `synthetic_fixture_only`: `true`.
- `default_off`: `true`.
- `live_adapter_invoked`: `false`.
- `guarded_callback_counters`.
- `unsupported_behavior`: `write/custody/delete/reindex/rollback/cache-purge`.
- `public_hygiene_result`.

The stdout report must not echo raw prompts, raw source content, private paths, source URIs, credentials, token-like material, env values, OAuth material, keychain material, auth-file content, raw backend responses, Runtime Registry references, audit/custody bodies, persistence bodies, or private correlation references.

## Zero guarded counters

The local smoke design requires these counters to remain zero:

| Counter family | Required value | Rationale |
| --- | ---: | --- |
| `source_discovery_count` | `0` | No source discovery, workspace scans, family scans, broad recall, or index queries. |
| `runtime_registry_consumption_count` | `0` | No Runtime Registry lookup or consumption. |
| `provider_callback_count` | `0` | no provider callbacks. |
| `backend_callback_count` | `0` | No backend callbacks. |
| `source_stat_callback_count` | `0` | No source-stat callbacks. |
| `source_read_callback_count` | `0` | no source-read callbacks or live/private reads. |
| `write_callback_count` | `0` | Write behavior remains unsupported. |
| `custody_callback_count` | `0` | Custody behavior remains unsupported. |
| `delete_callback_count` | `0` | Delete behavior remains unsupported. |
| `reindex_callback_count` | `0` | Reindex behavior remains unsupported. |
| `rollback_callback_count` | `0` | Rollback behavior remains unsupported. |
| `cache_purge_callback_count` | `0` | Cache-purge behavior remains unsupported. |
| `persistence_record_count` | `0` | No persistence/audit/custody records. |
| `cache_mutation_count` | `0` | No cache mutation. |
| `service_activation_count` | `0` | No service/listener/startup/cron activation. |

Any non-zero guarded counter is a HOLD before callbacks and before any live adapter invocation.

## Unsupported behavior remains unsupported

The design explicitly treats `write/custody/delete/reindex/rollback/cache-purge` as unsupported behavior. A future smoke must reject requests for those behaviors with `HOLD_NO_LIVE_ADAPTER` before callbacks, persistence, cache mutation, or mutation execution. It must never produce an `allowed=true` path.

## Live adapter invocation remains prohibited

The smoke design proves local import/wiring only. Required sentinel: `live_adapter_invoked=false`.

If a future implementation attempts to invoke a live adapter, private source, provider/backend/source callback, source discovery path, Runtime Registry path, credential path, activation path, production/canary/provider path, publication path, visibility path, or Atlas Gate path, the smoke must stop with HOLD and must not continue.

## Preserved rail hold

L6U.03 preserves the full rail hold:

- no implementation or execution of live/private reads;
- no credentials, auth, env, keychain, OAuth, or auth-file reads;
- no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption;
- no Runtime Registry consumption;
- no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- no mutation execution, no `allowed=true` path;
- no persistence/audit/custody records;
- no cache mutation;
- no service/listener/startup/cron activation;
- no global Hermes/MCP/client/runtime config mutation;
- no package publication;
- no repository visibility change;
- no provider/prod/canary authority;
- no production authority;
- no Atlas Gate movement.

Companion tests prove this smoke design is discoverable from the docs index and contract-test inventory, local-only, synthetic-only, default-off, report-safe, no-live, no-callback, no-source-discovery, Runtime-Registry-free, keeps write/custody/delete/reindex/rollback/cache-purge unsupported, and requires `live_adapter_invoked=false` for the single future proof target.
