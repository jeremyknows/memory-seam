# L6AK.03 non-secret auth contract shim for supervised read retry

Status: `PASS_NON_SECRET_AUTH_CONTRACT_SHIM_READY_RETRY_STILL_HELD`

Rail issue: #343
Parent issue: #6
Depends on: #341-#342 closed/PASS
Roadmap step: 3 supervised real read with denial-before-read, auth blocker points toward step 5 service/provider auth
Rail starting source floor: `95e7a7979ae092703da8f77c4d897f703348a308`
Source floor entering slice: `5346907`
Prior receipt/design: #341 / PR #345 and #342 / PR #346
Operation class: `L6AK_NON_SECRET_ROUTE_AUDIENCE_AUTH_CONTRACT_SHIM`
Evidence class: `SUPERVISED_METADATA_READ_AUTH_CONTRACT_TYPED_RECEIPT`

## Verdict

Verdict vocabulary: `PASS_NON_SECRET_AUTH_CONTRACT_SHIM_READY_RETRY_STILL_HELD`, `FIX_AUTH_CONTRACT_BEFORE_RETRY`, `DENY_BEFORE_READ_AUTH_BINDING_MISMATCH`.
Verdict: `PASS_NON_SECRET_AUTH_CONTRACT_SHIM_READY_RETRY_STILL_HELD`
Next-frontier classification: `SOURCE_FLOOR_PARENT_TRACKER_RECONCILIATION_FOR_AUTH_BLOCKER`

The implementation adds `src/memory_seam/l6ak_route_audience_auth_contract.py`, a pure data-only non-secret contract shim. It validates `identity_subject`, `acting_for`, agent, audience, recall scope, context include, output mode, approval freshness, max operation count, metadata/report-safe posture, and held-surface request flags. It returns typed metadata-only receipts for exact readiness or denial-before-read.

## Exact contract fixture

The exact readiness fixture requires:

- `identity_subject`: `atlas-query-supervised-metadata-reader`
- `acting_for`: `sax`
- `agent`: `sax`
- `audience`: `memory-seam:supervised-metadata-read:atlas-query-mcp`
- `scope`: `wiki`
- `context_include`: `health`
- `output_mode`: `metadata_only_report_safe`
- `approval_freshness`: `fresh_issue_bound_l6ak`
- `max_operation_count`: `1`
- `metadata_only`: `true`
- `report_safe`: `true`

When all bindings match, the shim returns `ready_for_exact_retry=true` only as non-secret readiness metadata. It still returns `read_authorized=false`, `retry_executed=false`, `source_access_attempted=false`, and all guarded counters at zero. It does not execute the retry.

## Denial behavior

The shim denies before read for:

- `wrong_route_audience`
- `unauthorized_narrowing`
- `stale_approval`
- `mismatched_agent`
- `broadened_scope`
- `raw_output_requested`
- `missing_identity_subject`
- `mismatched_identity_subject`
- `broad_allowed_true_requested`
- held-surface requests for activation, provider routes, Runtime Registry, persistence/mutation, publication, or Gate movement

All denial receipts keep `ready_for_exact_retry=false`, `read_authorized=false`, `retry_executed=false`, `source_access_attempted=false`, `source_discovery_attempted=false`, `runtime_registry_consumed=false`, `provider_route_invoked=false`, `callback_invoked=false`, `persistence_or_mutation_attempted=false`, `activation_attempted=false`, `publication_or_gate_movement_attempted=false`, `broad_allowed_attempted=false`, and zero guarded counters.

## Boundary

This shim does not load secrets. It does not read environment values, keychain entries, OAuth material, auth files, credentials, Runtime Registry data, callback payloads, provider payloads, source cards, source URIs, platform raw IDs, raw private content, or raw source text. It does not discover sources, run broader recall, run index queries, activate services, change cron, persist, mutate, write, delete, reindex, cache purge, execute rollback, publish, change visibility, move provider/prod/canary/Gate state, move Atlas Gate, retry a real read, and does not create broad `allowed=true` behavior.

## Handoff to #344

#344 should reconcile the source floor, parent #6, and the Atlas tracker with this auth-blocker outcome. The next frontier is exact supervised metadata read retry only if this non-secret binding is accepted as ready and a separate exact issue-bound retry remains inside the authorized scope; otherwise Step 3 execution stays held and Step 5 service/provider auth work remains the active frontier.

## Verification gate

Required verification for the #343 PR:

- `python -m pytest -q tests/test_l6ak03_route_audience_auth_contract.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`
