"""Regression guard: the breadth model (roles, leaves, containment, canDrop)
must keep working after we add families + question-groups."""
from spec import can_drop


def test_twenty_leaves(model):
    assert len(model["leaves"]) == 20


def test_roles_tally(model):
    roles = model["roles"]
    counts = {}
    for r in roles.values():
        counts[r] = counts.get(r, 0) + 1
    assert counts["leaf"] == 20
    assert counts["container"] == 1
    assert counts["plumbing"] == 1


def test_agent_selectable_is_leaf_plus_container(model):
    roles = model["roles"]
    expected = sorted(n for n, r in roles.items() if r in ("leaf", "container"))
    assert model["agent_selectable"] == expected


def test_cluster_accepts_item_members(model):
    cluster = model["containment"]["ClusterType"]
    item_slots = [s for s in cluster if s["slot"] == "Item"]
    assert item_slots, "ClusterType must have an Item slot"
    assert set(item_slots[0]["accepts"]) == {"ClusterType", "XdAdapterType"}


def test_can_drop_predicate(model):
    # A Field cannot be a Model's root; only a Group can.
    assert can_drop(model, "Field", "Model") is False
    assert can_drop(model, "Group", "Model") is True
    # Root is 1..1: a second Group cannot drop once a root exists.
    assert can_drop(model, "Group", "Model", target_has_root=True) is False
    # A Group nests Groups and Fields.
    assert can_drop(model, "Group", "Group") is True
    assert can_drop(model, "Field", "Group") is True
    # A Field is terminal.
    assert can_drop(model, "Field", "Field") is False
    assert can_drop(model, "Group", "Field") is False
