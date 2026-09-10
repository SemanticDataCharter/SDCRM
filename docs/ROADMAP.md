# SDCRM Roadmap

Future direction for the Semantic Data Charter Reference Model.

## Table of Contents

- [Current Status](#current-status)
- [SDC4 Maintenance (2025-2027)](#sdc4-maintenance-2025-2027)
- [SDC5 Planning (Future)](#sdc5-planning-future)
- [Community Feedback](#community-feedback)
- [Standards Evolution](#standards-evolution)

---

## Current Status

**SDC4**: Version 4.0.0 (October 20, 2025)

**Status**: ✅ Stable and production-ready

**Ecosystem**:
- SDCRM 4.0.0 - Reference model repository
- SDCStudio 4.0.0 - Web application for model generation
- Obsidian Template 4.0.0 - Markdown template for datasets

---

## SDC4 Maintenance (2025-2027)

SDC4 is designed for **long-term stability**. Focus is on refinement, not radical change.

### Planned PATCH Releases (4.0.x)

**Timeline**: As needed (monthly if active)

**Focus**:
- Documentation clarifications
- Specification improvements
- Bug fixes in examples
- Schema comment enhancements

**Recent/Upcoming**:
- ✅ 4.0.0 - Initial release (October 2025)
- ⏳ 4.0.1 - Documentation improvements (planned)

### Planned MINOR Releases (4.x.0)

**Timeline**: Quarterly or as needed

**Under Consideration**:

#### 4.1.0 (Q1 2026)
- **Additional List Types**
  - `XdRatioList` - For ratio collections
  - `XdIntervalList` - For interval ranges
- **Enhanced Temporal Types**
  - Duration with precision
  - Recurring temporal patterns
- **Expanded Exception Values**
  - Domain-specific exception codes
  - Custom exception taxonomies
- **Examples**
  - More healthcare examples
  - Financial domain examples
  - IoT sensor data examples

#### 4.2.0 (Q2 2026)
- **Improved Ontology Bindings**
  - Multiple terminology bindings per element
  - Terminology mapping support
- **Enhanced Cluster Features**
  - Cluster templates
  - Reusable cluster definitions
- **Quality Enhancements**
  - Data quality scores
  - Confidence intervals
  - Data lineage tracking

#### 4.3.0 (Q3-Q4 2026)
- **Performance Optimizations**
  - Schema validation improvements
  - Large dataset handling
- **Tool Integrations**
  - Additional validators
  - Code generators for more languages
  - IDE plugins

**Note**: These are proposals, not commitments. Community feedback drives priorities.

---

## SDC5 Planning (Future)

**Timeline**: No earlier than 2027

SDC5 will be the next **MAJOR** version with breaking changes. This is long-term planning only.

### Potential Breaking Changes Under Discussion

⚠️ **Not decided** - These are ideas for community discussion:

#### Namespace Simplification
```xml
<!-- SDC4 -->
xmlns:sdc="https://semanticdatacharter.com/ns/sdc4/"

<!-- SDC5 (proposed) -->
xmlns:sdc="https://semanticdatacharter.com/ns/sdc5/"
```

#### Enhanced Composition Patterns
- More flexible cluster hierarchies
- Component inheritance improvements
- Template-based model generation

#### JSON Schema Compatibility
- Dual validation (XSD + JSON Schema)
- JSON-native instance documents
- Bidirectional conversion guarantees

#### Simplified Audit Structure
- Streamlined required fields
- Optional extended audit
- Provenance chain support

#### Type System Enhancements
- Union types (e.g., String or Link)
- Optional fields without exception values
- More flexible list constraints

### RFC Process for SDC5

When SDC5 planning begins:

1. **RFC Phase** (3-6 months)
   - Public proposal
   - Community discussion
   - Consensus building

2. **Design Phase** (6 months)
   - Detailed specifications
   - Prototype implementations
   - Migration path design

3. **Alpha/Beta** (6-12 months)
   - Early testing
   - Tool updates
   - Documentation

4. **Release**
   - Official SDC5 launch
   - Migration guide
   - Parallel SDC4 support

**SDC4 Support**: Continues for 6+ months after SDC5 release

---

## Community Feedback

### How to Influence the Roadmap

1. **GitHub Issues**
   - Tag: `enhancement` or `roadmap`
   - Describe use case and benefits
   - Provide examples

2. **GitHub Discussions**
   - Roadmap category
   - Propose new features
   - Vote on proposals

3. **RFC Process**
   - For MAJOR changes
   - Detailed proposals
   - Community review

### Current Community Requests

*Track top community requests here as they emerge*

#### Most Requested Features

1. **More examples** - Diverse domains
2. **Better tool integration** - IDE support
3. **Performance guides** - Large dataset optimization
4. **Migration tools** - From other standards

#### Under Active Discussion

*None currently - join discussions to propose ideas!*

---

## Standards Evolution

### Tracking W3C Standards

SDC evolves with W3C standards:

| Standard | Current | Planned | Impact |
|----------|---------|---------|--------|
| XSD | 1.1 | 1.1 | Stable |
| RDF | 1.1 | 1.2 (if released) | Minor updates |
| OWL | 2 | 2 | Stable |
| SPARQL | 1.1 | 1.2 (proposed) | Evaluate |

### ISO Standards

| Standard | Usage | Planned |
|----------|-------|---------|
| ISO 8601 (Date/Time) | ✅ Full support | Continue |
| ISO/IEC 11179 (Metadata) | Aligned | Closer alignment? |
| UCUM (Units) | ✅ Recommended | Continue |

### Healthcare Standards

| Standard | Current | Planned |
|----------|---------|---------|
| HL7 FHIR | Compatible | Maintain compatibility |
| OpenEHR | Aligned concepts | Continue alignment |
| SNOMED CT | Supported | Enhanced integration? |
| LOINC | Supported | Enhanced integration? |

---

## Documentation Roadmap

### Short Term (2025-2026)

- ✅ Complete specification migration from website
- ✅ Comprehensive README and contributing guidelines
- ⏳ Getting started guide
- ⏳ Implementation guides
- ⏳ Migration guide (from other standards)
- ⏳ Best practices guide
- ⏳ Performance optimization guide

### Medium Term (2026)

- Video tutorials
- Interactive examples
- Online playground (validate, generate)
- Certification program for implementers
- Case studies from real deployments

### Long Term (2027+)

- Academic papers on SDC approach
- Formal verification of schemas
- Automated conformance testing
- SDC training courses

---

## Tool Ecosystem Roadmap

### SDCStudio (Web Application)

**Current**: 4.0.0

**Planned**:
- AI-powered model suggestions (enhanced)
- Batch model generation
- Template library
- Collaboration features
- API for external integrations

### Obsidian Template

**Current**: 4.0.0

**Planned**:
- More template prompts
- Visual schema designer integration
- Export to multiple formats
- Template variants for specific domains

### New Tools (Proposals)

- **CLI validator** - Command-line validation tool
- **VS Code extension** - IDE support for SDC4
- **Python SDK** - pythonic SDC4 API
- **JavaScript SDK** - browser/Node.js support
- **Data converters** - From FHIR, OpenEHR, etc.

---

## Research Directions

Areas for academic research:

1. **Formal Methods** - Proving schema correctness
2. **Machine Learning** - Automated model generation
3. **Interoperability** - Cross-standard mappings
4. **Optimization** - Performance at scale
5. **Usability** - Developer experience studies

**Collaboration Welcome**: Contact us if interested in SDC research.

---

## Release Calendar (Tentative)

| Quarter | Release | Type | Focus |
|---------|---------|------|-------|
| Q4 2025 | 4.0.1 | PATCH | Documentation fixes |
| Q1 2026 | 4.1.0 | MINOR | Additional types, more examples |
| Q2 2026 | 4.2.0 | MINOR | Enhanced bindings, cluster features |
| Q3 2026 | 4.0.x | PATCH | As needed |
| Q4 2026 | 4.3.0 | MINOR | Performance, tools |
| 2027 | SDC5 RFC | MAJOR | Community discussion begins |

**Note**: Dates are estimates. Actual releases depend on development progress and community needs.

---

## How to Track Progress

- **GitHub Milestones** - Track release progress
- **GitHub Projects** - Kanban boards for features
- **CHANGELOG.md** - Detailed release notes
- **Discussions** - Community updates

---

## Get Involved

Want to shape the future of SDC?

1. **Star the repo** - Show your support
2. **Join discussions** - Share your ideas
3. **Open issues** - Request features
4. **Submit PRs** - Contribute code/docs
5. **Spread the word** - Share SDC with others

---

## Long-Term Vision

**SDC Goal**: Universal framework for semantically rich, interoperable data models

**Success Criteria**:
- ✅ Adopted across multiple domains (healthcare, finance, IoT, etc.)
- ⏳ Standard tooling in major IDEs
- ⏳ Integration with major data platforms
- ⏳ Academic recognition and research
- ⏳ Enterprise adoption
- ⏳ Open-source community of contributors

**Timeline**: 3-5 years to widespread adoption

---

**The future of SDC is shaped by its community. Join us!**
