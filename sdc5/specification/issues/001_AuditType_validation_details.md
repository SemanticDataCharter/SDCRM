# SDC5 Issue: AuditType Needs Validation Details Slot

**Filed**: May 5, 2026
**Priority**: Medium
**Affects**: AuditType specification
**Discovered during**: PROV-O conformance validation for sdcgovernance

## Problem

In SDC4, AuditType has four elements: `system-id`, `system-user`, `location`, `timestamp`. There is no structural slot for recording entity state hashes (SHA-256 before/after) that enable tamper-evident provenance chains.

In sdcgovernance 4.0.0, entity state hashes were incorrectly modeled as invented sdc4 namespace properties (`sdc4:entityHashBefore`, `sdc4:entityHashAfter`). This violates the principle that the sdc4 namespace is defined exclusively by the Reference Model specification.

## SDC4 Workaround

For SDC4, entity state hashes are modeled as XdFileType components (using the RM-defined `hash-function` + `hash-result` elements) within a `ValidationDetails` subcluster in the data Cluster. This is RM-compliant but places validation metadata in the data Cluster rather than in AuditType where it semantically belongs.

Fixed in sdcgovernance 4.0.1.

## SDC5 Recommendation

Add a `validation-details` element to AuditType:

```
AuditType
  ├── system-id       (XdStringType, 1..1) -> prov:Entity context
  ├── system-user     (PartyType, 0..1)    -> prov:Agent
  ├── location        (ClusterType, 0..1)  -> where
  ├── timestamp       (xs:dateTime, 1..1)  -> when
  └── validation      (ClusterType, 0..1)  -> entity state hashes, validation results
      ├── entity-state-before (XdFileType, 0..1) -> hash-function + hash-result
      ├── entity-state-after  (XdFileType, 0..1) -> hash-function + hash-result
      └── [extensible for future validation metadata]
```

This keeps entity state hashes structurally within the audit record where they semantically belong, uses the existing XdFileType hash pattern, and is extensible for future validation information (sdcvalidator results, SHACL outcomes, etc.).
