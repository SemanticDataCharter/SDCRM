# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Semantic Data Charter Reference Model (SDCRM)** is the foundational open-source project for the SDC4 specification and reference model schemas.

This repository contains the **normative source of truth** for the Semantic Data Charter ecosystem.

---

## Source of Truth Hierarchy

### CRITICAL: Understanding the Truth Hierarchy

**The core source of truth for everything in the SDC4 ecosystem is the reference model schema: `sdc4.xsd`**

Everything else describes its function and usage.

```
┌─────────────────────────────────────────┐
│  SDCRM Repository                        │  ← SOURCE OF TRUTH (Normative)
│  /sdc4/schemas/sdc4.xsd                 │
│  Machine-readable, executable           │     Changes made here
│  Defines structure, types, constraints  │
└──────────────────┬──────────────────────┘
                   │
                   ├──→ Specification (markdown)    [Descriptive, human-readable]
                   ├──→ OWL ontologies              [Semantic layer]
                   ├──→ Examples                    [Demonstrates usage]
                   ├──→ Guides                      [Teaches implementation]
                   ├──→ Tools (SDCStudio, etc.)     [Implements the schema]
                   │
                   └──→ Website Namespace           [HTTP endpoint for XML namespace]
                        semanticdatacharter.github.io/ns/sdc4/
                        Copy of sdc4.xsd served for namespace resolution
```

### Namespace Serving vs. Source of Truth

**IMPORTANT DISTINCTION**:

- **SDCRM Repository**: Source of truth - changes are made here
- **Website (semanticdatacharter.github.io)**: Serves the namespace for HTTP resolution

The website's `ns/sdc4/` directory contains a **copy** of `sdc4.xsd` that is served at the namespace URI (e.g., `http://semanticdatacharter.com/ns/sdc4/`). This is required for:

1. **XML Schema namespace resolution** - XML processors fetch schemas via HTTP
2. **RDF/OWL ontology loading** - Semantic tools resolve namespace URIs
3. **Standards compliance** - W3C best practices for namespace URIs

**Workflow**:
1. Changes made in SDCRM repository (source of truth)
2. Changes committed and pushed to SDCRM
3. Schema files copied to website's `ns/sdc4/` directory
4. Website updated to serve new namespace versions
5. XML processors can resolve namespace via HTTP

**Never**:
- ❌ Edit files directly in website's `ns/` directory
- ❌ Make schema changes on website first
- ❌ Skip updating SDCRM when website is updated

### What This Means

1. **Changes to sdc4.xsd** require careful review and versioning
   - These are breaking changes (potentially)
   - Must follow semantic versioning
   - Require community RFC process

2. **Documentation describes the schema** but doesn't define it
   - If documentation conflicts with schema, schema wins
   - Documentation should be updated to match schema
   - Specification is descriptive, not prescriptive

3. **All implementations must conform to the schema**
   - SDCStudio generates models that validate against sdc4.xsd
   - Examples must validate
   - Tools must respect schema constraints

4. **OWL provides semantic layer** but XSD defines structure
   - OWL adds meaning and relationships
   - XSD defines validation rules
   - Both are normative, but XSD takes precedence for structure

---

## Repository Structure

```
SDCRM/
├── sdc4/
│   ├── schemas/
│   │   ├── sdc4.xsd              ← SOURCE OF TRUTH (normative)
│   │   ├── sdc4.owl              ← Semantic layer (normative)
│   │   └── sdc4-meta.owl         ← Meta ontology (normative)
│   ├── specification/
│   │   └── sdc4-specification.md ← Human-readable description (descriptive)
│   ├── examples/
│   │   └── ... (must validate against schema)
│   └── guides/
│       └── ... (teaches usage)
├── docs/
│   └── ... (architectural documentation)
└── README.md
```

---

## Versioning Strategy

### Semantic Versioning for Reference Models

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR** (4.x.x → 5.0.0): Breaking changes to schema
  - Removed types or required attributes
  - Changed element structure
  - Incompatible modifications
  - **These create SDC5, SDC6, etc.**

- **MINOR** (4.0.x → 4.1.0): Backward-compatible additions
  - New optional types
  - New optional attributes
  - Enhanced annotations
  - **Still SDC4**

- **PATCH** (4.0.0 → 4.0.1): Non-breaking fixes
  - Documentation clarifications
  - Comment improvements
  - Bug fixes in examples
  - **Still SDC4**

### Current Version

