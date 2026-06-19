---
name: jgs-v1-inspect
description: Deep-dive a single SysML v1 element — type, structure, ports, relationships, allocations, stereotypes, tagged values, and requirement links in one dossier. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "inspect", "tell me everything about", "describe this element/block/part", "what is X", "show details of".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-inspect — Single-Element Deep Dive

You are a context-free AI agent executing the `jgs-v1-inspect` skill. Follow these steps exactly. This
skill is **read-only** — never call `enable_writes`, `begin_batch`, or any create/update/delete tool.

Distinct from `jgs-v1-impact` (which assesses change blast-radius). This skill produces a complete
reference dossier for one element.

**Invocation:** `/jgs-v1-inspect <element-name-or-qualified-name-or-id>`

---

## Tool constraints — read before calling anything

- `find_by_name` is capped at **50 results** (model-wide). If the count equals 50, warn and advise the
  qualified name.
- All the detail calls below are **single-element** and take `element_id` only (no scope arg):
  `get_element`, `describe_element`, `get_element_structure`, `get_qualified_name`, `list_children`
  (takes `parent_id`), `get_ports`, `get_relationships`, `get_allocations`, `list_applied_stereotypes`.
- `trace_requirement` takes `requirement_id` and only returns data for elements that are Requirements.

> **Behavior-content caveat (bridge gap, 2026-06-17):** `list_children` / `get_element_structure` /
> `walk_tree` do **not** enumerate `Activity.node`/`edge` or `StateMachine` region/state/transition —
> a populated activity/state-machine reports `childCount:1`. When inspecting an Activity or
> StateMachine, do not report it "empty" from those tools; note behavior is detailed via
> `get_model_metrics` type counts or `execute_groovy getNode()`/`getRegion().getTransition()`.

---

## Step 1 — Resolve the element

- If the argument looks like a qualified name (contains `::`), call
  `mcp__jgs-sysmlv1__find_by_qualified_name({"qualified_name": "<value>"})` (exact, no cap).
- Else if it looks like a raw element ID, use it directly as `element_id` and skip to Step 2.
- Otherwise call `mcp__jgs-sysmlv1__find_by_name({"name": "<value>"})`.

Handle results:
- **Zero:** "No element named '<value>' found. Try `/jgs-v1-navigate` to browse, or pass the qualified name (e.g. `Pkg::Block`)." Stop.
- **One:** use its ID as `element_id`.
- **Multiple (2–49):** list as `[N] Type — QualifiedName (ID: ...)` and ask which one. Wait.
- **Exactly 50:** list them and warn the result may be truncated; advise the qualified name. Wait.

---

## Step 2 — Core identity

Call `mcp__jgs-sysmlv1__get_element({"element_id": "<element_id>"})` and
`mcp__jgs-sysmlv1__get_qualified_name({"element_id": "<element_id>"})`.

Capture: type, name, qualified name, owner.

## Step 3 — Rich description

Call `mcp__jgs-sysmlv1__describe_element({"element_id": "<element_id>"})` for documentation, stereotypes
and tagged values, and `mcp__jgs-sysmlv1__list_applied_stereotypes({"element_id": "<element_id>"})` for
the applied-stereotype list.

## Step 4 — Structure

Call `mcp__jgs-sysmlv1__get_element_structure({"element_id": "<element_id>"})` (parts, properties,
nested structure) and `mcp__jgs-sysmlv1__list_children({"parent_id": "<element_id>"})` for direct owned
children.

## Step 5 — Interfaces

Call `mcp__jgs-sysmlv1__get_ports({"element_id": "<element_id>"})` for ports and their typing.

## Step 6 — Connections

Call `mcp__jgs-sysmlv1__get_relationships({"element_id": "<element_id>"})` and
`mcp__jgs-sysmlv1__get_allocations({"element_id": "<element_id>"})`.

## Step 7 — Requirement links (only if the element is a Requirement)

If Step 2 reported the type as a Requirement, call
`mcp__jgs-sysmlv1__trace_requirement({"requirement_id": "<element_id>"})` for its satisfy/verify/derive
chain. Skip otherwise.

---

## Output Format

```
## Element Dossier — <Name>

**Type:** <type>   **Qualified name:** <qn>   **ID:** <id>   **Owner:** <owner>

### Documentation
<doc text, or "— none —">

### Applied stereotypes & tagged values
<list, or "— none —">

### Structure
- Children: <N> (<names…>)
- Parts/properties: <summary from get_element_structure>

### Ports
<list with typing, or "— none —">

### Relationships
<grouped by kind: Association, Generalization, Dependency, ItemFlow, Satisfy, Verify, Allocate…>

### Allocations
<from/to, or "— none —">

### Requirement traceability   (only for Requirement elements)
<satisfy / verify / derive chain>
```

Omit any section whose call returned nothing rather than printing empty headers (except keep
Documentation and Ports as explicit "— none —" since their absence is itself meaningful).

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **A detail call fails:** note it inline under its section (e.g. "Ports: bridge returned no data") and continue with the rest.

## What not to do

- Do not call any write tool or `enable_writes`.
- Do not pass a scope/package argument to the single-element calls — they take `element_id` only.
- Do not call `trace_requirement` on non-Requirement elements — it returns nothing useful.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Activity / StateMachine reported "empty" (`childCount:1`) | `list_children`/`get_element_structure`/`walk_tree` do NOT enumerate Activity nodes/edges or SM regions/transitions — judge from `get_model_metrics` type counts or `execute_groovy getNode()`/`getRegion().getTransition()` |
| `find_by_name` result of exactly 50 treated as complete | It is capped at 50 (model-wide) — at 50, warn of possible truncation and advise the qualified name via `find_by_qualified_name` |
| Passing a package/scope arg to the detail calls | `get_element`/`describe_element`/`get_element_structure`/`get_ports`/`get_relationships`/`get_allocations`/`list_applied_stereotypes` take `element_id` only (`list_children` takes `parent_id`) — no scope arg |
| `trace_requirement` called on a non-Requirement | It takes `requirement_id` and returns nothing useful for other element types — only call when Step 2 typed the element as a Requirement |
