#!/usr/bin/env python3
"""
generate_composition.py — derive the SDC4 composition/validity map from sdc4.xsd.

Emits `composition-model.json`: the RM containment rules + role classification,
plus the canvas scoping (Model / Group / Field) and the drop-validity
rule a drag-and-drop assembly UI (Blockly `connectionChecker`, React Flow, a
custom QML canvas, ...) consumes.

What is COMPUTED from the schema (RM facts, regenerate-safe across SDC4->SDC5):
  - role per type (leaf / container / structural / abstract / plumbing / EV)
  - the leaf set (XdAny members) and the Item-family members
  - the content slots of the container types (DM, Cluster, XdAdapter)

What is POLICY (the Bench's choice, marked `policy: true`; the Bench is the
drag-and-drop modeling page in SDCStudio):
  - which subset the canvas exposes (Model/Group/Field), plain-language labels,
    auto-wrapping a leaf in XdAdapter, the structural slots held out of scope.

Authoritative validity stays server-side, in the publish/validate step. This map is the
client-side affordance layer only: it decides what *highlights* as a legal drop,
not what is ultimately valid.

Do NOT hand-edit the output — regenerate.

Usage:
  python tools/composition/generate_composition.py [--xsd PATH] [--out PATH]
"""
import argparse
import json
import os
import re
import xml.etree.ElementTree as ET

XSD_NS = "http://www.w3.org/2001/XMLSchema"
NS = {"xsd": XSD_NS}
HERE = os.path.dirname(os.path.abspath(__file__))
# The SDC4 reference model schema in this repository. Override with SDCRM_XSD.
DEFAULT_XSD = os.environ.get(
    "SDCRM_XSD", os.path.join(HERE, "..", "..", "sdc4", "schemas", "sdc4.xsd"))
DEFAULT_OUT = os.path.join(HERE, "composition-model.json")

EV_BASE = "ExceptionalValueType"
PLUMBING = {"XdAdapterType"}
CONTAINER = {"ClusterType"}
STRUCTURAL = {"PartyType", "ParticipationType", "AuditType", "AttestationType",
              "ReferenceRangeType", "DMType", "InvlType", "InvlUnits"}

# Substitution-group refs used inside the container content models. Item and
# XdAdapter-value are resolved from the schema; the DM-only structural refs are
# named here (DM is out of canvas scope, so they don't drive the tool).
STRUCT_REF = {"Participation": "ParticipationType", "Audit": "AuditType",
              "XdLink": "XdLinkType"}


def strip_ns(t):
    return t.split(":")[-1] if t else t


def collapse(s):
    return re.sub(r"\s+", " ", s or "").strip()


def local(node):
    return node.tag.split("}")[-1]


def content_root(ct):
    cc = ct.find("xsd:complexContent", NS)
    if cc is not None:
        ext = cc.find("xsd:extension", NS)
        if ext is not None:
            return strip_ns(ext.get("base")), ext
        res = cc.find("xsd:restriction", NS)
        if res is not None:
            return strip_ns(res.get("base")), res
    return None, ct


def own_elements(node):
    out = []

    def walk(n):
        for child in n:
            tag = local(child)
            if tag == "element":
                ref = child.get("ref")
                name = strip_ns(ref) if ref else child.get("name")
                typ = "ref" if ref else (strip_ns(child.get("type")) or "(inline)")
                out.append({
                    "name": name, "type": typ,
                    "min": child.get("minOccurs", "1"),
                    "max": child.get("maxOccurs", "1"),
                    "doc": collapse(child.findtext(
                        "xsd:annotation/xsd:documentation", default="", namespaces=NS)),
                })
            elif tag in ("sequence", "all", "choice"):
                walk(child)

    walk(node)
    return out


def inheritance_chain(name, types):
    out, cur, seen = [], name, set()
    while cur and cur in types and cur not in seen:
        seen.add(cur)
        out.append(cur)
        cur, _ = content_root(types[cur])
    return out


def role_of(name, ct, types):
    if EV_BASE in inheritance_chain(name, types):
        return "exceptional-value"
    if name in PLUMBING:
        return "plumbing"
    if ct.get("abstract") == "true":
        return "abstract"
    if name in CONTAINER:
        return "container"
    if name in STRUCTURAL:
        return "structural"
    return "leaf"


