# Formal Geometric Description of the Restriction Lattice

- **Proposed by**: Kris Welford (external) / Tim Cook, 2026-03-27
- **Status**: PROPOSED

## Summary

Formally describe the SDC restriction lattice in geometric and topological terms. The lattice already has these properties -- this proposal is about documenting them mathematically, not changing the implementation.

## Motivation

Kris Welford independently derived a fiber bundle analogy for the SDC restriction lattice:

- **Base space**: The value domain V
- **Fiber** at each point: The space of reasons R (ExceptionalValue types)
- **Constraints**: Define how fibers connect or transform

This gives SDC a mathematical vocabulary accessible to control systems engineers, information theorists, and physicists -- audiences that currently don't encounter SDC. It also opens the door to formal proofs about lattice properties (completeness, subsumption, closure).

Additionally, the lattice can be described as a partially ordered manifold where:
- Operations like subsumption resemble projections between subspaces
- The restriction-only inheritance creates a monotonic constraint propagation
- Validation is geometrically equivalent to testing membership in a constrained region

## Impact on RM

None. This is a formalization of existing structure, not a change to it. The output would be a mathematical specification document, not a code change.

## Domain Neutrality Check

Yes -- geometric formalization is inherently domain-neutral. It describes the structure of the reference model itself.

## Compatibility

N/A -- documentation only.

## Deliverable

A formal specification paper describing:
1. The restriction lattice as a partially ordered set with lattice operations
2. The fiber bundle structure (values x absence types x constraints)
3. Formal properties: closure, completeness, monotonic constraint propagation
4. Relationship to information geometry (entropy-to-geometry transformation)

## Open Questions

- Is this a standalone paper or a section of the SDC specification?
- Target audience: academic (journal/conference) or practitioner (technical report)?
- Should it include formal proofs or just the structural description?
