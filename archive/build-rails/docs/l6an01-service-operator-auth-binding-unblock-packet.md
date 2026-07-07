# L6AN.01 service/operator auth-binding unblock packet

Status: `PASS_SERVICE_OPERATOR_AUTH_BINDING_UNBLOCK_PACKET_READY_RETRY_HELD`

Rail issue: #370  
Parent issue: #6  
Rail starting source floor: `c7574563ac1be1bf4c9c135586338ab760c0eb28`

## Why this packet exists

L6AM safe denial: `auth_status_code=403`, `wrong_route_audience`, `items=0`, safe item labels `[]`.

That denial is enough to name the next unblock precisely, but not enough to run another retry. L6AN.01 asks the operator/service owner for an exact, non-secret service/operator binding proof for the `memory_seam_recall` route. The retry remains `HELD_MISSING_FRESH_OPERATOR_SERVICE_BINDING` until that proof exists and a later authorized slice explicitly permits execution.

## Exact retry binding to prove

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

## Required operator/service proof shape

Before any future retry runs, an operator/service owner must supply a fresh issue-bound, report-safe reference with:

- operator/service binding reference with expiry or one-run custody
- binding owner / service owner identity label
- identity_subject bound to the supervised service caller for `sax`
- exact route audience, acting-for, agent, scope, query label, evidence class, max-operation-count, report-safe metadata-only, and denial-before-read labels from the table above
- explicit statement that the proof contains no secret material and no raw auth payload

This packet does not authorize, perform, or schedule a retry. Approval is not inferred from parent successor receipt #6 comment `4656321058`, issue-bound preauth comment #370 `4656320851`, packet merge, PR merge, issue closure, stale/copied comments, or broad keep-going language.

## Held retry decision

Current retry state: `HELD_MISSING_FRESH_OPERATOR_SERVICE_BINDING`.

If a fresh exact operator/service binding approval appears in issue comments, record it as report-safe metadata only. Keep actual retry held unless the approval explicitly authorizes a new max-one retry issue.

## Boundaries preserved

No live/private retry, raw/private/source/auth/provider/callback output, secret/env/keychain/OAuth/auth-file/credential read, Runtime Registry consumption, service activation, source discovery, broad recall, persistence/mutation/write, provider/prod/canary/Gate movement, or broad `allowed=true` behavior occurred.

## Verification commands

```bash
python -m pytest -q tests/test_l6an01_service_operator_auth_binding_packet.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
