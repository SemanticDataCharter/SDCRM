# Workflow & State Machine — RM Gap Analysis

## Purpose

This document catalogs the gaps in the SDC4 Reference Model related to workflow and state machine capabilities, assesses which gaps are resolved by redefining `DMType.workflow` from `XdLinkType` to `ClusterType`, and identifies what remains to be addressed through conventions or future RM changes.

## Background

The SDC4 XSD defines two workflow-related elements in `DMType`:

- **`current-state`** (`xsd:string`, line 2749 in `sdc4.xsd`) — Holds the current state of the data model instance.
- **`workflow`** (`ClusterType`, line 2833 in `sdc4.xsd`) — Workflow definition containing state definitions, transitions, and execution logic as a structured Cluster. (Changed from `XdLinkType` — see Gap 2.)

Neither element was documented in the SDC4 specification (`sdc4-specification.md` section 4.3.1) and no tooling was built around them. The `DM.asserts` field in SDCStudio stores XPath assertions but never emits them into generated XSD output.

### Key Decision

Since no legacy models use `DMType.workflow`, the element will be **redefined from `XdLinkType` to `ClusterType`** in the RM. ClusterType is described in the XSD as "the root component for arbitrarily complex structures" — it can contain nested Clusters plus any Xd* type, enabling rich state machine definitions with no new XSD complex types needed.

---

## Gap Assessment

### Summary Table

| # | Gap | Pre-Change Status | Post-Change Status | Resolution |
|---|-----|-------------------|-------------------|------------|
| 1 | `current-state` is unrestricted `xsd:string` | Open | **Remains** | Constrain via `xsd:assert` enumerations per DM |
| 2 | `workflow` is a pointer to external system only | ~~Open~~ | **Resolved — Implemented** | ClusterType enables full intrinsic tree structure (sdc4.xsd updated) |
| 3 | No transition model in RM | Open | **Resolved by convention** | Cluster patterns define state/transition compositions |
| 4 | No workflow-specific audit trail | Open | **Remains** | Document conventions using existing Audit component |
| 5 | `workflow` and `current-state` omitted from specification | Open | **Fix in spec update** | Add to `sdc4-specification.md` section 4.3.1 |
| 6 | No decision logic container | Open | **Resolved by convention** | XdString holds XPath expressions; `xsd:assert` enforces |
| 7 | No plan definition structure | Open | **Resolved by convention** | Nested Clusters model hierarchical plans |
| 8 | `DM.asserts` stored but not generated in XSD | ~~Open~~ (tooling) | **Resolved** (tooling) | SDCStudio publisher now generates xsd:assert elements at both Cluster and DM levels |

### Detailed Analysis

#### Gap 1: Unrestricted `current-state`

**Issue**: `current-state` is typed as `xsd:string` with no enumeration or pattern restriction, meaning any string value is valid.

**Resolution**: This is by design at the RM level — different DMs will have different valid states. The constraint mechanism is `xsd:assert` at the DM level:

```xml
<xsd:assert test="current-state = 'Draft' or current-state = 'Review' or current-state = 'Approved'"
            xpathDefaultNamespace="##targetNamespace"/>
```

**Status**: Remains open at RM level (correct behavior). Resolved per-DM via assertions.

#### Gap 2: Workflow as External Pointer

**Issue**: As `XdLinkType`, the `workflow` element can only point to an external workflow engine via URI. This prevents the "smart packet" pattern where workflow definitions travel with the data.

**Resolution**: Redefining to `ClusterType` allows the workflow element to contain:
- Nested Clusters for hierarchical plans
- XdString elements for state definitions, XPath expressions, and descriptions
- XdLink elements for optional external engine references (preserving backward compatibility by convention)
- XdTemporal elements for timestamps
- XdBoolean elements for flags and conditions
- Any other Xd* type as needed

**Status**: **Resolved — Implemented**. The `sdc4.xsd` schema has been updated to use `ClusterType` for the workflow element. SDCStudio model, publisher, and agentic system updated to match.

#### Gap 3: No Transition Model

