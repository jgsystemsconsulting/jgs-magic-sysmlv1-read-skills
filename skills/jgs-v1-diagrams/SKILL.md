---
name: jgs-v1-diagrams
description: Inventory and export SysML v1 diagrams — build a visual review pack of diagram images, list diagram kinds, and compare layout styles. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "export diagrams", "diagram images", "PNG", "review pack", "visual review", "diagram inventory", "layout styles", "compare layouts".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-diagrams — Diagram Inventory & Visual Export

You are a context-free AI agent executing the `jgs-v1-diagrams` skill. **Read-only** — never call
`enable_writes` or any mutation tool. Any image files are saved with the agent's own Write tool.

**Invocation:** `/jgs-v1-diagrams [<package-name-or-id>]`

> **Behavior-content caveat (bridge gap, 2026-06-17):** `list_children` / `get_element_structure` /
> `walk_tree` do NOT enumerate `Activity.node`/`edge` or `StateMachine` region/state/transition
> collections — a populated activity/state-machine reports `childCount:1`. Never judge an Activity or
> StateMachine "empty" from those tools. Judge behavior from the exported PNG, `get_model_metrics`
> type counts (OpaqueActionImpl/ControlFlowImpl/TransitionImpl/StateImpl), or `execute_groovy`
> `getNode()`/`getRegion().getTransition()`.

---

## Tool constraints — read before calling anything

- `list_diagrams` **requires `parent_id`** — there is no model-wide form. Call it once per package node.
- `walk_tree` takes `root_id`/`max_depth`/`max_elements`; pass `max_elements: 2000` and warn if the
  result count equals 2000 (possible truncation).
- `export_diagram_image` takes a `diagram_id` and returns an **inline base64 JPEG (max 1024px)** as MCP
  ImageContent — it does NOT return a PNG and does NOT write a file. To persist it, decode the base64
  and write a `.jpg` with the agent's Write tool.
- `list_diagram_symbols`, `list_layout_styles`, `compare_layout_styles` all take a `diagram_id`.
- `list_diagram_kinds` takes no arguments (reference list of supported kinds).

---

## Step 1 — Resolve scope

- No argument: call `mcp__jgs-sysmlv1__get_root_package` → `root_id`.
- Argument given: resolve via `find_by_name`/`find_by_qualified_name` (handle 0 / 1 / many / 50-cap as in
  `jgs-v1-navigate`) → `root_id`.

## Step 2 — Collect package nodes

Call `mcp__jgs-sysmlv1__walk_tree({"root_id": "<root_id>", "max_depth": 10, "max_elements": 2000})`.
Collect every package node ID. (Truncation warning if count == 2000.)

## Step 3 — Inventory diagrams

For **each package node**, call `mcp__jgs-sysmlv1__list_diagrams({"parent_id": "<package_id>"})`.
Collect diagram id, name, kind, owning package. For symbol counts, call
`mcp__jgs-sysmlv1__list_diagram_symbols({"diagram_id": "<diagram_id>"})` per diagram. **Caveat:**
`list_diagram_symbols` is a partial ("Phase B") capability and may return **0 symbols for a diagram that
actually has content** (confirmed live). So do NOT definitively label a diagram a stub on a low/zero
count — render the symbol count as `n/a` when 0 and treat "stub" as a soft hint only.

Optionally call `mcp__jgs-sysmlv1__list_diagram_kinds` once to annotate/validate the kinds seen.

## Step 4 — Export images (visual review pack)

Ask the user: "Export images for all N diagrams, or a subset? (all / list names)". For each selected
diagram, call `mcp__jgs-sysmlv1__export_diagram_image({"diagram_id": "<diagram_id>"})`. Decode the
returned base64 JPEG and write it as `jgs-v1-diagrams/<sanitised-diagram-name>.jpg` with the agent's
Write tool. If an export fails, note it and continue.

## Step 4b — Visual self-check (vision; bounded)

Exporting proves the diagram rendered — not that it is **readable**. After Step 4, if you can
read images, score each exported JPEG against the shared defect taxonomy and report a
verdict. Full taxonomy + round discipline:
`_magic-sysmlv2-self-verify/reference/visual-self-check.md` (v1 flavour).

Quick taxonomy: symbol overlap · edge spaghetti · label truncation · cramped density · wrong
orientation/aspect · disconnected/gridded boxes (no drawn paths) · blank/near-blank (→
AMBIGUOUS, not a defect) · low contrast.

- **Read-only skill:** you may NOT re-layout (no `auto_layout_diagram` — that's a write).
  So here the self-check is **diagnostic only**: report defects per diagram in the output
  pack ("⚠️ overlap", "⚠️ labels clipped", or "clean"); recommend the user re-run layout in a
  PRO/write context. Max **1 scoring pass** (no fix loop — you can't fix read-only).
- **Blank/stub image → AMBIGUOUS** ("diagram may not be open / export failed"), never a clean
  verdict and never an "empty diagram" claim.
- **No vision → skip**; show the images and state the visual layer was not auto-checked.

Add a `Visual` column to the output table (clean / ⚠️ <defects> / n/a).

## Step 5 — (optional) Layout comparison

If the user asks about layout, call `mcp__jgs-sysmlv1__list_layout_styles({"diagram_id": "<id>"})` and
`mcp__jgs-sysmlv1__compare_layout_styles({"diagram_id": "<id>"})` for a chosen diagram and summarise.

---

## Output Format

```
## Diagram Review Pack — <model or package name>

**Diagrams:** <total> (<count> by kind…)
**Exported:** <n> images → ./jgs-v1-diagrams/
**Stub diagrams (<3 symbols):** <list or "none">

| Diagram | Kind | Package | Symbols | Image | Visual |
|---|---|---|---|---|---|
| <name> | <kind> | <pkg> | <n> | <file.jpg or — not exported —> | clean / ⚠️ <defects> / n/a |
```

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **`list_diagrams` fails for a package:** note inline and continue with other packages.
- **`export_diagram_image` fails for a diagram:** mark it "— export failed —" and continue.

## What not to do

- Do not call `list_diagrams` without `parent_id`.
- Do not describe the export output as PNG — it is JPEG (≤1024px).
- Do not call any model write tool.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `list_diagram_symbols` returns 0 → diagram called a "stub" | 0 is a known partial-capability result, NOT proof of emptiness — render the count `n/a`, treat "stub" as a soft hint only |
| Activity / StateMachine reported "empty" (`childCount:1`) | `list_children`/`get_element_structure`/`walk_tree` do NOT enumerate Activity nodes/edges or SM regions/transitions — judge from the exported image, `get_model_metrics` type counts, or `execute_groovy getNode()`/`getRegion().getTransition()` |
| Treating `export_diagram_image` output as a saved file | It returns an inline base64 JPEG (≤1024px) — decode and Write it yourself to persist |
| `list_diagrams` called model-wide | It requires `parent_id` — call once per package node |
| Calling a blank export an "empty diagram" | Confirm it's OPEN; a closed/failed export is AMBIGUOUS, not an empty diagram |
