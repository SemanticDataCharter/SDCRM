# Choosing an SDC4 Datatype

This guide walks through a short decision tree to help you pick the appropriate `Xd*` type for a piece of data.

## Decision Tree

Answer the questions in order and stop at the first match.

**1. Is the data textual?**
- **Yes**: `XdString` (or `XdToken` for normalized codes)

**2. Is the data boolean (true/false)?**
- **Yes**: `XdBoolean`

**3. Is the data numeric?**
- **Yes, whole numbers only (counts)**: `XdCount`
- **Yes, decimal values with units**: `XdQuantity`
- **Yes, scientific floating-point**: `XdFloat` or `XdDouble`
- **Yes, ordered categorical**: `XdOrdinal`

**4. Is the data temporal (date/time)?**
- **Yes**: `XdTemporal`

**5. Is the data a reference or link?**
- **Yes**: `XdLink`

**6. Is the data binary or a file?**
- **Yes**: `XdFile`

**7. Is the data a range or interval?**
- **Yes**: `XdInterval`

## Further Reference

For the full type reference, including constraint summaries by type, common datatype mapping examples (CSV, SQL), and the complete `Xd*` inheritance hierarchy, see **Appendix A** of the SDC4 specification (`sdc4/specification/sdc4-specification.md`).
