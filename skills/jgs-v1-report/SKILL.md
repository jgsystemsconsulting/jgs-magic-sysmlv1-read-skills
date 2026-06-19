---
name: jgs-v1-report
description: Produce a shareable model-health report and Requirements Traceability Matrix (RTM) for a SysML v1 model, written to a file. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "RTM", "traceability matrix", "requirements matrix", "model health report", "model summary report", "export a report".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-report — Model-Health & RTM Export

You are a context-free AI agent executing the `jgs-v1-report` skill. **Read-only** — never call
`enable_writes` or any mutation tool. The only writes this skill performs are to the local filesystem
(via the agent's Read/Write tools) to save the report — never to the model.

**Invocation:** `/jgs-v1-report`

> **Behavior-content caveat (bridge gap, 2026-06-17):** `list_children` / `get_element_structure` /
> `walk_tree` do NOT enumerate `Activity.node`/`edge` or `StateMachine` region/state/transition.
> When the RTM or health report assesses functional/behavioral coverage, do not infer "empty
> activity/state-machine" from those tools — use `get_model_metrics` type counts
> (OpaqueActionImpl/ControlFlowImpl/TransitionImpl/StateImpl) or `execute_groovy` reading
> `getNode()`/`getRegion().getTransition()`.

---

## Scope note — read first

`generate_model_summary`, `get_model_metrics`, `check_requirement_coverage`, `export_requirements_matrix`
and `validate_model` all take **no arguments** and operate on the **whole open model** — there is no way
to scope this report to a sub-package. Always frame the output as model-wide.

---

## Step 1 — Model identity

Call `mcp__jgs-sysmlv1__get_root_package` for the model/root name and `mcp__jgs-sysmlv1__get_model_metrics`
for element/diagram/requirement counts by type.

## Step 2 — Narrative summary

Call `mcp__jgs-sysmlv1__generate_model_summary` for a high-level summary of element counts and coverage.

## Step 3 — Native validation

Call `mcp__jgs-sysmlv1__validate_model` for the host tool's own rule-violation list. Group results by
severity/rule. This is CATIA Magic's authoritative verdict, not a heuristic.

**Large output:** `validate_model` can return tens of thousands of characters on a real model (≈88 KB on
the qa-fixture-v1 model). Do **not** embed the full violation list in the report. Summarize: total count
and a breakdown by severity/rule, then list at most 25 representative violations (with element IDs). State
the omitted remainder count.

## Step 4 — Requirement coverage

Call `mcp__jgs-sysmlv1__check_requirement_coverage` for satisfied/verified statistics.

## Step 5 — Traceability matrix

Call `mcp__jgs-sysmlv1__export_requirements_matrix` for the full satisfy/verify matrix. For any
requirement where the matrix is ambiguous and you need the full chain, call
`mcp__jgs-sysmlv1__trace_requirement({"requirement_id": "<req_id>"})` (per requirement; takes
`requirement_id`). Do not call it on requirements that have no links — it returns empty.

---

## Step 6 — Write the report file

Build a markdown document and offer to save it as `jgs-v1-report-YYYY-MM-DD.md` (use today's date; if the
name exists append `-2`, `-3`, …). Use the agent's Write tool — never a bridge write tool.

```markdown
# SysML v1 Model Report — <model name>
*Generated: <date> · Scope: whole model*

## Health summary
<narrative from generate_model_summary>
**Stats:** <element_count> elements · <diagram_count> diagrams · <requirement_count> requirements

## Native validation (validate_model)
| Severity | Rule | Element | Detail |
|---|---|---|---|
| ... | ... | `<id>` | ... |
<or: "No validation violations reported.">

## Requirement coverage
- Satisfied: <n>/<total>   ·   Verified: <m>/<total>

## Requirements Traceability Matrix
| Requirement | Satisfied by | Verified by |
|---|---|---|
| <REQ-ID> <name> | <block(s) or — gap —> | <test(s) or — gap —> |

**Every blank cell is a traceability gap.**
```

After writing, print the file path and a one-line summary (e.g. "12 of 40 requirements unsatisfied,
3 validation violations — see <file>").

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **A section call fails:** include the section with a note "data unavailable — <tool> returned an error" and continue; never omit silently.

## What not to do

- Do not pass any arguments to the no-arg tools listed in the Scope note.
- Do not claim the report is scoped to a package — it is always model-wide.
- Do not call any model write tool.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reporting an Activity / StateMachine as "empty" from low child counts | `list_children`/`get_element_structure`/`walk_tree` do NOT enumerate Activity nodes/edges or SM regions/transitions — assess behavioral coverage from `get_model_metrics` type counts (OpaqueActionImpl/ControlFlowImpl/TransitionImpl/StateImpl) or `execute_groovy getNode()`/`getRegion().getTransition()` |
| Passing arguments to the report tools | `generate_model_summary`/`get_model_metrics`/`check_requirement_coverage`/`export_requirements_matrix`/`validate_model` take NO args and are whole-model — never scope them to a package |
| Embedding the full `validate_model` output | It can exceed tens of thousands of characters — summarize by severity/rule and list at most ~25 representative violations with the omitted count |
| Calling `trace_requirement` on non-Requirement links | It takes `requirement_id` and returns empty for requirements with no links — only call it where the matrix needs the full chain |
