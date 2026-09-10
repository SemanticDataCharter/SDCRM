# SDC4 Architecture

This document provides a high-level overview of the Semantic Data Charter version 4 (SDC4) reference model architecture.

## Table of Contents

- [Architectural Principles](#architectural-principles)
- [Component Hierarchy](#component-hierarchy)
- [The Three Pillars](#the-three-pillars)
- [Type System](#type-system)
- [Extension Pattern](#extension-pattern)
- [Governance Layer](#governance-layer)
- [Semantic Layer](#semantic-layer)
- [Quality Layer](#quality-layer)

---

## Architectural Principles

### 1. XSD as Normative Source

**`sdc4.xsd` is the source of truth** for all structural definitions.

```
┌─────────────────────────────────────────┐
│  sdc4.xsd (XSD Schema)                  │  ← NORMATIVE
│  Defines structure, constraints         │
│  Machine-readable, executable           │
└──────────────────┬──────────────────────┘
                   │
                   ├──→ Specification (markdown)    [Descriptive]
                   ├──→ OWL ontologies              [Semantic layer]
                   ├──→ Examples                    [Usage demos]
                   └──→ Tools                       [Implementations]
```

### 2. Restriction-Only Extension

All data models **must use XSD restriction**, never extension:

```xml
<!-- ✅ CORRECT: Restriction -->
<xs:restriction base="sdc:XdStringType">
  <xs:minLength value="1"/>
  <xs:maxLength value="100"/>
</xs:restriction>

<!-- ❌ WRONG: Extension -->
<xs:extension base="sdc:XdStringType">
  <xs:attribute name="customAttr"/>
</xs:extension>
```

**Why?**
- Ensures conformance to reference model
- Maintains validation integrity
- Enables universal tooling
- Guarantees semantic consistency

### 3. Semantic Enrichment via Links

Semantics added through **links**, not structure:

```xml
<PatientName xsi:type="XdStringType">
  <label>Patient Full Name</label>
  <data>Jane Doe</data>
  <links>
    <meaning>http://hl7.org/fhir/StructureDefinition/Patient#name</meaning>
  </links>
  <audit>...</audit>
</PatientName>
```

### 4. Explicit Quality Management

Data quality is **explicit**, not implicit:

```xml
<!-- Missing data is explicit -->
<BloodType xsi:type="XdStringType">
  <label>Blood Type</label>
  <data/>  <!-- Empty -->
  <exceptionValue>unknown</exceptionValue>  <!-- Why empty -->
  <audit>...</audit>
</BloodType>
```

---

## Component Hierarchy

### Base Type: XdAnyType

All SDC4 types inherit from `XdAnyType`:

```
XdAnyType (abstract)
├── label: string (required)
├── audit: AuditType (required)
├── links: LinksType (optional)
├── exceptionValue: string (optional)
└── [type-specific components]
```

### Inheritance Tree

```
XdAnyType
├── XdStringType
├── XdBooleanType
├── XdTemporalType
├── XdLinkType
├── XdFileType
├── XdQuantifiedType (abstract)
│   ├── XdCountType
│   ├── XdQuantityType
│   ├── XdOrdinalType
│   └── XdIntervalType
└── XdListType (abstract)
    ├── XdStringList
    ├── XdBooleanList
    ├── XdFileList
    ├── XdLinkList
    ├── XdOrdinalList
    ├── XdDecimalList
    ├── XdIntegerList
    └── XdTemporalList
```

### Component Categories

1. **Simple Types** - Single values
   - XdStringType, XdBooleanType, XdTemporalType

2. **Reference Types** - Links and files
   - XdLinkType, XdFileType

3. **Quantified Types** - Measurements
   - XdCountType, XdQuantityType, XdOrdinalType, XdIntervalType

4. **List Types** - Multiple values
   - Non-quantified: XdStringList, XdBooleanList, etc.
   - Quantified: XdDecimalList, XdIntegerList, XdTemporalList

---

## The Three Pillars

### Pillar 1: Enforce Governance

Every data element includes **audit trail**:

```xml
<audit>
  <createdBy>user-id</createdBy>
  <createdOn>2025-11-02T10:00:00Z</createdOn>
  <rationale>Why this data exists</rationale>
  <versionInfo>Optional version details</versionInfo>
  <attestation>Optional attestation info</attestation>
</audit>
```

**Governance Components**:
- **Who**: `createdBy` (required)
- **When**: `createdOn` (required)
- **Why**: `rationale` (optional but recommended)
- **Where**: `location` (optional)
- **How**: `method` (optional)

### Pillar 2: Embed Meaning

Every element can link to **ontologies and vocabularies**:

```xml
<links>
  <meaning>http://purl.obolibrary.org/obo/NCIT_C42614</meaning>
  <media>http://example.org/icon.png</media>
  <terminology>
    <system>http://snomed.info/sct</system>
    <code>363787002</code>
    <display>Observable entity</display>
  </terminology>
</links>
```

**Semantic Integration**:
- **Ontology links** - URIs to concepts
- **Terminology bindings** - Coded values (SNOMED, LOINC, etc.)
- **Media links** - Icons, images, representations
- **Documentation** - Human-readable references

### Pillar 3: Mandate Quality

Explicit handling of **data quality and exceptional values**:

```xml
<!-- Type 1: Data present -->
<Temperature xsi:type="XdQuantityType">
  <magnitude>37.2</magnitude>
  <units>°C</units>
  <normalStatus>normal</normalStatus>
</Temperature>

<!-- Type 2: Data missing (known reason) -->
<Temperature xsi:type="XdQuantityType">
  <magnitude/>
  <exceptionValue>not-measured</exceptionValue>
</Temperature>

<!-- Type 3: Data uncertain -->
<Temperature xsi:type="XdQuantityType">
  <magnitude>37.2</magnitude>
  <magnitudeStatus>approximate</magnitudeStatus>
  <error>0.5</error>
</Temperature>
```

**Quality Components**:
- **Exception values** - unknown, masked, not-applicable, etc.
- **Normal status** - normal, abnormal, warning, critical
- **Magnitude status** - =, <, >, ≤, ≥, approximate
- **Error margins** - Precision and accuracy
- **Normal ranges** - Expected value ranges

---

## Type System

### Simple Types

**XdStringType** - Text data
```xml
<Name xsi:type="XdStringType">
  <label>Full Name</label>
  <data>Jane Doe</data>
  <audit>...</audit>
</Name>
```

**XdBooleanType** - True/false
```xml
<IsActive xsi:type="XdBooleanType">
  <label>Active Status</label>
  <data>true</data>
  <audit>...</audit>
</XdBooleanType>
```

**XdTemporalType** - Dates/times
```xml
<BirthDate xsi:type="XdTemporalType">
  <label>Date of Birth</label>
  <data>1985-03-15</data>
  <temporalType>date</temporalType>
  <audit>...</audit>
</XdTemporalType>
```

### Quantified Types

**XdCountType** - Countable quantities
```xml
<ItemCount xsi:type="XdCountType">
  <label>Number of Items</label>
  <magnitude>42</magnitude>
  <audit>...</audit>
</XdCountType>
```

**XdQuantityType** - Measurements with units
```xml
<Weight xsi:type="XdQuantityType">
  <label>Patient Weight</label>
  <magnitude>70.5</magnitude>
  <units>kg</units>
  <magnitudeStatus>exact</magnitudeStatus>
  <audit>...</audit>
</XdQuantityType>
```

### List Types

**Non-Quantified Lists** - Simple value collections
```xml
<Tags xsi:type="XdStringList">
  <label>Product Tags</label>
  <items>
    <item>electronics</item>
    <item>wireless</item>
    <item>audio</item>
  </items>
  <audit>...</audit>
</XdStringList>
```

**Quantified Lists** - Measurement collections
```xml
<Temperatures xsi:type="XdDecimalList">
  <label>Daily Temperatures</label>
  <units>°C</units>
  <items>
    <item>36.5</item>
    <item>36.8</item>
    <item>37.1</item>
  </items>
  <audit>...</audit>
</XdDecimalList>
```

---

## Extension Pattern

### Creating Domain Models

Domain-specific models created via **XSD restriction**:

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:sdc="https://semanticdatacharter.com/ns/sdc4/">

  <!-- Import SDC4 reference model -->
  <xs:import namespace="https://semanticdatacharter.com/ns/sdc4/"
             schemaLocation="sdc4.xsd"/>

  <!-- Define domain model by restricting SDC4 types -->
  <xs:element name="PatientRecord">
    <xs:complexType>
      <xs:sequence>

        <!-- Patient name: restrict XdStringType -->
        <xs:element name="PatientName">
          <xs:complexType>
            <xs:complexContent>
              <xs:restriction base="sdc:XdStringType">
                <xs:sequence>
                  <!-- Require label, data, audit -->
                  <xs:element ref="sdc:label"/>
                  <xs:element ref="sdc:data"/>
                  <xs:element ref="sdc:audit"/>
                </xs:sequence>
              </xs:restriction>
            </xs:complexContent>
          </xs:complexType>
        </xs:element>

        <!-- Additional elements... -->

      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
```

### Cluster-Based Organization

Complex models organized using **Clusters**:

```xml
<PatientRecord>
  <Demographics>  <!-- Cluster -->
    <PatientName xsi:type="XdStringType">...</PatientName>
    <DateOfBirth xsi:type="XdTemporalType">...</DateOfBirth>
  </Demographics>

  <VitalSigns>  <!-- Cluster -->
    <Temperature xsi:type="XdQuantityType">...</Temperature>
    <BloodPressure>  <!-- Nested cluster -->
      <Systolic xsi:type="XdQuantityType">...</Systolic>
      <Diastolic xsi:type="XdQuantityType">...</Diastolic>
    </BloodPressure>
  </VitalSigns>
</PatientRecord>
```

**Cluster Benefits**:
- Logical grouping
- Hierarchical organization
- Reusable components
- Clear structure

---

## Governance Layer

### Audit Trail Components

```
AuditType
├── createdBy: string (required)      # User/system identifier
├── createdOn: dateTime (required)    # ISO 8601 timestamp
├── rationale: string (optional)      # Why this data exists
├── location: string (optional)       # Where created/captured
├── method: string (optional)         # How created/measured
├── versionInfo: string (optional)    # Version tracking
└── attestation: AttestationType      # Digital signatures, etc.
```

### Provenance Tracking

```xml
<audit>
  <createdBy>lab-system-01</createdBy>
  <createdOn>2025-11-02T14:30:00Z</createdOn>
  <rationale>Routine blood test</rationale>
  <location>Lab Room 3B</location>
  <method>Automated analyzer XYZ-1000</method>
  <attestation>
    <signature>Digital signature here</signature>
    <attestedBy>dr-smith-001</attestedBy>
  </attestation>
</audit>
```

---

## Semantic Layer

### OWL Ontology Structure

`sdc4.owl` provides semantic definitions:

- **Classes** - Concepts for each XSD type
- **Properties** - Relationships between concepts
- **Restrictions** - Semantic constraints
- **Annotations** - Human-readable descriptions

### RDF Integration

SDC4 data can be exported to RDF:

```turtle
@prefix sdc: <https://semanticdatacharter.com/ns/sdc4/> .
@prefix ex: <http://example.org/patient/> .

ex:patient123 a sdc:PatientRecord ;
    sdc:hasName [
        a sdc:XdString ;
        sdc:label "Patient Full Name" ;
        sdc:data "Jane Doe" ;
        sdc:createdBy "registration-clerk" ;
        sdc:createdOn "2025-11-02T10:00:00Z"^^xsd:dateTime
    ] .
```

---

## Quality Layer

### Exception Value Taxonomy

```
Exception Values
├── unknown              # Value exists but unknown
├── not-applicable       # Question doesn't apply
├── not-measured         # Measurement not taken
├── not-asked            # Question not asked
├── masked               # Value hidden for privacy
├── not-specified        # Deliberately not specified
└── [domain-specific]    # Custom exception types
```

### Normal Status Indicators

```
Normal Status
├── normal        # Within expected range
├── abnormal      # Outside normal range
├── warning       # Concerning but not critical
├── critical      # Requires immediate attention
└── unknown       # Normal status not determined
```

### Magnitude Status

For quantified types:

```
Magnitude Status
├── =             # Exact value
├── <             # Less than
├── >             # Greater than
├── ≤             # Less than or equal
├── ≥             # Greater than or equal
└── approximate   # Approximate value
```

---

## Design Patterns

### Pattern 1: Required Data

```xml
<Element xsi:type="XdStringType">
  <label>Required Field</label>
  <data>Actual value</data>
  <audit>...</audit>
</Element>
```

### Pattern 2: Optional Data (Present)

```xml
<Element xsi:type="XdStringType">
  <label>Optional Field</label>
  <data>Provided value</data>
  <audit>...</audit>
</Element>
```

### Pattern 3: Optional Data (Missing)

```xml
<Element xsi:type="XdStringType">
  <label>Optional Field</label>
  <data/>
  <exceptionValue>not-applicable</exceptionValue>
  <audit>...</audit>
</Element>
```

### Pattern 4: Measured Value with Accuracy

```xml
<Element xsi:type="XdQuantityType">
  <label>Measured Value</label>
  <magnitude>37.2</magnitude>
  <units>°C</units>
  <magnitudeStatus>exact</magnitudeStatus>
  <error>0.1</error>  <!-- ±0.1 -->
  <accuracy>99</accuracy>  <!-- 99% accuracy -->
  <audit>...</audit>
</Element>
```

---

## Standards Compliance

SDC4 architecture builds on W3C standards:

- **XSD 1.1** - Schema validation
- **RDF** - Semantic triples
- **OWL 2** - Ontology definitions
- **SPARQL** - Query language

Additional standards:

- **ISO 8601** - Date/time formats
- **UCUM** - Units of measure
- **BCP 47** - Language tags
- **XML Namespaces** - URI-based namespacing

---

## References

- [SDC4 Specification](../sdc4/specification/sdc4-specification.md)
- [Core Types](../sdc4/specification/core-types.md)
- [Examples](../sdc4/examples/)
- [CLAUDE.md](../CLAUDE.md) - Contributor guidance

---

**SDC4 architecture balances simplicity, expressiveness, and rigor.**
