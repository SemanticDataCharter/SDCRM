"""Question-groups are well-formed, the editor composes up the inheritance
chain, and the intent anchors hold (docs/COMPOSITION-MODEL.md §7.2-§7.4)."""
import pytest

from spec import (REQUIRED_BASE_GROUPS, REQUIRED_LEAF_GROUPS, VALID_OWNERS,
                   VALID_TIERS, editor_for)


def _all_questions(model):
    for group_id, questions in model["question_groups"].items():
        for q in questions:
            yield group_id, q


def test_question_groups_present(model):
    assert "question_groups" in model


def test_required_groups_exist(model):
    keys = set(model["question_groups"])
    assert REQUIRED_BASE_GROUPS <= keys
    assert REQUIRED_LEAF_GROUPS <= keys


def test_every_question_has_required_keys(model):
    for group_id, q in _all_questions(model):
        assert q.get("id"), f"{group_id}: question missing id"
        assert q.get("tier") in VALID_TIERS, f"{group_id}/{q.get('id')}: bad tier"
        assert q.get("owner") in VALID_OWNERS, f"{group_id}/{q.get('id')}: bad owner"


def test_visible_questions_have_a_prompt(model):
    # Tier 1/2 are user-facing, so they must read as a plain-language prompt.
    for group_id, q in _all_questions(model):
        if q["tier"] in (1, 2):
            assert q.get("prompt"), f"{group_id}/{q['id']}: tier {q['tier']} needs a prompt"


def test_binding_questions_bind_to_fields(model):
    # Tier 1/2 questions that capture a value must say which API field they fill.
    for group_id, q in _all_questions(model):
        if q["tier"] in (1, 2):
            bt = q.get("binds_to")
            assert isinstance(bt, list) and bt, f"{group_id}/{q['id']}: empty binds_to"


def test_ids_unique_within_group(model):
    for group_id, questions in model["question_groups"].items():
        ids = [q["id"] for q in questions]
        assert len(ids) == len(set(ids)), f"{group_id}: duplicate question ids"


def test_editor_composes_for_every_selectable_leaf(model):
    for leaf in model["leaves"]:
        questions = editor_for(model, leaf)
        assert questions, f"{leaf}: empty editor"
        ids = [q["id"] for q in questions]
        assert len(ids) == len(set(ids)), f"{leaf}: duplicate ids across composed editor"
        assert any(q["tier"] == 1 for q in questions), f"{leaf}: no tier-1 question"
        assert "label" in ids and "description" in ids, f"{leaf}: missing base questions"


# ---- intent anchors ----

def _q(model, group, qid):
    for q in model["question_groups"][group]:
        if q["id"] == qid:
            return q
    raise AssertionError(f"{group}/{qid} not found")


def test_description_is_the_handoff_artifact(model):
    d = _q(model, "xdany", "description")
    assert d["tier"] == 1 and d["owner"] == "researcher"
    assert "description" in d["binds_to"]


def test_quantified_units_and_range(model):
    units = _q(model, "xdquantified", "units")
    assert "units" in units["binds_to"] and units["tier"] == 1
    rng = _q(model, "xdquantified", "range")
    assert rng["tier"] == 1


def test_quantified_precision_and_discriminator_are_auto(model):
    assert _q(model, "xdquantified", "precision")["owner"] == "auto"
    disc = _q(model, "xdquantified", "leaf_discriminator")
    assert disc["owner"] == "auto" and disc["tier"] == 3


def test_temporal_precision_binds_allow_flags(model):
    ps = _q(model, "xdtemporal", "precision_set")
    assert ps["tier"] == 1 and ps["owner"] == "researcher"
    assert any(f.startswith("allow_") for f in ps["binds_to"])


def test_ordinal_levels_bind_ordinals_and_symbols(model):
    lv = _q(model, "xdordinal", "levels")
    assert {"ordinals", "symbols"} <= set(lv["binds_to"])


def test_ordered_normal_range_binds_reference_ranges(model):
    nr = _q(model, "xdordered", "normal_range")
    assert "reference_ranges" in nr["binds_to"]


def test_token_codes_bind_enums(model):
    codes = _q(model, "xdtoken", "codes")
    assert "enums" in codes["binds_to"]
