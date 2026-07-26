# SDC5 Issue: AuditType Needs a Native W3C PROV-O Derivation Graph

**Filed**: July 26, 2026
**Priority**: High (converges with Issues 001 and 002 toward an AuditType redesign)
**Affects**: AuditType specification
**Discovered during**: CordovaOS governance composition mapping (10 government domains) and the Symphony / AI-GRC agentic-provenance requirements built on the same substrate

## Problem

Native `AuditType` records **who / where / when** (`system-id`, `system-user`, `location`, `timestamp`) as an instance moves system to system. It has no structural slot for a **W3C PROV-O derivation graph**: which `prov:Entity` was derived from which other Entity, via which `prov:Activity`, attributed to which `prov:Agent`.

For custody tracking, who/where/when is correct and sufficient. Two drivers need more:

1. **Data lineage.** Governed records whose provenance is "this value was produced from these inputs by this transformation" require a derivation chain (`wasDerivedFrom`, `wasGeneratedBy`, `used`) that who/where/when cannot express.
2. **Agentic governance.** For the AI-GRC / Symphony layer built on this substrate, the core auditable fact is "what did the agent read, through what activity, to produce this output." That is exactly a `prov:Entity -> prov:Activity -> prov:Agent` graph. Native `AuditType` cannot represent the agent-activity-entity triangle or the derivation edges between entities.

## SDC4 Workaround

Model the provenance as a **W3C PROV-O cluster** (`PROV Entity` / `PROV Activity` / `PROV Agent` / `PROV Bundle`) inside the data `Cluster` (`DMType.Item`), reusing the ProvGov catalog components. This is fully RM-compliant: each component carries its own `rdfs` semantic binding, so PROV-O semantics are bound into the payload. But it places provenance in the data `Cluster` rather than in `AuditType`, where it semantically belongs. This is the same class of compromise as Issue 001 (validation-details) and Issue 002 (action/outcome): correct data, semantically misplaced container.

**Adopted for the CordovaOS rebuild** (2026-07-26): provenance is a PROV-O cluster in `Item`; native `AuditType` still available for the system-handling trail.

## SDC5 Recommendation

Redesign `AuditType` to natively carry (or reference) a PROV-O derivation structure. Sketch:

```
AuditType
  ├── system-id     (XdStringType, 1..1)   -> prov:Entity context / which system
  ├── system-user   (PartyType, 0..1)      -> prov:Agent (custody actor)
  ├── location      (ClusterType, 0..1)    -> where
  ├── timestamp     (xs:dateTime, 1..1)    -> when
  ├── validation    (ClusterType, 0..1)    -> entity state hashes (Issue 001)
  └── provenance    (ClusterType, 0..1)    -> W3C PROV-O derivation graph
        ├── entity   (0..unbounded) -> prov:Entity   (wasDerivedFrom)
        ├── activity (0..unbounded) -> prov:Activity  (used / wasGeneratedBy)
        └── agent    (0..unbounded) -> prov:Agent     (wasAssociatedWith / actedOnBehalfOf)
```

## Note: the three AuditType issues converge

This is the **third** AuditType issue (001 validation-details, 002 action/outcome, 003 derivation graph). Individually each is a slot addition; together they indicate `AuditType` should be reconsidered **holistically** in SDC5 as a first-class, PROV-O-aligned provenance record rather than incrementally patched. Recommend an SDC5 **"AuditType 2.0" design pass** that folds in all three (validation, action/outcome for the audit-only case, and the derivation graph) in one coherent structure, rather than three independent additions.

## Reference

- CordovaOS Governance Composition Map (`CordovaOS/docs/design/2026-07-26-Governance-Composition-Map.md`).
- GRC component set plan (`Advisors/TimLee/SDC+SoD/2026-07-26-GRC-component-set-plan.md`) — the AI-GRC layer that makes the derivation graph a hard requirement.
- Related: Issues 001 and 002 (this directory).
