# SDC4 Datatype Mapping

This guide maps common source datatypes (CSV/spreadsheet columns, SQL types, JSON/JavaScript values, and native types in Python, Java, and C#) to the SDC4 extended (Xd*) types, so you can pick the right type when modeling existing data. For the full type reference, constraints, and structure of each Xd* type, see Appendix A of the [SDC4 specification](../specification/sdc4-specification.md).

## CSV / Spreadsheet to Xd* Types

| CSV Data | Example Value | Xd* Type | Reasoning |
|----------|---------------|----------|-----------|
| Name, Address, Description | "John Doe" | XdString | Free-text character data |
| Country Code, Product SKU | "US", "SKU-12345" | XdString (with enumeration or pattern) | Controlled codes |
| Enabled, Active, Consented | "true", "yes", "1" | XdBoolean | Boolean logic |
| Quantity, Count, Number of Items | 42, 1000 | XdCount | Non-negative integers |
| Price, Weight, Temperature | 19.99, 72.5 | XdQuantity | Decimal with units |
| Date, DateTime, Timestamp | "2025-11-09", "2025-11-09T15:30:00Z" | XdTemporal | Temporal data |
| Priority, Severity, Rating | "High", "Severe" | XdOrdinal | Ordered categories |
| Email, URL, Reference ID | "user@example.com" | XdString (with regex pattern) | Formatted strings |

## Database Column (SQL) to Xd* Types

| SQL Type | Xd* Type | Notes |
|----------|----------|-------|
| VARCHAR, CHAR, TEXT | XdString | General text |
| VARCHAR (with normalized whitespace) | XdToken | Machine-readable codes/identifiers |
| BOOLEAN, BIT, TINYINT(1) | XdBoolean | Boolean values |
| INTEGER, SMALLINT, BIGINT, INT (with CHECK >= 0) | XdCount | Non-negative counts; use XdQuantity if negative values allowed |
| DECIMAL, NUMERIC, MONEY | XdQuantity | Quantities with required units |
| REAL, FLOAT(24) | XdFloat | Single-precision floating-point |
| DOUBLE PRECISION, FLOAT, FLOAT(53) | XdDouble | Double-precision floating-point |
| DATE, TIME, TIMESTAMP, DATETIME, TIMESTAMPTZ | XdTemporal | Temporal data |
| SMALLINT or ENUM (ordered), VARCHAR with lookup table | XdOrdinal | Ordered enumerations (code + label pairs) |
| BLOB, BYTEA, VARBINARY | XdFile | Binary data |
| Foreign Key, URI column | XdLink | References to other entities |
| Two columns (lower_bound, upper_bound), or RANGE types (PostgreSQL) | XdInterval | Ranges/bounds |

## JSON/JavaScript and Programming-Language Types to Xd* Types

| Xd* Type | JSON/JavaScript | Python | Java | C# |
|----------|-----------------|--------|------|-----|
| XdString | `string` | `str` | `String` | `string` |
| XdToken | `string` | `str` | `String` | `string` |
| XdBoolean | `boolean` | `bool` | `Boolean`, `boolean` | `bool`, `Boolean` |
| XdCount | `number` (integer) | `int` (>= 0) | `Integer`, `Long` (>= 0) | `int`, `long` |
| XdQuantity | `number` | `Decimal`, `float` | `BigDecimal`, `Double` | `decimal` |
| XdFloat | `number` | `float` | `Float`, `float` | `float`, `Single` |
| XdDouble | `number` | `float` | `Double`, `double` | `double`, `Double` |
| XdTemporal | `string` (ISO 8601) | `datetime.date`, `datetime.time`, `datetime.datetime` | `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime` | `DateTime`, `DateOnly`, `TimeOnly` |
| XdOrdinal | `number` or `string` | `int` or `str` (often `Enum`) | `Enum` | `enum` |
| XdLink | `string` (URI/URL), object reference | Foreign key, URI string | `URI`, `URL`, reference | `Uri`, reference |
| XdFile | Base64 string, file path | `bytes`, file path string | `byte[]`, `File`, `Path` | `byte[]`, file path |
| XdInterval | Object with `min` and `max` properties | Tuple, custom Range class | Custom Range class | Custom Range struct |

Notes:

- For financial data, prefer **XdQuantity** with a DECIMAL source over XdFloat/XdDouble to avoid floating-point rounding.
- Use **XdCount** for non-negative whole-number counts and **XdQuantity** for decimal measurements that carry units (units are required on XdQuantity).
- Choose **XdOrdinal** (not XdString) when categories have a meaningful order (severity, priority, Likert scales).
- Choose **XdToken** (not XdString) when whitespace normalization is desired for codes/identifiers.

## Corrected Instance Examples

The SDC4 namespace is `https://semanticdatacharter.com/ns/sdc4/` (bound to the `sdc4:` prefix below). Scalar Xd types carry a type-prefixed `xd<type>-value` (with optional `xd<type>-units` / `xd<type>-language`); structured types carry semantically named parts. Element names below are verified against `sdc4/schemas/sdc4.xsd`.

XdCount (non-negative integer with units):

```xml
<sdc4:ms-share-quantity>
  <sdc4:label>Number of Shares</sdc4:label>
  <sdc4:xdcount-value>100</sdc4:xdcount-value>
  <sdc4:xdcount-units>
    <sdc4:xdstring-value>shares</sdc4:xdstring-value>
  </sdc4:xdcount-units>
</sdc4:ms-share-quantity>
```

XdQuantity (decimal with required units):

```xml
<sdc4:ms-systolic-bp>
  <sdc4:label>Systolic Blood Pressure</sdc4:label>
  <sdc4:xdquantity-value>120</sdc4:xdquantity-value>
  <sdc4:xdquantity-units>
    <sdc4:xdstring-value>mmHg</sdc4:xdstring-value>
  </sdc4:xdquantity-units>
</sdc4:ms-systolic-bp>
```

XdBoolean (structured: a `true-value`/`false-value` choice carrying the enumerated option label):

```xml
<sdc4:ms-consent-given>
  <sdc4:label>Patient Consent Given</sdc4:label>
  <sdc4:true-value>Granted</sdc4:true-value>
</sdc4:ms-consent-given>
```

XdTemporal (ISO 8601 datetime):

```xml
<sdc4:ms-measurement-time>
  <sdc4:label>Measurement Timestamp</sdc4:label>
  <sdc4:xdtemporal-datetime>2025-11-09T14:30:00Z</sdc4:xdtemporal-datetime>
</sdc4:ms-measurement-time>
```

XdOrdinal (structured: `ordinal` code + `symbol` label):

```xml
<sdc4:ms-pain-level>
  <sdc4:label>Pain Severity</sdc4:label>
  <sdc4:ordinal>2</sdc4:ordinal>
  <sdc4:symbol>Moderate</sdc4:symbol>
</sdc4:ms-pain-level>
```

XdLink (structured: `link` / `relation` / `relation-uri`):

```xml
<sdc4:ms-patient-reference>
  <sdc4:label>Related Patient</sdc4:label>
  <sdc4:link>dm-patient-clj5x9z...</sdc4:link>
  <sdc4:relation>subject_of</sdc4:relation>
  <sdc4:relation-uri>http://purl.org/dc/terms/subject</sdc4:relation-uri>
</sdc4:ms-patient-reference>
```

XdFile (structured: bare `size` / `media-type` / `hash-result` / `hash-function` and a `uri` | `media-content` choice):

```xml
<sdc4:ms-patient-photo>
  <sdc4:label>Patient Photograph</sdc4:label>
  <sdc4:size>245760</sdc4:size>
  <sdc4:media-type>image/jpeg</sdc4:media-type>
  <sdc4:hash-result>a3f5b...</sdc4:hash-result>
  <sdc4:hash-function>SHA-256</sdc4:hash-function>
  <sdc4:uri>file:///patient-photos/12345.jpg</sdc4:uri>
</sdc4:ms-patient-photo>
```

XdInterval (structured: `lower` / `upper` bounds using `invl-*` value elements, inclusion and boundedness flags, optional `interval-units`):

```xml
<sdc4:ms-normal-systolic-range>
  <sdc4:label>Normal Systolic BP Range</sdc4:label>
  <sdc4:lower>
    <sdc4:invl-decimal>90</sdc4:invl-decimal>
  </sdc4:lower>
  <sdc4:upper>
    <sdc4:invl-decimal>120</sdc4:invl-decimal>
  </sdc4:upper>
  <sdc4:lower_included>true</sdc4:lower_included>
  <sdc4:upper_included>true</sdc4:upper_included>
  <sdc4:lower_bounded>true</sdc4:lower_bounded>
  <sdc4:upper_bounded>true</sdc4:upper_bounded>
  <sdc4:interval-units>
    <sdc4:units-name>mmHg</sdc4:units-name>
    <sdc4:units-uri>http://unitsofmeasure.org/ucum#mm[Hg]</sdc4:units-uri>
  </sdc4:interval-units>
</sdc4:ms-normal-systolic-range>
```

## Full Type Reference

This guide is a quick mapping aid. For the authoritative definition of each type, including available constraints, structure, use cases, the type-selection decision tree, list types, and exceptional values, see **Appendix A** ("Xd* Datatype Reference") of the [SDC4 specification](../specification/sdc4-specification.md). The reference model schema, `sdc4/schemas/sdc4.xsd`, is the normative source of truth.
