# Contributing to SDCRM

Thank you for your interest in contributing to the Semantic Data Charter Reference Model! SDC thrives on community input and collaboration.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Types of Contributions](#types-of-contributions)
- [Getting Started](#getting-started)
- [Contribution Workflow](#contribution-workflow)
- [Schema Change Process](#schema-change-process)
- [Documentation Guidelines](#documentation-guidelines)
- [Example Guidelines](#example-guidelines)
- [Review Process](#review-process)
- [Recognition](#recognition)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

**In summary:**
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on what's best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

There are many ways to contribute:

1. **Report issues** - Found a bug or ambiguity? Let us know!
2. **Suggest enhancements** - Have an idea for improvement?
3. **Improve documentation** - Fix typos, clarify explanations, add examples
4. **Create examples** - Demonstrate SDC4 usage in different domains
5. **Build tools** - Create validators, libraries, plugins
6. **Translate examples** - Add multilingual examples
7. **Answer questions** - Help others in discussions
8. **Review pull requests** - Provide feedback on proposed changes

---

## Types of Contributions

### ✅ Always Welcome

**Documentation Improvements**
- Fix typos and grammar
- Clarify ambiguous explanations
- Add missing information
- Improve formatting and readability

**Examples**
- New use cases and domains
- Multilingual translations
- Advanced patterns and techniques
- Edge cases and special scenarios

**Tools and Utilities**
- Validators (Python, JavaScript, etc.)
- Code generators
- Editor plugins
- Testing frameworks

**Community Support**
- Answering questions in Discussions
- Helping with troubleshooting
- Sharing use cases and experiences

### ⚠️ Requires Discussion

**Specification Changes**
- Updates to specification text
- Restructuring documentation
- New reference sections

**Process**: Open an issue first, discuss approach, then submit PR

### 🚨 Requires RFC

**Schema Changes**
- Modifications to `sdc4.xsd`
- Changes to `sdc4.owl` or `sdc4-meta.owl`
- Breaking changes to structure

**Process**: Schema changes require RFC (Request for Comments) with community review

---

## Getting Started

### 1. Set Up Your Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/SDCRM.git
cd SDCRM

# Add upstream remote
git remote add upstream https://github.com/SemanticDataCharter/SDCRM.git

# Install validation tools (optional but recommended)
sudo apt-get install libxml2-utils  # For xmllint
```

### 2. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-number-description

# For documentation
git checkout -b docs/what-you-are-documenting
```

### 3. Make Your Changes

Follow the guidelines for your contribution type (see below).

### 4. Test Your Changes

```bash
# Validate examples against schema
xmllint --schema sdc4/schemas/sdc4.xsd --noout sdc4/examples/**/*.xml

# Check markdown formatting
# Ensure all links work
# Verify spelling and grammar
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"

# Use conventional commit format
# Examples:
#   docs: fix typo in specification
#   feat: add healthcare example
#   fix: correct schema namespace
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
# Fill out the PR template completely
# Reference any related issues
```

---

## Contribution Workflow

### For Documentation Changes

1. **Identify the issue** - What needs to be fixed or improved?
2. **Check against schema** - Ensure documentation matches `sdc4.xsd`
3. **Make changes** - Follow documentation guidelines
4. **Test links** - Verify all internal/external links work
5. **Submit PR** - Use documentation PR template

### For Examples

1. **Create your example** - Follow example guidelines
2. **Validate** - Must validate against `sdc4.xsd`
3. **Add comments** - Explain your design choices
4. **Update README** - Add to examples README if needed
5. **Submit PR** - Use example PR template

### For Tools

1. **Propose the tool** - Open an issue describing the tool
2. **Discuss approach** - Get feedback on design
3. **Implement** - Follow coding standards
4. **Document** - Add usage instructions
5. **Submit PR** - Include tests and documentation

---

## Schema Change Process

⚠️ **Schema changes are serious and require careful review.**

### Why Schema Changes Are Different

Changes to `sdc4.xsd`, `sdc4.owl`, or `sdc4-meta.owl` affect the entire SDC4 ecosystem:
- All existing implementations (SDCStudio, templates, etc.)
- All data models created by users
- All tools and validators

### RFC Process

1. **Open an Issue** with `[RFC]` prefix
   - Title: `[RFC] Brief description of proposed change`
   - Content: Detailed proposal with rationale

2. **RFC Should Include:**
   - **Problem**: What issue are you solving?
   - **Proposed Solution**: Exact schema changes
   - **Rationale**: Why this approach?
   - **Impact Assessment**: What breaks? Who is affected?
   - **Migration Path**: How do existing users upgrade?
   - **Alternatives Considered**: What else did you evaluate?

3. **Community Discussion** (minimum 2 weeks)
   - Maintainers and community provide feedback
   - Revise proposal based on input
   - Build consensus

4. **Decision**
   - Maintainers make final decision
   - If approved, version is determined (MAJOR, MINOR, PATCH)

5. **Implementation**
   - Create PR with schema changes
   - Update ALL documentation
   - Update ALL examples to validate
   - Update changelog
   - Get maintainer review

6. **Testing**
   - Validate schema itself
   - Test with SDCStudio
   - Verify all examples
   - Check backward compatibility

### What Requires RFC?

- ✅ Adding new optional types or attributes (MINOR version)
- ✅ Removing types or making breaking changes (MAJOR version)
- ✅ Changing required attributes (MAJOR version)
- ✅ Restructuring element relationships (MAJOR version)
- ❌ Fixing schema bugs that don't change structure (PATCH version) - still needs discussion but faster approval
- ❌ Updating schema comments/documentation (PATCH version) - no RFC needed

---

## Documentation Guidelines

### Writing Style

- **Clear and concise** - Use simple, direct language
- **Accurate** - Verify against `sdc4.xsd`
- **Complete** - Don't leave gaps
- **Well-formatted** - Use proper markdown

### Structure

```markdown
# Title (H1)

Brief introduction paragraph.

## Section (H2)

Content organized logically.

### Subsection (H3)

Detailed information.

#### Details (H4)

Additional details as needed.
```

### Code Examples

Use proper syntax highlighting:

````markdown
```xml
<Example xmlns="https://semanticdatacharter.com/ns/sdc4/">
    <!-- Your code here -->
</Example>
```

```python
from lxml import etree
# Your code here
```
````

### Links

- Use relative links within the repository: `[Link](../path/to/file.md)`
- Use absolute URLs for external links: `[W3C XSD](https://www.w3.org/TR/xmlschema11-1/)`
- Always provide link text (no "click here")

### Important: Schema is Source of Truth

When documenting SDC4:
- Reference schema elements by name: `XdStringType`, not "string type"
- Cite attribute names exactly: `magnitudeStatus`, not "magnitude status"
- If documentation conflicts with schema, **fix the documentation**

---

## Example Guidelines

### Requirements

1. **Must validate** against `sdc4.xsd`
   ```bash
   xmllint --schema sdc4/schemas/sdc4.xsd --noout your-example.xml
   ```

2. **Must be well-commented** - Explain design choices
3. **Must demonstrate clear use case** - Not just random data
4. **Must be properly formatted** - Consistent indentation (2 or 4 spaces)
5. **Must use UTF-8 encoding** - Support international characters

### Example Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Brief Description of Example

  This example demonstrates:
  - Concept 1
  - Concept 2
  - Concept 3
-->
<RootElement xmlns="https://semanticdatacharter.com/ns/sdc4/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://semanticdatacharter.com/ns/sdc4/ sdc4.xsd">

    <!-- Inline comments explaining choices -->
    <Component xsi:type="XdStringType">
        <label>Descriptive Label</label>
        <data>Value</data>
        <audit>...</audit>
    </Component>

</RootElement>
```

### Categorization

- **basic/** - Simple, single-concept examples
- **multilingual/** - Translations of examples
- **advanced/** - Complex, multi-concept examples

### Naming Conventions

- Lowercase with hyphens: `patient-vital-signs.xml`
- Descriptive: `sensor-temperature-readings.xml` not `example1.xml`
- Language suffix for translations: `patient-record-pt-BR.xml`

---

## Review Process

### Timeline

- **Documentation PRs**: 1-3 days
- **Example PRs**: 3-5 days
- **Tool PRs**: 5-10 days
- **Schema change PRs**: 2-4 weeks (after RFC approval)

### Review Criteria

Reviewers check for:

1. **Correctness** - Is it technically accurate?
2. **Completeness** - Does it cover everything needed?
3. **Clarity** - Is it easy to understand?
4. **Consistency** - Does it match existing style?
5. **Testing** - Have validations been run?
6. **Documentation** - Is it properly documented?

### Addressing Feedback

- Respond to all review comments
- Make requested changes or explain why not
- Be open to suggestions
- Keep discussions professional and constructive

### Approval

- Requires approval from at least one maintainer
- For schema changes: requires approval from multiple maintainers
- Once approved, maintainer will merge

---

## Recognition

We value all contributions! Contributors are recognized:

- **In CHANGELOG.md** - Significant contributions listed
- **In README.md** - Contributors section
- **On GitHub** - Contributor graph and statistics

### Types of Recognition

- 🏆 **Major Contributor** - Multiple substantial contributions
- 📚 **Documentation Hero** - Excellent documentation work
- 🌍 **Internationalization Champion** - Multilingual examples
- 🛠️ **Tool Builder** - Created useful tools
- 🎓 **Community Helper** - Active in discussions and support

---

## Questions?

- **GitHub Discussions** - Ask questions, start discussions
- **GitHub Issues** - Report bugs, suggest features
- **Pull Requests** - Submit changes

Thank you for contributing to SDCRM! Together we make SDC better for everyone.

---

## Quick Reference

```bash
# Fork, clone, branch
git clone https://github.com/YOUR-USERNAME/SDCRM.git
git checkout -b feature/your-feature

# Make changes, test, commit
xmllint --schema sdc4/schemas/sdc4.xsd --noout example.xml
git add .
git commit -m "docs: fix typo in specification"

# Push and create PR
git push origin feature/your-feature
# Go to GitHub and create Pull Request
```

**Remember: Documentation describes the schema. The schema defines SDC4.**
