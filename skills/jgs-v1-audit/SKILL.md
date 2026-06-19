---
name: jgs-v1-audit
description: |
  JGS Model Audit — free, read-only SysML model health audit. Surfaces structural and methodology
  findings with element-ID links, severity grades, and a data-driven Engagement Brief.

  Invocation: /jgs-v1-audit [<root-package-qn-or-id>]

  Requires the JGS MCP bridge (v1 or v2) running on LicenceTier.FREE or higher.
  Makes no writes to the model.

  Use when: auditing a SysML model for naming, documentation, requirement, duplicate, unused-type,
  or methodology issues. The report ends with an Engagement Brief listing JGS-FIXABLE findings
  and a contact CTA.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS Model Audit

You are the orchestrator for the `jgs-v1-audit` skill bundle. You coordinate six specialist
audit sub-skills, merge their findings, and produce a structured report.

**This skill makes no writes to the model.**

---

## Phase 1: Pre-flight

### Step 1.1 — Ping the bridge

Call `mcp__jgs-sysmlv1__ping({})`. If this fails, try `mcp__jgs-sysmlv2__ping({})`.

If both fail:
```
ERROR: JGS MCP bridge is not reachable. Ensure the bridge plugin is running in CATIA Magic
Systems of Systems Architect (MSOSA) and that an MCP server entry for jgs-sysmlv1 or
jgs-sysmlv2 is configured in .mcp.json.
```
Stop.

From the ping response, extract:
- `bridge_adapter` (default `"sysml-v1"` if absent)
- `bridge_version` (default `"unknown"` if absent)
- Project name (from `project_name` field or `"Unknown Project"` if absent)

### Step 1.2 — Resolve root package

If the user provided an argument to `/jgs-v1-audit`, use it as the root package ID directly.

Otherwise call:
```
mcp__jgs-sysmlv1__get_root_package({})
```
(or `mcp__jgs-sysmlv2__get_root_package({})` if v2 bridge detected)

If the response contains multiple top-level packages, list them and ask the user to select one before proceeding.

If no root package is found, print:
```
ERROR: No root package found in the model. Ensure a SysML model is open in MSOSA.
```
Stop.

Store: `root_package_id`, `project_name`, `bridge_adapter`, `bridge_version`.

### Step 1.3 — Validate specialist presence

The six required specialist directories are:
- `jgs-v1-audit-naming`
- `jgs-v1-audit-docs`
- `jgs-v1-audit-requirements`
- `jgs-v1-audit-duplicates`
- `jgs-v1-audit-unused`
- `jgs-v1-audit-methodology`

Check that each directory exists under the `jgs-v1-audit/` folder alongside this `SKILL.md`.
For each missing specialist, create a system finding:

```json
{
  "check_id": "SYS-003",
  "severity": "CRITICAL",
  "domain": "system",
  "title": "Required specialist not found: <name>",
  "detail": "The specialist skill directory '<name>' is missing from the jgs-v1-audit bundle. Reinstall the full bundle from the JGS distribution.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": false,
  "requires_jgs_skills": false
}
```

If any specialists are missing:
1. Assign IDs to the SYS-003 findings (format `AUDIT-SYS-001`, `AUDIT-SYS-002`, etc.)
2. Write a stub report containing only those findings (see Report Format below)
3. Print the terminal summary showing only those findings
4. Stop — do not proceed to Phase 2

---

## Phase 1.5: Native validation (validate_model)

Run CATIA Magic's own validation engine as an authoritative pre-pass, before the heuristic specialists.

Call `mcp__jgs-sysmlv1__validate_model({})` — **no arguments** (model-wide; cannot be scoped).

`validate_model` can return tens of thousands of characters on a real model (~88 KB observed). Do **not**
embed the raw result. Summarize: the total violation count plus a breakdown by severity/rule, and keep at
most **25 representative** violations (with element IDs) for the report's Native Validation section. Store
`native_validation_count` (the true total) and the capped list. If the call errors, set
`native_validation_count` to `"unavailable"` and note it — do **not** abort the audit.

This is the host tool's own verdict (not a heuristic) and leads the report: "CATIA Magic's validator
reported N issues before the JGS heuristic checks ran."

---

## Phase 2: Dispatch Specialists

Dispatch all six specialist sub-skills in parallel using the Agent tool. Pass each:
- The `root_package_id` as the primary argument
- The `bridge_adapter` value as context

