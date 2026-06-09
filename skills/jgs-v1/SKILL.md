---
name: jgs-v1
description: Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills — navigate, audit, impact analysis, migration inventory, cross-model compare. Routes any free-tier SysML v1 request to the right specialist skill.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1 Dispatcher

You are the entry point for all SysML v1 (jgs-magic-sysmlv1-mcp) free-tier skills. Execute the steps below in strict order. Do not skip steps or reorder them.

---

## Step 1 — Liveness check (ALWAYS FIRST)

Call `mcp__jgs-sysmlv1__ping`.

- If the call **fails** (tool error, timeout, connection refused): emit the message below and **HALT**. Do not proceed to Step 2, do not call get_licence, do not route.

  > **Bridge unreachable.** The jgs-magic-sysmlv1-mcp bridge is not responding. Ensure CATIA Magic is running and the v1 bridge plugin is active, then retry.

- If the call **succeeds**: continue to Step 2.

---

## Step 2 — Licence check

Call `mcp__jgs-sysmlv1__get_licence`.

Handle the three possible outcomes:

| Outcome | Action |
|---|---|
| Success, `valid=true` | Read the `tier` field (FREE / PRO / ENTERPRISE). Store it for Step 3. |
| Success, `valid=false` | Warn: "Licence appears invalid or expired — proceeding as FREE tier." Treat tier as FREE. |
| Call failed | Warn: "Could not read licence status — proceeding as FREE tier." Treat tier as FREE. |

---

## Step 3 — Tier guard (BEFORE routing)

Scan the user's request for write-intent phrases. Check for any of the following patterns (case-insensitive):

- "rename [element/block/property]"
- "create [a block/element/package/diagram]"
- "delete [element/block]"
- "add [a relationship/satisfy/dependency]"
- "move [element]"
- "update [element/property]"
- "set [a value/property/documentation]"
- "change [element]"
- "modify [element]"
- "populate [diagram]"
- "edit [element]"

If **any** write-intent phrase is detected **and** the tier is FREE:

> **Write operations require PRO or ENTERPRISE tier.**
>
> The free skills pack is read-only. The operation you requested ("_[phrase detected]_") modifies the model, which requires an upgraded licence.
>
> Would you like me to do a read-only equivalent instead? For example, I can show you the current state of the element, run an impact analysis, or produce an audit report.

**HALT** — do not route. Do not call any tool.

If write-intent is detected and the tier is PRO or ENTERPRISE: proceed normally — all free-tier skills work at higher tiers, and the bridge enforces write safety independently.

If no write-intent is detected: proceed to Step 4.

**Note:** This is a best-effort heuristic, not a security boundary. The bridge enforces read-only access through the absence of `enable_writes`. The tier guard exists to give the user a clear explanation before hitting a bridge-level rejection.

---

## Step 4 — Route to specialist skill

Match the user's request against the routing table below. Use the **first match** found. If no match or ambiguous (see Ambiguity rules), follow the Ambiguity procedure.

### Routing table

| Intent keywords / phrases | Route to |
|---|---|
| navigate, overview, summary, "what am I looking at", explore, browse, tree, packages, blocks, diagram list | `jgs-v1-navigate` |
| impact, "what uses", "blast radius", dependencies, "what references", "before I change" | `jgs-v1-impact` |
| migrate, migration, "v1 to v2", inventory, "v2 plan" | `jgs-v1-migrate-read` |
| cross-model, compare, "v1 vs v2", "v2 equivalent", dual-bridge | `jgs-v1-cross-model` |
| audit, health, naming, documentation, requirements coverage, duplicates, unused, validate, validation, diagram export, export diagrams, PNG, review pack, RTM, traceability matrix | `jgs-v1-audit` |

### Ambiguity rules

Ambiguity occurs when:
- (a) Zero keyword groups match, **or**
- (b) Two or more distinct specialist routes match simultaneously, **or**
- (c) The request contains only `?` or `help`

**Collision exception:** If audit keywords match alongside one other route, default to `jgs-v1-audit` — do not treat this as ambiguous. Exception to the exception: if the non-audit match is clearly dominant (e.g. the user explicitly says "impact" but also mentions "audit" in passing), ask the user to clarify rather than defaulting.

When ambiguous (and no exception applies), present this menu:

> I can help with several things using the SysML v1 skills. Which are you after?
>
> 1. **Navigate** — explore the model structure, packages, blocks, and diagrams
> 2. **Impact analysis** — find what uses an element and assess blast radius before a change
> 3. **Migration inventory** — produce a v1-to-v2 element inventory and migration plan
> 4. **Cross-model compare** — compare v1 and v2 models side by side via dual-bridge
> 5. **Audit** — health check, naming, documentation coverage, duplicates, diagram export, RTM

Ask the user to pick a number or describe what they need, then route accordingly.

---

## Step 5 — Dispatch

Invoke the matched skill using natural language skill composition:

> Use skill `<skill-name>` for this request: [pass through the user's original request verbatim]

Do not call bridge tools directly at this stage — the specialist skill owns its own tool calls.

---

## Missing skills

The following skills are provided by separate packs. If a skill is invoked and not found, tell the user which pack provides it:

| Skill | Pack |
|---|---|
| `jgs-v1-navigate` | jgs-magic-sysmlv1-free-skills |
| `jgs-v1-impact` | jgs-magic-sysmlv1-free-skills |
| `jgs-v1-migrate-read` | jgs-magic-sysmlv1-free-skills |
| `jgs-v1-cross-model` | jgs-magic-sysmlv1-free-skills |
| `jgs-v1-audit` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-naming` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-docs` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-requirements` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-duplicates` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-unused` | jgs-sysmlv1-audit-pack |
| `jgs-v1-audit-methodology` | jgs-sysmlv1-audit-pack |

---

## Direct invocation note

When specialists are invoked directly (not via this dispatcher), they skip liveness and tier checks — raw bridge errors will surface if the bridge is unavailable. This is by design. This dispatcher is the recommended entry point for all jgs-magic-sysmlv1-mcp work.
