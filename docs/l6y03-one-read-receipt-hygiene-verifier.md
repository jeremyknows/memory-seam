# L6Y.03 report-safe one-read receipt hygiene verifier

Status: `RECEIPT_HYGIENE_VERIFIER_NO_ADDITIONAL_READS`
Rail issue: #223
Parent issue: #6
Depends on: L6Y.02 HOLD receipt artifact `docs/l6y02-supervised-one-read-deny-before-read-hold.md`
Source floor verified before work: `f86eab3e16147b2aa2a2b77a7bf75608b6ddffde` (>= `e0d5b4158049870b50aa5f553f828f891716be92`)

## Purpose

L6Y.03 adds a verifier for the L6Y.02 report-safe one-read receipt. The verifier accepts the already supplied #222 HOLD receipt shape only when it remains metadata-only, denies broadening, and keeps every guarded source/callback/mutation/runtime/credential counter at the preserved hold value.

This verifier does not perform source discovery, workspace scans, family scans, broad recall, index queries, live/private reads, provider callbacks, backend callbacks, source-stat callbacks, source-read callbacks, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, persistence, mutation, write, delete, reindex, cache-purge, rollback execution, audit/custody writes, service/listener/startup/cron activation, global runtime config mutation, publication, repository visibility changes, provider/prod/canary movement, Atlas Gate movement, or broad `allowed=true` routing.

## Accepted bounded receipt shape

The accepted fixture is `build_l6y02_approval_mismatch_hold_receipt()` from `memory_seam.l6y_one_read_receipt`. It represents the #222 outcome:

| Field | Required report-safe value |
| --- | --- |
| `schema_version` | `l6y-one-read-receipt-v1` |
| `receipt_status` | `HOLD_DENIED_BEFORE_READ_APPROVAL_MISMATCH_NO_LIVE` |
| `approval_result` | `DENIED_BEFORE_CALLBACK` |
| `live_read_invoked` | `false` |
| `allowed` | `false` |
| `allowed_result_count` | `0` |
| `operation_class` | `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` |
| `operation_count_attempted` | `0` |
| `descriptor_ref` | `MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ` |
| `source_card_ref` | `MISSING_EXECUTABLE_REF_DENIED_BEFORE_READ` |
| `read_usefulness_label` | `NOT_EVALUATED_NO_READ` |
| `redaction_status` | `REPORT_SAFE_METADATA_ONLY` |
| `rollback_status` | `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED` |
| `report_safe` | `true` |
| `metadata_only` | `true` |
| `unsafe_raw_fields_rejected_before_report` | `true` |

## Guarded counter requirements

| Counter | Required value |
| --- | --- |
| `approval_comments_examined` | `1` |
| `valid_owner_approval_comments` | `0` |
| `provider_callbacks` | `0` |
| `backend_callbacks` | `0` |
| `source_stat_callbacks` | `0` |
| `source_read_callbacks` | `0` |
| `credential_reads` | `0` |
| `runtime_registry_reads` | `0` |
| `persistence_writes` | `0` |
| `mutation_callbacks` | `0` |
| `rollback_callbacks` | `0` |
| `cache_purge_callbacks` | `0` |

`approval_comments_examined=1` is report-safe verifier evidence from the public issue metadata check. Every live/source/callback/credential/runtime/persistence/mutation/rollback/cache-purge counter must remain zero because #222 denied before read.

## Rejection matrix

The verifier rejects the following classes before treating a receipt as report-safe:

- unknown fields, including unknown unsafe fields;
- unsafe key names that imply raw private content, private paths/source URIs, raw platform IDs, prompt/query payloads, raw backend responses, credentials/auth material, OAuth/keychain/env/auth-file material, private correlation refs, source text, or raw approval text;
- unsafe echo markers in any accepted field value;
- raw private content, private absolute paths, source URIs, platform IDs, prompt/query payloads, raw payload content, backend responses, credentials/auth material, OAuth material, keychain material, auth-file material, private correlation refs, or raw approval text;
- nonzero guarded counters outside the approved #222 shape;
- missing guarded counters or extra guarded counter keys;
- `allowed=true`, nonzero `allowed_result_count`, live-read invocation, or any operation count above zero for the L6Y.02 HOLD path;
- receipt status, approval result, operation class, descriptor ref, source-card ref, usefulness label, redaction status, or rollback status that differs from the exact bounded #222 HOLD receipt.

## Preserved holds

L6Y.03 is verifier-only and creates no new approval. It does not authorize another read, callback, source discovery, Runtime Registry use, credential/auth access, persistence, mutation, rollback/cache-purge execution, service or cron activation, publication, visibility change, provider/prod/canary movement, Atlas Gate movement, or broad `allowed=true` behavior.

#224 may perform the post-read usefulness and redaction review over this verifier evidence without any additional live/private read.
