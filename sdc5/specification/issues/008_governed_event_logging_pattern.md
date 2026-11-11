# SDC5 Issue: Governed Event (Logging) Pattern: SDC4 Mapping and a Reusable Component Set

**Filed**: November 11, 2026
**Priority**: Medium
**Affects**: Published component library and modeller guides (no SDC4 RM change); informs the SDC5 AuditType design pass (Issues 001 to 003)
**Discovered during**: Review of a vendor-neutral security-logging event contract for logging-maturity and GRC work
**Raised by**: T. Cook (RM owner), 2026-11-11

## Problem

Security and operations logging is moving from "store the string" to treating each
log entry as a **governed, self-describing event**: a vendor-neutral event contract
that travels with the record, so events from different sources can be correlated,
policy can be applied by meaning rather than by emitting system, and logging
maturity can be shown through evidence instead of volume or retention settings.

A typical minimum event contract asks for:

- **Identity and time**: event ID, event time, collection time, source, schema version.
- **Who and what**: actor or service identity, action, target resource, outcome,
  privilege or authentication context.
- **Where and how it relates**: system or workload, environment, asset or tenant,
  trace and correlation identifiers.
- **Governance and evidence**: classification, provenance, integrity indicators,
  retention and access policy tags, lineage to the originating source, and the
  original event preserved beside the normalized form.

SDC4 can model all of this. There is, however, no published guidance or reusable
component set showing *how*, so each modeller would re-derive the mapping and
choose different homes for the same facts.

## SDC4 mapping (works today, no RM change)

| Event-contract element | SDC4 home |
|---|---|
| Event ID | `DMType/instance_id` (plus `instance_version`) |
| Schema version | The data model's own identifier. Models are immutable; a changed definition is a new model, so historical meaning is never silently edited. |
| Event time | `vtb` on the event component, or a bound `XdTemporal` in `Item` |
| Collection / recorded time | `tr`; DM `creation_timestamp`; `modified` for later change |
| Source system and custody trail | `Audit` (0..unbounded: `system-id`, `system-user`, `location`, `timestamp`) |
| Lineage to originating record | `source_instance_id`, `source_version_id`; PROV-O cluster in `Item` (Issue 003 workaround) |
| Actor or service identity | `Participation` (`performer`, `function`, `mode`, `start`, `end`); `subject` / `provider` (PartyType) |
| Action, target, outcome | Bound components in `Item` (`XdToken` / `XdString` against a published vocabulary; `XdLink` to the target resource). See Issue 002 for the audit-only case. |
| Privilege / authentication context | Bound components in a Cluster in `Item` |
| System, workload, environment, tenant | Cluster in `Item` |
| Trace and correlation IDs | `XdLink` (`link`, `relation`, `relation-uri`); see Issue 010 for a relation vocabulary |
| Classification, retention, handling and access tags | `act` on any component, with terms from the controlled vocabulary the DM names in `acs`; see Issue 009 |
| Integrity indicators | `attestation` (`proof`, `committer`, `committed`); `hash-result` / `hash-function` on `XdFile`. See Issue 004 for multiple attestations. |
| Original event preserved | `XdFile` (`media-content` or `uri`, `media-type`, `hash-result`, `hash-function`) |
| Masking, uncertain or derived mappings | Exceptional Values: `MSK` (masked), `UNC` (uncertain), `DER` (derived), `TRC` (truncated), `INV` (invalid) |
| Field ownership and definitions | Model-level metadata and each component's `rdfs` semantic binding |

Data-quality measures (coverage, required-field completeness, timestamp
reliability, mapping errors, schema drift by source) are corpus-level facts
produced by validation over many instances. They do not belong in the record,
and are not an RM gap.

## Recommendation

1. **Publish a reusable "governed event" component set** in the component library:
   an event Cluster with bound `action`, `target`, `outcome`, `correlation`
   (XdLink), and `original-event` (XdFile) components, ready to reuse inside
   `Item`. Domain-neutral: it names no vendor, product or log format.
2. **Add a modeller guide** ("Modelling governed events and logs in SDC") built on
   the mapping above, including the convention for event time (`vtb`) versus
   recorded time (`tr`).
3. **Feed the SDC5 AuditType design pass.** This pattern is the same pressure
   recorded in Issues 001 to 003: the audit-only access log (Issue 002, including
   its Read/View argument) and transformation lineage (Issue 003). The separate
   access-log DM suggested in Issue 002 is the natural home for this pattern.

## Domain neutrality check

Stays neutral. Logging is one use; the same pattern fits any event record (clinical
encounters, transactions, sensor readings). No vendor, product or log schema is
introduced into the RM.

## Compatibility

SDC4-only work (components and guides). Nothing changes in either namespace unless
the AuditType design pass decides to add slots.

## Related

Issues 001, 002, 003, 004 (this directory); Issues 009 and 010 (filed with this one).