**SDC4**: v4.0.0 (October 20, 2025)

### Version Alignment

The MAJOR version (4 in 4.x.x) represents the SDC generation. All projects in the SDC4 ecosystem use 4.x.x versioning:

- **SDCRM**: 4.0.0 (this repository)
- **SDCStudio**: 4.0.0 (application)
- **Obsidian Template**: 4.0.0 (template)

This makes compatibility clear at a glance.

---

## Making Changes

### To the Schema (sdc4.xsd)

⚠️ **EXTREME CAUTION REQUIRED**

1. **Propose change** via GitHub issue first
2. **Discuss with community** - breaking changes require RFC
3. **Create feature branch** from main
4. **Make minimal changes** with clear rationale
5. **Update all documentation** to reflect changes
6. **Update all examples** to validate
7. **Run validators** to ensure no breakage
8. **Create PR** with comprehensive description
9. **Wait for review** from maintainers
10. **Version appropriately** (MAJOR, MINOR, or PATCH)

**Never**:
- ❌ Make breaking changes without MAJOR version bump
- ❌ Change schema without updating documentation
- ❌ Break existing examples
- ❌ Add complexity without clear benefit

### To Documentation

✅ **Much Easier**

1. Ensure accuracy against schema
2. Improve clarity and examples
3. Fix typos and formatting
4. Add missing explanations
5. Update for new examples

**Key rule**: If documentation conflicts with schema, **update documentation to match schema**, don't change schema to match documentation.

### To Examples

✅ **Always Welcome**

1. **Must validate** against sdc4.xsd
2. Demonstrate clear use case
3. Include comments explaining choices
4. Add to appropriate category (basic, advanced, multilingual)
5. Update examples README

### To Guides

✅ **Encouraged**

1. Must be technically accurate
2. Should reference specification sections
3. Include working code/examples
4. Target specific audience (beginner, advanced, etc.)

---

## Validation

### Schema Validation

All examples and data models must validate against sdc4.xsd:

```bash
# Using xmllint
xmllint --schema sdc4/schemas/sdc4.xsd --noout example.xml

# Using Python (lxml)
from lxml import etree
schema = etree.XMLSchema(etree.parse('sdc4/schemas/sdc4.xsd'))
doc = etree.parse('example.xml')
schema.assertValid(doc)
```

### Documentation Accuracy

When updating documentation:

1. **Reference the schema** - cite element names, attribute names
2. **Use schema terminology** - don't invent new terms
3. **Verify examples** - ensure they match schema structure
4. **Check cross-references** - links should work

---

## Working with the Specification

### The specification document (sdc4-specification.md) is descriptive

It explains:
- **What** each schema component does
- **Why** it exists
- **How** to use it
- **When** to use it

But it does **not** define the schema. The schema defines itself.

### If you find a conflict

1. **Verify against sdc4.xsd** (the source of truth)
2. **Open an issue** describing the conflict
3. **Propose documentation fix** to match schema
4. If schema is truly wrong, propose schema change (requires RFC)

---

## Related Projects

### SDCStudio

**Repository**: https://github.com/AxiusSDC/SDCStudio

SDCStudio is a Django application that:
- **Reads** sdc4.xsd to understand structure
- **Generates** data models that validate against sdc4.xsd
- **Produces** XML instances that conform to generated models

When updating SDCRM:
- Ensure SDCStudio remains compatible
- Test generated models still validate
- Update SDCStudio if breaking changes

### Obsidian Template

**Repository**: https://github.com/SemanticDataCharter/SDCObsidianTemplate

Creates markdown dataset descriptions that:
- **Map to** SDC4 types
- **Generate** XSD restrictions of sdc4.xsd via SDCStudio
- **Validate** against the schema

When updating SDCRM:
- Ensure type mappings remain accurate
- Update template if new types added

---

## Testing

### Before Committing Schema Changes

1. **Validate the schema itself**
   ```bash
   xmllint --schema http://www.w3.org/2001/XMLSchema.xsd sdc4/schemas/sdc4.xsd
   ```

2. **Validate all examples**
   ```bash
   for f in sdc4/examples/**/*.xml; do
       xmllint --schema sdc4/schemas/sdc4.xsd --noout "$f"
   done
   ```

3. **Check documentation references**
   - Ensure all mentioned types exist in schema
   - Verify attribute names are correct

4. **Test with SDCStudio**
   - Generate a model
   - Ensure it validates

