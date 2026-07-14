# **Semantic Data Charter (SDC) Specification**

## **Version 4.0.0 - October 20, 2025**

**This version:**

* https://semanticdatacharter.com/spec/sdc4/

**Editors:**

* Timothy W. Cook, Axius-SDC, Inc.

Copyright © 2025 Axius-SDC, Inc.

## **Abstract**

The Semantic Data Charter (SDC) is a framework for creating semantically rich, machine-readable, and interoperable data models. It provides a set of principles and a reference model for defining data with clear, unambiguous meaning, ensuring that data is not only structured but also self-describing. This specification details the SDC Reference Model (RM), the core data types, and provides guidance on creating domain-specific data models.

## **1\. Introduction**

In an increasingly data-driven world, the ability to share, understand, and reuse data across different systems and domains is paramount. Traditional data modeling approaches often focus on data structure, leaving meaning implicit and open to misinterpretation. The Semantic Data Charter addresses this challenge by providing a framework for creating data models that are both structurally sound and semantically explicit.  
The SDC is founded on three core pillars:

* **Enforce Governance:** Establish a formal, machine-readable contract for your data.  
* **Embed Meaning:** Link your data to a universal business vocabulary.  
* **Mandate Quality:** Formally define rules for handling imperfect data.

This specification provides the technical details of the SDC Reference Model, which is implemented in XML Schema (XSD) and OWL (Web Ontology Language).

### **1.1. Notational Conventions**

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

The **normative** artifact of SDC4 is the reference model schema `sdc4.xsd`; this document *describes* it. Where this document and the schema disagree, the schema governs. Material marked *informative*, including the modeling examples (Section 5) and the mapping, decision-tree, and best-practice material in Appendix A, illustrates usage and adds no conformance requirements.

## 

## **2\. Standards Compliance and Enabling**

SDC4 is built upon and leverages established open standards from the World Wide Web Consortium (W3C) to ensure broad interoperability, machine readability, and semantic richness. It is designed not to replace existing domain-specific standards but to provide a foundational, unifying layer that enhances their capabilities, particularly in areas of data governance, semantic grounding, and data quality.

### **2.1. Foundational W3C Standards**

SDC4 directly utilizes and aligns with the following core W3C standards:

* **XML Schema (XSD):** The structural backbone of SDC4. All SDC Reference Models and derived Data Models are defined using XSD, providing a robust, widely understood mechanism for defining data structures, data types, and constraints. This ensures broad tool support and validation capabilities.  
* **Resource Description Framework (RDF):** SDC4's approach to embedding semantic meaning is fully compatible with RDF. The explicit labeling of model components, linked to universal business vocabularies, allows for easy transformation of SDC4 data into RDF triples, making it queryable via SPARQL and integrable into knowledge graphs.  
* **Web Ontology Language (OWL):** The semantic models underlying SDC4, particularly the universal business vocabulary and relationships between concepts, are expressible in OWL. This enables powerful reasoning, consistency checking, and automated semantic integration.  
* **SPARQL Protocol and RDF Query Language (SPARQL):** Because SDC4 data can be readily mapped to RDF, it becomes queryable using SPARQL, allowing for complex federated queries across diverse datasets that share an SDC4 foundation, regardless of their original domain-specific standard.

### **2.2. Enabling Industry-Specific Standards**

SDC4 acts as a "standard for standards," providing a meta-framework that complements and enhances existing industry data standards by addressing common challenges that often fall outside their primary scope of defining specific data elements. By adopting SDC4, organizations can bring a consistent approach to data governance, semantic clarity, and quality assurance *across* different standards they may use.  
Key areas where SDC4 enables and strengthens industry standards include:

* **Healthcare (e.g., HL7 FHIR):** While FHIR defines clinical data resources, SDC4 can standardize the governance and provenance metadata *around* FHIR resources, and provide a consistent mechanism for describing data quality issues (e.g., using ExceptionalValue types to explicitly tag why a FHIR element might be missing or invalid, rather than relying on implicit nulls).  
* **Financial Services (e.g., ISO 20022, ACORD):** ISO 20022 defines financial messages, and ACORD focuses on insurance. SDC4 can provide a common semantic layer that links elements from these standards to a unified enterprise business vocabulary. It also formalizes data quality rules and governance for the exchange of these messages.  
* **Privacy Regulations (e.g., PIPEDA, GDPR, CCPA):** SDC4's granular XdAnyType includes access control tags (act) and robust provenance. This allows for explicit, machine-readable declaration of data sensitivity, consent information, and data lineage directly within the data model, simplifying compliance with complex privacy regulations.  
* **Regulatory Reporting (e.g., SEC EDGAR, XBRL):** XBRL provides a language for tagging financial data. SDC4 can ensure the underlying factual data being tagged is semantically unambiguous and includes robust quality and governance metadata, improving the reliability and auditability of regulatory submissions.

By providing a consistent, machine-readable framework for governance, semantics, and quality across these diverse domains, SDC4 reduces integration friction, improves data trustworthiness, and allows for more sophisticated data analytics and AI applications across an enterprise's entire data landscape.

## 

## **3\. Conformance**

Conformance is defined against three targets: a Data Model, an instance, and a processor.

### **3.1. Conformant Data Model**

An XML Schema is a **conformant SDC4 Data Model** if and only if:

- it defines its components solely by `xsd:restriction` of the SDC4 reference model types, and **MUST NOT** use `xsd:extension` to add elements or attributes to any SDC4 type;
- it is itself a valid XSD 1.1 schema; and
- every component it defines resolves, through a chain of restrictions, to a reference-model type.

A conformant Data Model can be checked mechanically against the reference model (for example, with the `sdcvalidator` schema-compliance check).

### **3.2. Conformant Instance**

An XML document is a **conformant SDC4 instance** if and only if:

- it validates against a conformant SDC4 Data Model (Section 3.1); and
- it carries an `instance_id` (a CUID2), which is **REQUIRED** on every instance.

Instances conform to their Data Model schema, not to `sdc4.xsd` directly.

### **3.3. Conformant Processor**

Software is a **conformant SDC4 processor** to the extent that it preserves the guarantees above: it **MUST** reject a Data Model that applies `xsd:extension` to an SDC4 type, **MUST** treat `sdc4.xsd` as normative where documentation and schema disagree, and **MUST NOT** silently discard `ExceptionalValue`, provenance, or identity elements when reading, transforming, or emitting instances.

### **3.4. Principles Conformance**

Beyond the mechanical targets above, an organization's data practices conform to the SDC principles when they uphold the three pillars, governance, meaning, and quality, described in this specification.

## 

## **4\. Architecture**

The SDC architecture is composed of the following key components:

* **Reference Model (RM):** A set of core data types and structures that serve as the building blocks for all SDC-compliant data models. The RM is defined in sdc4.xsd and sdc4.ttl.  
* **Data Models (DMs):** Domain-specific models created by constraining the components of the Reference Model.  
* **Model Components (MCs):** The individual building blocks within a Data Model, derived from the RM components.  
* **Semantic Annotations:** Metadata embedded within the data models that provide context and meaning, linking the data to ontologies and controlled vocabularies.

### **4.1. Core Data Types**

The SDC Reference Model provides a rich set of extended data types (Xd\* types) that go beyond the standard XML Schema data types. The complete set, with its inheritance, is given in Appendix A (see A.14 for the hierarchy). The datatypes are:

