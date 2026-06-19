---
name: jgs-v1-search
description: Full-text search across element names in a SysML v1 model and present ranked hits with type, qualified name, and ID. FREE tier (read-only). Requires jgs-magic-sysmlv1-mcp. Trigger: "search", "find anything matching", "search the model for", "where is", "look for elements named".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-search — Full-Text Model Search

You are a context-free AI agent executing the `jgs-v1-search` skill. **Read-only** — never call
`enable_writes` or any mutation tool.

**Invocation:** `/jgs-v1-search <query> [<max-results>]`

---

## Tool constraint

`search` takes `query` (required) and an optional integer `max_results`. It is a full-text search across
element names. For an exact element by path, prefer `jgs-v1-navigate` / `jgs-v1-inspect` with a qualified
name instead.

---

## Step 1 — Run the search

Call `mcp__jgs-sysmlv1__search({"query": "<query>", "max_results": <n>})`. Default `max_results` to 50 if
the user did not specify one.

## Step 2 — Present results

Render hits as a numbered list, grouped by element type when there are many:

```
## Search results for "<query>"  (<count> hit(s))

### Blocks
[1] <Name> — <QualifiedName> (ID: <id>)
### Requirements
[2] <Name> — <QualifiedName> (ID: <id>)
...
```

If the number of hits equals the requested `max_results`, add:
> "Results may be truncated at <max_results>. Re-run with a higher max, or narrow the query."

If zero hits: "No elements matched '<query>'. Try a shorter or partial term, or `/jgs-v1-navigate` to browse."

## Step 3 — Offer next action

Append: "Use `/jgs-v1-inspect <name>` for a full dossier on any result, or `/jgs-v1-impact <name>` to
assess change blast-radius."

---

## Error handling

- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **Tool returns an error** (e.g. a bridge `ScriptException` / `script-execution-failed` — the `search`
  tool itself failed, not the connection): do not retry in a loop. Report clearly and offer the working
  fallbacks: "The `search` tool returned an error on this model (known bridge issue on some models). As
  a fallback, use `/jgs-v1-navigate` to browse the structure, or `/jgs-v1-inspect <name>` /
  `find_by_qualified_name` if you know roughly what you're after."
- **Empty/garbled response:** report "search returned no usable data" and stop.

## What not to do

- Do not call any write tool.
- Do not omit the truncation warning when hits == max_results.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Treating hits == `max_results` as the full set | The result is likely truncated — warn the user and offer to re-run with a higher max or a narrower query |
| Retrying `search` in a loop after a `ScriptException` | The tool errors on some models (known bridge issue) — report once and fall back to `/jgs-v1-navigate` or `find_by_qualified_name` |
