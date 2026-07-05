# L6AN.03 service-owner handoff receipt and retry gate

Status: `SERVICE_OWNER_HANDOFF_READY_RETRY_GATE_HELD`

Rail issue: #372  
Parent issue: #6

## Purpose

L6AN.03 turns the L6AN.01 packet plus L6AN.02 pure validator into a service-owner handoff receipt and retry-gate decision only. The packet names the exact non-secret service/operator binding proof needed for a future L6AO-style retry, while preserving the current hold.

This handoff does not execute another read, does not activate services/providers/callbacks, does not consume Runtime Registry, does not inspect credentials or auth configuration, and does not broaden into usefulness, fresh-agent, Gate, provider, prod, canary, write, or source-discovery surfaces.

## Retry-gate decision

Current gate: `RETRY_HELD_PENDING_FRESH_EXACT_BINDING_AND_NEW_MAX_ONE_RETRY_ISSUE`.

A candidate binding reference can be validated as report-safe metadata, but that ready/held/denied validator result is not execution authority. The actual retry remains held unless a fresh exact binding approval also explicitly authorizes a new max-one retry issue. This rail does not create that issue and does not infer approval from prior parent receipts, preauth comments, PR merge events, issue closure, stale/copied comments, or broad keep-going language.

## Required future evidence

The service owner/operator handoff asks for these exact report-safe fields only:

- fresh issue comment or service-owner reference
- `operator_service_binding_ref`
- identity subject bound to the supervised service caller for `sax`
- `route_audience=memory-seam:read:recall`
- `acting_for=sax`
- `agent=sax`
- `scope=wiki`
- `query_label=supervised_metadata_readiness`
- `evidence_class=SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`
- `max_operation_count=1`
- `report_safe_metadata_only=true`
- `denial_before_read_required=true`
- expiry or one-run custody
- explicit new max-one retry issue authorization

## Exact non-secret match target

| Field | Required value |
| --- | --- |
| endpoint | `memory_seam_recall` |
| route_audience | `memory-seam:read:recall` |
| acting_for | `sax` |
| agent | `sax` |
| scope | `wiki` |
| n | `3` |
| query_label | `supervised_metadata_readiness` |
| query_text | `Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read` |
| evidence_class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| max_operation_count | `1` |
| report_safe_metadata_only | `true` |
| denial_before_read_required | `true` |

## Boundaries preserved

No live retry, raw/private/source/auth/provider/callback output, secret/env/keychain/credential read, Runtime Registry consumption, provider callback, service activation, source discovery, broad recall, persistence/mutation/write, provider/prod/canary/Gate movement, or broad `allowed=true` behavior occurred.

## Verification commands

```bash
python -m pytest -q tests/test_l6an03_service_owner_handoff.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
