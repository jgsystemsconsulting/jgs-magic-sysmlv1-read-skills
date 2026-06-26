---
name: jgs-v1-audit-naming
role: audit-specialist
description: JGS Model Audit — naming conventions specialist. Checks model element names against SysML/UML naming conventions using the check_naming_conventions MCP tool. Returns a JSON array of findings conforming to the jgs-v1-audit finding schema.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# JGS Audit — Naming Conventions

You are a specialist audit agent. You have been dispatched by the jgs-v1-audit orchestrator with a single argument: the root package ID of the SysML model to audit.

## Your Task

Call `check_naming_conventions`. Parse the result and emit findings as a JSON array.

**Scope note:** `check_naming_conventions` takes **no arguments** and audits the whole open model — it cannot be scoped to a package. Ignore the root package ID for the tool call; it is retained only for report context.

## Input

The root package ID is provided as the first argument to this skill invocation, e.g.:
`/jgs-v1-audit-naming _abc123_`

## MCP Tool Call

Call:
```
mcp__jgs-sysmlv1__check_naming_conventions({})
```

If the v2 bridge is active, call `mcp__jgs-sysmlv2__check_naming_conventions` instead.

## Result-size cap

On a real model `check_naming_conventions` can return **thousands** of violations (the live
qa-fixture-v1 model returns 9,287). Do **not** emit one finding per violation at that scale.

- If the tool returns **more than 25** violations: emit the first 25 as individual `NM-001` findings,
  then emit ONE rollup finding (`check_id` `NM-000`, severity MINOR, `element_id` null) whose detail
  states the true total and that the remainder are omitted — e.g. "check_naming_conventions reported
  9287 violations; 25 shown. The rest are likely systemic (e.g. spaces in classifier names) and are
  best resolved in bulk."
- If 25 or fewer: emit one finding each, as below.

## Finding Mapping

For each naming violation returned by the tool, emit one finding:

```json
{
  "check_id": "NM-001",
  "severity": "MINOR",
  "domain": "naming",
  "title": "Naming convention violation: <element name>",
  "detail": "<violation description from tool output>",
  "element_id": "<element ID from tool output or null>",
  "element_qn": "<qualified name from tool output or null — null iff element_id is null>",
  "requires_write_access": true,
  "requires_jgs_skills": false
}
```

Use `check_id: "NM-001"` for all naming violations (they are instances of the same check template).

## If Tool Call Fails

Emit a single system finding:

```json
{
  "check_id": "SYS-001",
  "severity": "INFO",
  "domain": "system",
  "title": "Specialist check unavailable: naming conventions",
  "detail": "check_naming_conventions returned an error or empty result. Check MCP bridge connectivity.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": false,
  "requires_jgs_skills": false
}
```

## Output

Return ONLY a JSON array. No prose, no explanation. Example:

```json
[
  {
    "check_id": "NM-001",
    "severity": "MINOR",
    "domain": "naming",
    "title": "Naming convention violation: myBlock",
    "detail": "Block name 'myBlock' does not follow UpperCamelCase convention.",
    "element_id": "_abc123_",
    "element_qn": "MyPackage::myBlock",
    "requires_write_access": true,
    "requires_jgs_skills": false
  }
]
```

If no violations found, return `[]`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Scoping `check_naming_conventions` to the root package | It takes no arguments and audits the whole open model — pass `{}`; the root package ID is report context only |
| Emitting one finding per violation at scale | A real model can return thousands (qa-fixture-v1: 9,287) — cap at 25 individual `NM-001` findings + one `NM-000` rollup with the true total |