### Automated Testing

GitHub Actions workflow (`.github/workflows/validate-schemas.yml`) automatically:
- Validates sdc4.xsd against XSD spec
- Validates all examples against sdc4.xsd
- Checks documentation links
- Runs on every PR

---

## Documentation Style

### For Specification

- **Authoritative tone** - describes what IS, not what "should be"
- **Reference schema elements** - use `XdStringType`, not "string type"
- **Include examples** - show actual XML conforming to schema
- **Explain rationale** - why does this exist?

### For Guides

- **Teaching tone** - helps users learn
- **Step-by-step** - clear instructions
- **Working examples** - copy-paste ready code
- **Common pitfalls** - warn about mistakes

### For Examples

- **Self-contained** - validate on their own
- **Well-commented** - explain choices
- **Realistic** - based on real use cases
- **Minimal** - demonstrate one concept clearly

---

## Schema Design Principles

When considering changes to sdc4.xsd, remember:

1. **XSD Restriction Model** - All data models must use xsd:restriction, never xsd:extension
2. **Backward Compatibility** - Breaking changes require new MAJOR version
3. **Minimal Complexity** - Add only what's essential
4. **Clear Semantics** - Every element should have obvious meaning
5. **Validation-Friendly** - Schema should enable meaningful validation
6. **Tool-Friendly** - Consider implementation in parsers and generators

### The Three Pillars

All schema components support:

1. **Governance** - Who, when, why, where
2. **Meaning** - What does this represent?
3. **Quality** - Handle imperfect data explicitly

---

## Community

### Code of Conduct

This is a professional, respectful community. See CONTRIBUTING.md for full code of conduct.

### Getting Help

- **GitHub Issues** - For bugs, questions, proposals
- **GitHub Discussions** - For general discussion
- **Pull Requests** - For contributing changes

### Recognition

Contributors are recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- GitHub contributor graph

---

## License

Apache License 2.0 - See LICENSE file for details.

All contributions are made under the same Apache-2.0 license.

---

## Important Notes

### This is a Reference Model Repository

- **Not an application** - provides schemas, not software
- **Not a tutorial site** - provides reference, not courses
- **Normative specification** - defines what SDC4 IS

### Schema Changes are Serious

- Affect entire ecosystem (SDCStudio, templates, implementations)
- Require careful coordination
- Need thorough testing
- Follow RFC process for breaking changes

### Documentation is Important but Secondary

- Keep docs accurate to schema
- Update docs when schema changes
- If in doubt, schema is correct

---

## Syncing with Website Namespace

After making changes to schemas in SDCRM, they must be copied to the website for namespace resolution:

```bash
# After committing changes to SDCRM
cd /home/twcook/GitHub/SDCRM

# Copy schema to website namespace directory
cp sdc4/schemas/sdc4.xsd /home/twcook/GitHub/semanticdatacharter.github.io/ns/sdc4/

# Copy OWL ontologies if changed
cp sdc4/schemas/sdc4.owl /home/twcook/GitHub/semanticdatacharter.github.io/ns/sdc4/
cp sdc4/schemas/sdc4-meta.owl /home/twcook/GitHub/semanticdatacharter.github.io/ns/sdc4/

# Commit to website repository
cd /home/twcook/GitHub/semanticdatacharter.github.io
git add ns/sdc4/
git commit -m "Update namespace files from SDCRM v4.x.x"
git push origin main
```

**Important**: Always update SDCRM first, then sync to website. Never edit files directly in website's `ns/` directory.

---

## Quick Commands

```bash
# Validate a data model against schema
xmllint --schema sdc4/schemas/sdc4.xsd --noout your-model.xml

# Validate the schema itself
xmllint --schema http://www.w3.org/2001/XMLSchema.xsd sdc4/schemas/sdc4.xsd

# Count lines in specification
wc -l sdc4/specification/sdc4-specification.md

# Find all XML examples
find sdc4/examples -name "*.xml"

# Check for broken links in markdown
grep -r "](.*)" docs/ sdc4/specification/

# Sync schemas to website namespace (after SDCRM changes committed)
cp sdc4/schemas/*.xsd /home/twcook/GitHub/semanticdatacharter.github.io/ns/sdc4/
cp sdc4/schemas/*.owl /home/twcook/GitHub/semanticdatacharter.github.io/ns/sdc4/
```

---

**Remember**: sdc4.xsd is the source of truth. Everything else describes it.
