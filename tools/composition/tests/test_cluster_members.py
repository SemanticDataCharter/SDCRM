"""The reuse flyout must only ever offer components that can legally sit in a
Cluster — Xd* leaves (descendants of XdAnyType) and sub-Clusters, never structural
types like Party/Audit/Participation. `cluster_member_api_types` drives that
filter. That it matches SDCStudio's Cluster member fields exactly is checked in
SDCStudio, which vendors a copy of composition-model.json.
"""
import pytest


def test_no_structural_or_interval_members(model):
    members = set(model["canvas"]["cluster_member_api_types"])
    # XdInterval is a leaf but NOT a Cluster member (ReferenceRange building block).
    assert "interval" not in members
    # Structural types never appear (their api `type`s are party/audit/... which
    # are simply absent from the set).
    for forbidden in ("party", "participation", "audit", "attestation", "referencerange", "units"):
        assert forbidden not in members

