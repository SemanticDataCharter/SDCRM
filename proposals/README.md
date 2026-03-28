# SDC5 Planning -- Proposals

This directory collects candidate features, formalizations, and architectural ideas for SDC5. The `sdc5/` directory now exists at the repository root with the base namespace in place (see [`sdc5/schemas/sdc5.xsd`](../sdc5/schemas/sdc5.xsd)). Proposals here guide what changes beyond the namespace migration.

## Ground Rules

1. **Domain neutrality is non-negotiable.** Any proposal that introduces domain-specific concepts into the reference model will be rejected. SDC stays universally applicable.
2. **Restriction-only in data models is non-negotiable.** Data models use xsd:restriction only, never xsd:extension. The reference model itself uses extension to build the type hierarchy. Proposals for new RM types may use extension; proposals that affect how data models specialize those types must use restriction.
3. **Coexistence via namespacing.** SDC5 uses `xmlns:sdc5="https://semanticdatacharter.com/ns/sdc5/"` alongside SDC4's `xmlns:sdc4="https://semanticdatacharter.com/ns/sdc4/"`. Both versions coexist in the same system. SDC4 data models and instances remain valid forever. That's the permanence guarantee.
4. **Version implications.** A new reference model version bumps the major version across the entire SDC ecosystem. All tooling (SDCStudio, SDC_Agents, SDCObsidianTemplate, etc.) will carry `5.x.x` semantic versioning when SDC5 ships.
5. **Each proposal stands alone.** One idea per file. Include rationale, impact analysis, and who proposed it.

## Proposal Template

Each proposal should include:

- **Title**: Short name
- **Proposed by**: Who and when
- **Summary**: What it is in 2-3 sentences
- **Motivation**: Why this matters -- what problem does it solve?
- **Impact on RM**: What changes in the reference model? New types? Modified constraints? New metadata?
- **Domain neutrality check**: Does this stay domain-neutral? If not, it belongs in a domain-specific extension, not the RM.
- **Compatibility**: How does this coexist with SDC4?
- **Status**: PROPOSED | UNDER REVIEW | ACCEPTED | REJECTED | DEFERRED

## Current Proposals

| File | Title | Proposed By | Status |
|------|-------|------------|--------|
| [confidence-over-absence-type.md](confidence-over-absence-type.md) | Confidence Distribution Over Absence Types | Kris Welford (external) | PROPOSED |
| [geometric-formalization.md](geometric-formalization.md) | Formal Geometric Description of the Restriction Lattice | Kris Welford (external) / Tim Cook | PROPOSED |
| [markov-blanket-formalization.md](markov-blanket-formalization.md) | Markov Blanket as Data Model Boundary Definition | Tim Cook | PROPOSED |
| [3d-location-model.md](3d-location-model.md) | 3D Location Model for XdAnyType | Tim Cook | PROPOSED |
