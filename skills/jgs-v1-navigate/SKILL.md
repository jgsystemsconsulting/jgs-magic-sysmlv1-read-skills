---
name: jgs-v1-navigate
description: Navigate and inspect a SysML v1 model — produce a structured overview of packages, element counts, and diagrams. FREE tier. Requires jgs-magic-sysmlv1-mcp.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# jgs-v1-navigate — Model Navigation and Inspection (UC-V1-01)

You are a context-free AI agent executing the `jgs-v1-navigate` skill. Follow these instructions exactly. Do not improvise tool sequences. Do not skip steps. Do not call `find_by_type` for counts — it is silently capped at 50 and will undercount.

---

## Purpose

Give an engineer a structured orientation to an unfamiliar SysML v1 model. Produce a navigable overview: packages, element counts by type, and diagram inventory.

## Invocation

`/jgs-v1-navigate [<package-name-or-id>]`

The scope argument is optional. If omitted, operate from the model root. If provided, scope to that package.

---

## Tool constraints — read before calling anything

These are hard constraints confirmed against the bridge source. Violating them causes silent failures:

- **`list_diagrams` requires `parent_id`** — there is no model-wide call. You must call it once per package node. **Cap this on large models:** if `walk_tree` returned more than ~40 packages, do NOT call `list_diagrams` for every one — that can be hundreds of calls (the live reference model has 944 packages). Either collect diagrams only for the top two package levels, or omit the diagram inventory with a note ("diagram counts omitted on large model — re-run `/jgs-v1-navigate <package>` scoped for diagrams").
- **`find_by_type` is capped at 50 results and is model-wide** — never use it for counts. Use `get_model_metrics` instead.
- **`walk_tree` defaults to `max_elements=200`** — this silently truncates large models. Always pass `max_elements=2000` explicitly.
- **`find_by_name` is capped at 50 results** — if the result count equals 50, warn the user of possible truncation and advise using `find_by_qualified_name` for an exact match.
- **`walk_tree` returns structural elements only** — it does not return diagram metadata. Diagram names and kinds must be fetched separately via `list_diagrams`.
- **`walk_tree` / `list_children` do NOT enumerate Activity nodes/edges or StateMachine regions/transitions** — a populated activity/state-machine reports `childCount:1`. Never call a behavior "empty" from the tree; report its presence and note its internals need `get_model_metrics` type counts or `execute_groovy`.

---

## Path A — Unscoped (no package argument provided)

Execute these steps in order:

### Step 1 — Get model root

Call `mcp__jgs-sysmlv1__get_root_package`.

Extract the root element ID from the response. This is your `root_id` for Step 2.

### Step 2 — Walk the full model tree

Call `mcp__jgs-sysmlv1__walk_tree` with:
- `root_id`: the ID from Step 1
- `max_depth`: 10
- `max_elements`: 2000

**Truncation check:** If the number of elements returned equals exactly 2000, emit this warning immediately:
> "walk_tree result may be truncated — the model may have more than 2,000 elements. Results may be incomplete."

Note: `walk_tree` returns structural elements only — not diagram names or kinds. You will collect those in Step 4.

### Step 3 — Get model-wide metrics

Call `mcp__jgs-sysmlv1__get_model_metrics`.

Use this for the accurate model-wide Block count. Do not use `find_by_type` for the Block count — it caps at 50 and silently undercounts models with more than 50 Blocks.

### Step 4 — Collect diagrams per package

For each package node returned by `walk_tree`, call `mcp__jgs-sysmlv1__list_diagrams` with `parent_id` set to that package's ID.

Do this for every package node — one call per package. Never call `list_diagrams` without `parent_id`.

Collect diagram names and kinds from each call.

### Step 5 — Produce structured overview

Format the output as shown in the Output Format section below.

---

## Path B — Scoped (user provides a package name or ID)

Execute these steps in order:

### Step 1 — Resolve the package name

Call `mcp__jgs-sysmlv1__find_by_name` with `name` set to the user-provided value.

**Handle the result:**

- **Zero results:** Reply: "No package named '<name>' found. Use `/jgs-v1-navigate` without arguments to browse the full model, or provide the qualified name (e.g. `SensorsPackage::SubPkg`)." Stop.
- **Exactly one result:** Extract the element ID from the result. Proceed to Step 2.
- **Multiple results (2–49):** Present them as a numbered list in this format:
  ```
  [1] Package — SensorsPackage (ID: abc123)
  [2] Package — ArchPackage::SensorsPackage (ID: def456)
  ```
  Ask: "Which package did you mean? Reply with the number." Wait for confirmation before proceeding.
