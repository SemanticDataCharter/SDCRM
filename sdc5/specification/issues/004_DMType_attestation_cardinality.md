# SDC5 Issue: DMType attestation Cardinality (Single vs Multiple)

**Filed**: July 26, 2026
**Priority**: Medium
**Affects**: DMType specification (`attestation` element)
**Discovered during**: CordovaOS governance composition mapping (10 government domains)

## Problem

`DMType.attestation` is `{0,1}` — at most one attestation per Data Model instance. Several governed-record patterns are intrinsically **multiply attested** on the same record:

- **Property transfer**: grantor attestation + grantee attestation + notary attestation.
- **Law-enforcement chain of custody**: a sequence of custodian attestations over the life of the evidence.
- **Dual control / separation of duties**: preparer attestation + independent approver attestation.

A single native attestation slot cannot represent these. The record genuinely bears more than one attestation, each with its own committer, reason, proof, and timestamp.

## SDC4 Workaround

Model the additional attestations either as `AttestationType` components inside the data `Cluster` (`DMType.Item`), or as `Participation` entries (`performer` + `function`) where the attestation act is captured as a participation. RM-compliant: the primary attestation uses the native slot and the rest ride as data. The compromise is only that the native slot's singularity understates records that are, in fact, multiply attested.

## SDC5 Recommendation

Change `DMType.attestation` to `{0,unbounded}`:

```
DMType
  ...
  ├── attestation (AttestationType, 0..unbounded)   -- was 0..1
  ...
```

`AttestationType` already carries `committer`, `reason`, `proof`, `committed`, and `pending`. A repeatable list of these cleanly represents multi-party and sequential attestation with **no new structure** — a cardinality change only, and low-risk (relaxing an upper bound is backward-compatible for existing single-attestation instances).

## Reference

- CordovaOS Governance Composition Map (`CordovaOS/docs/design/2026-07-26-Governance-Composition-Map.md`), SDC4-native-vs-SDC5 section.
