# L6W.03 report-safe supervised live-read receipt output contract

Status: `RECEIPT_CONTRACT_ONLY_NO_APPROVAL_NO_EXECUTION`

Parent: #6  
Rail issue: #201  
Prerequisite: #200 closed/PASS  
Source floor: `9264533` or later on `origin/main`  
Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`  
Scaffold dependency: `docs/l6w01-supervised-live-read-approval-packet-scaffold.md`  
Denial dependency: `docs/l6w02-supervised-live-read-approval-denial-matrix.md`

This packet specifies the report-safe receipt shape for a future one-read supervised live/private source-card descriptor read. It is docs/tests/schema-fixture-only. It does not approve, implement, recognize, execute, or simulate a live/private read. It creates no callback, no source discovery, no Runtime Registry consumption, no persistence, no audit/custody record, no cache mutation, no activation, no publication, no production/provider/prod/canary authority, no Atlas Gate movement, no mutation behavior, and no `allowed=true` route.

## Receipt posture invariant

The contract is interpreted as `NO_APPROVAL_PRESENT` until a separate future issue-bound owner approval and later approved implementation recognition exist.

Any future receipt for this lane must bind exactly one operation:

- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ`
- `operation_count`: `1` or `0` when held/denied before read
- `max_operation_count`: `1`
- `one_operation_binding`: `true`
- `allowed`: `false`
- `allowed_result_count`: `0`
- `live_read_invoked`: `false` in all current fixtures/tests and in any stale/variant/held receipt
- `source_discovery_counter`: `0`
- `runtime_registry_consumption_counter`: `0`
- `persistence_record_counter`: `0`
- `audit_record_counter`: `0`
- `custody_record_counter`: `0`
- `cache_mutation_counter`: `0`
- `activation_counter`: `0`
- `publication_or_visibility_counter`: `0`
- `provider_prod_canary_counter`: `0`
- `atlas_gate_movement_counter`: `0`
- `guarded_callback_counters`: synthetic zeros for provider, backend, source-stat, source-read, write, custody, delete, reindex, rollback, and cache-purge families

## Permitted report-safe fields

A receipt may include only the following metadata classes:

| Field family | Permitted examples |
| --- | --- |
| Public refs | public issue refs, public PR refs, repository file names, upstream packet refs, source floor commit refs |
| Operation binding | operation class, operation count, max operation count, one-operation binding boolean |
| Approval posture | approval status labels such as `NO_APPROVAL_PRESENT`, `HELD_FOR_FUTURE_APPROVAL`, `DENIED_BEFORE_CALLBACK`, or `READY_FOR_FUTURE_REVIEW_ONLY` |
| Safe descriptor refs | report-safe descriptor ref, report-safe source-card ref, descriptor/source-card schema version ref |
| Counters | numeric counters, zero guarded callback counters, no-discovery/no-persistence/no-activation/no-production counters |
| Stop status | stop-condition status, stop reason label, expiry status label, retry requirement label |
| Usefulness | usefulness classification labels such as `useful`, `too_redacted`, `unsafe`, `ambiguous`, `held`, or `denied_before_callback` |
| Hygiene proof | report-safe boolean flags proving no raw content echo, no credential echo, no private path echo, no URI echo, and no unsafe payload echo |

The receipt may name the upstream packet and prior L6W docs by repository-relative file name only. It may cite issue and PR numbers because those are public coordination refs.

## Rejected receipt fields and unsafe echo

The contract rejects any receipt that includes or echoes:

- raw private source text;
- raw source content or source-card body text;
- private absolute paths or operator workspace paths;
- source URIs or backend locator strings;
- platform IDs, message IDs, provider IDs, account IDs, or tenant IDs in raw form;
- prompts, queries, broad recall text, index query text, or raw request payloads;
- backend responses, provider responses, source-stat responses, source-read responses, or callback payloads;
- private correlation refs, trace IDs, custody refs, audit refs, cache keys, Runtime Registry refs, or hidden run IDs;
- credentials, auth files, environment secrets, keychain entries, OAuth material, auth-file material, tokens, API keys, cookie values, or session material;
- raw approval text, copied approval comments, stale approval comments, or variant approval text;
- any unsafe submitted value after rejection, including redacted variants that still reveal private shape.

