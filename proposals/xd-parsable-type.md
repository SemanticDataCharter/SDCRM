# XdParsable Type for Structured Text Content

- **Proposed by**: Tim Cook, 2026-03-29
- **Status**: PROPOSED
- **Inspired by**: openEHR DV_PARSABLE (Thomas Beale, openEHR Reference Model)

## Summary

Add an XdParsable type to the reference model for carrying inline structured text content with a declared grammar. This fills the gap between XdString (text without grammar declaration) and XdFile (binary blob with media type but opaque content).

## Motivation

SDC4's XdFile can store any payload, but it treats content as an opaque binary blob. For structured text formats -- SVG, MathML, GeoJSON, JSON, CSV, clinical guideline languages, embedded XML fragments -- the content is parsable and potentially validatable, but XdFile discards that capability by treating it as binary.

Use cases across domains:

- **Engineering/industrial**: SVG diagrams of circuit layouts, piping schematics, or assembly instructions embedded in a data model instance. The SVG is W3C XML with its own namespace and schema -- it can be validated, queried, and transformed using standard XML tooling, but only if carried as parsable text.
- **Scientific**: MathML formulas embedded in research data instances. LaTeX expressions in publication metadata.
- **Geospatial**: GeoJSON geometry objects embedded inline rather than referenced as external files.
- **Healthcare**: Clinical guideline expressions (GDL, Arden Syntax), care pathway definitions, structured clinical notes in markdown.
- **Finance**: Inline JSON configuration for trading rules, regulatory reporting templates in CSV format.
- **Any domain**: Embedded XML fragments, JSON payloads, structured markdown, YAML configurations.

In all cases, the content is text that follows a declared grammar. The consuming system can parse it if it understands the formalism. If it doesn't, it can still store and transmit it faithfully as text.

## Proposed Design

### XdParsable Type (Reference Model level -- uses extension from XdAnyType)

```xml
<xs:complexType name="XdParsableType">
    <xs:complexContent>
        <xs:extension base="sdc5:XdAnyType">
            <xs:sequence>
                <xs:element name="parsable-value" type="xs:string"/>
                <xs:element name="formalism" type="xs:string"/>
                <xs:element name="formalism-version" type="xs:string"
                            minOccurs="0"/>
            </xs:sequence>
        </xs:extension>
    </xs:complexContent>
</xs:complexType>
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `parsable-value` | xs:string | Yes | The inline text content (SVG markup, JSON, CSV, MathML, etc.) |
| `formalism` | xs:string | Yes | The content grammar identifier. Media type (e.g., `image/svg+xml`, `application/json`, `text/csv`) or namespace URI (e.g., `http://www.w3.org/2000/svg`) |
| `formalism-version` | xs:string | No | Version of the grammar, for formalisms that version independently (e.g., SVG 1.1 vs SVG 2.0) |

### Inheritance

XdParsable extends XdAnyType, inheriting:
- Location (spatio-temporal coordinates)
- ExceptionalValue (typed absence via NULL Flavors)
- Access control (`act`, `acs`)
- Semantic links (pred_obj)

### How Data Models Use It

Data models specialize XdParsable via xsd:restriction to constrain the formalism:

```xml
<!-- A component that carries only SVG content -->
<xs:complexType name="mc-circuit-diagram">
    <xs:complexContent>
        <xs:restriction base="sdc5:XdParsableType">
            <xs:sequence>
                <xs:element name="parsable-value" type="xs:string"/>
                <xs:element name="formalism" type="xs:string" fixed="image/svg+xml"/>
            </xs:sequence>
        </xs:restriction>
    </xs:complexContent>
</xs:complexType>
```

The `fixed` attribute on formalism means this component only accepts SVG. The schema enforces the content type at validation time.

## Comparison to XdFile and XdString

| Capability | XdString | XdFile | XdParsable |
|-----------|----------|--------|------------|
| Carries text | Yes | No (binary) | Yes |
| Declares content grammar | No | Yes (media type) | Yes (formalism + version) |
| Content is inline | Yes | No (encoded blob) | Yes |
| Content is parsable by consuming system | No (no grammar declared) | No (opaque binary) | Yes |
| Constrainable by data model | Length, pattern | Media type, size | Formalism, version |
| Suitable for SVG/MathML/GeoJSON | Technically but semantically wrong | Yes but treats as blob | Yes -- designed for this |

## Domain Neutrality Check

Yes. Structured text content with declared grammars is domain-neutral. Every domain has parsable text payloads. The type prescribes no domain content -- it only declares that the content is structured text and identifies what grammar it follows.

## Compatibility

New type in SDC5 only. No impact on SDC4. SDC4 instances that currently use XdFile for structured text content would naturally migrate to XdParsable in SDC5, with the formalism field making the content grammar explicit rather than implicit.

## Open Questions

- Should `parsable-value` use `xs:string` or a more specific type? For XML content (SVG, MathML), `xs:anyType` with embedded elements would preserve XML structure. But this would not work for non-XML formalisms (JSON, CSV, LaTeX). `xs:string` with CDATA wrapping is the most portable approach.
- Should the type support an optional `schema-uri` field that points to the grammar's formal schema (e.g., the SVG XSD, a JSON Schema URI)? This would enable downstream validation but adds complexity.
- Should there be a maximum length constraint at the RM level, or should that be left entirely to data model restrictions?
- Naming: `XdParsable` follows the openEHR convention. Alternatives: `XdStructuredText`, `XdFormalism`, `XdInlineContent`. `XdParsable` is most descriptive of what the type enables.

## References

- openEHR Reference Model: `DV_PARSABLE` (carried `value` + `formalism` fields)
- W3C SVG: `http://www.w3.org/2000/svg` (namespace, inline XML)
- W3C MathML: `http://www.w3.org/1998/Math/MathML` (namespace, inline XML)
- GeoJSON: RFC 7946 (structured text, not XML)