* **Base and abstract:** XdAnyType (the base of every Xd\* type), and the abstract intermediates XdOrderedType (ordering and reference ranges) and XdQuantifiedType (units and magnitude metadata).
* **Textual:** XdStringType, XdTokenType.
* **Boolean:** XdBooleanType.
* **Numeric (quantified):** XdCountType, XdQuantityType, XdFloatType, XdDoubleType.
* **Ordinal:** XdOrdinalType.
* **Temporal:** XdTemporalType.
* **Link:** XdLinkType.
* **File:** XdFileType.
* **Interval and reference range:** XdIntervalType, ReferenceRangeType.
* **List types (8):** XdBooleanListType, XdStringListType, XdTokenListType, XdDecimalListType, XdDoubleListType, XdIntegerListType, XdNonNegativeIntegerListType, XdPositiveIntegerListType.

The **structural** components that assemble these into a Data Model, ItemType, ClusterType, and XdAdapterType, are described in Appendix A.18; the DMType instance root is detailed in Section 4.3.1.

### 

### **4.2. Governance and Provenance Components**

The SDC Reference Model includes a comprehensive set of components for capturing data governance, provenance, and audit information directly within the data model.

#### 

#### **4.2.1. Governance**

Governance components define the actors, roles, and responsibilities associated with the data.

* **PartyType**: An actor involved with the data (person, organization, device, or software). Elements: `party-name` (string), `party-ref` (an XdLink to an external identity), and `party-details` (a Cluster for structured detail).  
* **ParticipationType**: The role a party plays in an activity. Elements: `performer` (a Party), `function` and `mode` (XdString), and `start`/`end` (dateTime).  
* **AttestationType**: A formal attestation of the data's content. Elements: `view` and `proof` (XdFile), `reason` (XdString), `committer` (a Party), `committed` (dateTime), and `pending` (boolean).  
* **AuditType**: An audit-trail entry for one system or user interaction. Elements: `system-id` (XdString), `system-user` (a Party), `location` (a Cluster), and `timestamp` (dateTime).  
* **Access Control**: The model supports linking to external access control systems via the acs element and allows for fine-grained control via the act (Access Control Tag) element.

#### 

#### **4.2.2. Provenance**

Provenance components provide a complete history of the data's origin, creation, and modification.

* **Instance Metadata**: The root DMType contains key provenance fields: instance\_id (mandatory, CUID2), instance\_version, source\_instance\_id, source\_version\_id, creation\_timestamp, subject, and provider.  
* **Temporal Validity**: Every data element (XdAnyType) contains optional timestamp fields to track its lifecycle: vtb (Valid Time Begin), vte (Valid Time End), tr (Time Recorded), and modified.
* **Spatial Context**: Every data element (XdAnyType) may also carry optional `latitude` and `longitude` (decimal, constrained to ±90 and ±180 respectively), locating the datum in space at the point of capture. Together with the temporal fields this gives every element optional spatio-temporal context.

### 

### **4.3. The Data Model (DM) Wrapper and Semantic Grounding**

A critical distinction exists between the metadata for a *data instance* and the metadata for the *data model definition* itself. The SDC architecture addresses both.

#### 

#### **4.3.1. The DMType as an Instance Wrapper**

The DMType serves as the root element for every SDC data instance. Its primary role is to be a container for the data payload and the provenance and governance metadata of that *specific instance*. The elements within the DMType describe the "who, what, when, and where" of the data payload itself, not the abstract model it conforms to.

**Complete DMType Element Listing:**

| Element | Type | Cardinality | Description |
|---------|------|-------------|-------------|
| dm-label | xsd:string | 1..1 | Descriptive name of this data model. Provides the semantic 'name' for the model. |
| dm-language | xsd:language | 1..1 | Mandatory indicator of the localized language (RFC 3066). |
| dm-encoding | xsd:string | 1..1 | Character set encoding. Default is utf-8. |
| creation\_timestamp | xsd:dateTime | 0..1 | Run-time timestamp indicating when this data instance was created. |
| instance\_id | xsd:string | 1..1 | Mandatory, globally unique identifier for this data instance (CUID2). |
| instance\_version | xsd:string | 0..1 | Version identifier for this data instance. |
| source\_instance\_id | xsd:string | 0..1 | Identifier of this data instance in the originating source system (e.g., Epic, SAP). Enables auditable data lineage across system boundaries. |
| source\_version\_id | xsd:string | 0..1 | Version identifier from the originating source system. Paired with source\_instance\_id, provides a complete reference to the exact upstream version ingested. |
| current-state | xsd:string | 0..1 | The current state according to the workflow defined in the workflow element. |
| Item (ref) | ItemType | 1..1 | The data payload: an element in the `Item` substitution group (a `ClusterType` or `XdAdapterType`). In an instance this is the concrete `ms-<CUID2>` element that substitutes for `Item`. |
| subject | PartyType | 0..1 | Identity of the human subject of the data (patient, customer, etc.). |
| provider | PartyType | 0..* | Source of the information (clinician, device, software, etc.). |
| participations | ParticipationType (ref) | 0..* | Other participations in the data activity. |
| protocol | XdStringType | 0..1 | External identifier of the protocol used when collecting the data. |
| workflow | ClusterType | 0..1 | Workflow definition for this data model, containing state definitions, transitions, and execution logic. |
| acs | XdLinkType | 0..1 | Identifier of an externally held access control system. |
| audit | AuditType (ref) | 0..* | Audit trail entries from systems that have interacted with the data. |
| attestation | AttestationType | 0..1 | Attestation record verifying the data instance. |
| links | XdLinkType (ref) | 0..* | Optional links to other locatable structures or external entities. |

#### **4.3.1.1. Workflow and State Machine Capabilities**

The `current-state`, `workflow`, and `xsd:assert` elements work together to give every SDC4 data instance the ability to carry its own state machine definition. This creates a **smart packet** — a data instance that embeds its own behavioral rules alongside its structural definition.

**current-state**: Holds the active state value of the instance. At the RM level, this is an unrestricted `xsd:string` to allow each Data Model to define its own state vocabulary. Valid values are constrained per-DM using `xsd:assert` elements in the generated schema.

**workflow**: Typed as `ClusterType`, this element can contain arbitrarily complex workflow definitions using nested Clusters and any Xd\* type. Common patterns include:

* **State definitions**: XdString elements with fixed values listing valid states.
* **Transition rules**: Nested Clusters containing from-state, to-state, and guard conditions.
* **Hierarchical plans**: Nested Cluster trees for multi-phase workflows.
* **External engine references**: XdLink elements pointing to external BPMN or workflow engines.

**xsd:assert**: XSD 1.1 assertions placed within the DM's complexType definition enforce state constraints at schema validation time. Assertions use XPath 2.0 expressions evaluated against the DM instance.

Example — a DM with workflow state validation:

```xml
<dm-h7k2x xmlns:sdc4="https://semanticdatacharter.com/ns/sdc4/">
  <sdc4:dm-label>Patient Intake</sdc4:dm-label>
  <sdc4:dm-language>en-US</sdc4:dm-language>
  <sdc4:dm-encoding>utf-8</sdc4:dm-encoding>
  <sdc4:current-state>Triage</sdc4:current-state>
  <sdc4:ms-clj5x1g8f000008l09j7f6c3d>
    <!-- data payload -->
  </sdc4:ms-clj5x1g8f000008l09j7f6c3d>
  <sdc4:workflow>
    <sdc4:label>Intake Workflow</sdc4:label>
    <!-- Cluster containing state and transition definitions -->
  </sdc4:workflow>
</dm-h7k2x>
```

For comprehensive guidance on workflow patterns, see the **Workflow & State Machine Guide** (`sdc4/guides/workflow-state-machine.md`).

####