Unsafe input must be rejected before receipt output without echoing the unsafe value. A safe rejection may include only the stop reason label and zero counters.

## Synthetic fixture contract

The committed fixture shape for this rail is metadata-only:

```json
{
  "schema_id": "l6w03.report_safe_supervised_live_read_receipt.v1",
  "status": "HELD_FOR_FUTURE_APPROVAL",
  "approval_status": "NO_APPROVAL_PRESENT",
  "operation_class": "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ",
  "operation_count": 0,
  "max_operation_count": 1,
  "one_operation_binding": true,
  "allowed": false,
  "allowed_result_count": 0,
  "live_read_invoked": false,
  "descriptor_ref": "report-safe-descriptor-ref:l6w03-synthetic",
  "source_card_ref": "report-safe-source-card-ref:l6w03-synthetic",
  "stop_condition_status": "HELD_PENDING_FUTURE_ISSUE_BOUND_OWNER_APPROVAL",
  "stop_reason": "NO_APPROVAL_PRESENT",
  "usefulness_classification": "held",
  "source_discovery_counter": 0,
  "runtime_registry_consumption_counter": 0,
  "persistence_record_counter": 0,
  "audit_record_counter": 0,
  "custody_record_counter": 0,
  "cache_mutation_counter": 0,
  "activation_counter": 0,
  "publication_or_visibility_counter": 0,
  "provider_prod_canary_counter": 0,
  "atlas_gate_movement_counter": 0,
  "guarded_callback_counters": {
    "provider": 0,
    "backend": 0,
    "source_stat": 0,
    "source_read": 0,
    "write": 0,
    "custody": 0,
    "delete": 0,
    "reindex": 0,
    "rollback": 0,
    "cache_purge": 0
  },
  "report_safe_flags": {
    "raw_content_echoed": false,
    "credential_echoed": false,
    "private_path_echoed": false,
    "source_uri_echoed": false,
    "unsafe_payload_echoed": false
  }
}
```

This fixture is non-authoritative, non-persistent, and stdout/report-only. It does not permit a live read and must not be interpreted as a successful approval-recognized receipt.

## Stop-condition receipt statuses

The following statuses are report-safe and must remain pre-callback when they occur:

| Status | Meaning | Required counters |
| --- | --- | --- |
| `HELD_FOR_FUTURE_APPROVAL` | no exact future issue-bound owner approval exists | all guarded counters and side-effect counters are zero |
| `DENIED_BEFORE_CALLBACK` | stale, variant, copied, broadened, unsafe, expired, or mismatched approval/request shape | all guarded counters and side-effect counters are zero |
| `UNSAFE_RECEIPT_FIELD_REJECTED` | proposed receipt output contains a prohibited field or unsafe echo | all guarded counters and side-effect counters are zero |
| `STOPPED_REQUIRES_NEW_HUMAN_REVIEW` | retry/rollback/stop condition requires a new human issue review | all guarded counters and side-effect counters are zero |

No status in this packet authorizes `allowed=true`, non-zero allowed results, provider/backend/source-stat/source-read callbacks, live/private reads, source discovery, Runtime Registry consumption, persistence, activation, publication, production/provider/prod/canary authority, Atlas Gate movement, mutation execution, rollback callbacks, cache purge callbacks, or custody/write/delete/reindex behavior.

## Acceptance checklist

This contract is acceptable only if tests prove that it:

1. is discoverable in the docs index and contract-test inventory;
2. records `RECEIPT_CONTRACT_ONLY_NO_APPROVAL_NO_EXECUTION` and `NO_APPROVAL_PRESENT`;
3. permits only safe metadata fields, booleans, zero counters, one-operation binding, stop-condition status, and report-safe descriptor/source-card refs;
4. rejects raw private source text, private paths, source URIs, platform IDs, prompts/queries, payloads, backend responses, private correlation refs, credential/auth material, raw approval text, and unsafe echo;
5. keeps all fixtures no-live/no-callback/no-production/no-persistence/no-activation/no-mutation/no-`allowed=true`.
