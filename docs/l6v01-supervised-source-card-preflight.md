# L6V.01 supervised source-card proof preflight skeleton

Status: `DEFAULT_OFF_SYNTHETIC_NO_LIVE_PREFLIGHT`

Parent: #6  
Issue: #187  
Source floor: `876375b` or later on `origin/main`  
Upstream packet: `docs/l6u05-supervised-live-use-trust-boundary-review.md`  
Approval source: `fixture:l6v-supervised-source-card-approval-source:internal-review-2026`

This slice implements the smallest default-off preflight skeleton for one operation class, `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`. It recognizes only the issue #187 report-safe approval shape, `max_operation_count=1`, committed synthetic descriptor/source-card references, and metadata-only stop-condition references. It emits a non-persistent held/ready preflight receipt that remains report-safe and public-hygiene compatible.

The skeleton does not execute live/private reads, expose raw source content, discover sources, scan workspaces or source families, perform broad recall, query indexes, call source-stat/source-read, invoke provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, read credentials/auth/env/keychain/OAuth/auth files, consume Runtime Registry data, persist audit/custody/cache records, mutate caches, activate services/listeners/startup/cron paths, mutate global Hermes/MCP/client/runtime config, publish packages, change repository visibility, claim provider/prod/canary or production authority, move Atlas Gate, execute mutations, or introduce any `allowed=true` route.

## Exact recognized operation

The only recognized operation class is exactly:

`SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`

Variants such as lowercase, hyphenated, broadened, callback-requesting, source-read-requesting, copied, stale, or mismatched operation strings are denied or held before any callback. The preflight status can be `ready_metadata_only_preflight` for the exact fresh issue-bound shape, but the runtime authorization fields remain `allowed=false`, `allowed_result_count=0`, and `allowed_true_route_present=false`.

## Required approval fields

The issue-bound approval context fixture requires these report-safe fields:

- `issue_ref=#187`
- `operation_class=SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`
- `max_operation_count=1`
- `actor_ref`
- `subject_ref`
- `owner_ref`
- `audience`
- `scope`
- `approval_ref=issue-187-comment-4645178496`
- `approval_source_url=fixture:l6v-supervised-source-card-approval-source:internal-review-2026`
- `author_association=OWNER`
- `approval_created_at=2026-06-08T03:28:46Z`
- `approval_expires_at=2026-06-08T15:28:46Z`
- `evaluation_time`
- `descriptor_ref=synthetic_descriptor:l6v-report-safe-project-doc-v1`
- `source_card_ref=synthetic_source_card:l6v-report-safe-project-doc-v1`
- `stop_condition_refs`

The fixture explicitly excludes raw approval text, raw actor IDs, raw source content, source URIs, private paths, credentials, raw prompts, raw queries, raw payload content, raw backend responses, and private correlation references.

## Denial/HOLD before callback matrix

The L6V.02 hardening slice expands the preflight matrix while keeping the same default-off/no-live implementation boundary. The implementation validates stale, variant, missing, broadened, copied, mismatched, unrelated actor/subject/owner/audience, broadened stop-condition, callback-requesting, activation-requesting, publication-requesting, provider/prod/canary-requesting, Gate-moving, Runtime-Registry-requesting, source-discovery-requesting, live-private-read-requesting, and write-family-requesting approval shapes before any guarded callback surface. Denied or held outcomes keep:

- `denied_or_held_before_callback=true`
- `callbacks_invoked=false`
- `live_adapter_invoked=false`
- `mutation_attempted=false`
- `persistence_attempted=false`
- `allowed=false`
- `allowed_result_count=0`
- `allowed_true_route_present=false`

The guarded counter set stays at zero for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, cache-purge, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, source discovery, workspace scans, family scans, broad recall, index queries, live/private reads, persistence/audit/custody/cache mutation, service activation, publication, visibility changes, and Atlas Gate movement.

## Receipt posture

The receipt schema is `l6v-supervised-source-card-receipt-v1`. Receipts are metadata-only and non-persistent. A ready receipt means only that the synthetic issue-bound preflight shape matched; it is not approval to perform a live/private read, call an adapter, read a source, persist custody/audit/cache state, activate services, publish, change visibility, claim production/provider/prod/canary authority, or move Atlas Gate.

## L6V.03 report-safe source-card descriptor fixture proof

Issue #189 adds the committed synthetic descriptor/source-card fixture proof. The proof accepts only metadata fields such as `descriptor_ref`, `source_card_ref`, `fixture_ref`, subject/audience/scope refs, and boolean safety flags. It fails closed before report output if a fixture includes raw source content, private paths, raw source URIs, credential/auth/token-shaped material, raw prompts or queries, raw payload/backend response text, raw platform IDs, private correlation references, broadened scope, missing required fields, or unsafe report flags.

The report-safe descriptor proof output is limited to public-safe status strings, refs, booleans, zero guarded counters, denial codes, source floor, upstream packet, and operation class. It does not echo submitted unsafe values. It keeps `allowed=false`, `allowed_result_count=0`, `allowed_true_route_present=false`, `callbacks_invoked=false`, `live_adapter_invoked=false`, `mutation_attempted=false`, and `persistence_attempted=false` for both accepted and rejected synthetic fixture cases.

## Companion tests

`tests/test_l6v01_supervised_source_card_preflight.py` proves exact issue-bound operation recognition, max-one-operation binding, stale/variant/missing/broadened/copied denial or HOLD before callbacks, L6V.02 unrelated/held-authority denial hardening, zero callback/source/credential/runtime/persistence counters, report-safe descriptor/source-card fixture references, no raw unsafe request echoing, no live adapter invocation, no persistence, and no `allowed=true` path.

`tests/test_l6v03_report_safe_source_card_descriptor_fixture.py` proves the L6V.03 report-safe source-card descriptor fixture proof, including committed synthetic metadata-only fixture fields, raw content/private path/source URI/token/platform ID/query/payload/backend response/private correlation rejection before report output, no unsafe value echo, all-zero guarded counters, and preserved no-live/no-callback/no-production/no-`allowed=true` boundaries.

`docs/l6v04-supervised-source-card-no-live-smoke.md`, `examples/l6v_supervised_source_card_no_live_smoke.py`, and `tests/test_l6v04_supervised_source_card_no_live_smoke.py` add the L6V.04 local no-live smoke. The smoke runs one recognized synthetic preflight, emits stdout-only report-safe JSON with descriptor/source-card refs and all guarded counters at zero, and preserves no live adapter, no callbacks, no persistence, no mutation, no production authority, no Gate movement, and no `allowed=true` path.