#### **4.3.2. Semantic Grounding of the Data Model Definition**

The semantic meaning and descriptive metadata of the *data model definition* (i.e., the schema) are established separately. This is where semantic vocabularies like Dublin Core are properly applied. This definition-level metadata is typically embedded directly within the schema files (e.g., using xsd:appinfo and RDF annotations in the XSD) or maintained in an external metadata registry.

### 

### **4.4. Model Component Reusability and Immutability**

A cornerstone of the SDC architecture is the ability to create reusable and immutable Model Components (MCs). This is achieved through a specific pattern of schema definition.  
When a domain-specific structure is needed, it is defined by creating a new xsd:complexType that restricts a base type from the SDC Reference Model (e.g., sdc4:ClusterType). This new complexType is given a unique and permanent name using a Collision-Resistant Unique Identifier (CUID2), prefixed with mc-, such as mc-clj5x1g8f000008l09j7f6c3d.  
To incorporate this component into a Data Model, an xsd:element is declared with a corresponding ms- prefixed name, assigned the mc-\<CUID2\> type, and placed into the xsd:substitutionGroup of a generic element from the Reference Model (e.g., sdc4:Item).  
This mechanism provides three key advantages:

1. **Immutability and Reuse**: The mc-\<CUID2\> component can be imported and reused across multiple Data Models.  
2. **Consistent Querying**: An application can reliably query for all instances of the ms-clj5x1g8f000008l09j7f6c3d element, knowing it will always find the same structure.  
3. **Separation of Structure and Semantics**: This pattern decouples the immutable physical structure from its semantic meaning. The mc-\<CUID2\> and ms-\<CUID2\> define the structure, while the label element within that component's schema definition is *fixed* to provide the specific, immutable business context (e.g., fixed="Systolic").

### 

### **4.5. Data Longevity and Migration Avoidance**

A significant challenge in traditional data management is the need for costly, complex, and error-prone data migrations when underlying schemas evolve or applications are replaced. The SDC4 architecture is designed to address this issue at its core and promote data longevity.  
The combination of:

1. **A Stable Reference Model:** Providing a consistent set of base types and structural patterns.  
2. **Immutable Structural Components:** Using CUIDs (mc-\<cuid\> and ms-\<cuid\>) to define reusable data structures whose physical shape is guaranteed not to change.  
3. **Explicit, Decoupled Semantics:** Embedding the meaning via fixed label elements and optional RDF annotations, rather than relying on structural element names.

means that data created according to an SDC4 Data Model remains inherently understandable and processable over time.  
New applications or future versions of existing applications can interpret historical SDC4 data because:

* The **structure** associated with a given ms-\<cuid\> is permanently defined by its corresponding mc-\<cuid\> restriction in the schema.  
* The **meaning** of that structure is explicitly stated by the fixed label (and potentially richer RDF annotations) within that schema definition.

Unlike traditional approaches, which often break backward compatibility and require data transformation when element names or nesting structures change, SDC4 isolates structural definition from semantic interpretation. As long as the SDC Reference Model remains stable and the CUIDs persist, the data remains usable. This significantly reduces or potentially eliminates the need for large-scale data migrations, lowering long-term data management costs and preserving the value of historical data assets.

## 

## 

### **4.6. Identifiers and Federated Resolvability**

SDC4 identifies every model component and every data instance with a **CUID2**, a collision-resistant identifier that can be minted offline, with no central registry and no coordination between parties. This gives SDC identity three properties at once: it is **federated** (parties who have never met assign identifiers independently without collision), **permanent** (an identifier, once assigned, never changes), and **resolvable** (each identifier maps to a typed, dereferenceable URI).

**Identifier forms.**

- **Instance identity.** Every instance carries an `instance_id` (**REQUIRED**, a CUID2). Optional `instance_version`, `source_instance_id`, and `source_version_id` (Section 4.3.1) record versioning and lineage back to an originating system.
- **Component identity.** A reusable Model Component type is named `mc-<CUID2>`, the element that carries it is named `ms-<CUID2>`, and a Data Model root is named `dm-<CUID2>` (Section 4.4). These names are permanent: the structure bound to a given `ms-<CUID2>` never changes (Section 4.5).

**Typed, resolvable namespace.** Reference-model and model URIs live under a versioned namespace, `https://semanticdatacharter.com/ns/sdc4/`, served over HTTP so that a processor can dereference a schema or component URI directly. Because the namespace is versioned (`.../ns/sdc4/`, and in future `.../ns/sdc5/`), successor reference models are published *alongside* their predecessors, not on top of them.

**Permanence across reference-model versions.** When a new reference model is released it is published at a new versioned namespace; the previous namespace and every schema under it continue to resolve and validate unchanged. An SDC4 package therefore keeps working after SDC5 deploys: its identifiers still resolve, and its instances still validate against the SDC4 schema they were built against. The identifier and namespace resolve an element's *meaning* globally; access to the *data* itself remains governed separately through the access-control elements (`acs`, `act`; Section 4.2.1).

## **5\. Modeling Examples**

***Note:*** *The following XML snippets are instance documents. They are based on data model schemas where CUID-named elements (ms-... and dm-...) define the data structure. The semantic meaning, such as "Blood Pressure" or "Systolic", is not present in the instance-label element; instead, it is a fixed attribute in the schema definition of the corresponding component, as described in Section 4.4.*

### 

### **5.1. Healthcare**

**Use Case:** Modeling a patient's vital signs. The dm- and ms- elements are non-semantic structural identifiers.  
\<dm-h7k2x... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Patient Vitals\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>  
      
    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
            \<sdc4:xdquantity-value\>120\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>mmHg\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4e\>  
            \<sdc4:xdquantity-value\>80\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>mmHg\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4e\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-h7k2x...\>

### 

### 

### 

### **5.2. Agriculture**

**Use Case:** Tracking soil moisture levels.  
\<dm-a4g9y... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Soil Moisture Reading\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>

    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4f\>  
            \<sdc4:xdquantity-value\>35.5\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>%\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4f\>  
        \<sdc4:ms-clj5x3a9b000208l0e5f6g7h8\>  
            \<sdc4:xdtemporal-datetime\>2025-09-27T14:30:00Z\</sdc4:xdtemporal-datetime\>  
        \</sdc4:ms-clj5x3a9b000208l0e5f6g7h8\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-a4g9y...\>

### **5.3. Business**

**Use Case:** Representing a customer order.  
\<dm-b8f3z... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Customer Order\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>  
      
    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
            \<sdc4:xdstring-value\>ORD-2025-12345\</sdc4:xdstring-value\>  
        \</sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
            \<sdc4:xdquantity-value\>199.99\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>USD\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-b8f3z...\>

### **5.4. Finance**

**Use Case:** Modeling a stock trade.  
\<dm-f1d6w... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Stock Trade\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>  
      
    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
            \<sdc4:xdstring-value\>AXS\</sdc4:xdstring-value\>  
        \</sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
        \<sdc4:ms-clj5y5e2d000408l0m1n2o3p4\>  
            \<sdc4:xdcount-value\>100\</sdc4:xdcount-value\>  
            \<sdc4:xdcount-units\>  
               \<sdc4:xdstring-value\>shares\</sdc4:xdstring-value\>  
            \</sdc4:xdcount-units\>  
        \</sdc4:ms-clj5y5e2d000408l0m1n2o3p4\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
            \<sdc4:xdquantity-value\>50.25\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
               \<sdc4:xdstring-value\>USD\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4d\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-f1d6w...\>

### **5.5. Threat & Fraud Detection**

