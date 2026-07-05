# ADR 0005 — OSS release: read-seam first, Apache-2.0, sanitized origin story

**Status:** Accepted (maintainer decision, 2026-06-09)
**Deciders:** project maintainers

## Context

The OSS release (campaign rung W7 / plan Phase 8) needed three calls: timing, license, and public story. Timing alternatives: (A) complete-story release after the write/custody companion lands (most impressive single release; months away; sanitization surface grows while waiting); (B) read-seam-first — publish once the fleet read rollout has proven multi-agent reads in production (~post-W4), with the write companion headlining v2; (C) calendar-date driven. License: MIT vs Apache-2.0. Story: how much of the originating fleet ships in the README.

## Decision

1. **Timing: read-seam first (B).** Publish after multi-agent reads are proven in production (post fleet-rollout rung). Ship what's proven; v2 gets its own moment with the write companion.
2. **License: Apache-2.0.** The explicit patent grant suits an infrastructure trust layer adopted by organizations; simplicity loss vs MIT is acceptable.
3. **Story: sanitized origin — YES.** "Born inside a real multi-agent fleet, hardened by adversarial review" — no agent names, machine details, operational floors, or deployment config. The originating fleet remains the reference deployment as narrative, never as exposed configuration.

## Consequences

- W7's entry gate is W4 (fleet read rollout proven), not W6 — the release does not wait for writes.
- Sanitization scope is bounded to the read seam + patterns docs; the existing sanitization guard test + a full history/docs audit + security PRISM remain the release gate.
- `LICENSE` file lands as Apache-2.0 at release-prep time; package metadata aligns.
- README/origin copy is authored against the sanitized-story rule and reviewed in the release security PRISM.
