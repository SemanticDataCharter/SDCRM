# SDC4 Examples

This directory contains working examples of SDC4-compliant data models and instance documents.

**All examples validate against `sdc4.xsd`** - These are tested, working implementations.

## Directory Structure

### Basic Examples (`basic/`)

Simple, introductory examples demonstrating core SDC4 concepts:

- **patient-record.xml** - Basic patient demographics with XdString, XdTemporal, XdBoolean
- **product-catalog.xml** - Product data with XdQuantity, XdCount, XdLink
- **financial-transaction.xml** - Transaction record with XdDecimalList, XdTemporal, provenance

*Perfect for learning SDC4 basics.*

### Multilingual Examples (`multilingual/`)

The same patient vital signs data model in multiple languages:

- **pt-BR/** - Portuguese (Brazil) - sinais-vitais-paciente.xml
- **fr-FR/** - French (France) - signes-vitaux-patient.xml
- **es-MX/** - Spanish (Mexico) - signos-vitales-paciente.xml
- *Additional languages welcome via contributions!*

*Demonstrates internationalization and Unicode support.*

### Advanced Examples (`advanced/`)

Complex examples showing advanced SDC4 features:

- **linked-data.xml** - Semantic annotations, ontology links, RDF integration
- **exceptional-values.xml** - Handling missing data, masked values, null flavors
- **complex-provenance.xml** - Multi-level provenance, audit trails, policy links

*For experienced SDC4 implementers.*

## Validation

All examples should validate against the SDC4 schema:

```bash
# Validate a single file
xmllint --schema ../schemas/sdc4.xsd --noout basic/patient-record.xml

# Validate all examples
for f in **/*.xml; do
    echo "Validating $f..."
    xmllint --schema ../schemas/sdc4.xsd --noout "$f"
done
```

## Mandatory instance_id

As of the Beale-Sovereignty update, every SDC4 data instance **must** include an `instance_id` element. The SDC ecosystem uses CUID2 identifiers. New examples must include this element.

## Example Structure

Each example typically includes:

1. **XML Schema** - Defines the data model (using XSD restriction of sdc4.xsd)
2. **XML Instance** - Sample data conforming to the schema
3. **Comments** - Inline documentation explaining choices

Some examples may be complete XML instances that validate directly against sdc4.xsd without a custom schema.

## Creating New Examples

Want to contribute an example? Great! Here's how:

### 1. Choose a Category

- **Basic** - Simple, single-concept demonstrations
- **Multilingual** - Translations of existing examples
- **Advanced** - Complex, multi-concept demonstrations

### 2. Create Your Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<YourElement xmlns="http://semanticdatacharter.org/ns/sdc4/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://semanticdatacharter.org/ns/sdc4/ sdc4.xsd">

    <!-- Add your SDC4 components here -->

</YourElement>
```

### 3. Validate

```bash
xmllint --schema ../schemas/sdc4.xsd --noout your-example.xml
```

### 4. Add Comments

Explain your design choices:

```xml
<!-- Using XdStringType for patient name because it includes:
     - Label (e.g., "Patient Full Name")
     - Required audit trail (who, when, why)
     - Optional semantic links to ontologies
     - Exception handling for unknown values -->
<PatientName xsi:type="XdStringType">
    <label>Patient Full Name</label>
    <data>Jane Doe</data>
    <!-- ... -->
</PatientName>
```

### 5. Submit PR

Follow [CONTRIBUTING.md](../../CONTRIBUTING.md) to submit your example.

## Use Cases by Domain

### Healthcare
- Patient records
- Clinical observations
- Laboratory results
- Medication orders
- Care plans

### Finance
- Transaction records
- Account statements
- Regulatory filings
- Audit logs

### Research
- Experimental data
- Study protocols
- Dataset descriptions
- Measurement results

### Manufacturing
- Product specifications
- Quality control data
- Supply chain tracking
- Equipment telemetry

### IoT
- Sensor readings
- Device configurations
- Event streams
- Alert notifications

*Don't see your domain? Contribute an example!*

## Example Naming Conventions

- Use lowercase with hyphens: `patient-vital-signs.xml`
- Be descriptive: `sensor-temperature-readings.xml` not `example1.xml`
- Include language code for translations: `patient-record-pt-BR.xml`

## Testing Examples

Before submitting:

1. **Validate against schema**
   ```bash
   xmllint --schema ../schemas/sdc4.xsd --noout your-example.xml
   ```

2. **Check well-formedness**
   ```bash
   xmllint --noout your-example.xml
   ```

3. **Verify encoding**
   ```bash
   file your-example.xml  # Should show UTF-8
   ```

4. **Test with tools**
   - Try loading in SDCStudio
   - Verify in XML editor with schema validation

## Common Patterns

### Minimal SDC4 Element

```xml
<MyElement xsi:type="XdStringType">
    <label>My Element</label>
    <data>My Value</data>
    <audit>
        <createdBy>system-user</createdBy>
        <createdOn>2025-11-02T10:00:00Z</createdOn>
    </audit>
</MyElement>
```

### With Semantic Annotation

```xml
<MyElement xsi:type="XdStringType">
    <label>My Element</label>
    <data>My Value</data>
    <audit>...</audit>
    <links>
        <meaning>http://example.org/ontology#MyConceptName</meaning>
    </links>
</MyElement>
```

### With Exceptional Value

```xml
<MyElement xsi:type="XdStringType">
    <label>My Element</label>
    <data/>
    <exceptionValue>unknown</exceptionValue>
    <audit>...</audit>
</MyElement>
```

## Getting Help

- **Questions about examples?** Open a [GitHub Discussion](https://github.com/SemanticDataCharter/SDCRM/discussions)
- **Found an issue?** Open a [GitHub Issue](https://github.com/SemanticDataCharter/SDCRM/issues)
- **Want to contribute?** See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**All examples are MIT licensed. Use them freely!**
