# ADR 0001 — Fleet read privacy: open-within-fleet, walls by exception

**Status:** Accepted (maintainer decision, 2026-06-09)
**Deciders:** project maintainers

## Context

The seam must decide what cross-agent visibility its read scopes grant. Three models were on the table: hard walls (own-agent data only; sharing via wiki promotion), a metadata tier (cross-agent sees existence/title/date, never bodies), and open-within-fleet (bodies readable cross-agent with receipts). Relevant facts: the reference deployment is a controlled cooperative fleet; the legacy recall path already serves diary content cross-agent with no walls and no receipts; the seam's value-add is provenance and audit, not access reduction; `private_class` labeling and the universal secrets ban already exist in the envelope schema.

## Decision

**Open-within-fleet (option C).** Diary bodies and self-context families are readable across cooperating fleet agents through the seam, with every read identity-bound, receipted, and provenance-labeled (`source_tier`, `agent_owner`, `private_class`). Hard walls apply **by exception, not default**: files/classes explicitly marked private keep metadata-only or denied posture, and credential/secret material remains banned at every layer. Each agent also reads its **own** context families (soul/memory/last-session) through the seam. The rationale: open cooperative context should be the default for approved fleet members, and walls are cheap to add later with receipt evidence in hand, while re-opening a walled fleet is hard to justify.

## Consequences

- The seam matches (then audits) the fleet's existing de-facto openness rather than reducing capability at adoption time.
- W2 (context+diary scope grants) designs per-family grants with open-within-fleet defaults + an exception mechanism (private-class walls), instead of per-pair allowlists.
- A future tightening (isolating an agent, walling a repo/doc) is a **grant change + ADR**, not a redesign; the receipt history provides the evidence base for any such change.
- Cross-agent re-serving of `agent_private`-classed items stays banned per the Fleet Adoption Contract §4.5 — "open" applies to standard diary/context content, not to the explicitly-private class.
