# Getting Started with SDC5

Welcome to SDC5! This guide will help you understand and start using the Semantic Data Charter.

## What is SDC5?

SDC5 (Semantic Data Charter version 4) is a framework for creating **semantically rich, interoperable data models**. It provides:

- **Standardized data types** for all common data needs
- **Built-in governance** with audit trails and provenance
- **Semantic annotations** linking to ontologies and vocabularies
- **Quality management** with explicit handling of missing/exceptional data
- **Standards compliance** with W3C specifications (XSD, RDF, OWL)

## Core Concepts

### The Three Pillars

**1. Enforce Governance**
Every data element knows:
- Who created it (`createdBy`)
- When it was created (`createdOn`)
- Why it exists (`rationale`)

**2. Embed Meaning**
Every element can link to:
- Ontologies and vocabularies
- Standard terminologies (SNOMED, LOINC, etc.)
- Documentation and references

**3. Mandate Quality**
Every element explicitly handles:
- Missing data (different types of "unknown")
- Exceptional values (masked, not-applicable, etc.)
- Data quality indicators

### The Source of Truth

**Important**: `sdc5.xsd` is the normative source of truth.

```
sdc5.xsd → defines structure
Specification → describes structure
Examples → demonstrate usage
```

If documentation conflicts with `sdc5.xsd`, the schema is correct.

## Your First SDC5 Element

### Minimal Example

```xml
<PatientName
    xmlns="http://semanticdatacharter.com/ns/sdc5/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="XdStringType">

  <label>Patient Full Name</label>
  <data>Jane Doe</data>

  <audit>
    <createdBy>registration-clerk</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</PatientName>
```

**Breaking it down**:

1. **Namespace** - `xmlns="http://semanticdatacharter.com/ns/sdc5/"`
2. **Type** - `xsi:type="XdStringType"` (text data)
3. **Label** - Human-readable name
4. **Data** - The actual value
5. **Audit** - Who and when (required)

### Validate It

Save as `patient-name.xml` and validate:

```bash
xmllint --schema sdc4/schemas/sdc5.xsd --noout patient-name.xml
```

If no errors, congratulations! You've created valid SDC5 data.

## Common Data Types

### Text Data - XdStringType

```xml
<Name xsi:type="XdStringType">
  <label>Full Name</label>
  <data>John Smith</data>
  <audit>
    <createdBy>user-001</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</Name>
```

### Numbers - XdCountType

```xml
<ItemCount xsi:type="XdCountType">
  <label>Number of Items</label>
  <magnitude>42</magnitude>
  <audit>
    <createdBy>system</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdCountType>
```

### Measurements - XdQuantityType

```xml
<Weight xsi:type="XdQuantityType">
  <label>Patient Weight</label>
  <magnitude>70.5</magnitude>
  <units>kg</units>
  <magnitudeStatus>exact</magnitudeStatus>
  <audit>
    <createdBy>nurse-003</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdQuantityType>
```

### Dates/Times - XdTemporalType

```xml
<BirthDate xsi:type="XdTemporalType">
  <label>Date of Birth</label>
  <data>1985-03-15</data>
  <temporalType>date</temporalType>
  <audit>
    <createdBy>user-001</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdTemporalType>
```

### True/False - XdBooleanType

```xml
<IsActive xsi:type="XdBooleanType">
  <label>Account Active</label>
  <data>true</data>
  <audit>
    <createdBy>admin</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdBooleanType>
```

## Adding Semantic Meaning

Link your data to ontologies:

```xml
<PatientName xsi:type="XdStringType">
  <label>Patient Full Name</label>
  <data>Jane Doe</data>

  <links>
    <meaning>http://hl7.org/fhir/StructureDefinition/Patient#name</meaning>
    <terminology>
      <system>http://snomed.info/sct</system>
      <code>371484003</code>
      <display>Patient name</display>
    </terminology>
  </links>

  <audit>
    <createdBy>registration-clerk</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</PatientName>
```

## Handling Missing Data

### Data Unknown

```xml
<BloodType xsi:type="XdStringType">
  <label>Blood Type</label>
  <data/>  <!-- Empty -->
  <exceptionValue>unknown</exceptionValue>
  <audit>
    <createdBy>nurse</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
    <rationale>Patient unable to recall</rationale>
  </audit>
</BloodType>
```

### Not Applicable

```xml
<PregnancyStatus xsi:type="XdStringType">
  <label>Pregnancy Status</label>
  <data/>
  <exceptionValue>not-applicable</exceptionValue>
  <audit>
    <createdBy>nurse</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
    <rationale>Patient is male</rationale>
  </audit>
</XdStringType>
```

## Using Lists

### Simple List - XdStringList

```xml
<Allergies xsi:type="XdStringList">
  <label>Known Allergies</label>
  <items>
    <item>Penicillin</item>
    <item>Peanuts</item>
    <item>Shellfish</item>
  </items>
  <audit>
    <createdBy>nurse</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdStringList>
```

