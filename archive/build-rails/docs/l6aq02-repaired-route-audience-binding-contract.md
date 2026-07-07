# L6AQ.02 repaired route-audience binding contract

Status: `REPAIRED_ROUTE_AUDIENCE_BINDING_CONTRACT_READY_DEFAULT_OFF`

Rail issue: #401  
Parent issue: #6  
Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`

## Contract

This packet defines the minimal report-safe route-audience binding contract required before the later #403 max-one supervised metadata retry can run. It repairs the localized #400 target while remaining default-off: it does not read source, inspect credentials, activate services, or execute recall.

| Field | Value |
| --- | --- |
| repair target | `memory_seam_recall_service_operator_route_audience_binding` |
| endpoint | `memory_seam_recall` |
| route audience | `memory-seam:read:recall` |
| acting_for / agent | `sax` / `sax` |
| scope / n | `wiki` / `3` |
| query label | `supervised_metadata_readiness` |
| evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| operation class | `memory_seam_recall_report_safe_metadata_retry` |
| max operation count | `1` |
| report-safe metadata only | `true` |
| denial before read required | `true` |
| default-off until | `issue_403_preflight_and_max_one_retry_authority_pass` |
| retry_authorized_by_contract | `false` |

The non-secret binding fixture is a report-safe reference shape only. It is not an auth payload, not a provider payload, and not a runtime/service activation request.

## Mismatch and denial coverage

The validator denies or holds before read for wrong route audience, missing binding, stale binding, broadened audience, broad `allowed=true`, raw output, provider/prod/canary/Gate/write movement, Runtime Registry requests, provider callbacks, service activation, source discovery, broad recall, credential reads, and contract attempts to authorize the retry directly.

## Default-off handoff

The contract is ready for later preflight proof, but #401 does not authorize execution. #403 remains the only issue in this rail that may call `memory_seam_recall`, and only after #401/#402 preflight/config proof exists. No live retry was executed for this issue.

## Report-safe boundaries

No raw item text/content, source URI/path, private path, auth material, provider payload, callback payload, Runtime Registry payload, query text, credential material, secret/env/keychain/OAuth/auth-file material, service activation, source discovery, broad recall, write/mutation, provider/prod/canary/Gate movement, or broad `allowed=true` behavior was recorded.

## Verification commands

- `python -m pytest -q tests/test_l6aq02_repaired_route_audience_binding_contract.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`
