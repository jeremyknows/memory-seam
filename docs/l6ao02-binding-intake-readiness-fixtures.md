# L6AO.02 binding-intake readiness fixtures

Status coverage: `BINDING_INTAKE_READY_RETRY_HELD`, `BINDING_INTAKE_HELD_BEFORE_READ`, `BINDING_INTAKE_DENIED_BEFORE_READ`

Rail issue: #381  
Parent issue: #6  
Source floor: `57e8bd4612824ada20718e41b1eea33210fe2974`  
Preauth comment: `4656625391`

## Purpose

This packet adds pure, report-safe binding-intake fixture coverage for the L6AO max-one metadata retry rail. It does not inspect runtime configuration, credentials, auth files, environment variables, keychain material, OAuth material, Runtime Registry state, providers, callbacks, or services.

The exact held target remains `memory_seam_recall` with agent=`sax`, scope=`wiki`, n=`3`, max_operation_count=`1`, and report_safe_metadata_only=`true`.

## Fixture states

| State | Receipt status | Covered reasons | Retry and counters |
| --- | --- | --- | --- |
| Ready intake fixture | `BINDING_INTAKE_READY_RETRY_HELD` | `exact_default_off_binding_intake_ready_retry_still_held` | `retry_executed=false`; guarded counters remain zero |
| Missing or stale intake | `BINDING_INTAKE_HELD_BEFORE_READ` | `missing_binding_intake_reference`, `stale_binding_intake_reference` | `retry_executed=false`; guarded counters remain zero |
| Wrong target fields | `BINDING_INTAKE_DENIED_BEFORE_READ` | `wrong_route_audience`, `wrong_agent`, `wrong_scope`, `wrong_query`, `wrong_query_label`, `wrong_query_text`, `wrong_evidence_class`, `wrong_max_operation_count`, `wrong_n`, `wrong_report_safe_metadata_only` | `retry_executed=false`; guarded counters remain zero |
| Unsafe output or broad allow | `BINDING_INTAKE_DENIED_BEFORE_READ` | `raw_output_requested`, `broad_allowed_true` | `retry_executed=false`; guarded counters remain zero |

## Denial-before-read rule

Every non-ready case denies or holds before read. The helper accepts only committed report-safe metadata and returns a receipt with safe target labels and zero guarded counters. It does not authorize a retry, does not call a provider, does not read sources, and does not activate any service.

## Boundaries preserved

No live retry; no raw/private/source content; no secrets, environment, keychain, OAuth, auth-file, or credential reads; no source discovery or broad recall; no Runtime Registry/provider callback/service activation; no writes or mutations outside docs/tests/helpers; no provider/prod/canary/Gate or Atlas Gate movement; no broad `allowed=true` behavior.

## Verification commands

```bash
python -m pytest -q tests/test_l6ao02_binding_intake_readiness.py
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```
