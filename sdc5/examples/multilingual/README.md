# SDC5 Multilingual Examples

This directory demonstrates **SDC5's language agnosticism** - one of its primary differentiators in the semantic data modeling landscape.

## Language Agnosticism: A Core Differentiator

Unlike standards tied to English terminology (like Protocol Buffers or FHIR), SDC5 enables organizations to design data models in **any human language** while maintaining:

- **Structural immutability** through CUID-based component identifiers
- **Semantic consistency** via fixed labels in XSD schema definitions
- **Global interoperability** without requiring translation layers

## What Makes This Possible?

### Separation of Structure and Semantics

SDC5 decouples the immutable physical structure from its semantic meaning:

1. **Structure** is defined by CUID identifiers:
   - `mc-clj5x1g8f000008l09j7f6c3d` (Model Component type)
   - `ms-clj5x1g8f000008l09j7f6c3d` (Model Component element)

2. **Semantics** are fixed in the XSD schema:
   ```xml
   <xsd:element name="label" type="xsd:string" fixed="Pressão Arterial"/>
   ```

3. **Instance data** uses structural identifiers:
   ```xml
   <sdc5:ms-clj5x1g8f000008l09j7f6c3d>
     <!-- The label "Pressão Arterial" is in the schema, not here -->
   </sdc5:ms-clj5x1g8f000008l09j7f6c3d>
   ```

## Examples by Language

### Portuguese (Brazil) - `pt-BR/`

- **sinais-vitais-paciente.xml** - Patient vital signs with Brazilian healthcare context
  - Hospital: Hospital das Clínicas de São Paulo
  - Patient ID type: CPF (Cadastro de Pessoas Físicas)
  - Timezone: BRT (UTC-3)
  - Labels: "Pressão Arterial", "Sistólica", "Diastólica", "Frequência Cardíaca"

### French (France) - `fr-FR/`

