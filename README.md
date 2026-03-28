# Semantic Data Charter Reference Model (SDCRM)

![Version](https://img.shields.io/badge/version-4.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![W3C Standards](https://img.shields.io/badge/W3C-XSD%20|%20RDF%20|%20OWL-orange)
![Open Source](https://img.shields.io/badge/open%20source-❤️-ff69b4)

**The authoritative source for the Semantic Data Charter (SDC4) reference model, schemas, and specifications.**

---

## 📋 What is SDC?

The **Semantic Data Charter (SDC)** is a comprehensive framework for creating semantically rich, machine-readable, and highly interoperable data models. SDC4 is the fourth generation of this reference model, providing standardized data types and governance structures that enable:

- **Semantic Interoperability** - Data models that share meaning across systems
- **Built-in Governance** - Provenance, versioning, and auditing at the data element level
- **Quality Management** - Explicit handling of exceptional values and data quality markers
- **Standards Compliance** - Full alignment with W3C standards (XSD, RDF, OWL, SPARQL)

---

## 🎯 The Three Pillars of SDC

### 1. **Enforce Governance**
Every data element includes:
- Who created/modified it
- When it was created/modified
- Why it exists (rationale, policy links)
- Where it came from (provenance)

### 2. **Embed Meaning**
Every data element can be:
- Linked to ontologies and vocabularies
- Annotated with semantic metadata
- Connected to external knowledge bases
- Validated against domain concepts

### 3. **Mandate Quality**
Every data element explicitly handles:
- Missing data (different types of "unknown")
- Exceptional values (masked, null flavors)
- Data quality indicators
- Measurement accuracy and error margins

---

## 🔑 Critical Principle: Source of Truth

**⚠️ IMPORTANT**: `sdc4.xsd` is the normative source of truth for the SDC4 ecosystem.

```
sdc4.xsd (schema)          ← SOURCE OF TRUTH (normative, machine-readable)
    ↓
Specification (markdown)   ← Describes the schema (descriptive, human-readable)
    ↓
Examples                   ← Demonstrates usage
    ↓
Guides                     ← Teaches implementation
```

All documentation **describes** the schema; the schema **defines** SDC4. If documentation conflicts with `sdc4.xsd`, the schema is correct.

See [CLAUDE.md](CLAUDE.md) for detailed architectural guidance.

---

## 📦 Repository Contents

### Schemas (`sdc4/schemas/`)
- **`sdc4.xsd`** - XML Schema Definition (normative structural specification)
- **`sdc4.owl`** - OWL ontology (normative semantic layer)
- **`sdc4-meta.owl`** - Meta-ontology (maps XSD to conceptual entities)

### Specification (`sdc4/specification/`)
- **`sdc4-specification.md`** - Complete SDC4 specification (484 lines)
- **`core-types.md`** - Reference documentation for all SDC4 types
- **`governance.md`** - Governance component details
- **`conformance.md`** - Conformance requirements
- **`standards-compliance.md`** - W3C alignment documentation

### Examples (`sdc4/examples/`)
- **`basic/`** - Simple examples (patient records, product catalogs)
- **`multilingual/`** - Examples in multiple languages (en-US, pt-BR, fr-FR, es-MX)
- **`advanced/`** - Complex examples (linked data, exceptional values, provenance)

### Guides (`sdc4/guides/`)
- **`getting-started.md`** - Introduction for new users
- **`creating-data-models.md`** - Step-by-step modeling guide
- **`implementing-xsd-restriction.md`** - Using XSD restriction (required pattern)
- **`semantic-annotations.md`** - Adding ontology links and semantic metadata

### Documentation (`docs/`)
- **`ARCHITECTURE.md`** - High-level architecture overview
- **`VERSIONING.md`** - Semantic versioning strategy for reference models
- **`ROADMAP.md`** - Future direction (SDC5 planning)
- **`FAQ.md`** - Frequently asked questions

### Tools (`tools/`)
- **`validators/`** - Python validation scripts for SDC4 compliance

---

## 🚀 Quick Start

### 1. Validate Against SDC4 Schema

```bash
# Using xmllint
xmllint --schema sdc4/schemas/sdc4.xsd --noout your-model.xml

# Using Python (lxml)
from lxml import etree
schema = etree.XMLSchema(etree.parse('sdc4/schemas/sdc4.xsd'))
doc = etree.parse('your-model.xml')
schema.assertValid(doc)
```

### 2. Create a Data Model

SDC4 uses **XSD restriction** (never extension) to create domain-specific models:

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:sdc="http://semanticdatacharter.org/ns/sdc4/">

  <!-- Import SDC4 reference model -->
  <xs:import namespace="http://semanticdatacharter.org/ns/sdc4/"
             schemaLocation="sdc4.xsd"/>

  <!-- Create your model by restricting SDC4 types -->
  <xs:element name="PatientName">
    <xs:complexType>
      <xs:complexContent>
        <xs:restriction base="sdc:XdStringType">
          <!-- Add constraints here -->
        </xs:restriction>
      </xs:complexContent>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

### 3. Use Tools

**[SDCStudio](https://github.com/AxiusSDC/SDCStudio)** - Web application for generating SDC4 models
- Interactive UI for creating data models
- AI-powered component suggestions via RAG
- Generates XSD, XML, JSON, JSON-LD, RDF, SHACL, GQL

**[Obsidian Template](https://github.com/SemanticDataCharter/SDCObsidianTemplate)** - Markdown template for dataset descriptions
- Create SDC4 model definitions in Obsidian
- Upload to SDCStudio for generation
- Interactive prompts for all components

---

## 📚 Core Data Types

SDC4 provides standardized types for all common data needs:

| Type | Purpose | Examples |
|------|---------|----------|
| **XdStringType** | Text data | Names, descriptions, codes |
| **XdBooleanType** | True/false values | Flags, indicators |
| **XdCountType** | Countable quantities | Number of items, occurrences |
| **XdQuantityType** | Measured quantities with units | Length, weight, temperature |
| **XdTemporalType** | Dates and times | Timestamps, periods, durations |
| **XdLinkType** | References and URIs | External links, ontology references |
| **XdFileType** | File references | Documents, images, attachments |
| **XdOrdinalType** | Ranked categorical data | Severity levels, grades |
| **XdIntervalType** | Ranges and bounds | Age ranges, date periods |

**List Types** (with appropriate quantification):
- **Non-quantified**: `XdStringList`, `XdBooleanList`, `XdFileList`, `XdLinkList`, `XdOrdinalList`
- **Quantified**: `XdDecimalList`, `XdIntegerList`, `XdTemporalList`

See [`sdc4/specification/core-types.md`](sdc4/specification/core-types.md) for complete reference.

---

## 🌍 Use Cases

SDC4 is used across domains:

- **Healthcare** - Patient records, clinical observations, laboratory results
- **Finance** - Transaction records, account data, regulatory reporting
- **Manufacturing** - Product specifications, quality control data, supply chain
- **Research** - Scientific datasets, experimental data, study protocols
- **Government** - Census data, regulatory filings, public records
- **IoT** - Sensor data, device telemetry, environmental monitoring

---

## 🔄 Version Information

**Current Version**: 4.0.0 (October 20, 2025)

### Semantic Versioning for Reference Models

SDC uses **modified semantic versioning**:

- **MAJOR** (4.x.x → 5.0.0): Breaking changes to reference model → Creates SDC5
- **MINOR** (4.0.x → 4.1.0): Backward-compatible additions → Still SDC4
- **PATCH** (4.0.0 → 4.0.1): Non-breaking fixes, clarifications → Still SDC4

The MAJOR version represents the SDC generation. All SDC4 ecosystem projects use `4.x.x` versioning.

See [`docs/VERSIONING.md`](docs/VERSIONING.md) for complete versioning strategy.

---

## 🤝 Related Projects

- **[SDCStudio](https://github.com/AxiusSDC/SDCStudio)** - Web application for generating SDC4 models (v4.0.0)
- **[Obsidian Template](https://github.com/SemanticDataCharter/SDCObsidianTemplate)** - Markdown template for dataset descriptions (v4.0.0)
- **[Website](https://semanticdatacharter.github.io)** - Documentation and resources

All projects in the SDC4 ecosystem use version `4.x.x` for clear compatibility signaling.

---

## 🔗 Namespace and HTTP Resolution

**Namespace URI**: `http://semanticdatacharter.org/ns/sdc4/`

Schema files are served via HTTP from the website for XML namespace resolution. However:

- **SDCRM Repository** = Source of truth (changes made here)
- **Website** = Serves copies for HTTP resolution

Changes flow: **SDCRM → Website** (never the reverse)

See [CLAUDE.md](CLAUDE.md) for sync workflow.

---

## 🛠️ Contributing

We welcome contributions! SDC thrives on community input.

### Types of Contributions

1. **Documentation improvements** - Clarifications, examples, guides (✅ encouraged)
2. **Examples** - New use cases, domains, patterns (✅ always welcome)
3. **Tools and validators** - Utilities, libraries, plugins (✅ encouraged)
4. **Specification clarifications** - Documentation updates to match schema (✅ encouraged)
5. **Schema changes** - Modifications to `sdc4.xsd` (⚠️ requires RFC process, community discussion)

### Contribution Process

1. **Open an issue** - Describe your proposed contribution
2. **Discuss** - Get feedback from maintainers and community
3. **Fork and branch** - Create feature branch from `main`
4. **Make changes** - Follow coding standards and guidelines
5. **Test** - Validate all examples against schemas
6. **Submit PR** - Use PR template, reference issue
7. **Review** - Address feedback, iterate
8. **Merge** - Once approved, changes are merged

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines.

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Semantic Data Charter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[See LICENSE file for full text]
```

All contributions are made under the same MIT license.

---

## 📧 Support

- **GitHub Issues** - [Report bugs or request features](https://github.com/SemanticDataCharter/SDCRM/issues)
- **GitHub Discussions** - [Ask questions, share ideas](https://github.com/SemanticDataCharter/SDCRM/discussions)
- **Website** - [Documentation and resources](https://semanticdatacharter.github.io)

---

## 🌟 Acknowledgments

SDC is built on decades of standards development and open-source collaboration. We acknowledge:

- **W3C** - For XSD, RDF, OWL standards
- **HL7** - For healthcare data modeling inspiration
- **OpenEHR** - For archetype-based modeling concepts
- **FHIR** - For modern healthcare interoperability patterns
- **Contributors** - Everyone who has contributed code, documentation, and ideas

---

## 📊 Repository Structure

```
SDCRM/
├── sdc4/                 # SDC4 reference model (frozen, production)
│   ├── schemas/          # Normative schemas (XSD, OWL)
│   ├── specification/    # Complete specification and reference docs
│   ├── examples/         # Working examples in multiple languages
│   └── guides/           # Implementation and usage guides
├── sdc5/                 # SDC5 reference model (parallel namespace)
│   ├── schemas/          # sdc5.xsd, sdc5.owl, sdc5-meta.owl
│   ├── specification/    # SDC5 specification and reference docs
│   ├── examples/         # SDC5 examples
│   └── guides/           # SDC5 implementation guides
├── docs/                 # Architecture, versioning, roadmap, FAQ
├── tools/                # Validation scripts and utilities
├── .github/              # Issue/PR templates, workflows
├── CLAUDE.md             # Architectural guidance for contributors
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT License
├── README.md             # This file
└── SECURITY.md           # Security policy
```

---

**Note**: SDC4 and SDC5 coexist via separate namespaces (`xmlns:sdc4` and `xmlns:sdc5`). SDC4 schemas, instances, and data models remain valid forever. SDC5 lives in the `sdc5/` directory with its own namespace (`https://semanticdatacharter.com/ns/sdc5/`). See [`proposals/README.md`](proposals/README.md) for SDC5 planning ground rules.

---

**Transform your data models with semantic richness, governance, and quality.**

**Start building with SDC4 today!** 🚀
