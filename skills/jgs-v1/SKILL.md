---
name: jgs-v1
description: Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills — navigate, inspect, search, impact, audit, report, diagrams, units, status, fix-plan. Routes any free-tier SysML v1 request to the right specialist skill, and flags PRO-only capabilities (migration, cross-model, model writes).
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
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
> The read-only skills pack does not modify models. The operation you requested ("_[phrase detected]_") modifies the model, which requires an upgraded licence.
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
| inspect, "tell me everything about", "describe this element", element details, "what is X" | `jgs-v1-inspect` |
| search, "find anything matching", "look for", "where is" | `jgs-v1-search` |
| audit, "health check", naming, documentation coverage, requirements coverage, duplicates, unused, methodology | `jgs-v1-audit` |
| RTM, "traceability matrix", "requirements matrix", "model report", "model health report", "model summary", validate, validation | `jgs-v1-report` |
| "fix plan", remediation, "how do I fix", "proposed updates", "fix preview", "what to do about findings" | `jgs-v1-fixplan` |
| "diagram export", "export diagrams", PNG, "review pack", "diagram inventory", "layout styles", "compare layouts" | `jgs-v1-diagrams` |
| units, "quantity kind", "value types", "standard library types", "find unit" | `jgs-v1-units` |
| "safety state", tier, "dev mode", "edit history", "what changed", "undo stack" | `jgs-v1-status` |

### PRO-tier capabilities (not in this free pack)

The following are **read-only but premium** capabilities that ship in the separate **SysML v1 PRO skills pack** (sold by JG Systems Consulting Ltd), not in this free pack. If the request matches one of these intents, do **not** route to a specialist — instead tell the user it is a PRO capability and show the upgrade path below.

| Intent keywords / phrases | PRO capability |
|---|---|
| migrate, migration, "v1 to v2", "v2 migration", "v2 plan", "migration inventory" | Migration inventory (v1→v2 readiness) |
| cross-model, "v1 vs v2", "v2 equivalent", "compare v1 and v2", dual-bridge | Cross-model compare |

Response template:

> That capability ("_[intent]_") is part of the **SysML v1 PRO skills pack** (read-only migration tooling, sold separately). This free pack covers read / navigate / analysis only. To enable it, contact JG Systems Consulting Ltd at **support@jgsystemsconsulting.com** to upgrade.

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
> 2. **Inspect** — full dossier on a single element (type, ports, relationships, stereotypes, requirement links)
> 3. **Search** — full-text search across element names
> 4. **Impact analysis** — find what uses an element and assess blast radius before a change
> 5. **Audit** — heuristic health check: naming, documentation, requirements, duplicates, unused, methodology
> 6. **Report** — model-health summary + Requirements Traceability Matrix + native validation, exported to a file
> 7. **Diagrams** — inventory and export diagram images (visual review pack)
> 8. **Units** — look up units, quantity kinds, and standard-library types
> 9. **Status** — bridge safety tier/mode and recent edit history
> 10. **Fix plan** — turn audit findings into a remediation plan (recommended actions + computed fixes + the PRO tool to apply each)
>
> _Migration inventory and cross-model compare are PRO-tier capabilities (SysML v1 PRO skills pack) — ask to upgrade._

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
| `jgs-v1-navigate` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-inspect` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-search` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-impact` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-report` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-diagrams` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-units` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-status` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-fixplan` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-naming` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-docs` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-requirements` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-duplicates` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-unused` | jgs-magic-sysmlv1-read-skills |
| `jgs-v1-audit-methodology` | jgs-magic-sysmlv1-read-skills |

---

## Direct invocation note

When specialists are invoked directly (not via this dispatcher), they skip liveness and tier checks — raw bridge errors will surface if the bridge is unavailable. This is by design. This dispatcher is the recommended entry point for all jgs-magic-sysmlv1-mcp work.

## Common Mistakes

No tool gotchas — this dispatcher only calls `ping` and `get_licence` to route; the model-introspection, diagram, and write caveats live in each specialist skill it dispatches to.
