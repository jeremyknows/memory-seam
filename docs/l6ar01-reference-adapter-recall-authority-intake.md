# L6AR.01 reference adapter recall-authority intake

Status: `REFERENCE_ADAPTER_RECALL_AUTHORITY_INTAKE_RELOAD_BOUNDARY_ANCHORED`

Rail issue: #410  
Parent issue: #6  
Rail starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`  
Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`  
Parent #6 creation receipt: `4663160613`

## Purpose

This packet repairs the L6AQ/L6AR continuity gap at the first issue slice only. It records the reference adapter recall-authority intake and the reload boundary required before any usefulness attempt can be trusted.

## Reload-boundary anchor

| Boundary | Report-safe state |
| --- | --- |
| fresh adapter process | `AUTH_UNBLOCKED_IN_FRESH_ADAPTER_PROCESS_AFTER_REFERENCE_REPAIR` |
| stale client cache | `STALE_CLIENT_CACHE_NOT_RELIED_ON_FOR_RETRY_AUTHORITY` |
| #410 action | docs/tests intake only |
| #412 handoff | exact max-one fresh-process metadata attempt, only after #410 and #411 pass |

The reference adapter repair floor records that a fresh adapter process no longer has the same route-audience denial posture that was observed by stale client cache state. The stale cache is not authority for another retry. The next live boundary is a newly spawned reference-agent adapter process, and that boundary belongs to #412 only.

No recall/usefulness attempt was executed for #410.

## Exact target metadata carried forward

| Field | Value |
| --- | --- |
| endpoint | `memory_seam_recall` |
| route audience | `memory-seam:read:recall` |
| agent | `reference-agent` |
| acting_for | `reference-operator` |
| scope | `wiki` |
| n | `3` |
| query label | `supervised_metadata_readiness` |
| evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| output | report-safe metadata only |
| max operation count | `1`, owned by #412 only |

#412 owns at most one fresh-process report-safe metadata attempt after #410 and #411 pass.

## Preserved holds

- No raw/private/source item content.
- No source paths or URIs.
- No auth/provider/callback payloads.
- No secrets, environment, keychain, OAuth, auth-file, or credential reads.
- No broad recall or source discovery.
- No provider, production, canary, write, or mutation movement.
- No broad `allowed=true` behavior.
- No #412 usefulness attempt before #410 and #411 are merged.
- No second attempt outside issue #412.
- No successor issues or scheduler mutations.

## Verification commands

- `python -m pytest -q tests/test_l6ar01_recall_authority_intake.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`
