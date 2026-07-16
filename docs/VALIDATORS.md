# Validators and XSD 1.1 Conformance

This document explains a specific point of XSD 1.1 conformance that affects how SDC4 data models validate across different XML Schema processors. It exists because some widely used validators reject a construct that the XSD 1.1 specification permits, and implementers need a clear, citable statement of the correct behaviour.

## Table of Contents

- [Summary](#summary)
- [The Construct](#the-construct)
- [Why It Is Valid XSD 1.1](#why-it-is-valid-xsd-11)
- [Processor Status](#processor-status)
- [Guidance for Implementers](#guidance-for-implementers)
- [References](#references)

---

## Summary

SDC4 data models restrict the abstract substitution-group head `sdc4:Item` down to the specific member elements a model defines. For a cluster, the reference model content model `label?, Item*` is restricted to `label?, ms-A?, ms-B?, ...`, where each `ms-*` is a member of `Item`'s substitution group.

This is a valid restriction under **XSD 1.1 Part 1, §3.4.6.4 "Content type restricts (Complex Content)"**. XSD 1.1 removed the XSD 1.0 particle-restriction machinery (the rule historically known as *Particle Valid (Restriction)* / *NameAndTypeOK*, which required element names to match) and replaced it with a rule stated in terms of the instances a content model accepts.

Some processors still apply the removed XSD 1.0 rule and therefore reject the construct. That rejection is a processor limitation, not a defect in the schema. A conformant XSD 1.1 processor accepts it, and a W3C reference implementation (Apache Xerces-J, XML Schema 1.1) does accept it.

---

## The Construct

The reference model declares an abstract head and its members. In simplified form:

```xml
<!-- Reference model (sdc4.xsd) -->
<xsd:complexType abstract="true" name="ItemType"/>
<xsd:element abstract="true" name="Item" type="sdc4:ItemType"/>

<xsd:complexType name="ClusterType">
  <xsd:complexContent>
    <xsd:extension base="sdc4:ItemType">
      <xsd:sequence>
        <xsd:element name="label" type="xsd:string" minOccurs="0"/>
        <xsd:element ref="sdc4:Item" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:sequence>
    </xsd:extension>
  </xsd:complexContent>
</xsd:complexType>
```

A generated data model declares its components as substitution-group members of `sdc4:Item`, then restricts a cluster to exactly those members:

```xml
<!-- Data model (dm-*.xsd) -->
<xsd:element name="ms-A" substitutionGroup="sdc4:Item" type="sdc4:mc-A"/>
<xsd:element name="ms-B" substitutionGroup="sdc4:Item" type="sdc4:mc-B"/>

<xsd:complexType name="mc-cluster">
  <xsd:complexContent>
    <xsd:restriction base="sdc4:ClusterType">
      <xsd:sequence>
        <xsd:element name="label" type="xsd:string" minOccurs="0"/>
        <xsd:element ref="sdc4:ms-A" minOccurs="0" maxOccurs="1"/>
        <xsd:element ref="sdc4:ms-B" minOccurs="0" maxOccurs="1"/>
      </xsd:sequence>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

The same pattern applies to the payload slot of `sdc4:DMType`, which carries a single `sdc4:Item` that a data model restricts to one specific member.

This is the design the SDC reference model and its predecessor (S3Model) have used since their earliest published schemas.

---

## Why It Is Valid XSD 1.1

XSD 1.1 Part 1, §3.4.6.4 defines when a content type R (the restriction) restricts a content type B (the base). The relevant conditions are:

1. **Every sequence of element information items that is locally valid with respect to R is also locally valid with respect to B.**
2. **For every element in such a sequence, B's default binding for that element subsumes the binding defined by R.**

Apply this to the cluster case, where R offers `ms-A` where B offers the abstract head `Item`:

- **Condition 1 holds.** An instance permitted by R contains an `<ms-A>` element. Because `ms-A` is declared in the substitution group of `Item`, that same instance is accepted by B, whose content model expects `Item`. Substitution-group members are accepted wherever their head is expected. Every instance R accepts, B also accepts.
- **Condition 2 holds.** When `<ms-A>` is validated against either R or B, its governing element declaration resolves to the same declaration, `ms-A`. A declaration subsumes itself, so the binding condition is satisfied.

Both conditions are met, so R is a valid restriction of B.

The XSD 1.0 rule that some processors still apply required the restricting particle's element name to match the base particle's element name (`ms-A` would have had to be `Item`). XSD 1.1 does not contain that rule. The name-matching constraint (`NameAndTypeOK`) and the surrounding particle-restriction recursion (`RecurseAsIfGroup`, `NSRecurseCheckCardinality`) are absent from XSD 1.1 Part 1. The governing text is the instance-based rule in §3.4.6.4.

Substitution and derivation are distinct here, and both are satisfied:

- The member element `ms-A` is substitutable for `Item` in instances because it is in `Item`'s substitution group (an extension of `ItemType` is a valid substitution-group member).
- The restriction of the cluster content type is valid because §3.4.6.4's instance-subset condition is met, not because of any name match.

---

## Processor Status

The following reflects observed behaviour when validating SDC4 (and structurally identical S3Model) schemas as XSD 1.1.

| Processor | Result | Basis |
|-----------|--------|-------|
| Apache Xerces-J, XML Schema 1.1 build | Accepts | Implements §3.4.6.4; W3C reference implementation |
| xmlschema (Python) | Rejects | Applies the removed XSD 1.0 particle-restriction rule |
| Saxon-EE | Rejects when run as XSD 1.0; confirm the 1.1 flag before drawing conclusions | Defaults to XSD 1.0; `vc:minVersion="1.1"` does not switch the mode |
| Some recent Oxygen builds (bundled Xerces) | Rejects in 1.1 mode | Applies the removed XSD 1.0 particle-restriction rule |

Processors that accept the construct agree with both the specification text and a reference implementation. Processors that reject it are applying a rule XSD 1.1 removed. When a validator reports the SDC construct as an "illegal restriction" or "not a valid restriction of the particle of the base," this is the cause.

Note also that `xmllint` (libxml2) and lxml validate only XSD 1.0 and cannot process SDC4 schemas as XSD 1.1 at all; the reference model uses XSD 1.1 features including `xsd:assert`.

---

## Guidance for Implementers

- Validate SDC4 data models with a conformant XSD 1.1 processor. Apache Xerces-J's XML Schema 1.1 build is a reference for correct behaviour.
- When using Saxon, enable XSD 1.1 explicitly (for example `-xsdversion:1.1`). The presence of `vc:minVersion="1.1"` in the schema does not by itself select 1.1 mode.
- `sdcvalidator`, the SDC ecosystem validator, implements the §3.4.6.4 semantics so that the substitution-group restriction is accepted while genuinely invalid restrictions (restricting to a non-member element, widening cardinality, or using a type that is not validly derived) continue to fail.
- If a downstream toolchain rejects a valid SDC4 schema on this construct, the correct resolution is to validate with a conformant XSD 1.1 processor. The schema is correct; cite §3.4.6.4.

---

## References

- W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures, §3.4.6.4 "Content type restricts (Complex Content)". https://www.w3.org/TR/xmlschema11-1/#derivation-ok-restriction
- W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures, §3.9 (particles and substitution groups). https://www.w3.org/TR/xmlschema11-1/
- Apache Xerces-J, XML Schema 1.1 support. https://xerces.apache.org/xerces2-j/

---

*This note is descriptive. The normative source of truth is `sdc4/schemas/sdc4.xsd` and the XSD 1.1 specification it conforms to.*
