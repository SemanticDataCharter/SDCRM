# SDC4 Examples

> **Status: the example corpus is being regenerated.** The previous instance files did not
> conform to the current `sdc4.xsd` and have been removed. New, schema-validated examples will
> be added here. In the meantime, the public
> [CordovaOS](https://github.com/Axius-SDC/CordovaOS) `models/` directory contains complete,
> correct SDC4 data models (data-model schema + instance + RDF/SHACL/JSON-LD outputs) generated
> by SDCStudio, and is the best current reference for what conformant SDC4 looks like.

## What an example is

A complete example is a pair:

1. A **data-model schema** `<name>.xsd` — an `xsd:restriction` of `sdc4.xsd` (the reference model). It defines the `dm-`, `mc-`, and `ms-` components of the model.
2. An **instance** `<name>.xml` — data conforming to that data-model schema, including the mandatory `instance_id` (a CUID2).

Instances conform to their **data-model schema**, not to `sdc4.xsd` directly. `sdc4.xsd` is the reference model that data-model schemas restrict.

## Validation

SDC4 is an **XSD 1.1** schema (it uses `xsd:assert`), so `xmllint` (XSD 1.0 only) cannot compile or validate it. Use **[sdcvalidator](https://pypi.org/project/sdcvalidator/)**, the SDC-native validator:

```bash
pip install sdcvalidator
```

```python
import sdcvalidator

# 1) confirm a data-model schema is a compliant restriction of sdc4.xsd
ok, errors = sdcvalidator.validate_sdc4_schema_compliance("your-model.xsd")

# 2) validate an instance against its data-model schema
report = sdcvalidator.SDC4Validator("your-model.xsd", validation="lax").validate_and_report("your-instance.xml")
print(report["valid"])
```

The CI workflow (`.github/workflows/validate-schemas.yml`) confirms `sdc4.xsd` compiles as valid XSD 1.1, checks any `<name>.xsd` in this directory for SDC4 compliance, and validates any `<name>.xml` against its sibling `<name>.xsd`.

## Contributing an example

1. Generate the data-model schema + instance with SDCStudio; this guarantees a conformant restriction.
2. Place them here as a `<name>.xsd` + `<name>.xml` pair, and include the mandatory `instance_id`.
3. Confirm both pass sdcvalidator (above) before opening a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

Examples are MIT licensed.
