# SDC5 Workflow & State Machine Guide

## Version 1.0 — February 2026

## Table of Contents

- [1. Overview](#1-overview)
- [2. DMType Workflow Elements](#2-dmtype-workflow-elements)
- [3. Workflow Cluster Patterns](#3-workflow-cluster-patterns)
- [4. Conceptual Model](#4-conceptual-model)
- [5. Use Case Examples](#5-use-case-examples)
- [6. Integration with Other DM Elements](#6-integration-with-other-dm-elements)
- [7. Technology Stack](#7-technology-stack)
- [8. Glossary](#8-glossary)

---

## 1. Overview

### Purpose

SDC5 data models are not merely passive containers for structured data. Through the `current-state`, `workflow`, and `asserts` elements of DMType, every SDC5 data model instance can carry its own workflow definition and state machine logic. This guide explains how to design and use these capabilities.

### Self-Describing Data Philosophy

The SDC5 Reference Model embeds meaning directly into data structures so that any conforming processor can understand the data without external documentation. The workflow capability extends this philosophy from **structural meaning** (what the data looks like) to **behavioral meaning** (what can happen to the data).

A data model instance that includes a workflow definition is a **smart packet**: it carries its own rules for state transitions, guard conditions, and validation constraints. When the packet moves between systems, the rules travel with it.

### The Smart Packet Vision

Traditional systems separate workflow logic from data:

```
[Data] ──sent to──> [External Workflow Engine] ──decides──> [Next State]
```

SDC5 smart packets embed the logic:

```
[Data + Workflow + State + Assertions] ──self-validates──> [Next State]
```

This means:
- **Portability**: Move data between systems without losing workflow context.
- **Auditability**: The workflow definition is versioned alongside the data.
- **Validation**: Schema-level assertions enforce state constraints at parse time.
- **No vendor lock-in**: Any XSD 1.1 processor can validate the constraints.

---

## 2. DMType Workflow Elements

Three elements in DMType work together to provide workflow capabilities.

### 2.1 `current-state` (xsd:string)

Holds the current state of the data model instance within its workflow.

**XSD Definition** (sdc5.xsd):
```xml
<xsd:element maxOccurs="1" minOccurs="0" name="current-state" type="xsd:string">
  <xsd:annotation>
    <xsd:documentation xml:lang="en-us">The current state according to the state machine /
      workflow engine identified in the workflow element.</xsd:documentation>
  </xsd:annotation>
</xsd:element>
```

**Semantics**:
- Type is `xsd:string` at the RM level to allow any DM to define its own state vocabulary.
- Valid values are constrained per-DM using `xsd:assert` (see section 2.3).
- Empty or absent means the instance has no active workflow state.
- The default value (set in the DM schema via `default="..."`) represents the initial state.

**Example in instance data**:
```xml
<current-state>Triage</current-state>
```

### 2.2 `workflow` (ClusterType)

Contains the workflow definition as a structured Cluster. Because ClusterType can hold nested Clusters and any Xd* type, it supports arbitrarily complex workflow structures.

**XSD Definition** (sdc5.xsd, after type change):
```xml
<xsd:element maxOccurs="1" minOccurs="0" name="workflow" type="sdc5:ClusterType">
  <xsd:annotation>
    <xsd:documentation xml:lang="en-us">Workflow definition for this data model, containing
      state definitions, transitions, and execution logic as a structured Cluster.</xsd:documentation>
  </xsd:annotation>
</xsd:element>
```

**Capabilities**:
- Define states as XdString elements with fixed enumeration values.
- Define transitions as nested Clusters containing from-state, to-state, and guard conditions.
- Define hierarchical plans as nested Cluster trees.
- Include XdLink elements for optional references to external workflow engines.
- Include XdTemporal elements for deadline or duration constraints.
- Include XdBoolean elements for simple flags and conditions.

**Relationship to `current-state`**: The `workflow` element defines the structure (what states exist, what transitions are valid). The `current-state` element holds the runtime value (which state is active now).

### 2.3 `asserts` (xsd:assert in generated schema)

XSD 1.1 assertions enforce workflow constraints at the schema validation level.

**Mechanism**: The DM schema contains `<xsd:assert test="..."/>` elements inside the DM's complexType restriction. These assertions are evaluated during schema validation and reject instance documents that violate the constraints.

**Placement in generated XSD**:
```xml
<xsd:complexType name="mc-{cuid}">
  <xsd:complexContent>
    <xsd:restriction base="sdc5:DMType">
      <xsd:sequence>
        <!-- DM elements -->
      </xsd:sequence>
      <xsd:assert test="..." xpathDefaultNamespace="##targetNamespace"/>
      <xsd:assert test="..." xpathDefaultNamespace="##targetNamespace"/>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

**Common assertion patterns**:

Constrain valid states:
```xml
<xsd:assert test="current-state = 'Draft' or current-state = 'Review' or current-state = 'Approved'"
            xpathDefaultNamespace="##targetNamespace"/>
```

Require attestation for approved state:
```xml
<xsd:assert test="not(current-state = 'Approved') or boolean(attestation)"
            xpathDefaultNamespace="##targetNamespace"/>
```

Require provider for active records:
```xml
<xsd:assert test="not(current-state = 'Active') or count(provider) >= 1"
            xpathDefaultNamespace="##targetNamespace"/>
```

---

## 3. Workflow Cluster Patterns

This section defines recommended Cluster compositions for common workflow patterns. These are conventions, not RM requirements — the ClusterType allows any valid composition.

### 3.1 Simple State Machine

A flat set of states with transition rules. Suitable for linear or branching workflows with a small number of states.

**Structure**:
```
workflow (Cluster: "Document Approval Workflow")
├── states (Cluster: "Valid States")
│   ├── state-draft (XdString, fixed="Draft")
│   ├── state-review (XdString, fixed="Under Review")
│   ├── state-approved (XdString, fixed="Approved")
│   └── state-rejected (XdString, fixed="Rejected")
└── transitions (Cluster: "Allowed Transitions")
    ├── submit (Cluster: "Submit for Review")
    │   ├── from (XdString, fixed="Draft")
    │   └── to (XdString, fixed="Under Review")
    ├── approve (Cluster: "Approve Document")
    │   ├── from (XdString, fixed="Under Review")
    │   └── to (XdString, fixed="Approved")
    └── reject (Cluster: "Reject Document")
        ├── from (XdString, fixed="Under Review")
        └── to (XdString, fixed="Rejected")
```

**Assertions**:
```xml
<xsd:assert test="current-state = 'Draft' or current-state = 'Under Review'
                  or current-state = 'Approved' or current-state = 'Rejected'"
            xpathDefaultNamespace="##targetNamespace"/>
```

### 3.2 Decision-Driven Workflow

Transitions depend on data values. Guard conditions (XPath expressions) determine which transitions are valid.

**Structure**:
```
workflow (Cluster: "Triage Workflow")
├── states (Cluster: "Triage States")
│   ├── state-triage (XdString, fixed="Triage")
│   ├── state-admit (XdString, fixed="Admit")
│   ├── state-observe (XdString, fixed="Observe")
│   └── state-discharge (XdString, fixed="Discharge")
└── transitions (Cluster: "Decision Transitions")
    ├── admit-decision (Cluster: "Admit if Critical")
    │   ├── from (XdString, fixed="Triage")
    │   ├── to (XdString, fixed="Admit")
    │   └── guard (XdString: "xs:integer(//pain-score/xdcount-value) > 7")
    ├── observe-decision (Cluster: "Observe if Moderate")
    │   ├── from (XdString, fixed="Triage")
    │   ├── to (XdString, fixed="Observe")
    │   └── guard (XdString: "xs:integer(//pain-score/xdcount-value) >= 4
    │              and xs:integer(//pain-score/xdcount-value) <= 7")
    └── discharge-decision (Cluster: "Discharge if Minor")
        ├── from (XdString, fixed="Triage")
        ├── to (XdString, fixed="Discharge")
        └── guard (XdString: "xs:integer(//pain-score/xdcount-value) < 4")
```

**Note**: Guard condition XPath expressions are stored as XdString values within the workflow Cluster. They serve as documentation and can be evaluated by external XPath processors. The `xsd:assert` mechanism enforces the schema-level constraints.

### 3.3 Multi-Step Plan (Hierarchical)

Nested Clusters model phased plans where each phase contains ordered tasks.

**Structure**:
```
workflow (Cluster: "Treatment Plan")
├── phase-1 (Cluster: "Assessment Phase")
│   ├── task-1 (XdString: "Initial Assessment")
│   ├── task-2 (XdString: "Order Lab Work")
│   └── task-3 (XdString: "Review Results")
├── phase-2 (Cluster: "Treatment Phase")
│   ├── task-4 (XdString: "Prescribe Medication")
│   ├── task-5 (XdString: "Administer Treatment")
│   └── monitoring (Cluster: "Monitoring Sub-Plan")
│       ├── check-1 (XdString: "4-Hour Vitals Check")
│       └── check-2 (XdString: "24-Hour Lab Recheck")
└── phase-3 (Cluster: "Discharge Phase")
    ├── task-6 (XdString: "Discharge Assessment")
    └── task-7 (XdString: "Follow-Up Scheduling")
```

The hierarchical nesting models task decomposition. Each level can have its own state tracking.

### 3.4 Hybrid Approach

Combines intrinsic workflow definition (Cluster) with an external engine reference (XdLink). Use this when the workflow definition travels with the data but execution is managed externally.

**Structure**:
```
workflow (Cluster: "Managed Workflow")
├── engine-ref (XdLink: URI to external BPMN engine)
├── process-id (XdString: "proc-12345")
├── states (Cluster: "Defined States")
│   ├── state-1 (XdString, fixed="Pending")
│   ├── state-2 (XdString, fixed="Processing")
│   └── state-3 (XdString, fixed="Complete")
└── transitions (Cluster: "Transition Rules")
    └── ... (same pattern as 3.1)
```

The XdLink provides a reference to the external engine for runtime orchestration, while the Cluster structure documents the expected states and transitions for validation and portability.

---

## 4. Conceptual Model

### State Machine Semantics

An SDC5 workflow state machine consists of:

1. **States**: A finite set of named conditions (XdString values with fixed enumerations).
2. **Transitions**: Directed edges between states (Clusters containing from/to/guard).
3. **Guard Conditions**: XPath boolean expressions that must be true for a transition to be valid.
4. **Assertions**: XSD 1.1 `xsd:assert` elements that enforce constraints at validation time.
5. **Current State**: The `current-state` element holding the active state value.

### Workflow Lifecycle

```
1. DM Schema Definition
   └── Define workflow Cluster with states and transitions
   └── Define xsd:assert constraints
   └── Set default value for current-state

2. Instance Creation
   └── current-state = default (e.g., "Draft")
   └── workflow Cluster populated with definitions

3. State Transition
   └── External process evaluates guard conditions
   └── Updates current-state value
   └── Adds Audit entry recording the transition

4. Instance Validation
   └── XSD 1.1 processor validates instance against schema
   └── xsd:assert expressions check current-state against valid values
   └── Rejects instances with invalid state values
```

### Intrinsic vs. Extrinsic Workflow

| Aspect | Intrinsic (ClusterType) | Extrinsic (external engine) |
|--------|------------------------|---------------------------|
| Definition location | Inside the DM instance | External system |
| Portability | Travels with data | Lost when data moves |
| Validation | XSD 1.1 assert | External engine rules |
| Execution | Requires external processor | Managed by engine |
| Auditability | Immutable in schema | Depends on engine |
| Complexity | Medium (Cluster patterns) | Unlimited (BPMN, etc.) |

SDC5 supports both approaches. The hybrid pattern (section 3.4) combines them.

---

## 5. Use Case Examples

### 5.1 Healthcare: Patient Encounter

**Scenario**: A patient encounter progresses through triage, examination, treatment, and discharge.

**States**: Registered, Triage, Examination, Treatment, Discharge, Complete

**Instance fragment**:
```xml
<dm-h7k2x xmlns:sdc5="https://semanticdatacharter.com/ns/sdc5/">
  <sdc5:dm-label>Patient Encounter</sdc5:dm-label>
  <sdc5:dm-language>en-US</sdc5:dm-language>
  <sdc5:dm-encoding>utf-8</sdc5:dm-encoding>
  <sdc5:current-state>Examination</sdc5:current-state>

  <!-- data Cluster with clinical observations -->
  <sdc5:ms-clj5x1g8f000008l09j7f6c3d>
    <!-- ... clinical data ... -->
  </sdc5:ms-clj5x1g8f000008l09j7f6c3d>

  <sdc5:workflow>
    <sdc5:label>Encounter Workflow</sdc5:label>
    <sdc5:ms-wf001>
      <sdc5:label>Valid States</sdc5:label>
      <sdc5:ms-st001><sdc5:xdstring-value>Registered</sdc5:xdstring-value></sdc5:ms-st001>
      <sdc5:ms-st002><sdc5:xdstring-value>Triage</sdc5:xdstring-value></sdc5:ms-st002>
      <sdc5:ms-st003><sdc5:xdstring-value>Examination</sdc5:xdstring-value></sdc5:ms-st003>
      <sdc5:ms-st004><sdc5:xdstring-value>Treatment</sdc5:xdstring-value></sdc5:ms-st004>
      <sdc5:ms-st005><sdc5:xdstring-value>Discharge</sdc5:xdstring-value></sdc5:ms-st005>
      <sdc5:ms-st006><sdc5:xdstring-value>Complete</sdc5:xdstring-value></sdc5:ms-st006>
    </sdc5:ms-wf001>
  </sdc5:workflow>
</dm-h7k2x>
```

**Assertions**:
```xml
<!-- Only valid encounter states -->
<xsd:assert test="current-state = 'Registered' or current-state = 'Triage'
                  or current-state = 'Examination' or current-state = 'Treatment'
                  or current-state = 'Discharge' or current-state = 'Complete'"
            xpathDefaultNamespace="##targetNamespace"/>

<!-- Complete encounters must have attestation -->
<xsd:assert test="not(current-state = 'Complete') or boolean(attestation)"
            xpathDefaultNamespace="##targetNamespace"/>
```

### 5.2 Government: Permit Application

**Scenario**: A building permit moves through application, review, inspection, and approval.

**States**: Submitted, Under Review, Inspection Scheduled, Inspection Complete, Approved, Denied

**Key assertions**:
```xml
<!-- Approved permits must have an inspector (provider) -->
<xsd:assert test="not(current-state = 'Approved') or count(provider) >= 1"
            xpathDefaultNamespace="##targetNamespace"/>

<!-- Cannot be approved without passing inspection -->
<xsd:assert test="not(current-state = 'Approved') or
                  (current-state = 'Approved' and boolean(attestation))"
            xpathDefaultNamespace="##targetNamespace"/>
```

### 5.3 Enterprise: Invoice Processing

**Scenario**: An invoice flows through receipt, validation, approval, and payment.

**States**: Received, Validated, Pending Approval, Approved, Rejected, Paid

**Key assertions**:
```xml
<!-- Paid invoices must have been approved first (enforced by workflow) -->
<!-- Rejected invoices cannot be paid -->
<xsd:assert test="current-state != 'Paid' or boolean(attestation)"
            xpathDefaultNamespace="##targetNamespace"/>
```

### 5.4 Research: Study Protocol

**Scenario**: A research data collection follows a study protocol with defined phases.

**Workflow structure**: Multi-step plan (section 3.3) with phases for enrollment, baseline assessment, intervention, follow-up, and closeout. The `protocol` element of DMType references the governing study protocol, while the `workflow` Cluster defines the specific data collection plan and its execution states.

---

## 6. Integration with Other DM Elements

The workflow elements work in concert with other DMType components:

### Audit

`DMType.audit` (unbounded `AuditType`) records state transition history:
- **When**: Audit timestamp marks the transition time.
- **Who**: Audit system-user identifies the actor.
- **What**: Audit description captures from-state and to-state.
- **How**: Audit system-id identifies the process or engine.

Recommended convention: One Audit entry per state transition.

### Attestation

`DMType.attestation` provides formal verification of data correctness. Combined with workflow:
- Assertions can **require** attestation at specific states (e.g., approval, completion).
- The attestation record includes who attested and when.
- Useful for compliance workflows requiring sign-off.

### Participation

`DMType.participations` identifies parties involved in the data's lifecycle. Combined with workflow:
- Different states may require different participants (e.g., reviewer for "Under Review").
- Assertions can require specific participation cardinality per state.

### Protocol

`DMType.protocol` (XdStringType) identifies the governing protocol or guideline. This is complementary to workflow:
- The protocol defines **why** certain steps exist.
- The workflow defines **what** steps exist and their sequencing.
- Both are stored in the DM instance.

### Access Control (acs)

`DMType.acs` (XdLinkType) references an external access control system. Combined with workflow:
- Different states may have different access control requirements.
- The acs reference can point to state-dependent access policies.

### Links

`DMType.links` (unbounded XdLink) provides ad-hoc relationships. Combined with workflow:
- Link to related DM instances that are part of the same process.
- Link to external workflow engine dashboards or monitoring.
- Link to supporting documents required at specific states.

---

## 7. Technology Stack

### XPath 2.0 (in XSD assertions)

XSD 1.1 mandates XPath 2.0 for `xsd:assert` expressions. Key capabilities:

- **String comparison**: `current-state = 'Draft'`
- **Boolean logic**: `not(...) or boolean(...)`
- **Cardinality**: `count(provider) >= 1`
- **Numeric comparison**: `xs:integer(//xdcount-value) > 7`
- **Existence testing**: `boolean(attestation)`
- **Conditional**: `if (...) then ... else ...`

### XPath 3.1 (runtime processing)

Available for external processors beyond schema validation:

- **Maps and arrays**: Complex data structure manipulation.
- **Arrow operator**: `$data => filter(...) => sort(...)`
- **Higher-order functions**: `for-each`, `filter`, `fold-left`

### XProc 3.0 (pipeline orchestration)

An XML pipeline language for defining multi-step processing:

- **Steps**: Atomic operations on XML documents.
- **Pipes**: Connect step outputs to step inputs.
- **Branching**: Conditional execution paths.
- **Iteration**: Process collections of documents.

XProc pipelines can consume SDC5 instances, evaluate workflow states, and produce updated instances with new state values.

### XSLT 3.0 (transformation)

For generating views, reports, or transformed outputs based on workflow state:

- Generate state-specific HTML views of the data.
- Transform instances for state transitions.
- Produce audit reports from workflow execution history.

### xsd:assert (schema validation)

The schema-level enforcement mechanism:

- Evaluated during XSD 1.1 validation.
- Boolean result: pass or fail.
- Multiple assertions per complex type.
- Context node is the element being validated.
- `xpathDefaultNamespace="##targetNamespace"` resolves element names.

---

## 8. Glossary

**Assert/Assertion**: An XSD 1.1 `<xsd:assert>` element containing an XPath 2.0 boolean expression that must evaluate to `true` for an instance to be valid.

**ClusterType**: The SDC5 RM complex type that provides the grouping structure for arbitrarily complex data hierarchies. Can contain nested Clusters and any Xd* type.

**Current State**: The `current-state` element of DMType, holding the active state value of the instance within its workflow.

**Guard Condition**: An XPath boolean expression that must be true for a state transition to be valid. Stored as XdString values within the workflow Cluster.

**Intrinsic Workflow**: Workflow definition embedded within the data instance itself (via the workflow Cluster), as opposed to extrinsic workflow managed by an external engine.

**Model Component (MC)**: A reusable, immutable building block within an SDC5 Data Model, defined as an `xsd:restriction` of an RM type and identified by a CUID2.

**Smart Packet**: An SDC5 data instance that carries its own workflow definition, state, and validation constraints, making it self-describing in both structure and behavior.

**State**: A named condition within a workflow state machine, represented as an XdString value within the workflow Cluster.

**State Machine**: A computational model consisting of a finite set of states, transitions between states, and conditions governing those transitions.

**Transition**: A directed edge between two states in the workflow, optionally governed by a guard condition.

**Workflow Cluster**: The ClusterType instance used as the `workflow` element of DMType, containing state definitions, transition rules, and optionally decision logic and plan structures.

**XPath**: W3C standard expression language for selecting nodes and computing values in XML documents. Version 2.0 is used in XSD assertions; version 3.1 is available for runtime processing.

**XProc**: W3C XML pipeline language for defining sequences of operations on XML documents.

**XSD 1.1**: The version of XML Schema Definition language that introduces `xsd:assert` for schema-level constraints using XPath expressions.

---

## References

- SDC5 Reference Model XSD: `sdc4/schemas/sdc5.xsd`
- SDC5 Specification: `sdc4/specification/sdc5-specification.md`
- Gap Analysis: `docs/WORKFLOW_RM_GAPS.md`
- W3C XML Schema 1.1: https://www.w3.org/TR/xmlschema11-1/
- W3C XPath 2.0: https://www.w3.org/TR/xpath20/
- W3C XPath 3.1: https://www.w3.org/TR/xpath-31/
- W3C XProc 3.0: https://spec.xproc.org/3.0/xproc/
- W3C XSLT 3.0: https://www.w3.org/TR/xslt-30/
- openEHR PROC: https://specifications.openehr.org/releases/PROC/development
- openEHR Entity: https://specifications.openehr.org/releases/RM/development/entity.html
