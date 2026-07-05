# Portable schema contracts

Memory Seam's portable schema contract is a no-live control-plane contract. It describes how descriptors, grants, receipts, source-floor metadata, degraded/no-live labels, and report-safe disclosure labels fit together before any downstream adapter performs provider, file, stat, backend, service, Runtime Registry, credential, write, custody, reindex, or discovery work.

This document is documentation only. It does not authorize live reads, source discovery, service/listener activation, credential/auth/env/keychain reads, Runtime Registry runtime consumption, unsupervised reads, writes/custody/reindex behavior, package publication, repository visibility changes, provider/prod/canary authority, or Atlas Gate movement.

## Contract surfaces

| Surface | Portable contract | Fail-closed default | No-live boundary |
| --- | --- | --- | --- |
| Descriptor | `ContextSourceDescriptor` names an exact `(subject, include_family)` registration, opaque `root_ref`, relative path, source tier, private class, canonicality, retrieval backend, byte ceiling, freshness window, enabled flag, and optional safe summary. | Missing descriptors and disabled descriptors deny before read. Unknown include/source families are invalid policy data or denied by runtime preflight. | Descriptors are registrations, not discovery. The report helper emits root refs and relative paths only; it does not expose local root paths or source text. |
| Grant / control plane | `ContextSourceGrant` and `ContextSourceGrantMatrix` are per-subject/per-family allow rows. Materialization requires grants unless a legacy test-only escape hatch is explicitly used. | Blank/missing grant cells are denied by default as `source_grant_missing`; disabled grants deny as `source_grant_disabled`. A grant cannot invent a descriptor. | Grants carry no paths, root material, credentials, token material, discovery rules, or backend authority. |
| Receipt / source floor | Read receipts are metadata-only (`memory_seam_read_receipt_v0`) and runtime receipts include safe rollback/audit shapes. Source-floor evidence is an opaque label in receipts/docs, not a raw source pointer. | Denials are recorded as deny-before-read outcomes where applicable, including unknown source family, missing/blank grant, disabled descriptor, kill switch, and protected-path classes. | Receipts must not persist raw content, raw source paths, credentials, private absolute paths, raw platform IDs, or private correlation references in public artifacts. |
| Degraded / no-live labels | Envelopes and fixtures carry posture labels such as `read_backend_called=false`, `service_started=false`, `runtime_registry_consumed=false`, `raw_fallback_used=false`, and `write_custody_or_reindex=false`. | Unknown or unconfigured providers degrade safely (`provider_unconfigured`) instead of falling back to raw reads. | Degraded/no-live flags are evidence fields only; they do not activate services or widen authority. |
| Disclosure / redaction labels | Source cards and items use metadata labels (`source_tier`, `private_class`, `canonicality`, `retrieval_backend`, `redaction_applied`, `redaction_labels`) and safe summaries. | Unsafe source-card fields/fragments are rejected; redaction that erases usefulness is scored as not useful rather than bypassed. | Public artifacts may contain only report-safe labels, summaries, counts, and opaque/hashing handles that do not reveal private source text or raw local identifiers. |

## Deny-by-default semantics

The consolidated F2 contract uses these defaults across docs/tests/schema fixtures:

1. **Missing descriptor:** no descriptor row means no source registration. The portable core does not discover a substitute source.
2. **Disabled descriptor:** `enabled=false` yields `descriptor_disabled` during allowlist materialization and must deny before file/stat/backend reads.
3. **Missing or blank grant:** absence of an enabled grant row is a blank control-plane cell and yields `source_grant_missing`; descriptor materialization without grants is refused unless the caller names the legacy test-only escape hatch.
4. **Disabled grant:** an explicit disabled grant row yields `source_grant_disabled` and does not materialize the source.
5. **Unknown include/family:** unknown descriptor/grant include families are rejected as policy data; unknown context or recall families on the runtime path deny before provider calls.
6. **Unknown descriptor referenced by grant:** grant matrices cannot add new source authority; grants referencing absent descriptors raise before materialization.

## Held downstream surfaces

Atlas Query adapters, private source-card decks, real source-family fixtures, live provider integrations, real auth/verifier material, and release/publication decisions remain downstream or held. This schema contract only consolidates the portable no-live core boundary for future verifier work.
