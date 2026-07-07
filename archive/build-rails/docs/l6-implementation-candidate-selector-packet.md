# L6I.12 implementation-candidate selector packet

Status: docs/tests-only implementation-candidate selector packet. This packet is preparatory, non-approval, non-executable, and does not implement runtime behavior. It does not add any code path returning `allowed=true`, does not approve positive authorization acceptance, and does not unhold mutation, custody persistence, callbacks, source reads, activation, publication, provider/prod/canary authority, repository visibility change, or Atlas Gate movement.

Source floor: `7980a5b` or later `origin/main`.
Dependency: L6I.11 closed/PASS via issue `#153` and PR `#160`.
Frontier basis: `docs/l6-next-implementation-slice-frontier-packet.md` recommends `SPLIT_AGAIN_DOCS_TESTS_ONLY` before any additional implementation slice.

## Purpose

L6I.12 compares candidate future implementation slices and selects exactly one recommended future slice for a later HITL decision packet. It does not approve that slice and does not provide approval language. The selected slice still requires a fresh human approval packet, exact approval phrase fields, local verification, public hygiene review, and stop-condition proof before any implementation branch can begin.

The selector intentionally keeps the next possible slice smaller than custody persistence or write execution. The safest next request is a receipt-only positive-authorization skeleton that can recognize an exact future approval, emit a non-persistent report-safe receipt, keep mutation unsupported, and deny/stop before every provider, backend, source, write, custody, delete, reindex, rollback, cache-purge, storage, Runtime Registry, activation, publication, provider/prod/canary, visibility, and Atlas Gate surface.

## Candidate set

| Candidate | Selection | Safety value | Implementation size | Residual risk | Required approval phrase fields | Rollback/audit obligations |
| --- | --- | --- | --- | --- | --- | --- |
| `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON` | **SELECTED_FUTURE_CANDIDATE** | Highest near-term safety value: proves exact positive-authorization recognition can remain receipt-only, mutation-held, synthetic/no-production, and non-persistent while preserving all guarded counters at `0`. | Smallest: approval-field validation boundary plus report-safe non-persistent receipt shape only; no mutation executor, no custody transfer, no persistence adapter, no provider/backend/source callback. | Risk is constrained to approval-recognition confusion, stale/variant approval reuse, actor/owner mismatch, expiry, max-operation overflow, unsafe payload metadata, or accidental implication that receipt recognition means mutation support. | Future HITL packet must bind issue, exact phrase reference, actor binding, expiry, max operation count of one, operation class, custody owner role, report-safe approval reference, rollback/audit reference, synthetic/no-production target, and non-persistence statement. | Emit pre-mutation receipt only; `mutation_attempted=false`; `mutation_supported=false`; all guarded counters stay zero; rollback is no-op/posture-only; audit is report-safe and non-persistent unless separately approved. |
| `L6_APPROVAL_RECOGNIZED_MUTATION_HELD_SKELETON` | NOT_SELECTED_THIS_SLICE | Useful semantics, but it is broader because it centers the approval-recognized runtime state rather than the receipt contract boundary. | Medium: would need more runtime result-state wiring and stronger denied-vs-recognized semantics before a receipt-only proof is isolated. | Higher risk of readers inferring an `allowed=true` runtime path or future mutation capability from the approval-recognized state name. | Same fields as the selected candidate, plus stricter wording that recognized approval is not allowed execution. | Same no-op rollback posture, but with larger audit explanation burden because runtime state semantics are broader. |
| `L6_CUSTODY_RECEIPT_NONPERSISTENT_SKELETON` | NOT_SELECTED_THIS_SLICE | Potentially useful later for custody planning, but custody language is too close to persistence/ownership transfer for the next narrow step. | Larger: custody receipt terminology requires custody-owner semantics, storage non-goals, and transfer-denial proof before it can be safely requested. | Higher risk of implying custody transfer, durable audit, issue/PR-comment custody persistence, or storage authority. | Would require all selected-candidate fields plus custody-transfer denial language, storage-class exclusions, retention/cleanup plan, and ownership non-transfer proof. | Rollback remains no-op and audit non-persistent, but custody-specific obligations make this larger than receipt-only positive authorization. |