# Data-type badges (POLICY, PHASE-2-PRD FR-8b): the block-face label a scientist
# sees — the familiar data type (Decimal / Integer / Date / …), the deliberate middle
# level between an abstract phrase ("a measurement") and the RM type name. NEVER RM
# vocabulary in the UI (no XdQuantity/XdTemporal/…). This is the single display
# vocabulary; there is no separate meaning-phrase set.
#   Runtime note: XdTemporal refines to Date / Time / Datetime from the component's
#   allow_* config; the static badge here is the umbrella.
TYPE_BADGES = {
    "XdStringType": "Text",
    "XdTokenType": "Code",
    "XdCountType": "Integer",
    "XdQuantityType": "Decimal",
    "XdFloatType": "Decimal",
    "XdDoubleType": "Decimal",
    "XdOrdinalType": "Ranked",
    "XdBooleanType": "Boolean",
    "XdTemporalType": "Date / time",
    "XdLinkType": "Link",
    "XdFileType": "File",
    "XdIntervalType": "Range",
    "XdStringListType": "List (Text)",
    "XdTokenListType": "List (Code)",
    "XdBooleanListType": "List (Boolean)",
    "XdIntegerListType": "List (Integer)",
    "XdDecimalListType": "List (Decimal)",
    "XdDoubleListType": "List (Decimal)",
    "XdPositiveIntegerListType": "List (Integer)",
    "XdNonNegativeIntegerListType": "List (Integer)",
}

# SDCStudio's component-list API (`GET /dmgen/components/`) reports each row's
# `type` as a lowercase short key from `_COMPONENT_TYPE_TABLE` (dmgen/viewsets.py),
# e.g. `xdstring`, `xdquantity`, `cluster` — NOT the `XdStringType` RM name. The
# rule is "strip the Type suffix, lowercase" with `XdIntervalType` the lone
# exception (`interval`, not `xdinterval`). `api_type_badges` (below) is keyed by
# that API vocabulary so the canvas can badge search results directly; the
# test_api_type_badges drift guard checks it against SDCStudio's actual table.
API_TYPE_EXCEPTIONS = {"XdIntervalType": "interval"}


def api_type(rm):
    """RM type name -> SDCStudio component-list API `type` key."""
    return API_TYPE_EXCEPTIONS.get(rm, rm[:-4].lower())


# Families (COMPOSITION-MODEL §7.1): rm_base is the abstract base; members are
# COMPUTED from inheritance (nearest constraint-bearing base); color/label are POLICY.
FAMILY_POLICY = {
    "Group":      {"rm_base": "ClusterType",      "color": "#475569"},
    "Entry":      {"rm_base": "XdAnyType",        "color": "#2563eb"},
    "Ordered":    {"rm_base": "XdOrderedType",    "color": "#0d9488"},
    "Quantified": {"rm_base": "XdQuantifiedType", "color": "#d97706"},
}

