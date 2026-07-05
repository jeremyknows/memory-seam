# L6AQ.01 route-audience auth denial localization

Status: `ROUTE_AUDIENCE_AUTH_DENIAL_LOCALIZED_REPAIR_TARGET_READY`

Rail issue: #400  
Parent issue: #6  
Rail starting source floor: `755ab24e4ac5a283081f134cbc18c95c59d1c60e`

## Scope

This packet localizes the L6AP supervised metadata recall denial using only committed, public/report-safe retry metadata and existing repo route-audience/auth contracts. It does not inspect source content, auth payloads, provider payloads, secrets, environment, keychain, OAuth material, auth files, credentials, source paths, source URIs, Runtime Registry state, provider callbacks, or service activation state.

## Report-safe localization

| field | value |
| --- | --- |
| endpoint | `memory_seam_recall` |
| expected route audience | `memory-seam:read:recall` |
| agent | `sax` |
| scope | `wiki` |
| n | `3` |
| query label | `supervised_metadata_readiness` |
| evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| observed denial | `wrong_route_audience`; `auth_status_code=403` |
| items | `0`; safe item labels `[]` |

Blocker classification: `SERVICE_ROUTE_AUDIENCE_AUTH_BINDING_MISMATCH_LOCALIZED`

Repair target: `memory_seam_recall_service_operator_route_audience_binding`

The prior denial already proved the attempted metadata retry stopped before read. The expected contract still names the narrow recall route audience label, while the observed safe denial names `wrong_route_audience` with zero items. That localizes the next repair to the service/operator route-audience binding for `memory_seam_recall`, not to source content, query text, or provider payloads.

## Repair target requirements

The next issue-scoped repair should:

- bind `memory_seam_recall` to route audience `memory-seam:read:recall` for agent `sax` and scope `wiki`;
- preserve metadata-only output and denial-before-read behavior;
- stay default-off unless the later preflight/config proof and exact max-one retry issue authorization pass;
- refuse broad audience values, broad `allowed=true` behavior, raw output, source discovery, Runtime Registry/provider callback/service activation, and provider/prod/canary/Gate/write/mutation movement.

## Preserved holds

No live retry was executed for this issue.

No raw item text/content, source URI/path, private path, auth material, provider payload, callback payload, Runtime Registry payload, or query text was recorded.

Preserved boundaries:

- no raw/private/source content;
- no source paths or URIs;
- no auth payloads, provider payloads, secrets, env, keychain, OAuth, auth-file, or credential reads;
- no source discovery or broad recall;
- no Runtime Registry, provider callback, or service activation;
- no provider/prod/canary/Gate/write/mutation movement;
- no broad `allowed=true`;
- no second retry.

## Verification

Required verification commands for this issue:

```bash
python -m pytest -q tests/test_l6aq01_route_audience_denial_localization.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
