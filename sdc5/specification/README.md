# SDC5 Specification

This directory contains the complete Semantic Data Charter version 4 (SDC5) specification and reference documentation.

## Contents

### Core Specification

**[sdc5-specification.md](sdc5-specification.md)** - The complete SDC5 specification (484 lines)

This is the primary human-readable documentation that describes the SDC5 reference model. It covers:
- Introduction and overview
- W3C standards compliance
- Conformance requirements
- Reference model architecture
- Core data types and components
- Governance components
- Quality components
- Semantic annotations
- Best practices and examples

**Important**: The specification is **descriptive** documentation. The normative source of truth is `sdc5.xsd` in the `schemas/` directory. If there is ever a conflict between this specification and the schema, the schema is correct.

### Reference Documentation

Additional reference documents extracted from the main specification for easier navigation:

- **core-types.md** - Detailed reference for all SDC5 data types
- **governance.md** - Governance component details
- **conformance.md** - Conformance requirements and validation
- **standards-compliance.md** - W3C standards alignment

*(These will be created as the specification evolves)*

## Reading the Specification

### For New Users

Start with the main **sdc5-specification.md** to understand:
1. What SDC5 is and why it exists
2. The three pillars: Governance, Meaning, Quality
3. Core architecture and components
4. How to create SDC5-compliant models

Then move to the [guides](../guides/) for hands-on implementation.

### For Technical Implementers

Reference sections:
1. **Conformance Requirements** - What makes a model SDC5-compliant
2. **Core Data Types** - Detailed type specifications
3. **XSD Restriction Pattern** - How to create models (always restrict, never extend)
4. **Semantic Annotations** - Adding ontology links and RDF metadata

Also review the [schemas](../schemas/) for the normative XSD and OWL definitions.

### For Schema Designers

Key sections:
1. **Reference Model Architecture** - Understanding the component hierarchy
2. **Governance Components** - Adding provenance and audit trails
3. **Quality Components** - Handling exceptional values and data quality
4. **Best Practices** - Design patterns and anti-patterns

Also review [examples](../examples/) for working implementations.

## Standards Referenced

The SDC5 specification builds on these W3C standards:

- **XSD (XML Schema Definition)** - Structural validation
- **RDF (Resource Description Framework)** - Semantic annotations
- **OWL (Web Ontology Language)** - Ontology definitions
- **SPARQL** - Query language for RDF data

## Versioning

The specification version matches the reference model version:

- **Current Version**: 4.0.0 (October 20, 2025)
- **Versioning Scheme**: MAJOR.MINOR.PATCH
  - MAJOR = SDC generation (4 = SDC5)
  - MINOR = Backward-compatible additions
  - PATCH = Clarifications and fixes

See [docs/VERSIONING.md](../../docs/VERSIONING.md) for complete versioning strategy.

## Contributing

Found an error or ambiguity in the specification? Please:

1. Check if the issue is in the specification or the schema
2. Open an issue describing the problem
3. Propose a documentation fix (if specification is wrong)
4. If the schema is wrong, that requires a separate RFC process

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for complete contribution guidelines.

## Related Documentation

- **[Schemas](../schemas/)** - Normative XSD and OWL definitions
- **[Examples](../examples/)** - Working SDC5 examples
- **[Guides](../guides/)** - Implementation guides
- **[Architecture Docs](../../docs/)** - High-level architecture documentation

---

**The specification describes the schema. The schema defines SDC5.**
