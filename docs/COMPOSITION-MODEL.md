# SDC4 composition / validity model

**Status:** Draft, 2026-06-20; moved into SDCRM 2026-11-23. The foundation
artifact for a drag-and-drop assembly canvas; the Bench page in SDCStudio
consumes it. Proves that "components are restricted to where
they're valid" is **computable from SDC metadata** — not something to hand-encode
into a block grammar (the trap of the earlier Blockly-the-RM attempt).

- **Machine-readable:** [`tools/composition/composition-model.json`](../tools/composition/composition-model.json)
- **Generator:** `tools/composition/generate_composition.py` (from `sdc4/schemas/sdc4.xsd`; regenerate, don't hand-edit)
- **Tests:** `python -m pytest tools/composition/tests`

The lesson from before: *don't model the RM inside the canvas library.* Derive
validity from data the system already has (RM roles + containment), let the
server be the source of truth, and hide the plumbing. This doc is that data.

## 1. The whole RM containment, in three rules

The SDC composition graph is a **tree** (containment, not a wire-graph), and it
reduces to three rules — verified against `sdc4.xsd`:

1. **A `ClusterType` contains `Item`s** — `Item [0..unbounded]`, where an `Item`
   is either a **`ClusterType`** (a nested group) or an **`XdAdapterType`**.
2. **An `XdAdapterType` wraps exactly one leaf** — one `XdAny` subtype (a concrete
   `Xd*` datatype). This is the XSD wiring that lets a leaf sit inside a Cluster.
3. **A `DMType` (the model root) holds one root `Item [1..1]`** (a Cluster in the
   common case) plus structural slots (subject, provider, participations,
   workflow, acs, audit, attestation) and metadata.

That's the entire composition surface. Everything else (52 RM types) is either a
**leaf** you put in an adapter, a **structural/governance** type, an **abstract**
base, or an **exceptional value**.

## 2. Role gating (computed from the schema)

Every RM type carries a `role` (emitted by the
generator). The role *is* the validity gate:

| role | count | on the canvas? |
|---|---|---|
| `leaf` | 20 | **Yes** — a **Field** in the palette |
| `container` (`ClusterType`) | 1 | **Yes** — a **Group** |
| `plumbing` (`XdAdapterType`) | 1 | Hidden — auto-created, never shown |
| `structural` | 8 | No — done in SDCStudio UI |
| `abstract` | 4 | No — never a selection |
| `exceptional-value` | 17 | No — data/validation layer |

`agent_selectable = role in {leaf, container}` — the 21 types a user may place.

## 3. The canvas scoping (policy)

The tool does **not** expose the full RM (the "guided tour," not full power). It
exposes three node kinds (their families, colors, and per-type constraint
questions are specified in §7):

| Canvas node | RM type | Accepts | Notes |
|---|---|---|---|
| **Model** | `DMType` | one **Group** at the root | structural slots held out of scope |
| **Group** | `ClusterType` | **Groups** + **Fields** (0..∞ each) | nests arbitrarily |
| **Field** | the 20 leaf `Xd*` types | — (terminal) | shown by **data-type badge**, not type name |

**Data-type badges** — the block-face label (the user never sees `XdQuantityType`).
One display vocabulary (PHASE-2-PRD FR-8b): the familiar data type, the deliberate
middle level between an abstract phrase and the RM name. Emitted at
`canvas.node_kinds.Field.type_badges`.

| Badge | RM leaf |
|---|---|
| Decimal | XdQuantityType, XdFloatType, XdDoubleType |
| Integer | XdCountType |
| Ranked | XdOrdinalType |
| Code | XdTokenType |
| Text | XdStringType |
| Date / time | XdTemporalType (refines to Date / Time / Datetime by config at render) |
| Boolean | XdBooleanType |
| Range | XdIntervalType |
| Link | XdLinkType |
| File | XdFileType |
| List (Text / Code / Boolean / Integer / Decimal) | the corresponding list variants |

## 4. The drop-validity rule (what a `connectionChecker` implements)

A dragged palette item `C` may drop into target `T` iff:

```
canDrop(C, T):
  if T is a Group:   return C.kind in {Group, Field}     # leaf -> auto-wrap XdAdapter
  if T is a Model:   return C.kind == Group and T has no root yet   # root is 1..1
  if T is a Field:   return false                          # terminal
  # structural / abstract / plumbing / exceptional-value never enter the palette
```

This is **affordance only** — it decides what *highlights* as a legal drop. The
**authoritative** check is the SDCStudio publish/validate API. Never
re-implement RM validation in the client; that's the original Blockly mistake in
new clothes.

Auto-wrap: when a Field lands in a Group, the orchestration layer creates the
`XdAdapterType` around the leaf. **XdAdapter is never a block / node** — it is
Tier-3 plumbing (hidden from the canvas).

## 5. Out of scope for the canvas

Held back to keep the tour guided (done in the SDCStudio UI):

- **DM structural slots:** subject, provider, participations, workflow, acs,
  audit, attestation.
- **Structural types:** Party, Participation, Audit, Attestation, ReferenceRange,
  DM-as-editable, Invl*, InvlUnits.
- **Exceptional values:** ISO 21090 null-flavors — a validation-layer choice, not
  a modeling one.

## 6. Library-agnostic by design

The map is the engine; the renderer is swappable. The same JSON drives:

- **Blockly** — a custom `ConnectionChecker` calling `canDrop()` (the hook the
  earlier attempt lacked, instead of hand-authored `setCheck` strings).
- **React Flow / Rete.js** — `isValidConnection` / drop-target gating.
- **A custom QML/Tauri canvas** — the same predicate on drop.

Pick the renderer for the UX; the validity logic does not change.

## 7. Families, colors, and constraint question-groups

§3 gives the **breadth** model: every leaf is one "Field." This section adds the
**depth**: the palette groups leaves into **families** (color-coded), and each
component's constraint editor is **composed from question-groups that hang off the
RM abstract bases.** These are additive blocks in
[`tools/composition/composition-model.json`](../tools/composition/composition-model.json): a `families`
map and a `question_groups` map.

### 7.1 Families = the RM abstract bases

A family is an abstract base, and a leaf's family is its **nearest
constraint-bearing base** (`XdQuantified` ⊃ `XdOrdered` ⊃ `XdAny`). Membership is
**computed** from the schema; the color and label are **policy**.

| Family | RM base | Members (leaf `Xd*`) | Color | Hex |
|---|---|---|---|---|
| **Group** | `ClusterType` | (the container itself) | slate | `#475569` |
| **Entry** | `XdAny` (direct) | String, Token, Boolean, Link, File, Interval, StringList, TokenList, BooleanList | blue | `#2563eb` |
| **Ordered** | `XdOrdered` | Ordinal, Temporal | teal | `#0d9488` |
| **Quantified** | `XdQuantified` | Count, Quantity, Float, Double, DecimalList, DoubleList, IntegerList, NonNegativeIntegerList, PositiveIntegerList | amber | `#d97706` |

Color encodes **inheritance depth** (Entry is shallowest, Quantified carries the
most structure), which doubles as a quiet teaching signal. Color-coded block
*categories* are on-lineage with Scratch/Blockly — one more pedigreed UX choice,
not a novelty.

**Families affect the palette and the editor only.** They do **not** change
`canDrop()` (§4): drop-validity stays family-agnostic — any Field, whatever its
family, drops into a Group.

### 7.2 The editor composes up the inheritance chain

```
editor(leaf) = group:xdany
             ⊕ group:xdordered     (if leaf is Ordered or Quantified)
             ⊕ group:xdquantified  (if leaf is Quantified)
             ⊕ group:<leaf>        (the leaf-specific group)
```

Each question carries:

| key | meaning |
|---|---|
| `id` | stable handle |
| `prompt` | plain-language question (no RM vocab) |
| `tier` | **1** ask the researcher · **2** advanced / auto (inferred from the data sample, or behind "advanced") · **3** never on the bench (practitioner / SDCStudio only) |
| `owner` | `researcher` · `auto` (derived from data, never asked) · `practitioner` (completed in SDCStudio) |
| `binds_to` | the SDCStudio API field(s) the answer populates (`src/dmgen/{models,serializers}.py`) |

### 7.3 Shared base groups

**`xdany`** — every component:

| id | prompt | tier | owner | binds_to |
|---|---|---|---|---|
| `label` | "Name this in your own words." | 1 | researcher | `label` |
| `description` | "Describe what this is, what a normal or expected value looks like, and cite any guideline or protocol that defines it." | 1 | researcher | `description` |
| `context` | (valid-time / time-recorded / modified / location / access tags) | 3 | practitioner | `require_*`/`allow_*`, `act_class` |
| `ui` | (preferred rendering) | 3 | auto | `ui_type` |

The `description` is the **handoff artifact** (per the pipeline decision): it
carries every deferred semantic to the practitioner and is searchable for reuse.

**`xdordered`** — Ordinal, Temporal, and all Quantified:

| id | prompt | tier | owner | binds_to |
|---|---|---|---|---|
| `normal_range` | "What counts as a normal or expected range?" | 1 | researcher (prose) → practitioner (formalize) | `normal_status`, `reference_ranges` |

The researcher names it in the description; the practitioner mints the
`ReferenceRange` (+ `XdInterval`) and binds it.

**`xdquantified`** — Count, Quantity, Float, Double, numeric lists:

| id | prompt | tier | owner | binds_to |
|---|---|---|---|---|
| `units` | "What is the unit?" | 1 | researcher (name) → practitioner (confirm/mint) | `units` (FK to a `Units` component) |
| `range` | "Lowest and highest value that makes sense?" | 1 | researcher | `min_inclusive`, `max_inclusive` |
| `precision` | (decimal places) | 2 | auto | `fraction_digits`, `total_digits` |
| `magnitude_status` | (status / error / accuracy) | 3 | practitioner | `require_ms`/`allow_ms`/`require_error`/`allow_error`/`require_accuracy`/`allow_accuracy` |
| `leaf_discriminator` | — | 3 | auto | — |

`units` is **reuse-first** — match an existing `Units` component before minting.
`leaf_discriminator`: integer → XdCount, decimal → XdQuantity, float/double →
XdFloat/XdDouble; chosen from the data, **never asked** (canon
`datatype-numeric`).

### 7.4 Leaf-specific groups

| group | id | prompt | tier | owner | binds_to |
|---|---|---|---|---|---|
| `xdordinal` | `levels` | "List the values in order, lowest to highest." | 1 | researcher | `ordinals`, `symbols` |
| | `level_ids` | (identity URI per level) | 3 | practitioner | `annotations` |
| `xdtemporal` | `precision_set` | "What precision can this carry? (full date · year-month · year · time · duration)" | 1 | researcher | `allow_date`/`allow_year_month`/`allow_year`/`allow_time`/`allow_datetime`/`allow_duration`/… |
| `xdstring` | `allowed_values` | "Is this a fixed list of values? If so, list them." | 1 → practitioner (bind) | researcher | `enums`, `enum_descr`; `definitions` (URIs) practitioner-owned |
| | `length` | "How long can the text be?" | 2 | auto | `min_length`/`max_length`/`exact_length` |
| | `format` | "Any required format or pattern?" | 2 | researcher (assisted) | `str_fmt` |
| | `default` | (default value) | 2 | researcher | `def_val` |
| `xdtoken` | `codes` | "List the codes, and name the code system if you know it." | 1 → practitioner (bind) | researcher | `enums`, `enum_descr`; `definitions` (`system#code` URIs) practitioner-owned |
| | `language` | (code language) | 2 | researcher | `language` |
| `xdboolean` | `representations` | "How are yes and no written in your data? (e.g. Y/N, true/false)" | 2 | researcher | `trues`, `falses` |
| `xdlink` | `relationship` | "What is the relationship to the thing it points to?" | 1 → practitioner (formalize) | researcher | `relation`; `relation_uri` practitioner-owned |
| `xdfile` | `kind` | "What kind of file, and is it embedded or linked?" | 1 | researcher | `media_type`, `content_mode` |
| | `meta` | (encoding / language / alt text) | 2 | researcher | `encoding`, `language`, `alt_txt` |
| `xdinterval` | — | (not a standalone bench Field; only a building block of a `ReferenceRange`, question group `datatype-other-leaf`) | 3 | practitioner | `lower`/`upper`/`interval_type`/`*_bounded`/`*_included`/`units_*` |

For `xdstring`/`xdtoken` the `format` question may call the
`POST /api/dmgen/xdstrings/suggest-regex/` endpoint to draft `str_fmt`.

### 7.5 Why the owner split — the business model

The tier/owner split is the **funnel**, not just UX. The researcher answers
**tier-1** on the bench and produces structurally-correct **drafts** plus a cited
description. Everything deferred — **tier-3**, and the *formalize* half of the
prose tier-1 questions — is the **practitioner's** work in SDCStudio: reuse
search, semantic binding, units / reference-range construction, then publish. That
is precisely what pulls users from the bench **into SDCStudio for reuse and
construction, and onward to the VSL**. Roles are functions: a researcher or a
modeler can earn the practitioner credential and complete their own drafts
in-house — handed off **in-band via project ACLs** (see the *Researcher →
Practitioner → SDCStudio* pipeline note).

### 7.6 Emitted shape

```jsonc
"families": {
  "Quantified": {
    "rm_base": "XdQuantifiedType",
    "label": "Quantified",
    "color": "#d97706",
    "members": ["XdCountType", "XdQuantityType", "XdFloatType", "XdDoubleType",
                "XdDecimalListType", "XdDoubleListType", "XdIntegerListType",
                "XdNonNegativeIntegerListType", "XdPositiveIntegerListType"]
  }
  // Group / Entry / Ordered …
},
"question_groups": {
  "xdquantified": [
    {"id": "units", "prompt": "What is the unit?", "tier": 1, "owner": "researcher",
     "binds_to": ["units"], "note": "reuse an existing Units component before minting"},
    {"id": "range", "prompt": "Lowest and highest value that makes sense?", "tier": 1,
     "owner": "researcher", "binds_to": ["min_inclusive", "max_inclusive"]},
    {"id": "precision", "prompt": "Decimal places", "tier": 2, "owner": "auto",
     "binds_to": ["fraction_digits", "total_digits"]},
    {"id": "leaf_discriminator", "tier": 3, "owner": "auto",
     "note": "integer->Count, decimal->Quantity, float/double->Float/Double; from the data"}
  ]
  // xdany / xdordered / xdordinal / xdtemporal / xdstring / …
}
```

`families.members` regenerates from inheritance; `color`/`label` and every
`question_groups` entry are **policy**, hand-maintained in the generator.

## 8. Regenerating

```
python tools/composition/generate_composition.py   # roles + families derived from sdc4.xsd
```

RM facts are computed from the schema, so the map stays correct across
SDC4 → SDC5 (the leaf set, containment, and `families.members` regenerate); only
the policy layer — labels, scoping, family `color`/`label`, and the
`question_groups` (§7) — is hand-maintained in the generator.
