# SDC4 Modeling Best Practices

Practical guidance for choosing and constraining Xd* types when authoring SDC4 Data Models.

## Best Practices

1. **Always use units for quantified types.** `XdCountType` and `XdQuantityType` require units. Even if units seem obvious (for example, "items"), specify them explicitly.

2. **Choose appropriate numeric types.**
   - Use **`XdCountType`** for non-negative integer counts.
   - Use **`XdQuantityType`** for decimal measurements with units.
   - Use **`XdFloatType`/`XdDoubleType`** only for scientific calculations where floating-point representation is required.
   - Avoid `XdFloatType`/`XdDoubleType` for financial data; use `XdQuantityType` with a decimal value instead.

3. **Leverage constraints.** Define constraints in the schema (regex patterns, min/max values, enumerations) to ensure data quality.

4. **Use `XdOrdinalType` for ordered categories.** If categories have a meaningful order (severity, priority), use `XdOrdinalType` instead of `XdStringType`.

5. **Embed semantics in labels.** Use the fixed `label` element in schema definitions to provide immutable semantic meaning.

6. **Choose the right temporal granularity.** `XdTemporalType` supports various granularities. Choose the appropriate level (date only, datetime, and so on) based on requirements.

7. **Verify file integrity.** When using `XdFileType`, always include hash values for integrity verification, especially for medical or financial documents.

8. **Make link relationships explicit.** When using `XdLinkType`, specify the relationship semantics (for example, "subject_of", "part_of", "derived_from") for clarity.

## Reference

For the full type reference, inheritance hierarchy, exceptional values, and element-level detail, see the [SDC4 specification](../specification/sdc4-specification.md). The reference model schema (`../schemas/sdc4.xsd`) remains the normative source of truth: if any guidance here conflicts with the schema, the schema wins.
