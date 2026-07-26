# SDC5 Issue: Generalize subject / provider / Participation (openEHR Leftovers)

**Filed**: July 26, 2026
**Priority**: Medium
**Affects**: DMType specification (`subject`, `provider`, `Participation` elements)
**Discovered during**: CordovaOS governance composition mapping (10 government domains)
**Raised by**: T. Cook (RM owner), 2026-07-26

## Problem

`DMType` exposes three party-bearing elements inherited from the openEHR / ISO 13606 lineage:

- `subject` (`PartyType`, `{0,1}`) — the party the data is *about*.
- `provider` (`PartyType`, `{0,unbounded}`) — the party that *provided* it.
- `Participation` (`ParticipationType`, `{0,unbounded}`) — `performer` (Party) + `function` (role) + `mode` + `start`/`end`.

This vocabulary is **clinically shaped**: "subject" (the patient), "provider" (the clinician), "participation" (the care team). For a general-purpose, domain-agnostic reference model, these are:

1. **Semantically narrow.** "subject" and "provider" pre-suppose a two-party clinical framing that does not fit many domains as naturally as a generic party-in-role model. A maritime manifest, a business registration, a property transfer, or a financial transaction has parties in roles (shipper, registrant, grantor/grantee, notary, custodian) that do not map cleanly onto "subject/provider."
2. **Redundant with Participation.** `subject` and `provider` are effectively two pre-named Participations with fixed `function` values. A single generic participation list, with role drawn from a vocabulary, subsumes both and is more uniformly useful.

These are **openEHR leftovers** — a modeling choice carried over from clinical archetypes that a neutral substrate does not need to inherit.

## SDC4 Workaround

None required; SDC4 is frozen and the elements are usable as-is (a non-clinical domain simply treats `subject`/`provider` as conventional roles, or leaves them empty and models everyone as `Participation`). This issue is a **design-direction** note for SDC5, not a correctness gap.

## SDC5 Recommendation

Consider collapsing `subject` / `provider` / `Participation` into a single, generic **party-in-role** structure:

```
DMType
  ...
  ├── participation (0..unbounded)
  │     ├── party  (PartyType)
  │     ├── role   (XdStringType / coded)  -> "subject", "provider", "notary",
  │     │                                      "custodian", "shipper", "registrant", ...
  │     ├── mode   (XdStringType, 0..1)
  │     ├── start  (xs:dateTime, 0..1)
  │     └── end    (xs:dateTime, 0..1)
  ...
```

"Subject" and "provider" become **roles in a vocabulary** rather than hard-coded elements. This removes the clinical bias, unifies the party model, and is more generically useful across domains.

**Weigh against:**
- **Migration cost.** SDC4 instances that use `subject`/`provider` need a mapping: `subject -> participation[role=subject]`, `provider -> participation[role=provider]`. Straightforward but a breaking change (belongs in the SDC5 major bump).
- **Legibility.** Pre-named `subject`/`provider` may aid human readers in domains where that framing *is* natural. Decide whether to keep them as conventional/well-known roles in the recommended vocabulary, or drop them entirely.

## Reference

- CordovaOS Governance Composition Map (`CordovaOS/docs/design/2026-07-26-Governance-Composition-Map.md`), SDC4-native-vs-SDC5 section.
