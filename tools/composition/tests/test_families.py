"""Families partition the leaves by nearest constraint-bearing base, and each
family carries a valid distinct color (docs/COMPOSITION-MODEL.md §7.1)."""
import re

import pytest

from spec import (EXPECTED_FAMILY_BASE, EXPECTED_FAMILY_COLORS,
                   EXPECTED_FAMILY_MEMBERS, EXPECTED_FAMILY_NAMES)

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def test_families_key_present(model):
    assert "families" in model


def test_exactly_the_four_families(model):
    assert set(model["families"]) == EXPECTED_FAMILY_NAMES


def test_each_family_has_base_label_color_members(model):
    for fam, spec in model["families"].items():
        assert spec.get("rm_base"), f"{fam} missing rm_base"
        assert spec.get("label"), f"{fam} missing label"
        assert spec.get("color"), f"{fam} missing color"
        assert isinstance(spec.get("members"), list), f"{fam} members not a list"


def test_family_bases_match_inheritance(model):
    for fam, base in EXPECTED_FAMILY_BASE.items():
        assert model["families"][fam]["rm_base"] == base


def test_leaf_families_partition_the_leaves(model):
    leaves = set(model["leaves"])
    entry = set(model["families"]["Entry"]["members"])
    ordered = set(model["families"]["Ordered"]["members"])
    quant = set(model["families"]["Quantified"]["members"])
    # disjoint
    assert entry & ordered == set()
    assert entry & quant == set()
    assert ordered & quant == set()
    # exhaustive
    assert entry | ordered | quant == leaves


def test_family_membership_is_ground_truth(model):
    for fam, members in EXPECTED_FAMILY_MEMBERS.items():
        assert set(model["families"][fam]["members"]) == members


def test_colors_are_valid_hex(model):
    for fam, spec in model["families"].items():
        assert HEX.match(spec["color"]), f"{fam} color {spec['color']!r} not #RRGGBB"


def test_colors_are_distinct(model):
    colors = [spec["color"].lower() for spec in model["families"].values()]
    assert len(colors) == len(set(colors))


def test_colors_match_policy(model):
    for fam, color in EXPECTED_FAMILY_COLORS.items():
        assert model["families"][fam]["color"].lower() == color.lower()


def test_families_do_not_change_drop_validity(model):
    # Families are a palette/editor concern only; node_kinds (the canDrop source)
    # must still expose exactly Model/Group/Field.
    assert set(model["canvas"]["node_kinds"]) == {"Model", "Group", "Field"}