### Quantified List - XdDecimalList

```xml
<DailyTemperatures xsi:type="XdDecimalList">
  <label>Daily Temperature Readings</label>
  <units>°C</units>
  <items>
    <item>36.5</item>
    <item>36.8</item>
    <item>37.1</item>
    <item>36.9</item>
  </items>
  <audit>
    <createdBy>nurse</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</XdDecimalList>
```

## Creating a Complete Record

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PatientVitalSigns
    xmlns="http://semanticdatacharter.com/ns/sdc5/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://semanticdatacharter.com/ns/sdc5/ sdc5.xsd">

  <Temperature xsi:type="XdQuantityType">
    <label>Body Temperature</label>
    <magnitude>37.2</magnitude>
    <units>°C</units>
    <magnitudeStatus>exact</magnitudeStatus>
    <audit>
      <createdBy>nurse-station-2</createdBy>
      <createdOn>2025-11-02T14:30:00Z</createdOn>
    </audit>
  </Temperature>

  <HeartRate xsi:type="XdCountType">
    <label>Heart Rate</label>
    <magnitude>72</magnitude>
    <audit>
      <createdBy>nurse-station-2</createdBy>
      <createdOn>2025-11-02T14:30:00Z</createdOn>
    </audit>
  </HeartRate>

  <MeasurementTime xsi:type="XdTemporalType">
    <label>Measurement Timestamp</label>
    <data>2025-11-02T14:30:00Z</data>
    <temporalType>datetime</temporalType>
    <audit>
      <createdBy>nurse-station-2</createdBy>
      <createdOn>2025-11-02T14:30:00Z</createdOn>
    </audit>
  </XdTemporalType>

</PatientVitalSigns>
```

Save and validate:

```bash
xmllint --schema sdc4/schemas/sdc5.xsd --noout patient-vital-signs.xml
```

## Using Tools

### Command Line (xmllint)

```bash
# Validate
xmllint --schema sdc4/schemas/sdc5.xsd --noout your-file.xml

# Format nicely
xmllint --format your-file.xml
```

### Python (lxml)

```python
from lxml import etree

# Load schema
schema_doc = etree.parse('sdc4/schemas/sdc5.xsd')
schema = etree.XMLSchema(schema_doc)

# Validate document
doc = etree.parse('your-file.xml')
schema.assertValid(doc)
print("✅ Valid SDC5 document")
```

### SDCStudio (Web Application)

[SDCStudio](https://github.com/AxiusSDC/SDCStudio) provides:
- Interactive model creation
- AI-powered suggestions
- Multiple export formats (XSD, XML, JSON, RDF, SHACL, GQL)

## Next Steps

### Learn More

- **[Specification](../specification/sdc5-specification.md)** - Complete reference
- **[Examples](../examples/)** - More working examples
- **[Architecture](../../docs/ARCHITECTURE.md)** - How SDC5 works
- **[FAQ](../../docs/FAQ.md)** - Common questions

### Build Your Own

1. **Identify your domain** - Healthcare? Finance? IoT?
2. **Choose your types** - Which SDC5 types fit your data?
3. **Create schema** - Use XSD restriction pattern
4. **Validate** - Test against `sdc5.xsd`
5. **Add semantics** - Link to ontologies
6. **Generate instances** - Create actual data

### Get Help

- **GitHub Discussions** - Ask questions, share experiences
- **GitHub Issues** - Report problems, request features
- **Examples** - Study working implementations

## Common Pitfalls

### ❌ Missing Audit

```xml
<Name xsi:type="XdStringType">
  <label>Name</label>
  <data>John</data>
  <!-- ❌ No audit! -->
</Name>
```

**Fix**: Always include audit

```xml
<Name xsi:type="XdStringType">
  <label>Name</label>
  <data>John</data>
  <audit>
    <createdBy>user</createdBy>
    <createdOn>2025-11-02T10:00:00Z</createdOn>
  </audit>
</Name>
```

### ❌ Wrong Namespace

```xml
<Name xmlns="http://wrong-namespace.org/" ...>
```

**Fix**: Use correct namespace

```xml
<Name xmlns="http://semanticdatacharter.com/ns/sdc5/" ...>
```

### ❌ Missing Type Attribute

```xml
<Name>  <!-- ❌ No xsi:type -->
  <label>Name</label>
</Name>
```

**Fix**: Always specify type

```xml
<Name xsi:type="XdStringType">
  <label>Name</label>
</Name>
```

## Resources

- **Official Website** - https://semanticdatacharter.github.io
- **GitHub Repository** - https://github.com/SemanticDataCharter/SDCRM
- **SDCStudio** - https://github.com/AxiusSDC/SDCStudio
- **Obsidian Template** - https://github.com/SemanticDataCharter/SDCObsidianTemplate

---

**You're ready to start building with SDC5!** 🚀
