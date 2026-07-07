# L6AR.02 report-safe usefulness query/source-card candidate packet

Status: `REPORT_SAFE_USEFULNESS_QUERY_SOURCE_CARD_CANDIDATE_PACKET_READY`

Rail issue: #411  
Parent issue: #6  
Rail starting source floor: `67b5bcc1019899ed3075c8bc44dcfdb9221d9c33`  
Reference adapter repair floor: `a709b14a33b7d22ec980dba97ce20bf56a6c2d86`
Parent #6 creation receipt: `4663160613`

## Purpose

This packet repairs the second L6AR continuity slice by defining the report-safe usefulness query/source-card candidate that #412 may use for exactly one fresh-process metadata usefulness attempt after #410 and #411 are merged.

No live/private read, recall attempt, source discovery, or source-card read is executed for #411.

## Candidate query metadata

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
| usefulness goal label | `post_auth_metadata_usefulness_signal` |
| output | report-safe metadata only |
| max operation count | `1`, owned by #412 only |
| process boundary | fresh reference-agent adapter process |

## Candidate source-card metadata

| Field | Value |
| --- | --- |
| descriptor candidate label | `report_safe_metadata_descriptor_candidate` |
| source-card candidate label | `report_safe_metadata_usefulness_candidate` |
| expected evidence label | `endpoint_route_audience_alignment` |
| expected evidence label | `auth_status_label` |
| expected evidence label | `item_count_scalar` |
| expected evidence label | `safe_item_label_set` |
| expected evidence label | `degraded_flag_set` |
| raw content required | `false` |
| source path or URI required | `false` |
| private identifier required | `false` |

These labels are candidate labels only. They do not identify, disclose, or discover a private source item. They only constrain the future #412 receipt to scalar/label metadata if the fresh-process attempt returns a report-safe result.

#412 owns at most one fresh-process report-safe metadata usefulness attempt after #410 and #411 pass.

## #412 stop conditions carried forward

#412 must stop immediately after one attempt if the fresh adapter boundary returns denial or zero items. A denied/empty result may persist only approved scalar/label metadata: endpoint, route audience, agent/acting_for, scope, n, query label, evidence class, auth status, degraded flags, item count, safe labels, attempt count, and guarded counters.

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

- `python -m pytest -q tests/test_l6ar02_usefulness_candidate_packet.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`