## Selected future slice

Selected future candidate: `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON`.

Selection reason: it is the smallest implementation-facing step that can add useful evidence without crossing the held surfaces. A later decision packet may ask whether to implement a synthetic/no-production receipt skeleton that recognizes only a fresh exact approval and emits a report-safe non-persistent receipt with status `positive_authorization_recognized_mutation_held`; it must keep mutation unsupported and stop before all guarded callback, storage, source, activation, publication, provider/prod/canary, visibility, and Atlas Gate surfaces.

This selector is not approval. It does not authorize `allowed=true`, mutation, write execution, custody transfer, custody persistence, delete execution, reindex execution, rollback execution, cache-purge execution, provider callbacks, backend callbacks, source-stat callbacks, source-read callbacks, persistence, live/private reads, source discovery, credential/auth/env/keychain/OAuth/auth-file reads, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, service/listener/startup/cron activation, recurring runner activation, provider/prod/canary authority, repository visibility change, package publication, Atlas Gate movement, or production-authoritative claims.

## Required prerequisites before any future implementation approval

A later HITL packet must carry these prerequisites forward before implementation can be considered:

1. a fresh issue-scoped approval request for exactly one implementation slice;
2. exact phrase reference and report-safe approval reference;
3. actor binding, custody owner role, subject/owner checks, expiry, and max operation count of one;
4. operation class fixed to the selected receipt skeleton;
5. synthetic/no-production target only;
6. report-safe payload constraints excluding raw private source text, credentials, auth/env/keychain material, OAuth/auth-file material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, private correlation refs, and raw approval text;
7. pre-callback stop conditions for stale approval, variant approval, implied approval, actor mismatch, subject mismatch, owner mismatch, expiry, max-operation-count overflow, unsafe payload, callback attempt, storage attempt, source-read attempt, source-discovery attempt, Runtime Registry attempt, activation attempt, publication attempt, provider/prod/canary claim, visibility-change attempt, private-data inclusion, and Atlas Gate movement;
8. receipt-only output with `mutation_attempted=false`, `mutation_supported=false`, `fixture_is_persistent=false`, `persistent_receipt_count=0`, `durable_write_record_count=0`, `audit_persistence_count=0`, and `cache_mutation_count=0`;
9. all guarded callback counters fixed at zero: `allowed_result_count=0`, `provider_callback_count=0`, `backend_callback_count=0`, `source_stat_callback_count=0`, `source_read_callback_count=0`, `write_callback_count=0`, `custody_callback_count=0`, `delete_callback_count=0`, `reindex_callback_count=0`, `rollback_callback_count=0`, and `cache_purge_callback_count=0`;
10. rollback/audit plan stating rollback is no-op/posture-only and audit remains report-safe/non-persistent unless separately approved.

## Stop conditions for the future slice

The selected candidate must stop as denied/unsupported before receipt recognition, mutation, callbacks, storage, source access, or activation if any approval is stale, variant, implied by issue closure, implied by PR merge, copied from issue `#137`, actor-mismatched, subject-mismatched, owner-mismatched, expired, over max operation count, missing operation class, requesting custody persistence, requesting write/delete/reindex/rollback/cache-purge execution, requesting provider/backend/source-stat/source-read callbacks, requesting live/private reads or source discovery, requesting credentials/auth/env/keychain/OAuth/auth-file access, requesting Runtime Registry consumption, requesting global configuration mutation, requesting service/listener/startup/cron activation, requesting publication, requesting repository visibility change, claiming provider/prod/canary authority, or moving Atlas Gate.

## L6I.12 recommendation

Proceed to L6I.13 as a docs/tests-only HITL decision packet for `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON`. The L6I.13 packet may draft future-only exact approval language and acceptance gates, but it must clearly state that the packet itself is not approval and cannot authorize implementation, `allowed=true`, mutation, persistence, callbacks, source reads, activation, publication, visibility changes, provider/prod/canary authority, or Atlas Gate movement.
