# Security Policy

Memory Seam is a public source package for a no-live/read-only memory-boundary core. It is not a production service, live adapter, credential surface, or custody system.

## Supported status

| Area | Status |
| --- | --- |
| Standalone package contracts, policy, descriptors, receipts, router, testing helpers | Supported |
| Synthetic examples and fixtures | Supported |
| Live adapters, service/listener wiring, Runtime Registry reads, unsupervised reads | Not supported |
| Writes, custody, reindexing, provider/prod/canary authority | Not supported |

## Reporting security issues

Report suspected security problems through GitHub Security Advisories using the
repository's private vulnerability reporting flow. Please do not open public
issues for vulnerabilities before maintainers have reviewed them. Include:

- the affected file or API surface;
- the observed behavior;
- whether any live/private source read, credential access, write/custody/reindex action, or service start was involved.

## Release safety boundary

Before any package publication, maintainers must verify:

1. `python scripts/public_hygiene_scan.py` passes;
2. no host-private paths, raw source identifiers, credentials, tokens, or private provenance details exist in shipped artifacts;
3. examples use only synthetic committed content;
4. package metadata and documentation do not imply live adapter, write custody, or production authority support;
5. package publication is approved explicitly.
