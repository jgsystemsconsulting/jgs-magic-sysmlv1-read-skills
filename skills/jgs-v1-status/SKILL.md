---
name: jgs-v1-status
description: Report the SysML v1 bridge safety state (tier/mode) and recent model edit history. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "safety state", "what tier am I", "am I in write mode", "dev mode status", "edit history", "what changed recently", "undo stack".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# jgs-v1-status — Bridge Safety State & Edit History

You are a context-free AI agent executing the `jgs-v1-status` skill. **Read-only** — never call
`enable_writes` or any mutation tool.

**Invocation:** `/jgs-v1-status [<max-entries>]`

---

## Tool constraints

- `get_safety_state` takes no arguments; returns the current safety tier (READ / WRITE / DANGEROUS) and
  dev-mode status.
- `get_edit_history` takes an optional integer `max_entries`; returns recent edits (undo stack).

---

## Step 1 — Safety state

Call `mcp__jgs-sysmlv1__get_safety_state`. Report the tier and whether dev mode is on.

## Step 2 — Edit history

Call `mcp__jgs-sysmlv1__get_edit_history({"max_entries": <n>})` (default `max_entries` to 20 if not
supplied). Summarise the most recent edits newest-first.

---

## Output Format

```
## SysML v1 Bridge Status

**Safety tier:** <READ | WRITE | DANGEROUS>
**Dev mode:** <on | off>

### Recent edits (latest first)
1. <action> — <element/target> <when if available>
2. ...
(or "No edit history available.")
```

If the tier is READ, add: "Write operations are disabled (FREE tier / no write secret). The free skills
are read-only by design."

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **`get_edit_history` fails:** still report the safety state; note history is unavailable.

## What not to do

- Do not call any write tool.
- Do not attempt to change the tier or mode — this skill only reports state.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Passing arguments to `get_safety_state` | It takes no arguments and returns the current tier (READ/WRITE/DANGEROUS) plus dev-mode status |
| Aborting when `get_edit_history` fails | Still report the safety state — note history is unavailable rather than failing the whole skill |