**Use Case:** Logging a suspicious login attempt.  
\<dm-t5c2v... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Suspicious Login Attempt\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>

    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
            \<sdc4:xdstring-value\>198.51.100.1\</sdc4:xdstring-value\>  
        \</sdc4:ms-clj5x4b1c000308l0i9j8k7l6\>  
        \<sdc4:ms-clj5x3a9b000208l0e5f6g7h8\>  
            \<sdc4:xdtemporal-datetime\>2025-09-27T18:00:00Z\</sdc4:xdtemporal-datetime\>  
        \</sdc4:ms-clj5x3a9b000208l0e5f6g7h8\>  
         \<sdc4:ms-clj5x4b1c000308l0i9j8k7l7\>  
            \<sdc4:xdstring-value\>Multiple failed attempts\</sdc4:xdstring-value\>  
        \</sdc4:ms-clj5x4b1c000308l0i9j8k7l7\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-t5c2v...\>

### **5.6. Aerospace**

**Use Case:** Recording telemetry from a satellite.  
\<dm-s9p8q... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Satellite Telemetry\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>  
      
    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4f\>  
            \<sdc4:xdquantity-value\>400\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>km\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4f\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4g\>  
            \<sdc4:xdquantity-value\>-10.5\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>C\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4g\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-s9p8q...\>

### **5.7. Engineering**

**Use Case:** Defining the specifications for a mechanical part.  
\<dm-e3n7m... xmlns:sdc4="\[https://semanticdatacharter.com/ns/sdc4/\](https://semanticdatacharter.com/ns/sdc4/)"\>  
    \<sdc4:dm-label\>Mechanical Part Specification\</sdc4:dm-label\>  
    \<sdc4:dm-language\>en-US\</sdc4:dm-language\>  
    \<sdc4:dm-encoding\>UTF-8\</sdc4:dm-encoding\>

    \<sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4h\>  
            \<sdc4:xdquantity-value\>50\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>mm\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4h\>  
        \<sdc4:ms-clj5x2p4k000108l01a2b3c4i\>  
            \<sdc4:xdquantity-value\>10\</sdc4:xdquantity-value\>  
            \<sdc4:xdquantity-units\>  
                \<sdc4:xdstring-value\>mm\</sdc4:xdstring-value\>  
            \</sdc4:xdquantity-units\>  
        \</sdc4:ms-clj5x2p4k000108l01a2b3c4i\>  
    \</sdc4:ms-clj5x1g8f000008l09j7f6c3d\>  
\</dm-e3n7m...\>

## **6\. Security Considerations**

Implementers of the Semantic Data Charter should be aware of the following security considerations:

* **Data Privacy:** When modeling data that contains personally identifiable information (PII), care must be taken to ensure compliance with relevant privacy regulations (e.g., GDPR, HIPAA).
* **Access Control:** The act (Access Control Tag) element in XdAnyType should be used to enforce access control policies.
* **Data Integrity:** The hash-result and hash-function elements in XdFileType can be used to verify the integrity of binary data.

## **Appendix A: Xd* Type Reference and Standard Datatype Mappings**

This appendix provides a comprehensive reference for all SDC4 extended data types (Xd* types), their corresponding Type classes, mappings to standard database and programming language datatypes, available constraints, and usage guidance.

### **A.1. Overview**

SDC4 provides semantically rich extended data types that enhance basic data values with governance, provenance, and constraint information. Each Xd* type consists of:

- **Value or Parts**: A scalar type carries its data in a type-prefixed value element (e.g., `xdstring-value`, `xdcount-value`); a structured type carries semantically-named parts instead (see the naming convention below)
- **Type Class**: The corresponding complexType definition (e.g., `XdStringType`, `XdCountType`)
- **Constraint Capabilities**: Available validation rules specific to the type
- **Metadata Support**: Inherited from `XdAnyType` (label, access control, temporal and spatial validity, and exceptional values)

**Element Naming Convention.** A *single-value* (scalar) Xd type exposes its payload with a type-prefixed name, `xd<type>-value` (for example `xdstring-value`, `xdcount-value`, `xdquantity-value`), plus the modifiers `xd<type>-units` and `xd<type>-language` where applicable. A *structured* Xd type, one whose parts each carry their own distinct meaning, names those parts semantically instead, because there is no single payload value: `XdBoolean` uses a `true-value`/`false-value` choice; `XdOrdinal` uses `ordinal` and `symbol`; `XdLink` uses `link`, `relation`, and `relation-uri`; `XdFile` uses `size`, `media-type`, `uri`/`media-content`, and related metadata; `XdInterval` uses `lower`, `upper`, and the boundary flags. In short: scalar types carry a typed `-value`; structured types carry semantically-named parts. Do not apply an `xd<type>-` prefix to a structured type's elements.

### **A.2. Textual Data Types**

#### **A.2.1. XdString / XdStringType**

**Purpose**: General-purpose character string data with rich constraint support.

**Standard Datatype Mappings**:
- SQL: `VARCHAR`, `TEXT`, `CHAR`, `NVARCHAR`, `CLOB`
- JSON/JavaScript: `string`
- Python: `str`
- Java: `String`
- C#: `string`

**Available Constraints**:
- `min_length`: Minimum string length (integer)
- `max_length`: Maximum string length (integer)
- `exact_length`: Fixed string length (integer)
- `regex_pattern`: Regular expression pattern for validation
- `enumeration`: List of allowed values (controlled vocabulary)

**Use Cases**:
- Free-text fields (names, addresses, descriptions)
- Formatted strings (email, phone, postal codes) using regex patterns
- Controlled vocabularies using enumeration constraints
- Customer IDs, order numbers, SKUs

**Example Schema Definition**:
```xml
<xsd:complexType name="mc-email-address">
  <xsd:complexContent>
    <xsd:restriction base="sdc4:XdStringType">
      <xsd:sequence>
        <xsd:element name="label" type="xsd:string" fixed="Email Address"/>
        <xsd:element name="xdstring-value">
          <xsd:simpleType>
            <xsd:restriction base="xsd:string">
              <xsd:pattern value="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"/>
            </xsd:restriction>
          </xsd:simpleType>
        </xsd:element>
      </xsd:sequence>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

**When to Use**: Any textual data that doesn't require numeric calculations.

---

#### **A.2.2. XdToken / XdTokenType**

**Purpose**: Normalized whitespace string for machine-readable identifiers and codes.

**Standard Datatype Mappings**:
- SQL: `VARCHAR` (with normalized whitespace)
- JSON/JavaScript: `string`
- Python: `str`
- XML Schema: `xsd:token` (collapses whitespace, trims leading/trailing)

**Available Constraints**:
- Same as XdString (length constraints, patterns, enumeration)
- Automatic whitespace normalization

**Use Cases**:
- Machine-readable codes (ISO codes, medical codes, product codes)
- Standardized identifiers where whitespace variations should be ignored
- API tokens, authentication codes

**When to Use**: Choose XdToken over XdString when whitespace normalization is desired (e.g., codes that should ignore extra spaces).

---

### **A.3. Boolean Data Types**

#### **A.3.1. XdBoolean / XdBooleanType**

**Purpose**: True/false logical values with semantic labeling.

**Standard Datatype Mappings**:
- SQL: `BOOLEAN`, `BIT`, `TINYINT(1)`
- JSON/JavaScript: `boolean`
- Python: `bool`
- Java: `Boolean`, `boolean`
- C#: `bool`, `Boolean`

**Available Constraints**:
- Default value specification
- Required/optional flags

**Use Cases**:
- Yes/no questions
- Feature toggles, flags, switches
- Consent indicators (GDPR, medical consent)
- Status indicators (active/inactive, enabled/disabled)

**Structure**: `XdBooleanType` records its value through an `xsd:choice` of `true-value` and `false-value` (both `xsd:string`). Exactly one is present in an instance; the element that appears indicates the state, and its content is the enumerated option label defined in the Data Model (for example "Yes"/"No" or "Granted"/"Denied"). This forces the value into one of the two carefully-defined options rather than an implicit boolean.

**Example Instance**:
```xml
<sdc4:ms-consent-given>
  <sdc4:label>Patient Consent Given</sdc4:label>
  <sdc4:true-value>Granted</sdc4:true-value>