Specialist invocations:
- `/jgs-v1-audit-naming <root_package_id>`
- `/jgs-v1-audit-docs <root_package_id>`
- `/jgs-v1-audit-requirements <root_package_id>`
- `/jgs-v1-audit-duplicates <root_package_id>`
- `/jgs-v1-audit-unused <root_package_id>` (with bridge_adapter context)
- `/jgs-v1-audit-methodology <root_package_id>` (with bridge_adapter context)

Each specialist returns a JSON array of findings (without `id` or `jgs_fixable` fields).

If a specialist fails to return valid JSON, emit a SYS-001 finding for it and continue.

---

## Phase 3: Merge, Dedup, Assign IDs

### Step 3.1 — Collect all findings

Combine all finding arrays from all specialists into one pool. Each finding has `check_id`, `severity`, `domain`, `title`, `detail`, `element_id`, `element_qn`, `requires_write_access`, `requires_jgs_skills`.

### Step 3.2 — Deduplicate

Dedup key: `(element_id ?? hash(detail), check_id)`

- If two findings have the same `check_id` and the same non-null `element_id`, they are duplicates — keep the first.
- If two findings have `element_id: null` and the same `check_id` and the same `detail` (trimmed), they are duplicates — keep the first.
- Cross-domain collisions cannot occur because each domain uses a distinct `check_id` prefix (NM, DC, RQ, DU, UN, MT, SYS).

### Step 3.3 — Derive `jgs_fixable`

For each surviving finding:
```
jgs_fixable = requires_write_access OR requires_jgs_skills
```

### Step 3.4 — Assign `id`

Assign `id` after deduplication. NNN increments per domain across post-dedup survivors only (contiguous within each domain):

- `AUDIT-NM-001`, `AUDIT-NM-002`, … for naming findings
- `AUDIT-DC-001`, `AUDIT-DC-002`, … for docs findings
- `AUDIT-RQ-001`, … for requirements findings
- `AUDIT-DU-001`, … for duplicates findings
- `AUDIT-UN-001`, … for unused findings
- `AUDIT-MT-001`, … for methodology findings
- `AUDIT-SYS-001`, … for system findings

### Step 3.5 — Sort

Sort all findings by: severity order (CRITICAL → MAJOR → MINOR → INFO), then by `id`.

---

## Phase 4: Write Report

### Step 4.0 — Emit findings JSON (handoff for jgs-v1-fixplan)

Also write the merged, deduped finding pool (the same findings going into the report) as
`jgs-audit-findings-YYYY-MM-DD.json` — a JSON array of the finding objects plus `project_name`,
`bridge_adapter`, and `root_package_id`. This is the machine-readable handoff that `/jgs-v1-fixplan`
consumes (it never parses the markdown report). No extra tool calls — it serialises the pool already built
in Phase 3.

### Step 4.1 — Determine output filename

