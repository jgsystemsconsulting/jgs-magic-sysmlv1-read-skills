---
name: jgs-v1-impact
description: Impact analysis for a SysML v1 element — map dependents, diagrams, and requirement links before making a change. FREE tier. Requires jgs-magic-sysmlv1-mcp.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-impact — Impact Analysis (UC-V1-10)

Before an engineer modifies a shared element, map the full blast radius: what depends on it, what diagrams show it, what requirements it satisfies.

**Invocation:** `/jgs-v1-impact <element-name>`

Do not call any write tools. Do not call `enable_writes`, `begin_batch`, or any create/update/delete tool.

---

## Step 1 — Resolve the element name

Call `mcp__jgs-sysmlv1__find_by_name` with the element name provided by the user.

The bridge returns at most 50 results (hard cap — larger result sets are silently truncated).

Handle the three possible outcomes:

**Empty result:**
Reply:
> No element named '<name>' found. Try `/jgs-v1-navigate` to browse available elements, or provide the qualified name (e.g. `SensorsPackage::DataBus`).

Stop here. Do not proceed to step 2.

**Multiple hits:**
List every returned match in this format:
```
[1] TypeName — QualifiedName (ID: ...)
[2] TypeName — QualifiedName (ID: ...)
...
```
Ask: "Which element did you mean?"

If the result count is exactly 50, add: "The list may be incomplete — the bridge returns at most 50 results. If your element is not shown, provide its qualified name (e.g. `PackageName::ElementName`) for an exact match."

Wait for the user to select an element before continuing to step 2.

**Single hit:**
Proceed directly to step 2 using the element ID from the result.

---

## Step 2 — Get dependents

Call `mcp__jgs-sysmlv1__impact_analysis` with the resolved `element_id`.

This is a single-element lookup — not a bulk traversal. Collect the full response.

---

## Step 3 — Get relationship links

Call `mcp__jgs-sysmlv1__get_relationships` with the same `element_id`.

This is a single-element call. Collect all returned relationships — specifically satisfy, verify, and allocation links.

---

## Step 4 — Present the impact report

Produce a structured report in this format:

```
## Impact Report — <ElementName>

**Element type:** <type>
**Qualified name:** <qualified name>
**Element ID:** <id>

### Dependents
<Summarise what impact_analysis returned: part properties, diagrams that show the element as a symbol, connectors or item flows that reference it. Count and group by category. List the most significant items by name.>

### Requirement links
<Summarise what get_relationships returned: satisfy links, verify links, allocations. List the requirement IDs and their text where available.>

### Recommendation
<One of the three recommendations below, based on the dependent count:>
```

**Recommendation logic:**

- If the total dependent count (across all categories) is **0**: "No dependents found. This element appears safe to change in isolation. Recommend running the v1 audit after the change to confirm no unintended effects."
- If the total dependent count is **1–10**: "This element has a small number of dependents. Review each one listed above before proceeding. Recommend running the v1 audit after the change."
- If the total dependent count is **greater than 10**: "This element has a high number of dependents. Coordinate with the owners of the affected packages before making any change. Recommend running the v1 audit after the change."

Always append: "Run `/jgs-v1` (audit) after the change to confirm the model remains consistent."

---

## Error handling

If `impact_analysis` or `get_relationships` returns an error or empty response, note it explicitly in the report under the relevant section heading (e.g. "Dependents: bridge returned no data — result may be empty or the element has no tracked dependents."). Do not silently omit the section.

---

## Constraints

- Read-only. No write tools. No `enable_writes`, `begin_batch`, or any mutation tool.
- `find_by_name` bridge cap is 50 results — always check the count and warn if it equals 50.
- `impact_analysis` and `get_relationships` are single-element calls — do not call them in a loop across multiple elements in this skill.
- If the user provides a qualified name directly (e.g. `SensorsPackage::DataBus`), call `mcp__jgs-sysmlv1__find_by_qualified_name` instead of `find_by_name` in step 1 — this has no cap concern and returns an exact match.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `find_by_name` result of exactly 50 treated as complete | It is capped at 50 (model-wide, silently truncated) — at 50, warn the list may be incomplete and advise the qualified name via `find_by_qualified_name` |
| Calling `impact_analysis` / `get_relationships` in a loop | Both are single-element lookups, not bulk traversals — call once on the resolved `element_id` |
| Treating an empty `impact_analysis` as an error | A zero-dependent result is a valid "safe to change in isolation" finding — note it explicitly rather than omitting the section |