**Issue**: The RM has no dedicated transition type connecting one state to another.

**Resolution**: Transitions are modeled as Cluster patterns within the workflow. A recommended pattern:

```
workflow (Cluster)
├── states (Cluster)
│   ├── state-1 (XdString, fixed="Triage")
│   ├── state-2 (XdString, fixed="Admit")
│   └── state-3 (XdString, fixed="Discharge")
└── transitions (Cluster)
    ├── transition-1 (Cluster)
    │   ├── from-state (XdString)
    │   ├── to-state (XdString)
    │   └── guard-condition (XdString, holds XPath expression)
    └── transition-2 (Cluster)
        ├── from-state (XdString)
        ├── to-state (XdString)
        └── guard-condition (XdString)
```

**Status**: **Resolved by convention**. The Cluster compositional model provides sufficient expressiveness.

#### Gap 4: No Workflow-Specific Audit

**Issue**: State transitions should be auditable, but no workflow-specific audit mechanism exists.

**Resolution**: The existing `DMType.audit` element (`AuditType`, unbounded) already supports multiple audit records per DM instance. Workflow state changes should produce Audit entries following these conventions:

- The audit `system-id` identifies the workflow engine or process
- The audit `system-user` identifies the actor performing the transition
- The audit `timestamp` captures when the transition occurred
- Free-text fields capture from-state, to-state, and justification

**Status**: **Remains** — no RM change needed, but conventions should be documented.

#### Gap 5: Specification Omission

**Issue**: Section 4.3.1 of `sdc4-specification.md` lists only `instance_id`, `creation_timestamp`, `provider`, and `subject`. It omits `current-state`, `workflow`, `acs`, `protocol`, `attestation`, `audit`, `links`, and `participations`.

**Resolution**: Update the specification to include all DMType elements.

**Status**: **Fix in specification update** (deliverable R1).

#### Gap 6: No Decision Logic Container

**Issue**: No place in the RM to store executable decision logic (guard conditions, routing rules).

**Resolution**: Within the workflow Cluster, XdString elements can hold XPath expressions as their values. These expressions are referenced by `xsd:assert` elements in the DM's complexType definition to create enforceable constraints. The XdString `label` describes the rule; the `xdstring-value` holds the XPath expression.

**Status**: **Resolved by convention**.

#### Gap 7: No Plan Definition Structure

**Issue**: No way to model multi-step plans, task sequences, or hierarchical workflows.

**Resolution**: Nested Clusters within the workflow element can model arbitrarily complex hierarchical plans:

```
workflow (Cluster: "Treatment Plan")
├── phase-1 (Cluster: "Assessment")
│   ├── task-1 (XdString: "Initial Triage")
│   └── task-2 (XdString: "Lab Orders")
└── phase-2 (Cluster: "Treatment")
    ├── task-3 (XdString: "Administer Medication")
    └── task-4 (XdString: "Follow-up Schedule")
```

**Status**: **Resolved by convention**.

#### Gap 8: Asserts Not Generated

**Issue**: SDCStudio's `DM.asserts` field stores XPath assertions but `publisher.py` never generates `<xsd:assert>` elements in the XSD output.

**Resolution**: This is a tooling gap, not an RM gap. SDCStudio now generates `<xsd:assert>` elements at both the Cluster and DM levels in the published XSD output (implemented in commit `6ae6015`).

**Status**: **Resolved** (implemented in SDCStudio).

---

## openEHR PROC Conceptual Mapping

The openEHR Process Model (PROC) specification provides a comprehensive clinical workflow framework. This section maps PROC concepts to SDC4 equivalents to validate that ClusterType provides sufficient expressiveness.

### Three-Tier Mapping

#### Tier 1: Direct Matches

| openEHR PROC Concept | SDC4 Equivalent | Notes |
|----------------------|-----------------|-------|
| Task Plan | Workflow Cluster | Top-level container for workflow definition |
| Task | XdString within Cluster | Individual action or step |
| Task Group | Nested Cluster | Grouping of related tasks |
| Plan state | `current-state` element | Current execution state |
| Decision Path | XdString holding XPath | Guard conditions on transitions |
| Performer | Participation / Party | Who executes the task |
| Audit trail | DMType.audit | Record of state changes |

