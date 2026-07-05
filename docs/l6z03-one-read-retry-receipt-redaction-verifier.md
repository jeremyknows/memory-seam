# L6Z.03 one-read retry receipt and redaction verifier

Status: `RECEIPT_REDACTION_VERIFIER_NO_ADDITIONAL_READS`
Rail issue: #233
Verified receipt issue: #232
Prerequisite packet issue: #231
Parent issue: #6
Depends on: L6Z.02 HOLD receipt artifact `docs/l6z02-exact-target-ref-one-read-denial-hold.md`
Source floor verified before work: `a71f9f78afd5e0d254719acaf70cad8219ad23e6` (>= `c7e335bf6b68e084088c6deaa4b28dd84f9ed9f6`)
Preauthorization proof anchors: #6 comment `4649391691`; #215 comment `4649391836`; Jeremy voice-message anchor recorded for the bounded L6Z rail.
Parent L6Z rail receipt: `issuecomment-4650001541`

This verifier is docs/tests/fixture-only over the already-produced #232 receipt. It performs no live/private read and does not call provider, backend, source-stat, source-read, credential/auth/env/keychain/OAuth/auth-file, Runtime Registry, discovery, workspace/family scan, broad recall, index, persistence, mutation, write, delete, reindex, rollback, cache-purge, service/listener/startup, cron, publication, repository-visibility, provider/prod/canary, or Atlas Gate surfaces.

## Accepted #232 receipt shape

The accepted fixture is `build_l6z02_target_ref_mismatch_hold_receipt()` from `memory_seam.l6z_one_read_receipt`. It represents the #232 outcome:

| field | accepted value |
| --- | --- |
| `schema_version` | `l6z-one-read-receipt-v1` |
| `receipt_status` | `HOLD_DENIED_BEFORE_READ_APPROVAL_TARGET_REF_MISMATCH_NO_LIVE` |
| `approval_result` | `DENY_BEFORE_READ` |
| `stop_condition` | `DENIED_BEFORE_CALLBACK` |
| `operation_class` | `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` |
| `packet_issue_id` | `#231` |
| `read_issue_id` | `#232` |
| `parent_issue_id` | `#6` |
| `descriptor_ref_expected` | `descriptor:l6z/report-safe-operator-preference-card` |
| `source_card_ref_expected` | `source-card:l6z/report-safe-operator-preference-card` |
| `descriptor_ref_presented` | `descriptor:l6z/operator-proof` |
| `source_card_ref_presented` | `source-card:l6z/operator-proof` |
| `mismatch_reason` | `EXECUTABLE_TARGET_REFS_DO_NOT_MATCH_L6Z01_PACKET` |
| `live_read_invoked` | `false` |
| `allowed` | `false` |
| `allowed_result_count` | `0` |
| `operation_count_attempted` | `0` |
| `read_usefulness_label` | `NOT_APPLICABLE_NO_READ_EXECUTED` |
| `redaction_status` | `REPORT_SAFE_METADATA_ONLY_RAW_APPROVAL_TEXT_OMITTED` |
| `rollback_status` | `NO_SIDE_EFFECT_ROLLBACK_NOT_REQUIRED` |

The only nonzero guarded counter accepted is `approval_comments_examined: 1`, because #232 examined one owner comment metadata record before denying. These guarded counters must remain zero: valid owner approval comments, live read invocations, attempted operations, allowed result count, provider/backend/source callbacks, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry reads, discovery/workspace/family/broad recall/index queries, persistence/mutation/rollback/cache-purge callbacks, service/listener/startup activations, publication/visibility changes, and provider/prod/canary/Gate moves.

## Redaction and rejection guarantees

`validate_l6z_one_read_receipt()` accepts only the exact report-safe metadata fields listed above plus owner/comment metadata required to explain the denial: comment id, comment author, owner association, comment creation timestamp, evaluation timestamp, and freshness result. It rejects:

- raw private source text or raw payload content
- private absolute paths, source URIs, private correlation refs, or platform IDs
- prompt/query payloads or backend responses
- credential values, token-shaped values, auth/env/keychain/OAuth/auth-file material
- raw approval text or copied approval-body echoes
- unknown unsafe fields or unsafe guarded-counter names
- any nonzero guarded counter outside the #232 deny-before-read shape
- any `allowed=true`, broad allow route, operation attempt, or live-read invocation

## Verification boundary for #234

#234 may review usefulness/trust-boundary implications of this verifier and the #232 HOLD receipt. This verifier does not authorize another read, callback, discovery query, Runtime Registry read, credential/auth read, persistence/mutation/write/delete/reindex/cache-purge/rollback execution, activation, publication/visibility change, provider/prod/canary/Gate movement, or broad `allowed=true` route.
