---
name: jgs-v1-cross-model
description: Cross-model gap analysis — compare satisfied v1 requirements against element presence in a live v2 model, and surface unsatisfied v1 requirements as traceability gaps. FREE tier on both bridges. Requires jgs-magic-sysmlv1-mcp AND jgs-magic-sysmlv2-mcp both running.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-cross-model — Cross-Model Query (UC-V1-12)

## Purpose

For requirements that are **satisfied** in the v1 model, confirms whether the satisfying Block has been created in the v2 model. Useful for tracking migration progress. For **unsatisfied** v1 requirements, reports them separately as traceability gaps requiring manual triage.

## Critical design note

`trace_requirement` traces **existing** satisfy/verify links only. It returns **empty** for unsatisfied requirements — there are no links to trace. Do **NOT** call `trace_requirement` on unsatisfied requirements. This skill operates on satisfied requirements (v2 equivalence check) and surfaces unsatisfied ones separately.

## Precondition check

Call **both** pings before doing anything else:

1. `mcp__jgs-sysmlv1__ping` — v1 bridge liveness
2. `mcp__jgs-sysmlv2__ping` — v2 bridge liveness

If **either** fails, halt immediately and emit:

```
❌ [jgs-magic-sysmlv1-mcp | jgs-magic-sysmlv2-mcp] bridge is not reachable. Is [the v1 | v2] CATIA Magic instance running with its bridge plugin active?
```

Use the specific bridge name that failed. Do not proceed.

## Tool sequence

### Step 1 — Get requirement coverage from v1

Call: `mcp__jgs-sysmlv1__check_requirement_coverage`

Split the returned requirements into two groups:
- **Satisfied** — requirements that have at least one satisfy link
- **Unsatisfied** — requirements with no satisfy links

If there are **zero satisfied requirements**, stop and report:

> No satisfied v1 requirements found — there is nothing to compare against v2. Check requirement coverage first with /jgs-v1-audit.

Do not proceed further.

### Step 2 — Trace satisfying elements for each satisfied requirement

For each **satisfied** requirement:

Call: `mcp__jgs-sysmlv1__trace_requirement(req_id)`

Extract the satisfying element name(s) from the result. Each requirement may have one or more satisfying elements.

### Step 3 — Look up each satisfying element name in v2

For each satisfying element name extracted in Step 2:

Call: `mcp__jgs-sysmlv2__find_by_name(element_name)`

Bridge cap: up to 50 results.

**Match semantics:** case-sensitive exact name match against the element's simple name.

Handle all three result cases:

- **Any result = hit.** Mark as found in the output table.
- **Multiple hits** — list all returned results with their qualified names. Do **not** silently pick the first. Render in the table cell as:
  `[N candidates] QualifiedName1, QualifiedName2, ...`
  Do not expand to multiple table rows.
  If result count = 50, append: `(list may be truncated — use mcp__jgs-sysmlv2__find_by_qualified_name for exact lookup)`
- **Zero results = missing in v2.** Record as:
  `✗ Missing in v2 (verify manually — see name-match warning)`

### Step 4 — Get model name headers

Call `mcp__jgs-sysmlv1__get_root_package` and `mcp__jgs-sysmlv2__get_root_package` to get the model names for the output headers.

Do **not** use ping for model names.

### Step 5 — Produce output (two tables)

See Output Format section below.

## Do not call any write tools

Do not call `enable_writes`, `enable_dangerous_writes`, or any create/update/delete tool on either bridge. This skill is read-only.

## Output format

```
## Cross-Model Migration Progress Report
*v1 model: <name from mcp__jgs-sysmlv1__get_root_package>*
*v2 model: <name from mcp__jgs-sysmlv2__get_root_package>*
*Generated: <date>*

### Satisfied v1 requirements — v2 element check

| Requirement | Satisfying v1 Block | Found in v2? |
|---|---|---|
| REQ-047 | DataBus | ✓ found |
| REQ-088 | ThermalController | ✗ Missing in v2 (verify manually — see name-match warning) |
| REQ-055 | DataBus | ✓ found (2 candidates — SensorsPackage::DataBus, ArchPackage::DataBus) |

**Summary:** N of M satisfying Blocks found in v2 (name match).

### Unsatisfied v1 requirements — traceability gaps

These requirements have no satisfy links in v1. They cannot be compared to v2 automatically.
Manual triage required.

| Requirement ID | Requirement text |
|---|---|
| REQ-112 | Thermal regulation within ±2°C |

**Summary:** P unsatisfied requirements in v1. These are traceability gaps that require satisfy links in v1 before migration can be verified.

---

> ⚠ **Name-match limitation:** This comparison joins on element name only. Elements renamed during v1→v2 migration (e.g. `ThermalMgmtSys` → `ThermalManagementSystem`) will appear as "missing in v2" even if the equivalent element exists under a different name. Verify all "missing" results manually before concluding the element is absent from v2.
```

## Name-match warning (mandatory)

**Always include the name-match warning block verbatim in the output, even if all results are found.** This is not optional.

## Error handling

| Condition | Action |
|---|---|
| v1 ping fails | Halt: "❌ jgs-magic-sysmlv1-mcp bridge is not reachable. Is the v1 CATIA Magic instance running with its bridge plugin active?" |
| v2 ping fails | Halt: "❌ jgs-magic-sysmlv2-mcp bridge is not reachable. Is the v2 CATIA Magic instance running with its bridge plugin active?" |
| Zero satisfied requirements | Report message and stop (do not call trace_requirement on unsatisfied reqs) |
| trace_requirement returns empty for a requirement that appeared satisfied | Flag that requirement with a note: "trace returned no links — requirement may have been reclassified; verify manually" |
| find_by_name returns 50 results | Include truncation warning; advise mcp__jgs-sysmlv2__find_by_qualified_name |

## Tool reference

| Tool | Purpose |
|---|---|
| `mcp__jgs-sysmlv1__ping` | v1 bridge liveness check |
| `mcp__jgs-sysmlv2__ping` | v2 bridge liveness check |
| `mcp__jgs-sysmlv1__check_requirement_coverage` | Get all requirements with satisfaction status |
| `mcp__jgs-sysmlv1__trace_requirement` | Trace existing satisfy/verify links for a satisfied requirement |
| `mcp__jgs-sysmlv1__get_root_package` | Get v1 model name for output header |
| `mcp__jgs-sysmlv2__find_by_name` | Look up element in v2 by simple name (cap: 50) |
| `mcp__jgs-sysmlv2__find_by_qualified_name` | Exact v2 lookup when find_by_name hits cap (50 results) |
| `mcp__jgs-sysmlv2__get_root_package` | Get v2 model name for output header |