</sdc4:ms-consent-given>
```

**When to Use**: Binary states, logical conditions, yes/no decisions.

---

### **A.4. Numeric Data Types**

SDC4's numeric types, `XdCount`, `XdQuantity`, `XdFloat`, and `XdDouble`, all extend `XdQuantifiedType`, which adds an optional units element and measurement-quality metadata to the value.

**Quantified metadata (shared by all four numeric types via `XdQuantifiedType`):**

- `magnitude-status` (`MagnitudeStatus`): how the recorded magnitude relates to the true value, one of `equal`, `less_than`, `greater_than`, `less_than_or_equal`, `greater_than_or_equal`, or `approximate` (for example, a reading recorded as "less than 140").
- `accuracy_margin` (`xsd:decimal`): the accuracy margin of the measurement.
- `precision_digits` (`xsd:nonNegativeInteger`): the number of significant digits of precision.

#### **A.4.1. XdCount / XdCountType**

**Purpose**: Non-negative integer counts with optional units.

**Standard Datatype Mappings**:
- SQL: `INTEGER`, `BIGINT`, `SMALLINT`, `INT` (with CHECK >= 0)
- JSON/JavaScript: `number` (integer)
- Python: `int` (>= 0)
- Java: `Integer`, `Long` (>= 0)

**Available Constraints**:
- `min_value`: Minimum count (>= 0)
- `max_value`: Maximum count
- `units`: Required units specification (e.g., "items", "people", "shares")

**Use Cases**:
- Item quantities in inventory
- Number of people, animals, objects
- Event counts, occurrence counts
- Share counts in financial trading

**Example**:
```xml
<sdc4:ms-share-quantity>
  <sdc4:label>Number of Shares</sdc4:label>
  <sdc4:xdcount-value>100</sdc4:xdcount-value>
  <sdc4:xdcount-units>
    <sdc4:xdstring-value>shares</sdc4:xdstring-value>
  </sdc4:xdcount-units>
</sdc4:ms-share-quantity>
```

**When to Use**: Non-negative integers representing counts or quantities. Unlike XdQuantity, XdCount values are always whole numbers.

---

#### **A.4.2. XdQuantity / XdQuantityType**

**Purpose**: Decimal numeric values with required units of measure (physical quantities).

**Standard Datatype Mappings**:
- SQL: `DECIMAL`, `NUMERIC`, `MONEY`
- JSON/JavaScript: `number`
- Python: `Decimal`, `float`
- Java: `BigDecimal`, `Double`

**Available Constraints**:
- `min_value`: Minimum allowed value
- `max_value`: Maximum allowed value
- `precision`: Total number of significant digits
- `scale`: Number of decimal places
- `units`: **Required** units specification (e.g., "mmHg", "kg", "USD")

**Use Cases**:
- Physical measurements (blood pressure, temperature, weight, distance)
- Financial amounts (currency values with currency code as unit)
- Scientific measurements (chemical concentrations, power, energy)
- Any decimal value requiring units

**Example**:
```xml
<sdc4:ms-systolic-bp>
  <sdc4:label>Systolic Blood Pressure</sdc4:label>
  <sdc4:xdquantity-value>120</sdc4:xdquantity-value>
  <sdc4:xdquantity-units>
    <sdc4:xdstring-value>mmHg</sdc4:xdstring-value>
  </sdc4:xdquantity-units>
</sdc4:ms-systolic-bp>
```

**When to Use**: Any numeric value that represents a physical quantity and requires units. This is the most common quantified numeric type.

---

#### **A.4.3. XdFloat / XdFloatType**

**Purpose**: Single-precision floating-point numbers (IEEE 754).

**Standard Datatype Mappings**:
- SQL: `REAL`, `FLOAT(24)`
- JSON/JavaScript: `number`
- Python: `float`
- Java: `Float`, `float`
- C#: `float`, `Single`

**Available Constraints**:
- `min_value`: Minimum allowed value
- `max_value`: Maximum allowed value

**Use Cases**:
- Scientific calculations requiring floating-point representation
- Graphics and gaming coordinates
- Signal processing values
- Performance metrics where precision beyond 7 significant digits is not required

**When to Use**: Prefer XdFloat when single-precision (32-bit) floating-point is sufficient and memory efficiency is important.

---

#### **A.4.4. XdDouble / XdDoubleType**

**Purpose**: Double-precision floating-point numbers (IEEE 754).

**Standard Datatype Mappings**:
- SQL: `DOUBLE PRECISION`, `FLOAT`, `FLOAT(53)`
- JSON/JavaScript: `number`
- Python: `float`
- Java: `Double`, `double`
- C#: `double`, `Double`

**Available Constraints**:
- `min_value`: Minimum allowed value
- `max_value`: Maximum allowed value

**Use Cases**:
- High-precision scientific calculations
- Astronomical calculations
- Financial calculations requiring high precision
- Geographic coordinates (latitude/longitude)

**When to Use**: Use XdDouble when double-precision (64-bit) floating-point is required for accuracy. For financial data, consider XdQuantity with DECIMAL type instead to avoid floating-point rounding issues.

---

### **A.5. Temporal Data Types**

#### **A.5.1. XdTemporal / XdTemporalType**

**Purpose**: Flexible temporal data supporting various granularities (date, time, datetime, partial dates).

**Standard Datatype Mappings**:
- SQL: `DATE`, `TIME`, `TIMESTAMP`, `DATETIME`, `TIMESTAMPTZ`
- JSON/JavaScript: `string` (ISO 8601 format)
- Python: `datetime.date`, `datetime.time`, `datetime.datetime`
- Java: `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`

**Available Constraints**:
- `min_value`: Earliest allowed date/time
- `max_value`: Latest allowed date/time
- `granularity`: Precision level (year, month, day, hour, minute, second)
- Timezone handling (with or without timezone)

**Supported Formats**:
- Full datetime: `2025-11-09T15:30:00Z`
- Date only: `2025-11-09`
- Time only: `15:30:00`
- Partial date (year-month): `2025-11`
- Year only: `2025`

**Use Cases**:
- Event timestamps
- Birth dates, expiration dates
- Appointment times
- Measurement timestamps
- Historical dates (with partial date support)

**Example**:
```xml
<sdc4:ms-measurement-time>
  <sdc4:label>Measurement Timestamp</sdc4:label>
  <sdc4:xdtemporal-datetime>2025-11-09T14:30:00Z</sdc4:xdtemporal-datetime>
