# SDC5 Issue: Workflow Structure Convention Disagrees Between the Guide and the Reference Implementation

**Filed**: September 25, 2026
**Priority**: Medium
**Affects**: `sdc5/guides/workflow-state-machine.md` (§2.2, §3); specification DMType `workflow` semantics
**Discovered during**: ProvGov library rebuild (Axius-SDC/ProvGovLibrary PRD, §2 and §4)
**Raised by**: T. Cook (RM owner), 2026-09-25

## Problem

Two different conventions for the content of `DMType.workflow` are in circulation, and they are incompatible.

**The guide** (`workflow-state-machine.md` §3) models states as `XdString` components with fixed values in a `states` Cluster, and transitions as `from`/`to` Clusters (optionally with an XPath `guard` string) in a `transitions` Cluster, enforced by hand-written `xsd:assert` tests on `current-state`.

**The reference implementation** (sdcgovernance 4.2.x, `workflow.py`, live in SDCStudio `/settle` since 2026-09-16) reads a different shape: each **path** is one `XdOrdinal` whose enumerated values are the states (`ordinal` = position, `symbol` = the state code); a legal transition is **ordinal adjacency within a path**; **branching** is two paths that share a state symbol; **loops** are additional paths. The model-side parser recognizes a path ordinal by an SCXML or "workflow" reference in its `rdfs:seeAlso`. The instance-side parser is content-based: a state is any element with `ordinal` and `symbol` children, a path is its nearest non-adapter ancestor. Every Settlement Receipt issued to date evaluates this shape; a model built to the guide's shape evaluates INDETERMINATE.

The ordinal-path form has properties the guide's form lacks: the state map is derivable from the schema's enumerations with no assertions; a path is a reusable published component, so a library of standard workflows (HL7 v3 ActStatus, FHIR status code systems, DPV, SPAR PSO, OSLC CM and others, each state bound to its standard IRI) composes into any model's `workflow` slot; and the same component validates the instance once issue 006 binds the slot.

What the guide's form has that the ordinal form does not: guard conditions on transitions. In the ordinal form a guard belongs in `asserts` on the DM, which is where the guide already says schema-level constraints are enforced.

## SDC4 Workaround

None required. The ordinal-path form is legal SDC4 and is what runs. The guide is documentation.

## SDC5 Recommendation

1. Adopt the ordinal-path form as the **normative convention** for `DMType.workflow`: a Cluster whose sub-Clusters are paths, each path holding `XdOrdinal` states ordered by `ordinal`, transitions by adjacency, branching by shared symbol, loops as further paths. State the convention in the specification under DMType `workflow`, not only in the guide.
2. Rewrite guide §2.2 and §3 to that form; keep §2.3 (`asserts`) for guards and cross-element constraints, which is what it is good for.
3. Require, for a path ordinal, one definition IRI per state (the standard's code IRI where one exists) and `rdfs:seeAlso` to SCXML, so a processor can recognize a path without naming conventions.
4. Considered and not recommended: retyping `current-state` from `xsd:string` to an ordinal value type. The enumeration restriction in issue 006 gives the same enforcement without an RM type change; revisit if a processor needs the ordinal position in the instance.

## Reference

- sdcgovernance `src/sdcgovernance/workflow.py` (`WorkflowPath`, `_parse_workflow_cluster`, `_extract_workflow_components`), 4.2.1 changelog (content-based parser).
- `sdc5/guides/workflow-state-machine.md` §2.2, §2.3, §3.
- SDCStudio verifier packet instance 2026-09-22 (`workflow` with one path of four ordinal states; settled PERMIT).
- Axius-SDC/ProvGovLibrary `ProvGov-library-PRD.md` §2, §4 (24 standard-bound workflows).
- Related: issue 006 (binding and `current-state` restriction).
