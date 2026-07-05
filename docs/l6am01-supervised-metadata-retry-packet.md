# L6AM.01 exact supervised metadata retry packet from service-auth floor

Status: `PASS_EXACT_SUPERVISED_METADATA_RETRY_PACKET_READY`

Rail issue: #357
Parent issue: #6
Depends on: L6AL #349-#352 closed/PASS and the operator's bounded L6AM authorization for a max-one report-safe retry rail.
Roadmap step: Step 3 supervised metadata retry / Step 5 service-provider auth bridge
Rail starting source floor: `9ea7cd0ab724292b8a2841c9e2c080f14a524ee2`
Packet class: `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`

## Exact retry packet

L6AM.01 creates the packet for the single L6AM.02 supervised metadata retry. It does not execute the retry.

| Field | Binding |
| --- | --- |
| endpoint | `recall` / `memory_seam_recall` |
| agent | `sax` |
| scope | `wiki` |
| n | `3` |
| query label | `supervised_metadata_readiness` |
| query text | `Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read` |
| evidence class | `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE` |
| max operation count | `1` |
| output mode | metadata-only report-safe envelope |
| denial-before-read case | one out-of-scope mismatch, preferred `wrong_route_audience`; `unauthorized_narrowing` remains an accepted fixture case |

The exact allowed tool call for #358 is:

```text
memory_seam_recall(
  agent="sax",
  scope="wiki",
  n=3,
  query="Memory Seam supervised metadata read retry source-floor readiness held surfaces denial-before-read",
)
```

No other recall, index, source discovery, workspace/family scan, service route, provider callback, Runtime Registry, Gate, canary, prod, write, custody, delete, reindex, persistence, or activation path is part of this packet.

## Service-auth floor consumed

The packet consumes L6AL service/provider auth readiness as non-secret repo-side evidence:

- L6AL.01 #349 / PR #353: capability matrix for Memory Seam `context`, `recall`, and `health` route audiences.
- L6AL.02 #350 / PR #354: provider auth readiness fixture with denied-before-read mismatch coverage.
- L6AL.03 #351 / PR #355: typed service auth contract returning `AUTH_READY_FOR_EXACT_SUPERVISED_METADATA_RETRY` or `AUTH_HELD_SERVICE_PROVIDER_BINDING_INCOMPLETE` without authorizing/executing a read.
- L6AL.04 #352 / PR #356: readiness decision marking repo contract ready while runtime retry auth had remained held before the operator authorized this L6AM exact retry rail.

`src/memory_seam/l6am_supervised_metadata_retry_packet.py` binds the exact recall packet to the L6AL.03 service-auth contract. Its ready receipt keeps `retry_executed=false`, all guarded counters zero, and no source/provider/callback/secret/Runtime-Registry counters.

## Report-safe output envelope for #358

L6AM.02 may record only these report-safe metadata fields:

- endpoint;
- auth status / denial reason;
- degraded flag and degraded reasons;
- item count;
- safe source/evidence labels if present;
- zero guarded counters for the denied mismatch case;
- blocker classification if denied or empty.

If metadata items are returned, #358 may record safe labels only. It must not quote raw item text, raw source text, private paths, source URIs, platform raw IDs, backend/provider payloads, callback payloads, auth material, credential secret strings, bearer secret strings, OAuth material, auth-file contents, environment secret strings, keychain secret strings, or private correlation references.

## Stop conditions

Stop immediately and do not broaden or loop on any of these outcomes:

- `auth_status_code=403` or equivalent denied auth status;
- `items=[]` / empty item count;
- `wrong_route_audience`;
- `unauthorized_narrowing`;
- raw/private/source/auth/provider/callback output request;
- source discovery, workspace/family scan, broad recall, or index query request;
- Runtime Registry request or consumption;
- provider callback, provider route, service activation, canary, prod, Gate, or Atlas Gate movement request;
- write, custody, delete, reindex, rollback, cache-purge, persistence, or mutation request;
- broad `allowed=true` behavior or any attempt to convert readiness metadata into standing authority.

## Required denied-before-read mismatch case

If the tool path safely supports an out-of-scope denial check without source access, #358 should run exactly one mismatch case and record zero counters. The packet's committed fixture proves the safe shape by changing the recall route audience to the context audience before evaluating the non-secret service-auth contract. The resulting receipt is `DENIED_BEFORE_READ_OUT_OF_SCOPE_MISMATCH`, `auth_status=denied_before_read`, `items=[]`, `denial_reason=wrong_route_audience`, and all guarded counters zero.

If the live MCP tool path does not expose a separate mismatch-only denial check that avoids source access, #358 must say so and skip the mismatch improvisation.

## Verification gate

L6AM.01 is complete when this packet and test are committed, discoverable from the docs index and contract-test inventory, and the following commands pass:

- `python -m pytest -q tests/test_l6am01_supervised_metadata_retry_packet.py`
- `python -m pytest -q`
- `python scripts/public_hygiene_scan.py`
- `git diff --check`
- `python -m compileall -q src tests examples`

Residual holds after this packet: no retry execution in #357; no secret/env/keychain/OAuth/auth-file/credential reads; no raw/private/source/auth/provider/callback payload output; no source discovery; no broad recall/index queries; no Runtime Registry consumption; no provider callback invocation; no service activation; no cron changes; no writes/mutations outside repo docs/tests/code for this issue; no provider/prod/canary/Gate/Atlas Gate movement; no broad `allowed=true` behavior.
