# L6AO.01 auth-held blocker receipt and default-off binding intake

Status: `AUTH_HELD_BLOCKER_RECEIPT_DEFAULT_OFF_BINDING_INTAKE_READY`

Rail issue: #380  
Parent issue: #6  
Rail starting source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`  
Preauth comment: `4656625129`  
Parent rail-created receipt: `4656626203`

## Why this packet exists

L6AO starts from the L6AN-auth-held floor: the service/operator binding request is ready, but the exact metadata retry remains held. The blocker receipt is report-safe only:

- blocker: `auth_held_missing_fresh_operator_service_binding`
- prior denial summary: `auth_status_code=403`, `wrong_route_audience`, `items=0`
- prior request class: `memory_seam_recall_report_safe_metadata_only_max_one`
- default decision: deny before read and hold retry

No raw/private/source content, credential material, auth-file material, source URI, provider payload, or Runtime Registry output is included.

## Default-off retry state

Current retry state: `HELD_NO_LIVE_RETRY_DEFAULT_OFF_UNTIL_EXACT_FRESH_BINDING_AND_MAX_ONE_EXECUTION_PACKET`.

Current intake state: `DEFAULT_OFF_REPORT_SAFE_NON_SECRET_BINDING_INTAKE_ONLY`.

All execution surfaces are off by default: retry authorization, retry execution, live retry enablement, Runtime Registry use, provider callbacks, service activation, source discovery, external writes, provider/prod/canary/Gate movement, and broad `allowed=true` behavior.

## Non-secret binding intake packet

The intake packet may receive only report-safe metadata. It does not authorize, perform, schedule, or enable a live retry.

| Field | Required value or constraint |
| --- | --- |
| operator_service_binding_ref | non-secret issue-bound reference |
| binding_owner | report-safe owner/service-owner label |
| identity_subject | supervised service caller bound to `sax` |
| route_audience | `memory-seam:read:recall` |
| acting_for | `sax` |
| agent | `sax` |
| scope | `wiki` |
| query_label | `supervised_metadata_readiness` |
| evidence_class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| max_operation_count | `1` |
| report_safe_metadata_only | `true` |
| denial_before_read_required | `true` |
| expires_at_or_one_run_custody | required, report-safe only |
| issue_bound_authorization_ref | required, report-safe only |

The packet may not contain secret material, raw private/source content, auth payloads, provider payloads, source paths, source URIs, environment labels, keychain labels, bearer strings, credential literals, or callback/activation handles.

## Approval boundaries

Approval is not inferred from parent issue #6 rail-created receipt comment `4656626203`, issue-bound preauth comment #380 `4656625129`, L6AN completion packet merge, PR merge, issue closure, stale copied approval text, broadened language, or any broad `allowed=true` wording.

A later issue must separately define any max-one execution packet and hard stops before a retry can be considered.

## Boundaries preserved

No live retry, no raw/private/source content, no secrets/env/keychain/OAuth/auth-file/credential reads, no source discovery or broad recall, no Runtime Registry/provider callback/service activation, no writes or mutations outside docs/tests/helpers, no provider/prod/canary/Gate or Atlas Gate movement, and no broad `allowed=true` behavior occurred.

## Verification commands

```bash
python -m pytest -q tests/test_l6ao01_auth_held_default_off_intake.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