Base name: `jgs-audit-report-YYYY-MM-DD.md` (today's date).

If a file with that name already exists in CWD, append a counter:
- `jgs-audit-report-YYYY-MM-DD-2.md`
- `jgs-audit-report-YYYY-MM-DD-3.md`
- etc.

Use the first available name.

### Step 4.2 — Compute counts

```
critical_count = count of findings where severity == "CRITICAL"
major_count    = count of findings where severity == "MAJOR"
minor_count    = count of findings where severity == "MINOR"
info_count     = count of findings where severity == "INFO"
jgs_fixable_count = count of findings where jgs_fixable == true
```

### Step 4.3 — Compute model stats

Call:
```
mcp__jgs-sysmlv1__get_model_metrics({})
```

`get_model_metrics` takes **no arguments** and returns whole-model counts (it cannot be scoped to a
package). Extract `element_count`, `diagram_count`, `requirement_count`. Use 0 if the call fails.
If the audit was scoped to a sub-package, note in the report that these model stats are model-wide.

### Step 4.4 — Write the markdown report

Write to the chosen filename. The report structure:

```
# JGS Model Audit Report

**Project:** <project_name>  **Date:** YYYY-MM-DD  **Bridge version:** <bridge_version>

## Executive Summary

| Severity | Count |
|---|---|
| CRITICAL | <critical_count> |
| MAJOR | <major_count> |
| MINOR | <minor_count> |
| INFO | <info_count> |
| **JGS-FIXABLE** | **<jgs_fixable_count>** |

**Model stats:** <element_count> elements · <diagram_count> diagrams · <requirement_count> requirements

**Native validation (validate_model):** <native_validation_count> rule violation(s) reported by CATIA
Magic's own validator (model-wide), before the JGS heuristic checks. See Native Validation section below.

## Native Validation

Summary of `validate_model` (Phase 1.5): total = <native_validation_count>, by severity/rule:
<one line per severity/rule with counts>. Up to 25 representative violations (element-ID linked):
<capped list, or "validator output unavailable">.

## Findings

### CRITICAL

For each CRITICAL finding, emit:

#### [<id>] <title>

**Element:** `<element_id>` — `<element_qn>`
(omit the Element line if element_id is null — model-wide finding)

**Detail:** <detail>

If jgs_fixable is true, add: **Tag:** `[JGS-FIXABLE]`

---

### MAJOR

(same structure as CRITICAL)

### MINOR

(same structure)

### INFO

(same structure)

## Methodology Assessment

Collect all MT-* findings and produce a prose summary: which layers were found/missing,
whether requirements are grounded, orphan count, allocation status, interface gaps, stub count.
Begin with the MT-000 heuristic disclaimer.
```

### Step 4.5 — Compute effort tier breakdown

For each JGS-FIXABLE finding, assign an effort tier using this lookup (specific check_id row first, then domain wildcard, then Moderate default):

| check_id | Tier |
|---|---|
| MT-001 | Complex |
| MT-002 | Moderate |
| MT-003 | Quick-win |
| MT-004 | Moderate |
| MT-005 | Moderate |
| MT-006 | Quick-win |
| NM-* | Quick-win |
| DC-* | Quick-win |
| DU-* | Quick-win |
| UN-* | Quick-win |
| RQ-* | Moderate |
| (default) | Moderate |

Count: `quick_win_count`, `moderate_count`, `complex_count`.

---

## Phase 5: Generate Engagement Brief

Append to the report file:

```
## Engagement Brief

### Risk Summary

One paragraph calibrated to finding distribution:
- If CRITICAL > 0: "This model has <critical_count> critical finding(s) indicating fundamental SE principle violations. Without resolution, downstream reviews and programme milestones are at risk. Immediate attention is recommended."
- If CRITICAL == 0 and MAJOR > 0: "This model is structurally sound at the critical level but has <major_count> significant gaps that will likely cause traceability failures or review challenges if left unaddressed."
- If CRITICAL == 0 and MAJOR == 0: "This model is in good structural health with <minor_count> quality improvements recommended. These are generally quick to resolve and will reduce maintenance burden."

### Fix Complexity Estimate

<jgs_fixable_count> JGS-FIXABLE finding(s) identified:

| Tier | Count | Description |
|---|---|---|
| Quick-win | <quick_win_count> | Addressable in a single session with write-enabled MCP |
| Moderate | <moderate_count> | Requires structural changes or traceability additions |
| Complex | <complex_count> | Requires methodology rework or governance setup |

### What a JGS Engagement Delivers

- Automated fixes for all quick-win and moderate JGS-FIXABLE findings via write-enabled MCP
- Proprietary methodology skills for SE layer compliance and requirement traceability
- Model governance setup (naming conventions, documentation standards, review checklists)
- Post-fix re-audit to confirm resolution

### Call to Action

Contact JG Systems Consulting Ltd. — <support@jgsystemsconsulting.com>
Most quick-win and moderate JGS-FIXABLE findings in this report can be resolved in a single JGS session.
Complex findings (e.g. SE layer restructure) require a scoped methodology engagement.
```

---

## Phase 6: Terminal Summary

Print to the terminal:

```
JGS Model Audit — <project_name> — YYYY-MM-DD
═══════════════════════════════════════════════
  CRITICAL    <critical_count>
  MAJOR       <major_count>
  MINOR       <minor_count>
  INFO        <info_count>
───────────────────────────────────────────────
  JGS-FIXABLE <jgs_fixable_count>   (require write access or proprietary skills)

Full report: <output_filename>
```

Done.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Passing arguments to `validate_model` / `get_model_metrics` | Both take no arguments and are model-wide — pass `{}`; they cannot be scoped to a package |
| Embedding the full `validate_model` output in the report | It can exceed tens of thousands of characters (~88 KB observed) — summarize by severity/rule, do not inline the raw list |
| Dispatching specialists sequentially | Dispatch all six in parallel via the Agent tool; if one returns invalid JSON, emit a SYS-001 finding and continue rather than aborting the audit |
| Aborting when only the v1 bridge answers `ping` | Fall back to `mcp__jgs-sysmlv2__ping` and the `v2` tool variants only if v1 is unreachable — the audit runs against whichever bridge responds |
