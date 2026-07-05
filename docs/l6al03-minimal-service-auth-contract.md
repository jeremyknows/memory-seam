# L6AL.03 minimal non-secret service auth contract

Status: `PASS_MINIMAL_SERVICE_AUTH_CONTRACT_READY_RETRY_STILL_HELD`

Rail issue: #351
Parent issue: #6
Depends on: L6AL.01-L6AL.02 closed/PASS
Roadmap step: 5 service/provider auth prerequisite for a future Step 3 exact supervised metadata read retry
Rail starting source floor: `f335f09891a41f43583fbf434482cfb096a04fcd`
Operation classified: `L6AL_MINIMAL_NON_SECRET_SERVICE_AUTH_CONTRACT`
Evidence class: `SERVICE_PROVIDER_AUTH_CONTRACT_TYPED_RECEIPT`

This packet implements the smallest non-secret service/provider auth contract needed to classify a future exact supervised metadata retry as auth-ready or auth-held. It does not perform a live/private read retry, does not authorize a read, does not start a service, does not invoke provider routes or callbacks, does not consume Runtime Registry data, and does not load secrets.

## Contract surface

`src/memory_seam/l6al_service_auth_contract.py` defines an immutable `ServiceAuthContract` fixture plus `evaluate_l6al03_service_auth_contract`. The evaluator accepts only non-secret labels:

- `endpoint`: one of `context`, `recall`, or `health`.
- `route_audience`: exactly one endpoint audience: `memory-seam:read:context`, `memory-seam:read:recall`, or `memory-seam:read:health`.
- `acting_for`: exactly `sax` for this issue-bound rail subject.
- `identity_subject`: exactly `atlas-query-supervised-metadata-reader`; missing or mismatched identity denies before read.
- `agent`: exactly `sax`; not inherited by other profiles or providers.
- `scope`: exactly `metadata_only:wiki:health:max_one`, preserving metadata-only, report-safe, max-one operation posture.
- `evidence_class`: endpoint-specific `SUPERVISED_METADATA_CONTEXT_READ_RETRY`, `SUPERVISED_METADATA_RECALL_READ_RETRY`, or `SUPERVISED_METADATA_HEALTH_AUTH_POSTURE`.
- `expiry`: exactly `fresh_issue_bound_not_expired`; stale approval denies before read.
- `provider_binding_present` and `service_binding_present`: non-secret readiness labels used only to distinguish auth-ready from auth-held.
- `authorization_narrowing`: exactly `exact`; cross-route fallback or narrower substitution denies before read as `unauthorized_narrowing`.

## Outcomes

| Outcome | Status | Meaning | Read posture |
| --- | --- | --- | --- |
| exact contract | `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY` | all non-secret service/provider bindings are present and exact | `read_authorized=false`, `retry_executed=false`, `items=[]` |
| missing service/provider binding | `AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE` | endpoint and identity labels are exact, but a required non-secret binding is absent | `read_authorized=false`, `retry_executed=false`, `items=[]` |
| auth mismatch | `DENIED_BEFORE_READ_AUTH_CONTRACT_MISMATCH` | wrong audience, unauthorized narrowing, missing/mismatched identity, stale approval, broadened scope, raw output, or unsafe payload request | `read_authorized=false`, `retry_executed=false`, `items=[]` |

`AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY` is report-safe readiness metadata only. It is not a live read grant and does not execute the retry. A future exact supervised metadata read retry still requires a separately issue-bound execution packet.

## Default-deny and held behavior

The evaluator denies before source access for:

- `wrong_route_audience`
- `unauthorized_narrowing`
- `missing_identity_subject`
- `mismatched_identity_subject`
- `mismatched_agent`
- `broadened_scope_denied`
- `raw_output_denied`
- `stale_approval`
- `mismatched_evidence_class`
- `unknown_endpoint`
- `broad_allowed_true_denied`

It returns auth-held, not auth-ready, for `provider_binding_missing` or `service_binding_missing`. Held receipts remain report-safe and side-effect-free.

All receipts keep `source_access_count=0`, `source_item_count=0`, `source_read_callback_count=0`, `provider_callback_count=0`, `provider_route_invocation_count=0`, `live_private_read_count=0`, `source_discovery_count=0`, `runtime_registry_read_count=0`, `credential_or_secret_read_count=0`, `persistence_or_mutation_attempt_count=0`, `activation_attempt_count=0`, `publication_or_gate_movement_attempt_count=0`, and `broad_allowed_attempt_count=0`.

## Report-safe output boundary

Receipt-safe output may include schema/repo/issue metadata, status, `auth_ready`, `auth_held`, denial/hold reason, endpoint labels, binding-summary booleans, `read_authorized=false`, `retry_executed=false`, `items=[]`, zero guarded counters, and artifact paths. It must not include raw item content, raw approval prose, credential/auth material, provider payloads, callback payloads, source URIs, private paths, platform raw IDs, token-like values, Runtime Registry payloads, private correlation refs, environment values, keychain entries, OAuth material, or auth-file material.

## Acceptance and verification gate

L6AL.03 is complete when this contract implementation, documentation, and tests are committed, discoverable from the docs index and contract-test inventory, and the following commands pass:

- `python -m pytest -q tests/test_l6al03_service_auth_contract.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

Residual holds after this packet: no live/private read retry; no secret/env/keychain/OAuth/auth-file/credential reads; no source discovery; no broad recall/index queries; no Runtime Registry consumption; no provider callback invocation; no provider route execution; no service activation; no cron changes; no persistence/mutation/write/delete/reindex/rollback/cache-purge; no publication/visibility/provider/prod/canary/Gate movement; no Atlas Gate movement; no broad `allowed=true` behavior.