</sdc4:ms-measurement-time>
```

**When to Use**: Any temporal data. XdTemporal's flexibility allows it to represent full timestamps, dates only, times only, or partial dates depending on data requirements.

---

### **A.6. Enumerated and Ordinal Data Types**

#### **A.6.1. XdOrdinal / XdOrdinalType**

**Purpose**: Ordered categorical values with semantic labels and numeric codes.

**Standard Datatype Mappings**:
- SQL: `SMALLINT` or `VARCHAR` with lookup table
- JSON/JavaScript: `number` or `string`
- Python: `int` or `str` (often using `Enum`)
- Java: `Enum`

**Available Constraints**:
- Defined set of allowed ordinal values (label + code pairs)
- Order preservation (codes represent meaningful ordering)

**Use Cases**:
- Severity levels (mild=1, moderate=2, severe=3)
- Priority rankings (low=1, medium=2, high=3)
- Educational levels (elementary=1, high school=2, college=3)
- Likert scales (strongly disagree=1, disagree=2, neutral=3, agree=4, strongly agree=5)

**Structure**: `XdOrdinalType` has two required children: `ordinal` (`xsd:decimal`, the ordered numeric code) and `symbol` (`xsd:string`, the display label for that code). As an ordered type it also inherits the optional `normal-status` and one or more `ReferenceRange` elements from `XdOrderedType` (see the Reference Ranges section).

**Example**:
```xml
<sdc4:ms-pain-level>
  <sdc4:label>Pain Severity</sdc4:label>
  <sdc4:ordinal>2</sdc4:ordinal>
  <sdc4:symbol>Moderate</sdc4:symbol>
</sdc4:ms-pain-level>
```

**When to Use**: Use XdOrdinal when categories have a meaningful order. For unordered categories (e.g., colors, countries), use XdString with enumeration constraint.

---

### **A.7. Reference and Link Types**

#### **A.7.1. XdLink / XdLinkType**

**Purpose**: References to other data models, external resources, or relationships.

**Standard Datatype Mappings**:
- SQL: `VARCHAR` (for URIs), foreign key references
- JSON/JavaScript: `string` (URI/URL), object reference
- Python: Foreign key, URI string
- Java: `URI`, `URL`, reference

**Available Constraints**:
- URI format validation
- Allowed target types
- Relationship semantics

**Use Cases**:
- References between data models (e.g., Patient → Encounter)
- External document links
- Ontology concept URIs
- API endpoint references
- Hyperlinks to related resources

**Structure**: `XdLinkType` has three children: `link` (`xsd:anyURI`, optional, the target address), `relation` (`xsd:string`, required, the human-readable relationship term), and `relation-uri` (`xsd:anyURI`, optional, a URI that formally defines the relation's semantics).

**Example**:
```xml
<sdc4:ms-patient-reference>
  <sdc4:label>Related Patient</sdc4:label>
  <sdc4:link>dm-patient-clj5x9z...</sdc4:link>
  <sdc4:relation>subject_of</sdc4:relation>
  <sdc4:relation-uri>http://purl.org/dc/terms/subject</sdc4:relation-uri>
</sdc4:ms-patient-reference>
```

**When to Use**: Any reference to another entity, document, or resource. XdLink provides semantic relationship information beyond simple foreign keys.

---

### **A.8. Binary Data Types**

#### **A.8.1. XdFile / XdFileType**

**Purpose**: Binary data or file references with metadata and integrity checking.

**Standard Datatype Mappings**:
- SQL: `BLOB`, `BYTEA`, `VARBINARY`, `VARCHAR` (for file paths)
- JSON/JavaScript: Base64 encoded string, file path
- Python: `bytes`, file path string
- Java: `byte[]`, `File`, `Path`

**Available Constraints**:
- File size limits (`max_size`)
- Allowed MIME types (`media_type`)
- Hash algorithm specification (`hash_function`)
- Storage location (embedded vs. referenced)

**Metadata Included** (all optional; the content is a required choice):
- `media-type` — MIME type
- `size` — size in bytes
- `encoding` — character encoding
- `compression-type` — compression algorithm, if compressed
- `hash-result` and `hash-function` — integrity hash and its algorithm
- `formalism`, `xdfile-language`, `alt-txt` — content formalism, language, and alternate text
- Content is an `xsd:choice` of `uri` (external reference) or `media-content` (embedded `xsd:base64Binary`)

**Use Cases**:
- Document attachments (PDFs, Word docs, spreadsheets)
- Images (JPEG, PNG, DICOM medical images)
- Audio/video files
- Encrypted files with hash verification
- Archived data

**Example** (elements follow the schema sequence order):
```xml
<sdc4:ms-patient-photo>
  <sdc4:label>Patient Photograph</sdc4:label>
  <sdc4:size>245760</sdc4:size>
  <sdc4:media-type>image/jpeg</sdc4:media-type>
  <sdc4:hash-result>a3f5b...</sdc4:hash-result>
  <sdc4:hash-function>SHA-256</sdc4:hash-function>
  <sdc4:uri>file:///patient-photos/12345.jpg</sdc4:uri>
</sdc4:ms-patient-photo>
```

**When to Use**: Binary data storage or file references. XdFile supports both embedded base64-encoded data and external file references with integrity verification.

---

### **A.9. Interval and Range Types**

#### **A.9.1. XdInterval / XdIntervalType**

**Purpose**: Ranges or intervals with upper and lower bounds.

**Standard Datatype Mappings**:
- SQL: Two columns (lower_bound, upper_bound), or `RANGE` types (PostgreSQL)
- JSON/JavaScript: Object with `min` and `max` properties
- Python: Tuple, custom Range class
- Java: Custom Range class

**Structure**: `XdIntervalType` is a single type; there are no per-datatype interval subtypes. The `lower` and `upper` boundaries are of type `InvlType`, an `xsd:choice` that carries the boundary value in the appropriate datatype element: `invl-int`, `invl-decimal`, `invl-float`, `invl-double`, `invl-date`, `invl-time`, `invl-dateTime`, or `invl-duration`. In a Data Model this choice is constrained to one datatype, and an XSD 1.1 assertion enforces that `lower` and `upper` use the same one. Four booleans describe the boundaries: `lower_included` / `upper_included` (inclusive vs exclusive) and `lower_bounded` / `upper_bounded` (set `false` for an open, unbounded end). Optional `interval-units` carries units as a `units-name` and `units-uri` pair.

**Use Cases**:
- Normal ranges (e.g., normal blood pressure: 90-120 mmHg)
- Age ranges (18-65 years)
- Date ranges (event start to end)
- Acceptable value ranges for validation
- Quantity ranges (price ranges, measurement ranges)

**Example** (a decimal interval, 90 to 120 mmHg, both bounds inclusive):
```xml
<sdc4:ms-normal-systolic-range>
  <sdc4:label>Normal Systolic BP Range</sdc4:label>
  <sdc4:lower>
    <sdc4:invl-decimal>90</sdc4:invl-decimal>
  </sdc4:lower>
  <sdc4:upper>
    <sdc4:invl-decimal>120</sdc4:invl-decimal>
  </sdc4:upper>
  <sdc4:lower_included>true</sdc4:lower_included>
  <sdc4:upper_included>true</sdc4:upper_included>
  <sdc4:lower_bounded>true</sdc4:lower_bounded>
  <sdc4:upper_bounded>true</sdc4:upper_bounded>
  <sdc4:interval-units>
    <sdc4:units-name>mmHg</sdc4:units-name>
    <sdc4:units-uri>http://unitsofmeasure.org/ucum#mm[Hg]</sdc4:units-uri>
  </sdc4:interval-units>
