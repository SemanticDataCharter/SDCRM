# SDC5 Issue: Bind the `workflow` Slot and Constrain `current-state` (Conformance Rule)

**Filed**: September 25, 2026
**Priority**: Medium
**Affects**: DMType specification (`workflow`, `current-state` elements); conformance section
**Discovered during**: ProvGov library rebuild (Axius-SDC/ProvGovLibrary PRD, §2)
**Raised by**: T. Cook (RM owner), 2026-09-25

## Problem

`DMType.workflow` is a **named** element typed `ClusterType` (sdc4.xsd line 2869; sdc5.xsd unchanged). Unlike the data slot, which is `ref="sdc:Item"` and is bound in a model by substitution to `ref="sdc:ms-{cuid2}"`, a named element is bound by **type restriction**: a model's `DMType` restriction may declare

```xml
<xsd:element maxOccurs="1" minOccurs="0" name="workflow" type="sdc5:mc-{workflow-cluster-cuid2}"/>
```

which is a valid particle restriction because every `mc-` type derives from `ClusterType` by restriction. The RM permits this binding but nothing in the specification requires it. The reference generator (SDCStudio `publisher.py`) repeats the base type, so today a published workflow cluster is present in a model's schema and bound to nothing: any `ClusterType` content validates in the `workflow` slot, and the state machine the model claims to carry is not what the schema enforces.

`current-state` is `xsd:string`. The SDC5 workflow guide (§2.3) constrains it with hand-written `xsd:assert` tests listing the state names. A plain enumeration restriction of the string type inside the same `DMType` restriction achieves the same without assertions and is derivable mechanically from the workflow cluster.

Gap 5 of `docs/WORKFLOW_RM_GAPS.md` (specification omits `workflow` and `current-state` from the DMType element list) is still open.

## SDC4 Workaround

None needed in the RM. The binding is legal SDC4 today; the generator is being changed to emit it (SDCStudio, ProvGov library phase 1). Instances validated against a schema without the binding remain valid after it is added only if their `workflow` content already conforms to the cluster, which is the intended effect.

## SDC5 Recommendation

Add to the conformance section, DMType:

1. A conforming model that carries a workflow **SHALL** restrict the `workflow` particle to the type of the published Cluster that defines it (`type="sdc5:mc-{cuid2}"`). A model that carries no workflow leaves the particle at the base type or omits it.
2. A conforming model that carries a workflow **SHOULD** restrict `current-state` to the set of state symbols the workflow defines, as an `xsd:enumeration` restriction of `xsd:string`, and **MAY** give the initial state as the element default.
3. List `workflow` and `current-state` (with `acs`, `protocol`, `attestation`, `audit`, `links`, `participations`) in the DMType element list of the specification (closes gap 5).

No XSD change. The RM already permits everything above; the issue is that the specification does not ask for it, so implementations skip it.

## Reference

- `docs/WORKFLOW_RM_GAPS.md`, gap 5.
- sdc4.xsd line 2869 (`workflow`), DMType data slot `ref="sdc4:Item"`.
- SDCStudio `dmgen/publisher.py` (DMType restriction; workflow particle emitted at base type).
- Axius-SDC/ProvGovLibrary `ProvGov-library-PRD.md` §2.4, §2.5.
- Related: issue 007 (workflow structure convention).
