---
name: jgs-v1-units
description: Look up units, quantity kinds, and standard-library types in a SysML v1 model. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "units", "quantity kind", "value types", "standard library types", "find unit", "what library types are available", "is there a unit for".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-units — Units, Quantity Kinds & Library Types

You are a context-free AI agent executing the `jgs-v1-units` skill. **Read-only** — never call
`enable_writes` or any mutation tool.

**Invocation:** `/jgs-v1-units [<name>]`

---

## Tool constraints — read before calling anything

- `find_unit` takes a `name` and returns Unit-stereotyped elements whose name **contains** that
  substring. It cannot enumerate all units — you must supply a name fragment.
- `find_quantity_kind` takes a `name` and works the same way for QuantityKind-stereotyped elements.
- `get_standard_library_types` takes **no arguments** and returns the available standard-library
  DataTypes from the open project (this is the one call that enumerates).

---

## Path A — Name supplied (`/jgs-v1-units <name>`)

1. Call `mcp__jgs-sysmlv1__find_unit({"name": "<name>"})`.
2. Call `mcp__jgs-sysmlv1__find_quantity_kind({"name": "<name>"})`.

Present both result sets:

```
## Units & Quantity Kinds matching "<name>"

### Units
- <Name> — <QualifiedName> (ID: <id>)   (or "— none found —")

### Quantity Kinds
- <Name> — <QualifiedName> (ID: <id>)   (or "— none found —")
```

If both are empty: "No unit or quantity kind matching '<name>'. Note these are substring searches — try a
shorter fragment. Run `/jgs-v1-units` with no argument to list the standard-library DataTypes."

## Path B — No argument (`/jgs-v1-units`)

Call `mcp__jgs-sysmlv1__get_standard_library_types`. Present the available standard-library DataTypes:

```
## Standard-library DataTypes

- <TypeName> (<qualified name if available>)
- ...
```

Then add: "To find a specific unit or quantity kind, run `/jgs-v1-units <name>` (substring match)."

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **A call fails:** note it under its section and continue.

## What not to do

- Do not claim to list *all* units/quantity kinds — `find_unit`/`find_quantity_kind` are substring
  lookups, not enumerations.
- Do not call any write tool.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Claiming `find_unit` / `find_quantity_kind` lists every unit | They are substring lookups requiring a `name` fragment — they cannot enumerate; only `get_standard_library_types` (no args) enumerates |
| Passing a `name` to `get_standard_library_types` | It takes no arguments and returns the open project's standard-library DataTypes — supply nothing |
