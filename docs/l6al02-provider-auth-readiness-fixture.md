# L6AL.02 non-secret provider auth readiness fixture

Status: `PASS_PROVIDER_AUTH_READINESS_FIXTURE_READY_RETRY_STILL_HELD`

Rail issue: #350
Parent issue: #6
Depends on: L6AL.01 #349 closed/PASS
Roadmap step: 5 service/provider auth prerequisite for a future Step 3 exact supervised metadata read retry
Rail starting source floor: `f335f09891a41f43583fbf434482cfb096a04fcd`
Operation classified: `L6AL_PROVIDER_AUTH_READINESS_FIXTURE`
Evidence class: `NO_LIVE_SERVICE_PROVIDER_AUTH_READINESS_FIXTURE`

This packet adds a fixture-only service/provider auth readiness evaluator. It uses non-secret labels only, performs no live/private read retry, loads no secret material, invokes no provider callback, calls no read callback, consumes no Runtime Registry payload, starts no service, and creates no route that can return broad `allowed=true` behavior.

## Fixture shapes

Authorized metadata-read readiness fixture fields:

- `route_audience`: exactly `memory-seam:read:recall` for this no-live recall-readiness fixture.
- `acting_for`: exactly `sax` for the issue-bound rail subject.
- `identity_subject`: exactly `atlas-query-supervised-metadata-reader`; missing or mismatched identity denies before read.
- `agent`: exactly `sax`; not inherited by another profile or provider identity.
- `scope`: exactly `metadata_only:wiki:health:max_one`, preserving metadata-only, report-safe, max-one posture.
- `evidence_class`: exactly `SUPERVISED_METADATA_RECALL_READ_RETRY`.
- `expiry`: exactly `fresh_issue_bound_not_expired`; stale or missing freshness denies before read.
- `provider_binding_present=true` and `service_binding_present=true` as non-secret readiness labels only.
- `authorization_narrowing=exact`; route fallback, cross-route narrowing, or narrower context substitutions deny before read.

Denied-before-read mismatch fixtures include `wrong_route_audience`, `unauthorized_narrowing`, `missing_identity_subject`, `stale_approval`, `broadened_scope_denied`, `raw_output_denied`, and `broad_allowed_true_denied` variants. The evaluator accepts only committed fixture labels; it does not read environment values, keychain entries, OAuth material, auth files, credentials, Runtime Registry data, callback payloads, provider payloads, source descriptors, source URIs, source items, platform raw IDs, private paths, raw private content, raw source text, or raw approval prose.

## Denial-before-read counters

All readiness and denial receipts keep these counters at zero:

- `source_item_count=0`
- `source_read_callback_count=0`
- `provider_callback_count=0`
- `provider_route_invocation_count=0`
- `live_private_read_count=0`
- `source_discovery_count=0`
- `runtime_registry_read_count=0`
- `credential_or_secret_read_count=0`
- `persistence_or_mutation_attempt_count=0`
- `activation_attempt_count=0`
- `publication_or_gate_movement_attempt_count=0`
- `broad_allowed_attempt_count=0`

The positive fixture may return `auth_ready=true`, but it still returns `read_authorized=false`, `retry_executed=false`, and `items=[]`. `auth_ready=true` is readiness metadata for a future separately issue-bound retry decision; it is not itself a read grant and does not call the inert `source_read_callback` fixture label.

## Required L6AK safe-403 coverage

The tests explicitly preserve the L6AK blocker vocabulary:

| Case | Expected denial | Required side-effect posture |
| --- | --- | --- |
| wrong route audience | `wrong_route_audience` | denied before source items/read callbacks |
| unauthorized narrowing | `unauthorized_narrowing` | denied before source items/read callbacks |

Both cases must keep `source_item_count=0`, `source_read_callback_count=0`, `provider_callback_count=0`, `read_authorized=false`, `retry_executed=false`, and `items=[]`.

## Report-safe receipt fields

Report-safe receipts may include schema/repo/issue metadata, status, `auth_ready`, `read_authorized=false`, `retry_executed=false`, `denial_before_read=true`, denial reason, `items=[]`, zero guarded counters, binding summary booleans/labels, and artifact paths. They must not include raw item content, raw approval prose, credential/auth material, provider payloads, callback payloads, source URIs, private paths, platform raw IDs, token-like values, Runtime Registry payloads, or private correlation refs.

## Acceptance and verification gate

L6AL.02 is complete when this fixture/evaluator, documentation, and contract tests are committed, discoverable from the docs index and contract-test inventory, and the following commands pass:

- `python -m pytest -q tests/test_l6al02_provider_auth_readiness_fixture.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

Residual holds after this packet: no secret/env/keychain/OAuth/auth-file/credential reads; no live/private read retry; no source discovery; no broad recall/index queries; no Runtime Registry consumption; no provider callback invocation; no provider route execution; no service activation; no cron changes; no persistence/mutation/write/delete/reindex/rollback/cache-purge; no publication/visibility/provider/prod/canary/Gate movement; no Atlas Gate movement; no broad `allowed=true` behavior.