</sdc4:ms-normal-systolic-range>
```

**When to Use**: Any data representing a range of values. XdInterval types provide semantic meaning for lower/upper bounds and can express inclusive/exclusive boundaries.

---

### **A.9.2. Reference Ranges (ReferenceRangeType)**

Reference ranges attach named, context-sensitive value ranges to any *ordered* datatype (XdOrdinal, XdCount, XdQuantity, XdFloat, XdDouble, XdTemporal). They express meaningful bands, normal, critical, therapeutic, dangerous, and so on, each defined by an interval and sensitive to context such as sex, age, or location.

Every `XdOrderedType` (the abstract base of the ordered datatypes) carries two optional children for this:

- `ReferenceRange` (0..unbounded): one or more named ranges. `ReferenceRange` is a substitution-group member of `XdAny`, so it also carries `XdAnyType` metadata such as `label`.
- `normal-status` (`xsd:string`, 0..1): the status of the instance value relative to those ranges.

A `ReferenceRangeType` has three required children:

- `definition` (`xsd:string`): the meaning of the range, for example `normal`, `critical`, or `therapeutic`.
- `interval` (`XdIntervalType`): the value range (see A.9.1).
- `is-normal` (`xsd:boolean`, default `false`): `true` if values in this range are considered normal in the context of `definition`.

Because each range carries its own interval (with its own `interval-units`), a single ordered element can hold several ranges expressed in different unit systems, for example a temperature range in Celsius and another in Fahrenheit.

**Example** (a normal systolic blood-pressure range):
```xml
<sdc4:ReferenceRange>
  <sdc4:label>Normal Range</sdc4:label>
  <sdc4:definition>normal</sdc4:definition>
  <sdc4:interval>
    <sdc4:lower><sdc4:invl-decimal>90</sdc4:invl-decimal></sdc4:lower>
    <sdc4:upper><sdc4:invl-decimal>120</sdc4:invl-decimal></sdc4:upper>
    <sdc4:lower_included>true</sdc4:lower_included>
    <sdc4:upper_included>true</sdc4:upper_included>
    <sdc4:lower_bounded>true</sdc4:lower_bounded>
    <sdc4:upper_bounded>true</sdc4:upper_bounded>
    <sdc4:interval-units>
      <sdc4:units-name>mmHg</sdc4:units-name>
      <sdc4:units-uri>http://unitsofmeasure.org/ucum#mm[Hg]</sdc4:units-uri>
    </sdc4:interval-units>
  </sdc4:interval>
  <sdc4:is-normal>true</sdc4:is-normal>
</sdc4:ReferenceRange>
```

---

### **A.10. Type Selection Decision Tree**

*(Informative.)* Moved to a guide: see [`sdc4/guides/type-selection.md`](../guides/type-selection.md) for the datatype decision tree.

---

### **A.11. Constraint Summary by Type**

| **Xd* Type** | **Length** | **Value Range** | **Format/Pattern** | **Enumeration** | **Units** | **Other** |
|--------------|------------|-----------------|-------------------|-----------------|-----------|-----------|
| XdString     | ✓          | -               | ✓ (regex)          | ✓               | -         | -         |
| XdToken      | ✓          | -               | ✓ (regex)          | ✓               | -         | Whitespace normalization |
| XdBoolean    | -          | -               | -                 | -               | -         | Default value |
| XdCount      | -          | ✓ (min/max)     | -                 | -               | ✓         | Non-negative integers |
| XdQuantity   | -          | ✓ (min/max)     | -                 | -               | ✓ (required) | Precision, scale |
| XdFloat      | -          | ✓ (min/max)     | -                 | -               | ✓         | IEEE 754 single |
| XdDouble     | -          | ✓ (min/max)     | -                 | -               | ✓         | IEEE 754 double |
| XdTemporal   | -          | ✓ (min/max)     | ✓ (ISO 8601)       | -               | -         | Granularity, timezone |
| XdOrdinal    | -          | ✓ (defined set) | -                 | ✓ (ordered)     | -         | Code + label pairs |
| XdLink       | -          | -               | ✓ (URI)            | ✓ (target types) | -         | Relationship semantics |
| XdFile       | ✓ (size)   | -               | ✓ (MIME type)      | -               | -         | Hash, compression |
| XdInterval   | -          | ✓ (bounds)      | -                 | -               | ✓ (optional) | Inclusive/exclusive, bounded/unbounded |

---

### **A.12. Common Datatype Mapping Examples**

*(Informative.)* Moved to a guide: see [`sdc4/guides/datatype-mapping.md`](../guides/datatype-mapping.md) for CSV, SQL, and cross-language mappings to Xd\* types.

---

### **A.13. Best Practices**

*(Informative.)* Moved to a guide: see [`sdc4/guides/best-practices.md`](../guides/best-practices.md) for SDC4 modeling best practices.

---

### **A.14. Xd* Type Inheritance Hierarchy**

```
XdAnyType (base type - provides label, access control, temporal + spatial metadata, exceptional values)
├── XdStringType
├── XdTokenType
├── XdBooleanType
├── XdOrderedType (abstract - ordering semantics, reference ranges)
│   ├── XdOrdinalType
│   └── XdQuantifiedType (abstract - units, magnitude status)
│       ├── XdCountType
│       ├── XdQuantityType
│       ├── XdFloatType
│       ├── XdDoubleType
│       ├── XdDecimalListType
│       ├── XdDoubleListType
│       ├── XdIntegerListType
│       ├── XdNonNegativeIntegerListType
│       └── XdPositiveIntegerListType
├── XdTemporalType
├── XdLinkType
├── XdFileType
├── XdIntervalType
├── ReferenceRangeType
├── XdBooleanListType
├── XdStringListType
└── XdTokenListType

ExceptionalValueType (abstract, standalone - 16 ISO 21090 null-flavor subtypes:
    NIType, MSKType, INVType, DERType, UNCType, OTHType, NINFType, PINFType,
    UNKType, ASKRType, NASKType, QSType, TRCType, ASKUType, NAVType, NAType)
```

**Key Points**:
- All types inherit governance and provenance metadata from `XdAnyType`
- **Quantified types** (XdCount, XdQuantity, XdFloat, XdDouble) inherit from `XdQuantifiedType` and require units
- **Interval types** provide range semantics for their corresponding base types

---

This appendix serves as the authoritative reference for Xd* type selection and usage in SDC4 data modeling.

## 

## 

## 

## 

### **A.15. Exceptional Values (ExceptionalValueType)**

Data quality, the third SDC pillar, is handled explicitly rather than with implicit nulls. Every SDC element (through `XdAnyType`) may carry zero or more `ExceptionalValue` elements. Their presence flags that the element's value is missing, masked, or otherwise outside the normal measurable range, **and records why**. In SDC terms, NULL is not an answer: the reason is stated, not left implicit.

`ExceptionalValueType` is an abstract base with a single `ev-name` element (a short descriptive phrase). The reference model defines sixteen concrete subtypes, each an ISO 21090-aligned null flavor that fixes `ev-name` to a specific value. A Data Model restricts `ExceptionalValue` to the subtype(s) it permits, and may add further domain-specific `ExceptionalValueType` restrictions.

| Subtype | ev-name | Meaning |
|---------|---------|---------|
| `NIType` | No Information | Value is exceptional (missing, omitted, incomplete, improper); no information. |
| `MSKType` | Masked | Information exists but was withheld (for example, for privacy). |
| `INVType` | Invalid | The represented value is not a member of the permitted set. |
| `DERType` | Derived | An actual value must be derived from the provided information. |
| `UNCType` | Unencoded | The information was not encoded; only the raw source is present. |
| `OTHType` | Other | The actual value is not among the permitted data values. |
| `NINFType` | Negative Infinity | Negative infinity. |
| `PINFType` | Positive Infinity | Positive infinity. |
| `UNKType` | Unknown | A proper value applies but is not known. |
| `ASKRType` | Asked and Refused | Information was sought but refused. |
| `NASKType` | Not Asked | The information was not sought. |
| `QSType` | Sufficient Quantity | The exact quantity is unknown but known to be non-zero and sufficient. |
| `TRCType` | Trace | Greater or less than zero, but too small to quantify. |
| `ASKUType` | Asked but Unknown | Information was sought but not found. |
| `NAVType` | Not Available | Not available; the specific reason is unknown. |
| `NAType` | Not Applicable | No proper value applies in this context. |

**Example** (an element whose value is unknown; the Data Model has restricted `ExceptionalValue` to `UNKType`, which fixes `ev-name`):
```xml
<sdc4:ms-patient-weight>
  <sdc4:label>Patient Weight</sdc4:label>
  <sdc4:ExceptionalValue>
    <sdc4:ev-name>Unknown</sdc4:ev-name>
  </sdc4:ExceptionalValue>
