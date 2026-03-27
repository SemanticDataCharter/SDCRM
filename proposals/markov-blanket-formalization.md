# Markov Blanket as Data Model Boundary Definition

- **Proposed by**: Tim Cook, 2026-03-27
- **Status**: PROPOSED

## Summary

Formally define each SDC data model as a Markov blanket in the Judea Pearl sense -- a structural boundary that creates genuine conditional independence between the model's interior and everything outside it.

## Motivation

The Markov blanket provides a precise, well-understood mathematical term for what SDC data models already do: define a boundary where everything inside the schema is conditionally independent of everything outside it. This gives SDC a one-liner for technical audiences:

"Each SDC data model is a Markov blanket. Everything inside the schema is conditionally independent of everything outside it. The boundary is fixed at publication and never changes."

This is the permanence guarantee expressed in language that probabilistic modelers, Bayesian network researchers, and information theorists already understand.

## The Three Layers

1. **Schema (the blanket)**: Defines the admissible state space for a single data instance. Deterministic. Fixed at publication. A value either conforms or it doesn't. This is the restriction lattice.

2. **Single data instance**: One observation that either conforms to the schema or doesn't. Deterministic validation against the blanket.

3. **Population of instances**: The aggregate of all conforming data instances collected against that data model. Statistical models (distributions, anomaly thresholds, absence type frequencies) live here. The statistics describe the population, not the schema.

Key: the blanket constrains what CAN exist. The statistical distribution describes what DOES exist across collected instances. Statistics never flow backward to modify the blanket. The statistical profile is a derived artifact, not a designed one. Different deployments of the same data model will have different statistical profiles because they sample different populations -- but the blanket is identical.

## Critical Scope Restriction

The Markov blanket applies at the DATA MODEL level only.

The reference model (XdString, XdQuantity, Cluster, DM, etc.) is NOT a blanket. It is the meta-structure that defines what valid blankets look like. It doesn't bound a specific domain because it is domain-neutral by design. Applying the Markov blanket concept to the reference model would be a category error.

## Distinguishing from Popular Science Usage

The term "Markov blanket" has been extended beyond Pearl's original definition by Friston (Free Energy Principle), Hoffman (Interface Theory of Perception), and Levin (Bioelectric Cognition). These extensions treat the blanket as dynamic, adaptive, or metaphorical.

SDC uses the term in the Pearl sense: fixed, structural, deterministic. The schema does not adapt, minimize free energy, or mediate perception. It defines admissible states and enforces them. When presenting this publicly, lead with Pearl, not Friston.

## Impact on RM

Minimal. This is primarily a formalization and documentation effort. Possible concrete additions:

- A "Formal Properties" section in the SDC specification describing the conditional independence guarantee
- Vocabulary for discussing model boundaries in integration guides and comparison documents

## Domain Neutrality Check

Yes -- the Markov blanket description is inherently domain-neutral. It describes a property of all SDC data models regardless of domain.

## Compatibility

N/A -- formalization of existing properties.

## Open Questions

- Should this be a section in the SDC specification, a standalone document, or part of the geometric formalization paper?
- How to handle the ontology links (RDF PredObj) in the blanket formalism -- they are the "sensory interface" that connects the model to external knowledge without breaking conditional independence. This needs precise definition.
