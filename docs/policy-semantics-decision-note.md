# Policy semantics decision note

## Decision

Memory Seam's portable F2 policy model is a fail-closed, no-live control-plane contract. A source is eligible for synthetic read-only routing only when all of these independent axes agree before any provider, backend, file, stat, service, Runtime Registry, credential, discovery, write, custody, or reindex behavior can occur:

1. **Subject:** the caller identity must be an exact portable subject such as `agent:example`; a wrong or unverified subject denies.
2. **Include family / scope:** the requested context include or recall scope must be one of the supported no-live families; unknown families deny before handler/provider work.
3. **Descriptor registration:** a descriptor registers an exact `(subject, include_family)` pair plus report-safe metadata. Missing or disabled descriptors mean there is no source authority.
4. **Grant / control-plane authority:** a grant enables the same exact subject/family pair. Missing, blank, disabled, or descriptor-mismatched grants do not imply permission.
5. **Receipt and source-floor labels:** receipts record metadata-only evidence labels, rollback hints, and no-live posture. A source-floor label is an opaque evidence floor, not a raw path, source dump, platform identifier, or live authority token.
6. **Reportable reason hygiene:** denial reasons must be distinct enough for operator audit while remaining safe for public issue/PR artifacts.

The portable package therefore treats descriptor registration and grant authority as an intersection, not a union. A descriptor without a grant is not enough; a grant without a descriptor is not enough; an unknown family is not a prompt to discover a source; and a degraded provider is not permission to fall back to raw reads.

## Semantic axes

| Axis | Meaning | Fail-closed reason shape | Held or no-live boundary |
| --- | --- | --- | --- |
| Subject | The authenticated or fixture identity used for policy lookup. | `mcp_authority_unverified`, subject mismatch, or verifier-specific denial. | No real credential, keychain, OAuth, auth-file, service identity, or provider authority is introduced here. |
| Include family / scope | The requested portable family, for example project context or supported recall scope. | `unsupported_context_include` or `unsupported_recall_scope` for unknown runtime families. | Unknown families do not trigger source discovery, crawl, registry lookup, or live adapter fallback. |
| Descriptor registration | A committed registration for an exact subject/family pair with safe metadata and an opaque root reference. | `descriptor_missing` or `descriptor_disabled`-class outcomes. | Descriptors are not filesystem roots for public artifacts and do not expose raw local paths or source text. |
| Grant / control plane | An explicit enabled allow row for the same subject/family pair. | `source_grant_missing`, `source_grant_disabled`, or an unknown-descriptor grant error. | Blank cells are denied; grants cannot create new source families, roots, credentials, or backend authority. |
| Receipt / source floor | Metadata-only audit labels, posture booleans, and opaque evidence floor handles. | Denied receipts preserve status and reason without materializing a source. | Source floors are labels for review, not Runtime Registry consumption, provider/prod authority, or private source pointers. |
| Reportable reason hygiene | Public-safe operator explanation of why a request was allowed, denied, or degraded. | Distinct reasons stay safe by avoiding raw payloads and private identifiers. | Public artifacts may include counts, booleans, opaque handles, and safe summaries only. |

## Denial reason semantics

Denial reasons are part of the contract because they tell operators which control-plane cell failed without revealing private material. The current rule is:

- Use **specific reasons** for bounded policy failures: missing grant, disabled grant, disabled descriptor, unknown family, wrong subject, wrong audience/scope, unsupported route, malformed parser input, or provider-unconfigured degradation.
- Prove relevant negative paths **before source materialization**. Tests must show zero provider/backend/read/stat calls or an equivalent spy/monkeypatch assertion when the denial is supposed to happen before reads.
- Keep reasons **reportable-safe**. They may name portable contract fields and sanitized family labels, but they must not include raw source text, credential material, auth/env/keychain values, raw platform IDs, private absolute paths, raw query payloads, or private correlation references.
- Treat degraded no-live outcomes as **safe non-authority**. A degraded or unconfigured provider can explain why no content was returned; it cannot authorize raw fallback, source discovery, service startup, or Runtime Registry consumption.

## Held authority boundaries

This decision note documents semantics only. It does not authorize or imply:

- service/listener activation or installation;
- credential/auth/env/keychain/OAuth/auth-file reads;
- global Hermes, MCP, client, or runtime configuration mutation;
- Runtime Registry runtime consumption;
- live/private source reads or source discovery;
- unsupervised reads, cron/startup activation, canaries, provider/prod authority, or Atlas Gate movement;
- writes, custody, reindex, thread-retirement behavior, repository visibility changes, or package publication.

Issue `#6` remains held unless Jeremy explicitly unholds it.

## Evidence needed next

Before any later wave can claim more than this F2 semantics floor, the verifier packet must collect local and CI evidence that:

1. descriptor/grant/source-floor contracts stay discoverable from public docs;
2. unknown, blank, disabled, mismatched, malformed, and wrong-subject paths deny before source/provider/file/stat/backend reads where applicable;
3. reportable public artifacts remain sanitized;
4. no service, credential, Runtime Registry, live/private source, write/custody/reindex, provider/prod/canary, release, or Gate authority moved.

For F3, the next safe unlock requires the F2 verifier issue to close/PASS, then a supervised manual pull dogfood harness can prove usefulness with source-card IDs, receipts, no raw fallback, and wrong-subject denial while preserving the same no-live boundary.
