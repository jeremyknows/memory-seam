# L6AM.03 next use-proof auth-unblock decision

Status: `PASS_NEXT_USE_PROOF_DECISION_AUTH_UNBLOCK_PACKET_PREPARED`

Rail issue: #359  
Parent issue: #6  
Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`

## Plain-English progress toward real use

L6AM.02 returned a real, bounded service denial, not another theoretical hold.

The safe retry metadata: `auth_status_code=403`, `wrong_route_audience`, `items=0`, safe item labels `[]`.

That means Memory Seam is no longer blocked on packet shape alone. The next proof is blocked on the actual service/operator auth binding needed for the `recall` route to return report-safe metadata. Because the retry returned denied/empty, the current-session usefulness proof and fresh-agent proof remain held until the exact metadata retry returns safe labels/items.

## Decision

`PREPARE_SERVICE_OPERATOR_AUTH_UNBLOCK_PACKET_BEFORE_USER_VISIBLE_USE_PROOF`

Next frontier:

`SERVICE_OPERATOR_AUTH_BINDING_UNBLOCK_FOR_EXACT_METADATA_RECALL`

User-visible proof state:

`HELD_UNTIL_AUTH_BINDING_RETURNS_METADATA`

## Exact missing binding fields

The unblock packet must bind these fields before another supervised metadata retry or user-visible proof packet can proceed:

- `route_audience=memory-seam:read:recall (recall endpoint)`
- identity_subject bound to the supervised service caller
- `acting_for=sax`
- `agent=sax`
- `scope=wiki`
- `query_label=supervised_metadata_readiness`
- `evidence_class=SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`
- `max_operation_count=1`
- `report_safe_metadata_only=true`
- `denial_before_read_required=true`
- operator/service binding reference with expiry or one-run custody

Approval is not inferred from L6AM.01 packet merge, L6AM.02 safe-denial receipt, issue closure, labels, stale parent comments, or broad keep-going language.

## Stop conditions

Stop before read or proof packaging on:

- `auth_status_code_403`
- `wrong_route_audience`
- `unauthorized_narrowing`
- `missing_identity_subject`
- `missing_acting_for`
- `missing_or_stale_operator_service_binding_ref`
- `empty_items`
- `raw_output_request`
- `source_discovery_or_broad_recall_request`
- `runtime_registry_or_provider_callback_request`
- `service_activation_or_prod_canary_gate_request`
- `write_mutation_or_persistence_request`
- `broad_allowed_true_request`

## Boundaries preserved

No additional live read retry was performed for L6AM.03.

No secret/env/keychain/OAuth/auth-file reads, raw/private/source/auth/provider/callback payloads, provider/prod/canary/Gate/write movement, service activation, Runtime Registry consumption, persistence/mutation, or broad `allowed=true` behavior occurred.

## Verification commands

```bash
python -m pytest -q tests/test_l6am03_next_use_proof_decision.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
