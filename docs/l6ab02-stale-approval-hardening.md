# L6AB.02 stale approval hardening

Status: `STALE_APPROVAL_HARDENING_FIXTURES_NO_LIVE_READS`

Rail issue: #252  
Parent issue: #6  
Depends on: #251 closed/PASS  
Source floor requirement: `91761ed55889f4c5432b55c445e396e727a6be93` or later

## Purpose

L6AB.02 expands report-safe stale-approval fixtures around the existing L6AA #242 value-proof helper without performing any new live/private read. The fixtures are derived from existing repo artifacts and public issue/PR metadata semantics only.

The hardening review covers denial-before-read cases for:

- stale issue numbers;
- copied owner text represented as the same owner/comment shape rebound to the wrong comment or issue metadata;
- broadened operation counts;
- expired approval windows;
- mismatched descriptor/source-card refs;
- non-owner approval;
- broad `allowed=true` variants.

## Consumed PASS boundary

The exact #242 PASS fixture is consumed historical evidence only. It records one already-executed, report-safe source-card read from L6AA.02 and is not standing authority for #252 or any future issue. Replaying the same metadata against another issue number must deny before read.

## Preserved holds

This packet is docs/tests/fixtures-only and preserves:

- no live/private reads;
- no raw private content or raw approval text;
- no callbacks;
- no credentials/auth/env/keychain/OAuth/auth-file reads;
- no discovery/workspace/family scans/broad recall/index queries;
- no Runtime Registry consumption;
- no persistence/mutation/write/delete/reindex/cache-purge/rollback execution;
- no service/listener/startup/global runtime config activation;
- no publication/repo visibility/provider/prod/canary/Gate movement;
- no broad `allowed=true` route.

## Verification hook

`tests/test_l6ab02_stale_approval_hardening.py` exercises the fixture classes above and keeps the L6AA #242 PASS row framed as a single consumed read rather than reusable approval.
