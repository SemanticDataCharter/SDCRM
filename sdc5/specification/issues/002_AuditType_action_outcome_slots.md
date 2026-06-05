# SDC5 Issue: AuditType Action/Outcome Slots for Audit-Only Models

**Filed**: June 5, 2026
**Priority**: Low (likely to be declined; see note)
**Affects**: AuditType specification
**Discovered during**: FHIR Provenance/AuditEvent ProvGov mapping

## Problem

FHIR `AuditEvent` carries `action` (C/R/U/D/E) and `outcome` as first-class
fields. When mapping FHIR governance onto SDC, the action verb maps cleanly to a
`DM.workflow` transition (XdOrdinal state change), so `AuditType` correctly
records only who/where/when. The audit record was never meant to hold the action.

The gap appears only in the **audit-only** case: a model with no workflow
dimension (e.g. a pure security access log) has no native slot for the action
verb or its outcome inside `AuditType`.

## SDC4 Workaround

Model `action` and `outcome` as bound `XdToken`/`XdString` components inside the
`AuditType.location` ClusterType. This is fully RM-compliant (each component
carries its own `rdfs` semantic binding, so the meaning travels in the payload)
but semantically misplaced: the `location` container's own RDF says "Location
information of the particular site/facility." It is a legibility compromise, not
a correctness one. The data is correct; only the container label misleads a human
reader.

## SDC5 Recommendation

Consider optional `activity` and `outcome` slots on AuditType for the audit-only
case:

```
AuditType
  ├── system-id   (XdStringType, 1..1) -> which system handled it
  ├── system-user (PartyType, 0..1)    -> who (custody actor)
  ├── location    (ClusterType, 0..1)  -> where
  ├── timestamp   (xs:dateTime, 1..1)  -> when
  ├── activity    (XdTokenType, 0..1)  -> the action verb, audit-only case
  └── outcome     (XdTokenType, 0..1)  -> the result, audit-only case
```

## Note (filer's inclination)

This is likely to be **declined** in SDC5 design. The action belongs in
`DM.workflow`, and `AuditType` is intentionally who/where/when. The audit-only
case can already be modeled via the `location` workaround above. Filed now per
the principle of capturing the question while it is fresh and deciding it during
SDC5 design, not because adoption is expected.

## Reference

Mapping that surfaced this: `/home/twcook/GitHub/FHIR-ProvGov/provgov-fhir-mapping.md`
(§6, sdc5-planning gaps).