#### Tier 2: Cluster Convention Equivalents

| openEHR PROC Concept | SDC4 Convention | Notes |
|----------------------|----------------|-------|
| Work Plan | Workflow Cluster with nested phase Clusters | Hierarchical task organization |
| Execution History | Audit entries with workflow context | State change records |
| Decision Logic (GDL) | XdString values + xsd:assert | XPath-based guard conditions |
| Task lifecycle | XdString enumerations in state Cluster | Available/active/complete/cancelled |
| Callback notification | XdLink within transition Cluster | Reference to notification endpoint |
| Context variables | XdString/XdCount/etc. within Cluster | Runtime values for decision logic |

#### Tier 3: Not Applicable / Out of Scope

| openEHR PROC Concept | SDC4 Position | Rationale |
|----------------------|--------------|-----------|
| Visual Modelling Language (TP-VML) | Tooling concern | SDCStudio UI responsibility, not RM |
| External scheduling integration | Out of scope | SDC defines data, not runtime orchestration |
| Real-time timer events | Out of scope | Requires runtime engine, not schema construct |
| Hand-off to external system | XdLink (by convention) | Reference to external system, not RM orchestration |

### openEHR Entity Model Observation

The openEHR Entity model (`entity.html`) defines physical entities (devices, people, organizations) but notably **contains no workflow concepts**. Workflow in openEHR is handled entirely at the PROC/Task Planning layer, not at the entity/data level.

This validates SDC4's approach of placing workflow at the **DMType level** (the data model wrapper) rather than at the component level. The data instance carries its own workflow definition, consistent with the "smart packet" philosophy.

---

## XML Technology Stack Binding

The workflow capability leverages established XML standards:

| Technology | Version | Role in SDC4 Workflow | Specification |
|-----------|---------|----------------------|---------------|
| **XPath** | 2.0 (in XSD), 3.1 (runtime) | Guard conditions, state validation via `xsd:assert` | W3C Recommendation |
| **XSD 1.1** | 1.1 | Schema-level assertions (`xsd:assert`), type definitions | W3C Recommendation |
| **XProc** | 3.0 | Pipeline orchestration for multi-step workflows (external) | W3C Note |
| **XSLT** | 3.0 | State transformation, view generation (external) | W3C Recommendation |

**Note**: XPath 2.0 is the version mandated by XSD 1.1 for `xsd:assert` expressions. XPath 3.1 is available for runtime processing by external engines but cannot be used in schema assertions.

---

## Roadmap Integration Recommendation

The workflow capability fits naturally into the **4.2.0 release** (Q2 2026), which already plans "Enhanced Cluster Features" and "Reusable cluster definitions" according to `docs/ROADMAP.md`.

### Suggested Additions to 4.2.0

1. **Schema Change**: Redefine `DMType.workflow` from `XdLinkType` to `ClusterType`
2. **Specification Update**: Add all missing DMType elements to specification section 4.3.1
3. **Guide Publication**: Publish the workflow-state-machine guide with recommended Cluster patterns
4. **Tooling Coordination**: Coordinate with SDCStudio for model migration and publisher updates

### Version Impact

This change is a **MINOR** version increment (4.1.0 or 4.2.0) because:
- No existing production models use the `workflow` element (confirmed)
- The change is additive in capability (Cluster can do everything XdLink can, plus more)
- No instance documents need migration
- The specification explicitly permits such changes at MINOR level

---

## References

- `sdc4/schemas/sdc4.xsd` — DMType definition (line 2637), current-state (2749), workflow (2833), ClusterType (2519)
- `sdc4/specification/sdc4-specification.md` — Section 4.3.1 (line 126)
- `docs/ROADMAP.md` — Release calendar and 4.2.0 plans
- openEHR PROC: https://specifications.openehr.org/releases/PROC/development
- openEHR Entity: https://specifications.openehr.org/releases/RM/development/entity.html
