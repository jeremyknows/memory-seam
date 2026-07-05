# L6AO.03 max-one metadata retry execution packet scaffold

Status coverage: `MAX_ONE_METADATA_RETRY_EXECUTION_PACKET_READY_RETRY_HELD`, `MAX_ONE_METADATA_RETRY_EXECUTION_REFUSED_BEFORE_READ`

Rail issue: #382  
Parent issue: #6  
Source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`  
Preauth comment: `4656625593`

## Purpose

This packet creates the future handoff scaffold for exactly one supervised metadata retry. It is not execution approval and does not run the retry. A future issue can consume it only after fresh exact non-secret binding approval and explicit retry issue authorization both exist.

The target remains `memory_seam_recall` with agent=`sax`, scope=`wiki`, n=`3`, query_label=`supervised_metadata_readiness`, evidence_class=`SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`, max_operation_count=`1`, and report_safe_metadata_only=`true`.

## Execution packet fields

The scaffold names these receipt-safe target and output fields only:

- endpoint, route audience, agent, scope, n, query label, and evidence class;
- max-one operation count and denial-before-read requirement;
- report-safe output fields: status, endpoint, route audience, agent, scope, n, query label, evidence class, items_count, safe_item_labels, denial_reason, guarded_counters.

The packet records `retry_authorized=false` and `retry_executed=false`. Guarded counters remain zero.

## Hard refusal before read

`MAX_ONE_METADATA_RETRY_EXECUTION_REFUSED_BEFORE_READ` is returned when any of these conditions appear:

- `missing_fresh_exact_non_secret_binding_approval`
- `missing_explicit_retry_issue_authorization`
- `stale_or_mismatched_binding_approval`
- `max_operation_count_not_one`
- `report_safe_metadata_only_not_true`
- `denial_before_read_not_required`
- `raw_private_source_or_auth_content_requested`
- `secret_env_keychain_oauth_auth_file_or_credential_read_requested`
- `runtime_registry_provider_callback_or_service_activation_requested`
- `source_discovery_broad_recall_or_broad_allowed_true_requested`
- `provider_prod_canary_gate_atlas_gate_write_or_mutation_requested`

Preauth comments, the parent rail-created receipt, binding-intake readiness, PR merge, issue closure, stale copied approval text, and broad `allowed=true` wording do not authorize execution.

## Rollback and stop conditions

If a future runner sees any missing, stale, mismatched, broadened, raw-output, secret-read, Registry, callback, activation, write, Gate, or multi-operation shape, it must stop before read, emit a receipt-only refusal, keep guarded counters zero, and avoid persistence or external mutation.

## Boundaries preserved

No live retry; no raw/private/source content; no secrets, environment, keychain, OAuth, auth-file, or credential reads; no source discovery or broad recall; no Runtime Registry/provider callback/service activation; no writes or mutations outside docs/tests/helpers; no provider/prod/canary/Gate or Atlas Gate movement; no broad `allowed=true` behavior.

## Verification commands

```bash
python -m pytest -q tests/test_l6ao03_max_one_metadata_retry_execution_packet.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
