# Confidence Distribution Over Absence Types

- **Proposed by**: Kris Welford (external), 2026-03-27
- **Status**: PROPOSED

## Summary

Extend the ExceptionalValue system to support a confidence distribution over NULL Flavor types, rather than a single categorical assignment. Instead of declaring a missing value as one specific NULL Flavor, the system would express a weighted distribution over possible absence causes.

## Motivation

In sensor networks and automated data capture, the exact cause of a missing value is not always deterministic at capture time. A missing temperature reading might be 70% likely to be a comm timeout (NAV), 20% likely to be a sensor fault (UNK), and 10% likely to be firmware rejection of an out-of-range value (OTH). Forcing a single categorical assignment discards this uncertainty.

Kris's formulation: `value x (reason_for_absence x confidence(reason))`

## Impact on RM

This could be accomplished without changing the core restriction lattice. Possible approaches:

1. **Metadata extension**: Add an optional confidence map to the ExceptionalValue metadata -- a dictionary of NULL Flavor codes to confidence weights. The primary NULL Flavor remains a single categorical value (backward compatible). The confidence map is supplementary.

2. **New type**: A dedicated XdConfidenceAbsence type that wraps ExceptionalValue with a probability distribution. More formal but heavier.

Approach 1 is preferred -- it preserves backward compatibility and keeps the deterministic lattice intact.

## Key Constraint

The confidence distribution describes the population of collected data instances, not the schema itself. The blanket (schema) defines which NULL Flavors are admissible. The statistical profile describes observed patterns across the population. Statistics never flow backward to modify the schema.

## Domain Neutrality Check

Yes -- confidence over absence types is domain-neutral. The NULL Flavor vocabulary is already domain-neutral (ISO 21090). Adding confidence weights doesn't introduce domain concepts.

## Compatibility

Fully backward compatible if implemented as optional metadata. SDC4 instances without confidence maps remain valid. SDC5 instances with confidence maps degrade gracefully to single-category absence in SDC4 systems.

## Open Questions

- Is there an existing formal vocabulary for confidence levels (analogous to NULL Flavors for absence types)?
- Should the confidence weights be required to sum to 1.0 (proper probability distribution) or can they be unnormalized?
- At what layer should the confidence be computed -- at data capture, at ingestion, or as a post-collection analysis artifact?