# Constraint question-groups (COMPOSITION-MODEL §7.3-§7.4). POLICY, hand-maintained.
# Each question: id, (prompt for tier 1/2), tier {1,2,3}, owner {researcher,auto,
# practitioner}, binds_to (SDCStudio dmgen model fields; `*` = wildcard family).
# The editor for a leaf composes xdany (+ xdordered if Ordered/Quantified)
# (+ xdquantified if Quantified) (+ the leaf-specific group).
QUESTION_GROUPS = {
    "xdany": [
        {"id": "label", "prompt": "Name this in your own words.",
         "tier": 1, "owner": "researcher", "binds_to": ["label"]},
        {"id": "description", "prompt": "Describe what this is, what a normal or "
         "expected value looks like, and cite any guideline or protocol that defines it.",
         "tier": 1, "owner": "researcher", "binds_to": ["description"]},
        {"id": "context", "tier": 3, "owner": "practitioner",
         "binds_to": ["require_*", "allow_*", "act_class"],
         "note": "valid-time / time-recorded / modified / location / access tags"},
        {"id": "ui", "tier": 3, "owner": "auto", "binds_to": ["ui_type"],
         "note": "preferred rendering"},
    ],
    "xdordered": [
        {"id": "normal_range", "prompt": "What counts as a normal or expected range?",
         "tier": 1, "owner": "researcher", "binds_to": ["normal_status", "reference_ranges"]},
    ],
    "xdquantified": [
        {"id": "units", "prompt": "What is the unit?", "tier": 1, "owner": "researcher",
         "binds_to": ["units"], "note": "reuse an existing Units component before minting"},
        {"id": "range", "prompt": "Lowest and highest value that makes sense?",
         "tier": 1, "owner": "researcher", "binds_to": ["min_inclusive", "max_inclusive"]},
        {"id": "precision", "prompt": "Decimal places", "tier": 2, "owner": "auto",
         "binds_to": ["fraction_digits", "total_digits"]},
        {"id": "magnitude_status", "tier": 3, "owner": "practitioner",
         "binds_to": ["require_*", "allow_*"], "note": "status / error / accuracy"},
        {"id": "leaf_discriminator", "tier": 3, "owner": "auto",
         "note": "integer->Count, decimal->Quantity, float/double->Float/Double; from the data"},
    ],
    "xdordinal": [
        {"id": "levels", "prompt": "List the values in order, lowest to highest.",
         "tier": 1, "owner": "researcher", "binds_to": ["ordinals", "symbols"]},
        {"id": "level_ids", "tier": 3, "owner": "practitioner", "binds_to": ["annotations"],
         "note": "identity URI per level"},
    ],
    "xdtemporal": [
        {"id": "precision_set", "prompt": "What precision can this carry? "
         "(full date, year-month, year, time, datetime, duration)",
         "tier": 1, "owner": "researcher",
         "binds_to": ["allow_date", "allow_year_month", "allow_year", "allow_time",
                      "allow_datetime", "allow_duration"]},
    ],
    "xdstring": [
        {"id": "allowed_values", "prompt": "Is this a fixed list of values? If so, list them.",
         "tier": 1, "owner": "researcher", "binds_to": ["enums", "enum_descr"]},
        {"id": "length", "prompt": "How long can the text be?", "tier": 2, "owner": "auto",
         "binds_to": ["min_length", "max_length", "exact_length"]},
        {"id": "format", "prompt": "Any required format or pattern?", "tier": 2,
         "owner": "researcher", "binds_to": ["str_fmt"]},
        {"id": "default", "prompt": "Is there a default value?", "tier": 2,
         "owner": "researcher", "binds_to": ["def_val"]},
    ],
    "xdtoken": [
        {"id": "codes", "prompt": "List the codes, and name the code system if you know it.",
         "tier": 1, "owner": "researcher", "binds_to": ["enums", "enum_descr"]},
        {"id": "language", "prompt": "What language are the codes in?", "tier": 2,
         "owner": "researcher", "binds_to": ["language"]},
    ],
    "xdboolean": [
        {"id": "representations", "prompt": "How are yes and no written in your data? "
         "(e.g. Y/N, true/false)", "tier": 2, "owner": "researcher",
         "binds_to": ["trues", "falses"]},
    ],
    "xdlink": [
        {"id": "relationship", "prompt": "What is the relationship to the thing it points to?",
         "tier": 1, "owner": "researcher", "binds_to": ["relation"]},
    ],
    "xdfile": [
        {"id": "kind", "prompt": "What kind of file, and is it embedded or linked?",
         "tier": 1, "owner": "researcher", "binds_to": ["media_type", "content_mode"]},
        {"id": "meta", "prompt": "Encoding, language, or alternate text?", "tier": 2,
         "owner": "researcher", "binds_to": ["encoding", "language", "alt_txt"]},
    ],
    "xdinterval": [
        {"id": "bounds", "tier": 3, "owner": "practitioner",
         "binds_to": ["lower", "upper", "interval_type"],
         "note": "not a standalone bench Field; a building block of a ReferenceRange"},
    ],
}


