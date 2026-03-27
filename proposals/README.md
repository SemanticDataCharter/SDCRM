# SDC5 Planning -- Proposals

This directory collects candidate features, formalizations, and architectural ideas for a future SDC5 reference model. Nothing here is committed to implementation. These are ideas under evaluation.

## Ground Rules

1. **Domain neutrality is non-negotiable.** Any proposal that introduces domain-specific concepts into the reference model will be rejected. SDC stays universally applicable.
2. **Restriction-only in data models is non-negotiable.** Data models use xsd:restriction only, never xsd:extension. The reference model itself uses extension to build the type hierarchy. Proposals for new RM types may use extension; proposals that affect how data models specialize those types must use restriction.
3. **Backward compatibility matters.** SDC5 data models must coexist with SDC4 data models in the same system. That's the permanence guarantee.
4. **Each proposal stands alone.** One idea per file. Include rationale, impact analysis, and who proposed it.

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
