# Frequently Asked Questions (FAQ)

Common questions about SDC4 and SDCRM.

## Table of Contents

- [General Questions](#general-questions)
- [Technical Questions](#technical-questions)
- [Usage Questions](#usage-questions)
- [Contribution Questions](#contribution-questions)
- [Versioning Questions](#versioning-questions)

---

## General Questions

### What is SDC4?

SDC4 (Semantic Data Charter version 4) is a comprehensive framework for creating semantically rich, machine-readable, and highly interoperable data models. It provides standardized data types with built-in governance, semantic annotations, and quality management.

### Why should I use SDC4?

**Use SDC4 if you need**:
- Semantic interoperability across systems
- Built-in audit trails and provenance
- Explicit data quality handling
- Standards-compliant data models (W3C XSD, RDF, OWL)
- Multi-domain data modeling (healthcare, finance, IoT, etc.)

### Who is SDC4 for?

- **Data architects** - Designing data models
- **Software developers** - Implementing data systems
- **Data scientists** - Working with structured data
- **Standards developers** - Building domain specifications
- **Researchers** - Creating interoperable datasets

### Is SDC4 production-ready?

Yes! SDC4 v4.0.0 (released October 2025) is stable and production-ready. It's used in:
- SDCStudio (web application)
- Obsidian Template (dataset descriptions)
- Various organizational implementations

### How does SDC4 relate to other standards?

SDC4 **builds on** W3C standards (XSD, RDF, OWL) and **aligns with** domain standards:
- **Healthcare**: HL7 FHIR, OpenEHR compatible
- **Metadata**: ISO/IEC 11179 aligned
- **Semantics**: RDF/OWL native support
- **Units**: UCUM recommended

SDC4 provides a **meta-framework** that works alongside these standards.

---

## Technical Questions

### What's the difference between `sdc4.xsd` and `sdc4.owl`?

- **sdc4.xsd** (XML Schema) - Normative structural definition
  - Defines element structure, attributes, constraints
  - Used for validation
  - Machine-readable, executable

- **sdc4.owl** (OWL Ontology) - Normative semantic layer
  - Defines concepts, relationships, meaning
  - Used for semantic reasoning
  - Enables RDF integration

**Both are normative** - structure from XSD, semantics from OWL.

### Why must I use XSD restriction instead of extension?

**Restriction ensures**:
- All models validate against `sdc4.xsd`
- Universal tooling works with your models
- Semantic consistency across implementations
- Governance and quality components present

**Extension breaks these guarantees** - tools won't understand custom elements.

### Can I add custom attributes?

No, you cannot add attributes via XSD extension. Instead:

**✅ Use semantic links**:
```xml
<Element xsi:type="XdStringType">
  <label>My Element</label>
  <data>Value</data>
  <links>
    <meaning>http://your-ontology.org/custom-concept</meaning>
  </links>
  <audit>...</audit>
</Element>
```

**✅ Use rationale field**:
```xml
<audit>
  <createdBy>user</createdBy>
  <createdOn>2025-11-02T10:00:00Z</createdOn>
  <rationale>Custom information: your-metadata-here</rationale>
</audit>
```

### How do I handle missing data?

Use **exception values**:

```xml
<Element xsi:type="XdStringType">
  <label>Blood Type</label>
  <data/>  <!-- Empty -->
  <exceptionValue>unknown</exceptionValue>  <!-- Why missing -->
  <audit>...</audit>
</Element>
```

**Available exception values**:
- `unknown` - Value exists but not known
- `not-applicable` - Question doesn't apply
- `not-measured` - Measurement not taken
- `masked` - Hidden for privacy
- *And more...*

### What validation tools are available?

**Built-in**:
- `xmllint` (command-line) - Standard XML validator
- `lxml` (Python) - XML processing library

**SDC-specific**:
- SDCStudio - Web-based validation and generation
- Validators in `tools/` directory (this repo)

**Planned**:
- CLI validator
- VS Code extension
- Python SDK
- JavaScript SDK

### Can I use SDC4 with JSON?

**Currently**: SDC4 is XML-native (XSD validation)

**Workarounds**:
- Convert JSON to XML for validation
- Use JSON-LD for semantic layer
- Generate JSON instances from validated models

**Future (SDC5)**: Native JSON Schema support under consideration

### How do I add semantic annotations?

Use the `links` element:

```xml
<Element xsi:type="XdStringType">
  <label>Patient Name</label>
  <data>Jane Doe</data>
  <links>
    <!-- Ontology reference -->
    <meaning>http://hl7.org/fhir/StructureDefinition/Patient#name</meaning>

    <!-- Terminology binding -->
    <terminology>
      <system>http://snomed.info/sct</system>
      <code>371484003</code>
      <display>Patient name</display>
    </terminology>

    <!-- Media/icon -->
    <media>http://example.org/icons/person.png</media>
  </links>
  <audit>...</audit>
</Element>
```

---

## Usage Questions

### How do I get started?

1. **Read the specification**: [`sdc4/specification/sdc4-specification.md`](../sdc4/specification/sdc4-specification.md)
2. **Study examples**: [`sdc4/examples/`](../sdc4/examples/)
3. **Try SDCStudio**: https://github.com/AxiusSDC/SDCStudio
4. **Or create manually**: Use XSD restriction pattern

### What tools should I use?

**For Learning**:
- Read examples in this repository
- Use SDCStudio web interface

**For Development**:
- XML editor with schema validation (VS Code, Oxygen, etc.)
- `xmllint` for command-line validation
- SDCStudio for generation

**For Production**:
- Language-specific XML libraries (lxml, JAXB, etc.)
- Custom validators from `tools/` directory
- Integration with your tech stack

### Can I create models without SDCStudio?

Yes! You can create models manually:

1. Create XSD schema using restriction of `sdc4.xsd`
2. Validate against `sdc4.xsd`
3. Create XML instances
4. Validate instances

See [implementation guide](../sdc4/guides/implementing-xsd-restriction.md) *(coming soon)*.

### How do I validate my model?

```bash
# Validate XSD schema
xmllint --schema http://www.w3.org/2001/XMLSchema.xsd your-schema.xsd

# Validate XML instance against SDC4
xmllint --schema sdc4/schemas/sdc4.xsd --noout your-data.xml

# Validate XML instance against your schema
xmllint --schema your-schema.xsd --noout your-data.xml
```

### Where can I find examples for my domain?

**Current examples**:
- `basic/` - Generic examples (patient, product)
- `multilingual/` - Same examples in multiple languages
- `advanced/` - Complex patterns

**Domain-specific examples** - We need your help! Please contribute examples for:
- Finance
- Manufacturing
- IoT
- Government
- Research
- *Your domain!*

### Can I translate examples to my language?

Yes! We welcome multilingual examples:

1. Fork the repository
2. Copy an example to `sdc4/examples/multilingual/[language-code]/`
3. Translate labels and data
4. Keep structure identical
5. Validate against `sdc4.xsd`
6. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md#example-guidelines).

---

## Contribution Questions

### How can I contribute?

**Many ways**:
- Improve documentation
- Add examples
- Fix bugs
- Build tools
- Answer questions
- Translate examples
- Report issues

See [CONTRIBUTING.md](../CONTRIBUTING.md) for complete guide.

### Can I propose new types?

Yes! New **optional** types can be added in MINOR versions (4.1.0, 4.2.0, etc.):

1. Open GitHub issue with proposal
2. Describe use case and rationale
3. Provide example usage
4. Discuss with community
5. If approved, submit PR with:
   - Schema changes
   - Documentation
   - Examples
   - Tests

### How do I suggest changes to the specification?

1. **For clarifications**: Open issue or submit PR directly
2. **For structural changes**: Open issue for discussion first
3. **For schema changes**: Use RFC process (see [CONTRIBUTING.md](../CONTRIBUTING.md))

### Do I need permission to use SDC4?

No! SDC4 is **Apache-2.0 licensed** - use freely:
- Commercial or non-commercial
- Modify as needed
- No attribution required (but appreciated!)
- Redistribute freely

---

## Versioning Questions

### What version should I use?

**Use the latest PATCH version** of your MAJOR.MINOR version:
- Currently: **4.0.0**
- When 4.0.1 releases: **4.0.1**

Stay on latest PATCH for bug fixes and documentation improvements.

### What does version 4.0.0 mean?

```
4  .  0  .  0
│     │     └── PATCH: Bug fixes, clarifications
│     └──────── MINOR: New optional features
└────────────── MAJOR: SDC generation (4 = SDC4)
```

### When will SDC5 be released?

**Not before 2027** - SDC4 is designed for long-term stability.

SDC5 will include breaking changes and require RFC process with community discussion.

### Will my SDC4 models work with SDC5?

**Not automatically** - MAJOR versions have breaking changes.

When SDC5 is released:
- Migration guide provided
- SDC4 supported for 6+ months after
- Migration tools available
- Backward compatibility where possible

### Can I use SDCStudio 4.1.0 with SDCRM 4.0.0?

Yes! MINOR versions are backward compatible. Tools with higher MINOR versions work with lower MINOR version schemas (same MAJOR).

See [VERSIONING.md](VERSIONING.md) for complete strategy.

---

## Common Issues

### My XML doesn't validate

**Check**:
1. Namespace correct? `http://semanticdatacharter.org/ns/sdc4/`
2. Schema location correct? `sdc4.xsd`
3. All required elements present? (label, audit, data/magnitude)
4. Using correct type? `xsi:type="XdStringType"`
5. Audit has required fields? (createdBy, createdOn)

**Validate step-by-step**:
```bash
# 1. Check XML well-formedness
xmllint --noout your-file.xml

# 2. Validate against SDC4
xmllint --schema sdc4/schemas/sdc4.xsd --noout your-file.xml
```

### I get namespace errors

**Ensure declarations**:
```xml
<RootElement
    xmlns="http://semanticdatacharter.org/ns/sdc4/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://semanticdatacharter.org/ns/sdc4/ sdc4.xsd">
```

### Schema says "must use restriction"

You're trying to **extend** SDC4 types. Use **restriction** instead:

```xml
<!-- ❌ WRONG -->
<xs:extension base="sdc:XdStringType">
  <xs:attribute name="custom"/>
</xs:extension>

<!-- ✅ CORRECT -->
<xs:restriction base="sdc:XdStringType">
  <xs:sequence>
    <xs:element ref="sdc:label"/>
    <xs:element ref="sdc:data"/>
    <xs:element ref="sdc:audit"/>
  </xs:sequence>
</xs:restriction>
```

---

## Support

**Still have questions?**

- **GitHub Discussions** - https://github.com/SemanticDataCharter/SDCRM/discussions
- **GitHub Issues** - https://github.com/SemanticDataCharter/SDCRM/issues
- **Specification** - [`sdc4/specification/sdc4-specification.md`](../sdc4/specification/sdc4-specification.md)
- **Examples** - [`sdc4/examples/`](../sdc4/examples/)

---

**Have a question not answered here? Open a discussion and we'll add it to the FAQ!**