def build_families(leaves, types):
    """Family per leaf = nearest constraint-bearing base (COMPOSITION-MODEL §7.1).
    Members computed from inheritance; color/label are policy."""
    def fam_of(leaf):
        chain = inheritance_chain(leaf, types)
        if "XdQuantifiedType" in chain:
            return "Quantified"
        if "XdOrderedType" in chain:
            return "Ordered"
        return "Entry"
    families = {}
    for name, pol in FAMILY_POLICY.items():
        members = [] if name == "Group" else sorted(l for l in leaves if fam_of(l) == name)
        families[name] = {"rm_base": pol["rm_base"], "label": name,
                          "color": pol["color"], "members": members}
    return families


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xsd", default=DEFAULT_XSD)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    root = ET.parse(args.xsd).getroot()
    types = {ct.get("name"): ct for ct in root.findall("xsd:complexType", NS)
             if ct.get("name")}

    roles = {n: role_of(n, ct, types) for n, ct in types.items()}
    leaves = sorted(n for n, r in roles.items() if r == "leaf")
    # Item-family = concrete subtypes of ItemType (what may sit in a Cluster).
    item_members = sorted(
        n for n in types
        if n != "ItemType" and "ItemType" in inheritance_chain(n, types)
        and types[n].get("abstract") != "true")

    def resolve_ref(ref_name):
        if ref_name == "Item":
            return item_members
        if ref_name == "XdAdapter-value":
            return leaves
        if ref_name in STRUCT_REF:
            return [STRUCT_REF[ref_name]]
        return []

    # Content slots of the container/wiring types.
    containment = {}
    for cname in ("DMType", "ClusterType", "XdAdapterType"):
        ct = types[cname]
        _, node = content_root(ct)
        slots = []
        for e in own_elements(node):
            accepts = resolve_ref(e["name"]) if e["type"] == "ref" else (
                [e["type"]] if e["type"] in types else [])
            composition = bool(accepts) and any(
                roles.get(a) in ("leaf", "container", "plumbing", "structural")
                for a in accepts)
            slots.append({
                "slot": e["name"],
                "card": f"{e['min']}..{e['max']}",
                "kind": "composition" if composition else "config",
                "accepts": accepts,
            })
        containment[cname] = slots

    # ---- Canvas scoping (POLICY) ----
    canvas = {
        "policy": True,
        "note": "The subset the drag-and-drop tool exposes. RM facts above are "
                "computed; this scoping is the Bench's product choice.",
        "node_kinds": {
            "Model": {
                "rm_type": "DMType",
                "label": "Model",
                "root_slot": "Item",
                "root_accepts_canvas": ["Group"],
                "note": "A model's root is a Group in the common case.",
            },
            "Group": {
                "rm_type": "ClusterType",
                "label": "Group",
                "accepts_canvas": ["Group", "Field"],
                "card_per_child": "0..unbounded",
            },
            "Field": {
                "rm_types": leaves,
                "label": "Field",
                "terminal": True,
                "auto_wrap": "XdAdapterType",
                "note": "A Field is a leaf Xd type; dropping it into a Group "
                        "auto-creates the (invisible) XdAdapter wrapper.",
                "type_badges": {t: TYPE_BADGES.get(t, t) for t in leaves},
            },
        },
        # Badge lookup keyed by SDCStudio's component-list API `type` vocabulary
        # (lowercase short keys), so the reuse-assembly canvas can badge search
        # results straight from the API without re-deriving RM names. Fields carry
        # their data-type badge; a reused Cluster badges as "Group".
        "api_type_badges": {
            **{api_type(t): TYPE_BADGES.get(t, t) for t in leaves},
            "cluster": "Group",
        },
        # The api `type`s that may legally sit in a Cluster (so the reuse flyout
        # never offers a non-member like Party/Audit/Participation). Mirrors
        # SDCStudio's Cluster M2M fields exactly: every Xd* leaf/list EXCEPT
        # XdInterval (a ReferenceRange building block, deliberately not a Cluster
        # member) plus `cluster` itself. Drift-guarded by test_cluster_members.
        "cluster_member_api_types": sorted(
            {api_type(t) for t in leaves if t != "XdIntervalType"} | {"cluster"}
        ),
        "drop_rules": [
            "A Group accepts Groups and Fields (0..unbounded each).",
            "A Model's root accepts exactly one Group (1..1).",
            "A Field is terminal on the canvas (its internal config is edited in "
            "the Field's own panel, not by dropping).",
            "Leaf dropped into a Group is auto-wrapped in XdAdapter; the user "
            "never sees XdAdapter.",
            "Types whose role is structural / abstract / plumbing / "
            "exceptional-value are never palette items and never droppable.",
            "This is the affordance layer only — the SDCStudio publish/validate "
            "API is the authoritative validity gate.",
        ],
        "out_of_scope": {
            "note": "Held out of the canvas (done in the SDCStudio UI). "
                    "Not palette items.",
            "dm_structural_slots": ["subject", "provider", "Participation",
                                    "workflow", "acs", "Audit", "attestation"],
            "structural_types": sorted(n for n, r in roles.items()
                                       if r == "structural"),
            "exceptional_values": "ISO 21090 null-flavors (data/validation layer)",
        },
    }

    out = {
        "sdc_version": "SDC4",
        "source": "generated from sdc4.xsd by tools/composition/generate_composition.py — do not hand-edit",
        "roles": dict(sorted(roles.items())),
        "agent_selectable": sorted(n for n, r in roles.items()
                                   if r in ("leaf", "container")),
        "leaves": leaves,
        "item_members": item_members,
        "containment": containment,
        "canvas": canvas,
        "families": build_families(leaves, types),
        "question_groups": QUESTION_GROUPS,
    }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    from collections import Counter
    tally = ", ".join(f"{r}: {n}" for r, n in sorted(Counter(roles.values()).items()))
    print(f"  composition-model.json: {len(types)} types [{tally}] -> {args.out}")
    print(f"  leaves: {len(leaves)}  item_members: {item_members}")


if __name__ == "__main__":
    main()
