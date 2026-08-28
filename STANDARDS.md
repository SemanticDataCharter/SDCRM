# Standards implemented across the SDC stack

Every standard the Semantic Data Charter implementation builds on, with the file,
namespace or module that proves it. This exists so that a claim like "built on
open standards" resolves to something a sceptic can open, rather than to a number
in a marketing table.

**Scope.** Four repositories: this one (SDCRM), [`sdcvalidator`], [`sdcgovernance`],
and SDCStudio, including the artefacts SDCStudio generates.

**Evidence rule.** A standard is listed only where there is a namespace URI, an
import, a module that implements it, or an explicit statement in that project's
own README. **A mention in prose is not evidence.** Rows that failed this test are
recorded at the bottom, so the omission is deliberate and reviewable.

Last verified: 2026-08-28.

---

## W3C — 13

| Standard | Where | Evidence |
|---|---|---|
| XML Schema 1.1 | SDCRM, sdcvalidator | `sdc4/schemas/sdc4.xsd`; `XMLSchema-versioning` namespace |
| RDF 1.1 | all four | `rdf-syntax-ns#` |
| RDF Schema | all four | `rdf-schema#` |
| OWL 2 | SDCRM, SDCStudio | ontology output |
| SHACL | sdcgovernance, SDCStudio | `ns/shacl#`; cross-entity constraint validation |
| SPARQL 1.1 | SDCRM, sdcgovernance, SDCStudio | query generation |
| SKOS | SDCRM, sdcgovernance, SDCStudio | `skos/core#` |
| PROV-O | sdcgovernance, SDCStudio | `ns/prov#`; `provenance.py` |
| PROV-DM | sdcgovernance | `provenance.py` |
| JSON-LD | SDCRM, SDCStudio | generated output |
| Verifiable Credentials Data Model 2.0 | sdcgovernance | attestation; `docs/test-harness/attestation.md` |
| Activity Streams 2.0 | sdcgovernance | `provenance.py`, activity type vocabulary |
| Data Privacy Vocabulary (DPV) | sdcgovernance | retention policy; README "Standards" |

**Concepts only, not conformance:** `sdcgovernance/src/sdcgovernance/workflow.py`
borrows *state* and *transition* from **W3C SCXML** without claiming SCXML
conformance. The code says so, and so does this table.

## ISO and ISO/IEC — 5

| Standard | Where | Evidence |
|---|---|---|
| ISO 21090 (exceptional values) | all four | the EV recovery path in `sdcvalidator` |
| ISO 8601 (date and time) | SDCRM, sdcgovernance, SDCStudio | schema types |
| ISO/IEC 21838-2 (BFO) | SDCRM, SDCStudio | ontology alignment |
| ISO 15836 (Dublin Core) | SDCRM, sdcgovernance, SDCStudio | `purl.org/dc/elements/1.1` |
| ISO/IEC 39075 (GQL) | SDCStudio | GQL `CREATE` statement output |

## OASIS — 1

| Standard | Where | Evidence |
|---|---|---|
| XACML | sdcgovernance | PERMIT / DENY / INDETERMINATE decision semantics |

## OMG — 1

| Standard | Where | Evidence |
|---|---|---|
| DMN (Decision Model and Notation) | sdcgovernance | `decision.py`; `docs/test-harness/decision-tables.md` |

## IETF — 2

| Standard | Where | Evidence |
|---|---|---|
| RFC 8785 (JSON Canonicalization) | sdcgovernance | `receipts.py`, `mtcp.py` — described as *RFC 8785-aligned* |
| BCP 47 / RFC 3066 (language tags) | SDCRM, SDCStudio | `dm-language`, `xsd:language` |

## IEEE — 1

| Standard | Where | Evidence |
|---|---|---|
| IEEE 754 | SDCRM | floating-point numeric types |

## IANA — 1

| Standard | Where | Evidence |
|---|---|---|
| Media type and character-set registries | SDCRM | encoding and media-type fields in `sdc4.xsd` |

## NIST / FIPS — 2

| Standard | Where | Evidence |
|---|---|---|
| FIPS 180-4 (SHA-256) | sdcgovernance | hash-chained decision receipts |
| FIPS 186-4 (ECDSA P-256) | sdcgovernance, SDCStudio | local signing backend |

---

## Total: 26 formal standards from eight bodies

W3C 13 · ISO/IEC 5 · OASIS 1 · OMG 1 · IETF 2 · IEEE 1 · IANA 1 · NIST 2

Plus eight open specifications that are not from a standards body but are load
bearing: **schema.org**, **FOAF**, **UCUM**, **JSON Schema**, **JSON-RPC 2.0**
(the MCP transport), **OpenAPI**, **SemVer**, **CUID2**.

## Counting honestly

Per repository, not additive — the same standard appears in several:

| Repository | Formal standards |
|---|---|
| SDCRM | 12 |
| sdcvalidator | 6 |
| sdcgovernance | 15 |
| SDCStudio (incl. generated output) | 14 |

**Do not attribute the stack total to one library.** `sdcgovernance` is the
richest single component and evidences 15 formal standards; its own README
lists 9 as core. Saying any one library implements "20+" overstates it.

## Rejected, and why

| Candidate | Why not |
|---|---|
| ISO 20022 | Named in `sdc4-specification.md` only as an *example of a domain standard SDC could model*. Not implemented. |
| ISO/IEC 11179 | Appears only inside a user upload under SDCStudio `mediafiles/`. Not ours. |
| ISO 27001 | SDCStudio compliance documentation, not something the software implements. |
| W3C SCXML | Concepts borrowed, conformance not claimed. Listed above as such rather than counted. |

## Keeping this true

Re-verify when a dependency or an emitted format changes. The website's numeric
claims are checked by `tools/stat-sweep/sweep.py` in the site repository; this
file is what that check should point at.
