# Changelog

All notable changes to the Semantic Data Charter Reference Model (SDCRM) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) adapted for reference models.

## Versioning for Reference Models

- **MAJOR** (4.x.x → 5.0.0): Breaking changes to reference model → Creates SDC5
- **MINOR** (4.0.x → 4.1.0): Backward-compatible additions → Still SDC4
- **PATCH** (4.0.0 → 4.0.1): Non-breaking fixes, clarifications → Still SDC4

The MAJOR version represents the SDC generation (4 = SDC4).

---

## [4.0.0] - Beale-Sovereignty Update (February 2026)

### Changed

**Sovereign Identity & Source Provenance (Beale-Sovereignty)**
- `instance_id` changed from optional (`minOccurs="0"`) to **mandatory** (`minOccurs="1"`) in DMType
- `instance_id` description updated: UUID recommendation replaced with **CUID2** as the SDC ecosystem standard
- Added `source_instance_id` element to DMType — preserves the upstream identifier from the originating source system
- Added `source_version_id` element to DMType — preserves the upstream version, paired with source_instance_id for complete lineage
- Updated `sdc4.owl` — instance_id property description reflects mandatory/CUID2; added source_instance_id and source_version_id DatatypeProperty definitions
- Updated `sdc4-meta.owl` — added NamedIndividual declarations, ClassAssertions, ObjectPropertyAssertions, and AnnotationAssertions for both new fields; added SourceInstanceIdentifier and SourceVersionIdentifier ConceptualAspect individuals
- Updated specification cardinality table and provenance description
- Injected mandatory instance_id into basic XML examples (patient-record.xml, product-catalog.xml)

*This is a retcon (no version bump, no namespace change) to enforce sovereign data identity from the outset.*

---

## [4.0.0] - 2025-10-20

### Added - Initial SDC4 Release

**Schemas**
- `sdc4.xsd` - Complete XML Schema Definition for SDC4 reference model
- `sdc4.owl` - OWL ontology providing semantic layer
- `sdc4-meta.owl` - Meta-ontology mapping XSD to conceptual entities

**Core Types**
- `XdAnyType` - Base type for all SDC4 components
- `XdStringType` - Text data with governance and semantics
- `XdBooleanType` - Boolean values
- `XdCountType` - Countable quantities (discrete)
- `XdQuantityType` - Measured quantities with units
- `XdTemporalType` - Dates, times, durations
- `XdLinkType` - URIs and references
- `XdFileType` - File references and attachments
- `XdOrdinalType` - Ranked categorical data
- `XdIntervalType` - Ranges and bounds

**List Types**
- Non-quantified: `XdStringList`, `XdBooleanList`, `XdFileList`, `XdLinkList`, `XdOrdinalList`
- Quantified: `XdDecimalList`, `XdIntegerList`, `XdTemporalList`

**Governance Components**
- Audit trail (who, when, why, where)
- Versioning support
- Provenance tracking
- Policy and rationale links

**Quality Components**
- Exception value handling (unknown, masked, etc.)
- Normal status indicators
- Magnitude status (=, <, >, ≤, ≥, approximate)
- Error margins and accuracy
- Normal ranges

**Semantic Features**
- RDF/OWL integration
- Ontology references via `meaning` links
- Media and terminology bindings
- Multi-language support

**Specification**
- Complete SDC4 specification document (484 lines)
- Architecture documentation
- Conformance requirements
- Standards compliance details

**Examples**
- Basic examples (patient records, product catalogs)
- Multilingual examples (pt-BR, fr-FR, es-MX)
- Advanced examples (linked data, exceptional values, provenance)

**Documentation**
- Comprehensive README
- Contributing guidelines
- Architecture documentation
- Versioning strategy
- FAQ

**Community Infrastructure**
- GitHub issue templates
- Pull request templates
- Code of conduct
- Security policy

### Standards Compliance

- **W3C XSD 1.1** - Schema validation
- **W3C RDF** - Semantic annotations
- **W3C OWL 2** - Ontology definitions
- **W3C SPARQL** - Query language support
- **ISO 8601** - Date/time formats
- **UCUM** - Units of measure
- **BCP 47** - Language tags

---

## [3.x.x] - Previous Versions

SDC version 3 and earlier were developed prior to this repository structure. Historical information available upon request.

---

## Version Migration

### From No Version to 4.0.0

If you have existing SDC-style data models:

1. Review the [specification](sdc4/specification/sdc4-specification.md)
2. Validate your models against `sdc4.xsd`
3. Use XSD restriction (never extension) for custom models
4. Add required audit components
5. Ensure namespace is `http://semanticdatacharter.org/ns/sdc4/`

See [migration guide](sdc4/guides/migration-guide.md) for detailed instructions.

---

## Future Releases

### Planned for 4.1.0 (Q1 2026)

Backward-compatible additions under consideration:

- Additional quantified list types
- Enhanced temporal type patterns
- More exceptional value codes
- Extended ontology binding options

*Note: These are proposals, not commitments. Community input welcome!*

### SDC5 Planning (Future MAJOR)

Breaking changes under consideration for next MAJOR version:

- Simplified namespace structure
- Enhanced composition patterns
- Improved cluster hierarchies
- JSON Schema compatibility layer

*Timeline TBD. RFC process will be used for all breaking changes.*

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes and additions.

For schema changes, use the RFC (Request for Comments) process described in contributing guidelines.

---

## Related Projects

- **[SDCStudio](https://github.com/AxiusSDC/SDCStudio)** v4.0.0 - Web application for generating SDC4 models
- **[Obsidian Template](https://github.com/SemanticDataCharter/SDCObsidianTemplate)** v4.0.0 - Markdown template for dataset descriptions

All SDC4 ecosystem projects use `4.x.x` versioning.

---

## Changelog Guidelines

When updating this changelog:

1. Add entries under appropriate version heading
2. Use sections: Added, Changed, Deprecated, Removed, Fixed, Security
3. Reference pull requests and issues: `#123`
4. Credit contributors: `@username`
5. Be clear and concise
6. Link to relevant documentation

---

**The format of this changelog**: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
**Versioning scheme**: [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (adapted for reference models)
