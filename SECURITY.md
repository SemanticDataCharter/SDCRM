# Security Policy

## Supported Versions

The following versions of SDCRM are currently supported with security updates:

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| 4.0.x   | :white_check_mark: | Current SDC4 release |
| < 4.0   | :x:                | Legacy versions - no longer maintained |

---

## What Qualifies as a Security Issue?

For SDCRM (a reference model specification repository), security issues may include:

### Schema-Related

- **XML External Entity (XXE) vulnerabilities** in schema definitions
- **Schema injection attacks** in validation examples
- **Denial of service** via crafted schema validation
- **Namespace hijacking** concerns

### Documentation-Related

- **Malicious code examples** in documentation
- **Command injection** in tool scripts
- **Unsafe validation patterns** in guides

### Infrastructure-Related

- **Compromised releases** or artifacts
- **Supply chain attacks** on dependencies
- **Unauthorized repository access**

---

## What Is NOT a Security Issue?

The following are **not** security issues for this repository:

- **Bugs in schema design** - Use normal issue tracker
- **Implementation bugs in tools** - Report to respective tool repositories (SDCStudio, etc.)
- **Data privacy concerns** - SDC4 provides framework, not implementation
- **Validation bypasses** - If they don't enable attacks

---

## Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

### Private Reporting

To report a security vulnerability:

Use GitHub's private vulnerability reporting (the only supported route; do not send reports by email):
   - Go to repository → Security tab → Report a vulnerability
   - Fill out the form with details, including a detailed description, reproduction steps and impact assessment

### What to Include

Please provide:

- **Description** - What is the vulnerability?
- **Impact** - What could an attacker do?
- **Reproduction** - Step-by-step instructions
- **Affected versions** - Which versions are vulnerable?
- **Suggested fix** - If you have ideas (optional)
- **Your contact info** - For follow-up questions

### What to Expect

1. **Acknowledgment** - Within 48 hours
2. **Initial assessment** - Within 1 week
3. **Updates** - Every week until resolved
4. **Disclosure** - Coordinated with you (typically 90 days)

---

## Security Best Practices for SDC4 Users

### When Creating Data Models

1. **Validate all inputs** - Use schema validation before processing
2. **Sanitize data** - Don't trust user-provided data
3. **Limit processing** - Set timeouts for validation
4. **Use safe parsers** - Configure parsers to prevent XXE

```python
# Example: Safe XML parsing with lxml
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,  # Prevent XXE
    no_network=True,         # Disable network access
    remove_comments=True     # Strip comments
)

doc = etree.parse('data.xml', parser)
```

### When Validating Against Schema

```bash
# Use xmllint with safe options
xmllint --nonet --schema sdc4.xsd --noout data.xml

# Avoid using --load-trace or --dtdvalid with untrusted data
```

### When Implementing Tools

1. **Never execute user-provided code** - Even in examples
2. **Sandbox validation** - Run in restricted environment
3. **Limit resource usage** - Set memory and CPU limits
4. **Validate file paths** - Prevent path traversal
5. **Use secure defaults** - Turn off dangerous features

### When Deploying Applications

1. **Keep dependencies updated** - Use Dependabot or similar
2. **Use HTTPS** - For schema and ontology fetching
3. **Verify signatures** - Check release signatures
4. **Principle of least privilege** - Minimal permissions
5. **Monitor logs** - Watch for suspicious activity

---

## Known Security Considerations

### XML Processing

**Potential Issues:**
- XXE (XML External Entity) attacks
- Billion laughs attack (XML bomb)
- DTD retrieval from network

**Mitigation:**
- SDC4 schemas don't use DTDs
- Examples avoid external entities
- Documentation recommends safe parsers

### Validation Performance

**Potential Issues:**
- ReDoS (Regular Expression Denial of Service)
- Excessive validation time with crafted input

**Mitigation:**
- Schema patterns tested for performance
- Validation timeouts recommended in documentation
- Complexity limits in schema design

### Namespace Resolution

**Potential Issues:**
- Namespace hijacking
- Man-in-the-middle during namespace fetch

**Mitigation:**
- Namespace served over HTTPS (on website)
- Local schema copies available (in repository)
- Documentation recommends local validation

---

## Security Update Process

### For PATCH Versions (4.0.x)

Security fixes released as PATCH versions:

1. Fix developed privately
2. New version prepared (e.g., 4.0.1)
3. Security advisory published
4. Release created with security note
5. Announcement to users

### For MINOR/MAJOR Versions

Security improvements included in regular releases with full changelog.

---

## Dependency Security

This repository has **minimal dependencies**:

- **Schemas**: Pure XSD/OWL (no runtime dependencies)
- **Validation tools**: Standard system tools (xmllint)
- **Documentation**: Markdown (no processing required)

### Tool Dependencies

Tools in `tools/` directory may have dependencies. Each tool maintains its own security policy and dependency management.

---

## Vulnerability Disclosure Policy

### Timeline

1. **Day 0**: Vulnerability reported
2. **Day 2**: Acknowledgment sent
3. **Day 7**: Initial assessment complete
4. **Day 30**: Fix developed and tested (target)
5. **Day 90**: Public disclosure (default, adjustable)

### Public Disclosure

- **Coordinated** - With reporter and affected parties
- **Credit given** - To reporter (if desired)
- **CVE assigned** - For significant issues
- **Advisory published** - GitHub Security Advisories
- **Changelog updated** - Security section

### Exceptions

- **Active exploitation** - May accelerate disclosure
- **Low severity** - May delay disclosure
- **Reporter request** - We'll work with you

---

## Security Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

*None yet - be the first!*

---

## Contact

For security issues: GitHub private vulnerability reporting (Security tab → Report a vulnerability)

For non-security issues:
- **GitHub Issues** - https://github.com/SemanticDataCharter/SDCRM/issues
- **GitHub Discussions** - https://github.com/SemanticDataCharter/SDCRM/discussions

---

## Additional Resources

- [OWASP XML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html)
- [W3C XML Security](https://www.w3.org/standards/xml/security)
- [CWE-611: XXE](https://cwe.mitre.org/data/definitions/611.html)

---

**Security is a shared responsibility. Thank you for helping keep SDCRM secure!**
