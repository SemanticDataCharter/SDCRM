"""Shared spec constants and helpers for the composition-model test suite.

These constants are the SDC4 GROUND TRUTH for the families/question-groups
contract (docs/COMPOSITION-MODEL.md §7). They are intentionally hand-maintained:
a deliberate SDC5 change to membership or policy should fail a test and be
updated here on purpose, not silently.
"""

# Family membership, derived from the sdc4.xsd inheritance (nearest
# constraint-bearing base: XdQuantified > XdOrdered > XdAny). 9 / 2 / 9 = 20.
EXPECTED_FAMILY_MEMBERS = {
    "Entry": {
        "XdBooleanListType", "XdBooleanType", "XdFileType", "XdIntervalType",
        "XdLinkType", "XdStringListType", "XdStringType", "XdTokenListType",
        "XdTokenType",
    },
    "Ordered": {
        "XdOrdinalType", "XdTemporalType",
    },
    "Quantified": {
        "XdCountType", "XdDecimalListType", "XdDoubleListType", "XdDoubleType",
        "XdFloatType", "XdIntegerListType", "XdNonNegativeIntegerListType",
        "XdPositiveIntegerListType", "XdQuantityType",
    },
}

# The leaf families above + the structural container family.
EXPECTED_FAMILY_NAMES = {"Group", "Entry", "Ordered", "Quantified"}

EXPECTED_FAMILY_BASE = {
    "Group": "ClusterType",
    "Entry": "XdAnyType",
    "Ordered": "XdOrderedType",
    "Quantified": "XdQuantifiedType",
}

# Policy colors (docs/COMPOSITION-MODEL.md §7.1). Color encodes inheritance depth.
EXPECTED_FAMILY_COLORS = {
    "Group": "#475569",
    "Entry": "#2563eb",
    "Ordered": "#0d9488",
    "Quantified": "#d97706",
}

# Base question-groups (attach to abstract bases) + leaf-specific groups.
REQUIRED_BASE_GROUPS = {"xdany", "xdordered", "xdquantified"}
REQUIRED_LEAF_GROUPS = {
    "xdordinal", "xdtemporal", "xdstring", "xdtoken", "xdboolean",
    "xdlink", "xdfile", "xdinterval",
}

# Maps a leaf RM type to its leaf-specific question-group key (when it has one).
LEAF_GROUP_KEY = {
    "XdOrdinalType": "xdordinal",
    "XdTemporalType": "xdtemporal",
    "XdStringType": "xdstring",
    "XdTokenType": "xdtoken",
    "XdBooleanType": "xdboolean",
    "XdLinkType": "xdlink",
    "XdFileType": "xdfile",
    "XdIntervalType": "xdinterval",
}

VALID_TIERS = {1, 2, 3}
VALID_OWNERS = {"researcher", "auto", "practitioner"}


def family_of(model, leaf):
    """Family name a leaf belongs to, per the emitted families map."""
    for fam, spec in model["families"].items():
        if leaf in spec.get("members", []):
            return fam
    return None


def editor_for(model, leaf):
    """Compose the constraint editor for a leaf: base groups up the inheritance
    chain + the leaf-specific group (docs/COMPOSITION-MODEL.md §7.2)."""
    qg = model["question_groups"]
    fam = family_of(model, leaf)
    keys = ["xdany"]
    if fam in ("Ordered", "Quantified"):
        keys.append("xdordered")
    if fam == "Quantified":
        keys.append("xdquantified")
    leaf_key = LEAF_GROUP_KEY.get(leaf)
    if leaf_key:
        keys.append(leaf_key)
    questions = []
    for k in keys:
        questions.extend(qg.get(k, []))
    return questions


def can_drop(model, child_kind, target_kind, target_has_root=False):
    """The drop-validity predicate, read from the emitted node_kinds
    (docs/COMPOSITION-MODEL.md §4). Affordance layer only."""
    nk = model["canvas"]["node_kinds"]
    if target_kind == "Group":
        return child_kind in nk["Group"]["accepts_canvas"]
    if target_kind == "Model":
        return child_kind in nk["Model"]["root_accepts_canvas"] and not target_has_root
    if target_kind == "Field":
        return False
    return False