- **Exactly 50 results:** Present the list as above, then add:
  > "The list may be truncated at 50 results. If your target is not listed, use `find_by_qualified_name` with the fully qualified name (e.g. `RootModel::SensorsPackage`)."
  Wait for user selection.

The ID field in the `find_by_name` response is the value to pass as `root_id` to `walk_tree` in Step 2.

### Step 2 — Walk the scoped tree

Call `mcp__jgs-sysmlv1__walk_tree` with:
- `root_id`: the confirmed package ID from Step 1
- `max_depth`: 10
- `max_elements`: 2000

**Truncation check:** Same as Path A — if result count equals 2000, emit the truncation warning.

### Step 3 — Scoped Block count

Count Block elements by filtering the `walk_tree` result for entries where the element type equals `Block`. This is your scoped Block count.

Do not call `find_by_type` for scoped counts — it is always model-wide and cannot be scoped.

Do not call `get_model_metrics` for the scoped Block count — it is always model-wide.

### Step 4 — Collect diagrams per package (scoped)

For each package node returned by the scoped `walk_tree`, call `mcp__jgs-sysmlv1__list_diagrams` with `parent_id` set to that package's ID.

One call per package. Never call `list_diagrams` without `parent_id`.

### Step 5 — Produce structured overview

Format the output as shown below, noting it is scoped to the confirmed package.

---

## Output Format

```
## <Model or Package Name> — Model Overview

**Root package:** <name> (ID: <id>)
**Packages:** <count>
**Blocks:** <count> (from get_model_metrics [unscoped] / from walk_tree result [scoped])
**Diagrams:** <total count> (<count> BDD · <count> IBD · <count> <other kinds>)

### Package tree
- <PackageName> (<N> Blocks, <N> diagrams)
  - <ElementName>, <ElementName>, ...
- <PackageName> (<N> Blocks, <N> diagrams)
  - ...
```

For scoped runs, prefix the heading with the confirmed package name rather than the model root name.

If no diagrams were found in a package, omit the diagram count rather than showing "0 diagrams."

---

## Error handling

- **Bridge not reachable:** If any tool call fails with a connection error, emit: "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" and stop. Do not retry.
- **`walk_tree` returns an error** (a bridge `ScriptException` / `script-execution-failed`, NOT a connection error): do not abort. **Fall back to `list_children`** — start at the resolved root/package ID and recurse into children whose `type` ends in `Package` (or `Profile`), bounded to a sensible size (e.g. depth 10, stop after ~2,000 nodes). Take the model-wide Block count from `get_model_metrics` (not from the fallback). Add a one-line note that the tree was built via the `list_children` fallback because `walk_tree` errored. (Known bridge issue on some models.)
- **`list_diagrams` returns an error for every package** (bridge ScriptException, not a single-package miss): omit diagram counts and add ONE note — "Diagram inventory unavailable — the bridge `list_diagrams` tool errored." Continue with the structural tree.
- **Empty model:** If the tree traversal returns zero elements, emit: "The model appears to be empty or the root package has no child elements."
- **`list_diagrams` call fails for a specific package:** Note the failure inline in the package tree entry (e.g. "SensorsPackage — diagram list unavailable") and continue with remaining packages.

---

## What not to do

- Do not call `find_by_type` to count Blocks or any other element type — it caps at 50 and silently undercounts.
- Do not call `list_diagrams` without `parent_id`.
- Do not call `walk_tree` without `max_elements=2000`.
- Do not infer diagram counts from `walk_tree` results — `walk_tree` does not return diagram metadata.
- Do not skip the truncation check after `walk_tree`.
- Do not call `enable_writes` or any write tool — this skill is read-only.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `list_diagrams` called model-wide | It requires `parent_id` — call once per package node; cap the fan-out on large models (top two levels, or omit with a note) |
| Counting Blocks with `find_by_type` | It is capped at 50 and model-wide — use `get_model_metrics` (unscoped) or filter the `walk_tree` result (scoped) |
| `walk_tree` truncating silently | It defaults to `max_elements=200` — always pass `max_elements=2000` and warn if the count equals 2000 |
| Inferring diagram counts from `walk_tree` | `walk_tree` returns structural elements only, no diagram metadata — fetch names/kinds via `list_diagrams` |
| Activity / StateMachine reported "empty" from the tree | `walk_tree`/`list_children` do NOT enumerate Activity nodes/edges or SM regions/transitions — judge from `get_model_metrics` type counts or `execute_groovy getNode()`/`getRegion().getTransition()` |
