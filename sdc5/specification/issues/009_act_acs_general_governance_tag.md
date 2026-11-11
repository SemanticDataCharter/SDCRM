# SDC5 Issue: `act` / `acs` Are a General Governance Tag; the Spec Text Says "Access Control"

**Filed**: November 11, 2026
**Priority**: Medium (spec clarification; one open cardinality question)
**Affects**: `XdAnyType/act` and `DMType/acs` documentation; modeller guides
**Discovered during**: Governed event (logging) mapping, Issue 008
**Raised by**: T. Cook (RM owner), 2026-11-11

## Problem

The intended semantics of `act` are general: **`act` can be used in any context,
as the modeller defines it.** Its meaning comes entirely from the controlled
vocabulary the data model names in `DMType/acs`. That vocabulary may hold access
classifications, but equally retention classes, handling caveats, data-sensitivity
levels, use restrictions, or any other governance tag the model needs.

The current documentation reads narrower than that:

- `act`: "Access Control Tag. If this is used it must contain a valid term from the
  Access Control System linked to by the containing Data Model."
- `acs`: "Identifier of an externally held access control system. This URI can be
  an ontology, vocabulary or descriptive document URI link."

A reader, human or machine, concludes that `act` is for access control only, then
reports "no slot for retention or classification tags" as a gap. That has already
happened in a logging-governance review: the retention and policy tags in the event
contract were judged unmodellable when `act` covers them.

## SDC4 position (no change needed to use it)

SDC4 already supports the general use. A model points `acs` at its own controlled
vocabulary, and every component's `act` carries a term from it. Nothing in the
schema restricts the vocabulary to access control.

## SDC5 recommendation

1. **Rewrite the documentation** for both elements:
   - `acs`: the link to the controlled vocabulary for this data model's governance
     tags (`act`). The vocabulary defines what the tags mean: access, classification,
     retention, handling, or any other governance dimension.
   - `act`: a governance tag whose value must be a term from the vocabulary named in
     the containing Data Model's `acs`.
2. **Keep the element names** (`act`, `acs`) for continuity with SDC4. Explain in the
   spec that the expansion "Access Control Tag" is historical and the element is
   general.
3. **Guide text and an example** showing an `acs` vocabulary that covers more than
   one dimension (for example, sensitivity plus retention class).

## Open question: one tag or several per component

`act` is `0..1` per component, so a component carries one term. When a model needs
several independent dimensions on the same component (a sensitivity level *and* a
retention class), there are two options:

- **(a) Keep `0..1`; compound terms in the vocabulary.** The `acs` vocabulary defines
  combined terms (for example, `confidential-retain-7y`), or terms that themselves
  carry properties. No RM change; the vocabulary designer carries the complexity.
- **(b) Relax to `0..unbounded`.** Each term is one dimension. Simpler vocabularies,
  but conflict rules are needed (two terms from the same dimension) and every
  processor that reads `act` must handle a list.

Inclination: **(a)**, unless a concrete model shows compound terms to be
unworkable. Relaxing the upper bound would be backward-compatible for existing
instances but not for processors that assume one value.

## Domain neutrality check

Neutral. The RM states only that the tag is governed by the model's vocabulary; it
defines no tag values.

## Compatibility

Documentation-only for SDC4 users (meaning unchanged). Option (b), if chosen, is an
SDC5 cardinality change.

## Related

Issue 008 (governed event pattern).