- **signes-vitaux-patient.xml** - Patient vital signs with French healthcare context
  - Hospital: Hôpital Universitaire de Paris
  - Patient ID type: NIR (Numéro d'Inscription au Répertoire)
  - Timezone: CEST (UTC+2)
  - Labels: "Pression Artérielle", "Systolique", "Diastolique", "Fréquence Cardiaque"

### Spanish (Mexico) - `es-MX/`

- **signos-vitales-paciente.xml** - Patient vital signs with Mexican healthcare context
  - Hospital: Hospital General de México
  - Patient ID type: CURP (Clave Única de Registro de Población)
  - Timezone: CST (UTC-6)
  - Labels: "Presión Arterial", "Sistólica", "Diastólica", "Frecuencia Cardíaca"

## Key Observations

### Same Structure, Different Languages

All three examples use **identical CUID identifiers** for components:

| Component | CUID | pt-BR Label | fr-FR Label | es-MX Label |
|-----------|------|-------------|-------------|-------------|
| Blood Pressure Cluster | `ms-clj5x1g8f000008l09j7f6c3d` | Pressão Arterial | Pression Artérielle | Presión Arterial |
| Systolic Pressure | `ms-clj5x2p4k000108l01a2b3c4d` | Sistólica | Systolique | Sistólica |
| Diastolic Pressure | `ms-clj5x2p4k000108l01a2b3c4e` | Diastólica | Diastolique | Diastólica |
| Heart Rate | `ms-clj5xheart000208l0def456xx` | Frequência Cardíaca | Fréquence Cardiaque | Frecuencia Cardíaca |

### Localized Metadata

Each example includes culturally appropriate metadata:

- **National ID systems**: CPF (Brazil), NIR (France), CURP (Mexico)
- **Institution names**: Brazilian, French, Mexican hospitals
- **Timezones**: UTC-3, UTC+2, UTC-6
- **Language tags**: `pt-BR`, `fr-FR`, `es-MX`

### No Translation Layer Required

Applications processing SDC5 data can:

1. **Query by CUID** to find all blood pressure readings globally
2. **Extract semantics** from fixed labels in the schema
3. **Display in target language** using the schema's fixed labels

**No runtime translation is needed** - the semantic meaning is embedded at design time.

## Global Market Implications

### Language Agnosticism Unlocks 75% of the World

| Market | Population | Primary Languages | SDC5 Advantage |
|--------|-----------|-------------------|----------------|
| **Latin America** | 650M+ | Portuguese, Spanish | Build models in native languages |
| **Europe (non-English)** | 500M+ | French, German, Italian, etc. | GDPR-compliant models in local languages |
| **East Asia** | 1.5B+ | Chinese, Japanese, Korean | Domain experts design in native scripts |
| **Middle East** | 400M+ | Arabic, Hebrew, Farsi | Right-to-left language support |

### Comparison with Competitors

| Standard | Language Support | Translation Required | Domain Expert Design |
|----------|------------------|---------------------|---------------------|
| **Protocol Buffers** | English-centric | Yes (manual) | No (requires English) |
| **FHIR** | English-centric | Yes (via extensions) | No (requires English) |
| **JSON-LD** | English-centric | Yes (via i18n) | No (requires English) |
| **SDC5** | ✅ **Language-agnostic** | ❌ **No** | ✅ **Yes** |

## Use Case: Brazilian SUS (Sistema Único de Saúde)

Brazil's public healthcare system serves **200M+ citizens**. With SDC5:

1. **Domain experts** design models in Portuguese (native language)
2. **Labels are fixed** in XSD schema: "Pressão Arterial", "Temperatura Corporal"
3. **Components are reusable** across all Brazilian healthcare institutions
4. **No translation layer** needed for interoperability
5. **LGPD compliance** (Brazilian GDPR) built into access control tags

**Value Proposition**: Eliminate the "English barrier" preventing Brazilian healthcare informaticists from designing semantic models.

## Technical Details

### Schema Definition (Language-Specific)

Each language has its own XSD schema with fixed labels:

**Portuguese Schema (pt-BR):**
```xml
<xsd:complexType name="mc-clj5x1g8f000008l09j7f6c3d">
  <xsd:complexContent>
    <xsd:restriction base="sdc5:ClusterType">
      <xsd:sequence>
        <xsd4:element name="label" type="xsd:string" fixed="Pressão Arterial" />
        <!-- ... -->
      </xsd:sequence>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

**French Schema (fr-FR):**
```xml
<xsd:complexType name="mc-clj5x1g8f000008l09j7f6c3d">
  <xsd:complexContent>
    <xsd:restriction base="sdc5:ClusterType">
      <xsd:sequence>
        <xsd:element name="label" type="xsd:string" fixed="Pression Artérielle" />
        <!-- ... -->
      </xsd:sequence>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

**Spanish Schema (es-MX):**
```xml
<xsd:complexType name="mc-clj5x1g8f000008l09j7f6c3d">
  <xsd:complexContent>
    <xsd:restriction base="sdc5:ClusterType">
      <xsd:sequence>
        <xsd:element name="label" type="xsd:string" fixed="Presión Arterial" />
        <!-- ... -->
      </xsd:sequence>
    </xsd:restriction>
  </xsd:complexContent>
</xsd:complexType>
```

**Critical Insight**: The CUID (`mc-clj5x1g8f000008l09j7f6c3d`) remains identical across all three schemas. Only the fixed label changes.

### Instance Data (Language-Independent)

All instance documents reference the same CUID:

```xml
<sdc5:ms-clj5x1g8f000008l09j7f6c3d>
  <!-- Structural identifier is language-independent -->
  <sdc5:ms-clj5x2p4k000108l01a2b3c4d>
    <sdc5:xdquantity-value>120</sdc5:xdquantity-value>
    <!-- ... -->
  </sdc5:ms-clj5x2p4k000108l01a2b3c4d>
</sdc5:ms-clj5x1g8f000008l09j7f6c3d>
```

## Marketing Message

### For Academic Audiences (Bluesky):

> "Why is FHIR stuck with English labels? SDC5 lets Brazilian informaticists design in Portuguese, French researchers in French, Japanese hospitals in Kanji. Same CUID structure, native semantics. That's language agnosticism."

### For Commercial Audiences (LinkedIn):

> "Unlock global markets with SDC5's language-agnostic data models. Design once in your team's native language, deploy globally without translation overhead. From Brazilian SUS to French GDPR compliance - SDC5 speaks your language."

## Future Examples

Additional language examples planned:

- **Japanese** (`ja-JP`) - Kanji/Hiragana labels for healthcare
- **German** (`de-DE`) - Manufacturing specifications
- **Arabic** (`ar-SA`) - Government citizen records
- **Mandarin** (`zh-CN`) - Financial transaction records

## References

- **SDC5 Specification**: [specs/sdc4-markdown/index.md](../../specs/sdc4-markdown/index.md)
- **Section 4.4 (Reusability)**: Component immutability via CUID naming
- **Section 4.3 (Semantic Grounding)**: Fixed labels in XSD schemas

---

**Key Takeaway**: Language agnosticism is not just a feature - it's SDC5's **primary competitive differentiator** for global adoption.