</sdc4:ms-patient-weight>
```

---

### **A.16. List Types**

SDC provides list datatypes for whitespace-delimited sequences of primitive values, for the efficient storage and transmission of many related values in one field. Each `Xd<Type>ListType` adds a single value element, `xd<type>list-value`, typed as the corresponding `*ListSimpleType` (an `xsd:list` of the item type), and carries the standard `XdAnyType` metadata such as `label`. They split by base type: the **non-quantified** lists (`XdBooleanListType`, `XdStringListType`, `XdTokenListType`) extend `XdAnyType`; the **quantified** lists (`XdDecimalListType`, `XdDoubleListType`, `XdIntegerListType`, `XdNonNegativeIntegerListType`, `XdPositiveIntegerListType`) extend `XdQuantifiedType`, and so additionally carry units and magnitude metadata.

| Type | Value element | Item type |
|------|---------------|-----------|
| `XdBooleanListType` | `xdbooleanlist-value` | `xsd:boolean` |
| `XdStringListType` | `xdstringlist-value` | `xsd:string` |
| `XdTokenListType` | `xdtokenlist-value` | `xsd:token` |
| `XdDecimalListType` | `xddecimallist-value` | `xsd:decimal` |
| `XdDoubleListType` | `xddoublelist-value` | `xsd:double` |
| `XdIntegerListType` | `xdintegerlist-value` | `xsd:integer` |
| `XdNonNegativeIntegerListType` | `xdnonnegativeintegerlist-value` | `xsd:nonNegativeInteger` |
| `XdPositiveIntegerListType` | `xdpositiveintegerlist-value` | `xsd:positiveInteger` |

**Example**:
```xml
<sdc4:ms-daily-counts>
  <sdc4:label>Daily Counts</sdc4:label>
  <sdc4:xdintegerlist-value>12 15 9 20 7</sdc4:xdintegerlist-value>
</sdc4:ms-daily-counts>
```

---

### **A.17. Simple Types**

Beyond the complex Xd* types, the reference model defines eleven named simple types used as element datatypes:

- **`lattype`** and **`lontype`** — decimal restrictions for the spatial coordinates on `XdAnyType`: latitude constrained to `[-90.000000, 90.000000]` and longitude to `[-180.000000, 180.000000]`.
- **`MagnitudeStatus`** — the enumeration used by `XdQuantifiedType`'s `magnitude-status`, indicating how a recorded magnitude relates to the true value: `equal`, `less_than`, `greater_than`, `less_than_or_equal`, `greater_than_or_equal`, `approximate`.
- **The eight `*ListSimpleType`s** — the `xsd:list` types backing the List datatypes (A.16): `BooleanListSimpleType`, `StringListSimpleType`, `TokenListSimpleType`, `DecimalListSimpleType`, `DoubleListSimpleType`, `IntegerListSimpleType`, `NonNegativeIntegerListSimpleType`, and `PositiveIntegerListSimpleType`, each a whitespace-delimited list of its item type.

---

### **A.18. Structural Components**

These Item-family components assemble the datatypes above into a Data Model. They are defined by `xsd:restriction` of the reference-model types using the `mc-<CUID2>` / `ms-<CUID2>` pattern (Section 4.4); the DMType instance root is also detailed in Section 4.3.1.

* **DMType**: The mandatory root element type for any SDC instance document. It acts as a wrapper for the data payload and contains instance-specific metadata.  
  **Data Model Schema Example:** This example defines the root element for a "Patient Vitals" Data Model. It restricts the base DMType, fixes the dm-label to provide the model's semantic name, and specifies that the main data payload will be a specific "Vitals Cluster" component.  
  \<xsd:complexType name="mc-h7k2x..."\>  
    \<xsd:complexContent\>  
      \<xsd:restriction base="sdc4:DMType"\>  
        \<xsd:sequence\>  
          \<xsd:element name="dm-label" type="xsd:string" fixed="Patient Vitals"/\>  
          \<xsd:element name="dm-language" type="xsd:language" fixed="en-US"/\>  
          \<xsd:element name="dm-encoding" type="xsd:string" fixed="UTF-8"/\>  
          ...  
          \<\!-- The root item for this DM is a specific cluster \--\>  
          \<xsd:element ref="sdc4:ms-clj5x1g8f000008l09j7f6c3d"/\>  
          ...  
        \</xsd:sequence\>  
      \</xsd:restriction\>  
    \</xsd:complexContent\>  
  \</xsd:complexType\>

* **ItemType**: An abstract type that serves as the base for ClusterType and XdAdapterType. It is not used directly but enables polymorphism in the model.  
* **ClusterType**: A container component used to group other ItemType elements (either other clusters or adapters). This allows for the creation of arbitrarily complex hierarchical data structures.  
  **Data Model Schema Example:** This defines a reusable "Blood Pressure" cluster. It contains references to two adapted quantity components, one for systolic and one for diastolic pressure. The label is fixed, making the semantics of this structure immutable.  
  \<xsd:complexType name="mc-clj5x1g8f000008l09j7f6c3d"\>  
    \<xsd:complexContent\>  
      \<xsd:restriction base="sdc4:ClusterType"\>  
        \<xsd:sequence\>  
          \<xsd:element name="label" type="xsd:string" fixed="Blood Pressure" /\>  
          \<\!-- Reference to the adapter for the Systolic component \--\>  
          \<xsd:element ref="sdc4:ms-..." minOccurs="1" maxOccurs="1" /\>  
          \<\!-- Reference to the adapter for the Diastolic component \--\>  
          \<xsd:element ref="sdc4:ms-..." minOccurs="1" maxOccurs="1" /\>  
        \</xsd:sequence\>  
      \</xsd:restriction\>  
    \</xsd:complexContent\>  
  \</xsd:complexType\>

* **XdAdapterType**: A "leaf" node in a ClusterType structure. It acts as a wrapper that holds a single data-typed component (XdAnyType), adapting it for inclusion in a cluster's item list.  
  **Data Model Schema Example:** This defines an adapter for the "Systolic" component. It restricts XdAdapterType and specifies that it must contain exactly one ms-... element that represents the systolic blood pressure value.  
  \<xsd:complexType name="mc-lyp1zhdjr31il1qdhvhs828k"\>  
    \<xsd:complexContent\>  
      \<xsd:restriction base="sdc4:XdAdapterType"\>  
        \<xsd:sequence\>  
          \<\!-- The adapter holds a single reference to the data component \--\>  
          \<xsd:element ref="sdc4:ms-clj5x2p4k000108l01a2b3c4d"/\>  
        \</xsd:sequence\>  
      \</xsd:restriction\>  
    \</xsd:complexContent\>  
  \</xsd:complexType\>

The same `xsd:restriction` pattern shown above applies to every Xd\* datatype; see A.2 through A.17 for each type's structure and constraints.
