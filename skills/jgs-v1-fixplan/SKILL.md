---
name: jgs-v1-fixplan
description: Turn a SysML v1 audit's findings into a read-only remediation plan — per-finding recommended action, the exact computed fix where deterministic (rename mapping, removal list), and the PRO/DANGEROUS write tool that would apply each. FREE tier (read-only; computes fixes, never applies them). Requires jgs-magic-sysmlv1-mcp + a jgs-v1-audit findings file. Trigger: "fix plan", "remediation", "how do I fix", "proposed updates", "fix preview", "what to do about findings".
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-fixplan — Read-Only Remediation Plan

## When to use

Use after an audit: it turns severity-graded findings into a read-only remediation plan with the exact computed fix where one is deterministic.

## Prerequisites

- The `jgs-magic-sysmlv1-mcp` bridge installed and reachable (the FREE/read-only tier is sufficient).
- A SysML v1 project open in CATIA Magic / MSOSA.
You are a context-free AI agent executing the `jgs-v1-fixplan` skill. It **diagnoses nothing** — it
consumes a `jgs-v1-audit` findings file and **prescribes**: for each fixable finding it computes a
recommended action, the exact fix where that is deterministic, and the write tool (with its tier) that
would apply it. **This skill is read-only** — it COMPUTES fixes; it MUST NEVER apply them. Never call
`enable_writes`, `enable_dangerous_writes`, or any create/update/delete/rename/move/`execute_groovy`
tool. The only writes are to the local filesystem (the plan files) via the agent's own Write tool.

**Invocation:** `/jgs-v1-fixplan [<path-to-findings-json>]`

> **Behavior-content caveat (bridge gap, 2026-06-17):** the shared `walk_tree` used to compute MT-004/MT-005
> fixes does **not** enumerate `Activity.node`/`edge` or `StateMachine` region/state/transition — a populated
> activity/state-machine reports `childCount:1`. Do not plan a "remove orphaned/empty behavior" fix on that
> basis; if a finding hinges on behavioral content, derive it from `get_model_metrics` type counts, not the tree.

---

## Step 0 — Load the findings (handoff from jgs-v1-audit)

The input is `jgs-audit-findings-YYYY-MM-DD.json` (emitted by `jgs-v1-audit`). Resolve it:
- If a path argument is given, use it. Otherwise pick the **newest** `jgs-audit-findings-*.json` in CWD.
- **No file found:** reply "No audit findings file found. Run `/jgs-v1-audit` first, then re-run `/jgs-v1-fixplan`." Stop. (Do not re-implement the audit checks.)
- **Malformed / missing required fields / different `root_package_id` or `project_name` than the open
  model** (call `mcp__jgs-sysmlv1__get_root_package` to compare): halt with a clear error naming the file
  and the problem. Do NOT silently plan against stale or foreign findings.

**Staleness check:** call `mcp__jgs-sysmlv1__get_edit_history({"max_entries": 1})`; if the model's latest
edit entry is newer than the findings file's mtime, warn that the findings may be stale and recommend
re-running `/jgs-v1-audit`. Otherwise note the findings file timestamp and proceed.

Keep only findings where `jgs_fixable == true`.

---

## Step 1 — Read-only baseline (proof)

Call `mcp__jgs-sysmlv1__get_safety_state` (note the safety tier for the closing note) and
`mcp__jgs-sysmlv1__get_edit_history({"max_entries": 1})` — record the latest entry. At the end of the
run, call `get_edit_history` again; the **latest entry MUST be unchanged** (proof that planning made no
model edits). `count` is capped (~20) so it is only a secondary signal.

---

## Step 2 — Enrich each fixable finding

For each fixable finding compute four fields: `recommended_action` (always), `apply_tool` + its **tier**,
`fix_kind` (`exact` / `candidate` / `manual`), and `fix_preview` (per the table). **Null `element_id`
findings** (model-wide, e.g. MT-001/MT-006): skip per-element work, set `fix_kind=manual`,
`fix_preview=null`, still emit `recommended_action` + `apply_tool`.

| check_id | recommended_action | fix_kind | fix_preview (Slice 1) | apply_tool (tier) |
|---|---|---|---|---|
| NM-* | "Rename to convention." | `exact`* | **Compute the corrected name** (see Step 2a) → `old → new`. | `rename_element` (PRO) |
| UN-* | "Remove unused type." | `exact` | The element is the removal target. | `delete_element` (**DANGEROUS**) |
| MT-003 | "Remove or connect the orphan." | `exact` | The element is the removal target. | `delete_element` (**DANGEROUS**) |
| DU-* | "Merge into the richer twin; remove the other." | `candidate` | Computed keeper + removals (Step 2b). | `delete_element` (**DANGEROUS**) |
| RQ-001 | "Add a satisfy link to the realizing element." | `candidate` | Ranked candidate satisfier (Step 2b). | `add_satisfy` (PRO) |
| RQ-002 | "Add a verify link (test/verification)." | `candidate` | Ranked candidate verifier (Step 2b). | `add_verify` (PRO) |
| MT-002 | "Trace this root block to a requirement." | `candidate` | Ranked candidate requirement (Step 2b). | `add_satisfy` (PRO) |
| MT-004 | "Allocate logical→physical." | `candidate` | Ranked candidate physical target (Step 2b). | `create_allocation` (PRO) |
| MT-005 | "Type the port(s) with an interface block." | `candidate` | Suggested InterfaceBlock per port (Step 2b). | `set_type` (PRO) |
| DC-* | "Add documentation describing purpose." | `manual` | LLM-drafted doc stub (Step 2c). | `set_documentation` (PRO) |
| MT-001 | "Create a diagram/package for the missing SE layer." | `manual` | null. | `create_diagram` / `create_package` (PRO) |
| MT-006 | "Populate or remove the stub diagram." | `manual` | null. | `populate_diagram` / `delete_element` (PRO/DANGEROUS) |

\*NM is `exact` **unless** the computed name collides (Step 2a) → downgrade that finding to `candidate`.

### Step 2a — NM corrected-name computation (deterministic)
From the element's simple name (last segment of `element_qn`):
- **ClassifierMustBeUpperCamelCase:** split on spaces/punctuation; capitalise the first letter of each
  segment; preserve digits; join. e.g. `Use Case 1` → `UseCase1`; `System Requirement 1.1` →
  `SystemRequirement1_1` (keep a `_` where a dot joined two number groups, to avoid silent merge).
- **FeatureMustBeLowerCamelCase:** same, but the first letter is lower-case. e.g. `Total Mass` →
  `totalMass`; `total_mass_sys` → `totalMassSys`.
- **Collision guard:** if the computed name already exists among the element's siblings (same parent),
  do NOT emit it as `exact` — set `fix_kind=candidate` and note "computed name collides — manual choice
  needed." (Sibling names are taken from the findings set / `list_children` if available.)

### Step 2b — Candidate resolution (DU / RQ / MT-002 / MT-004 / MT-005)
Resolve candidates for at most the **top 25 findings per check** (rank: severity desc, then `element_qn`
asc); beyond that, emit action + tool with a "(candidate cap reached — N more unresolved)" note.
Candidate *suggestions within* a finding are ranked by match strength, tie-broken by `element_qn` asc.
All calls here are read-only (FREE). If MT-004/MT-005 need the element tree, call
`mcp__jgs-sysmlv1__walk_tree({"root_id": "<root_id>", "max_depth": 10, "max_elements": 2000})` **once**
and reuse it (warn if the returned count equals 2000 — truncated).

- **DU-*** — group the per-element findings by `type`+`name`. For each group (≤25), call
  `mcp__jgs-sysmlv1__get_relationships({"element_id": "<member>"})` on each member; **keeper = the member
  with the highest relationship count = len(outgoing)+len(incoming)+len(connectors)**; the others are
  removals. `fix_preview` = "keep <keeper_qn>; remove <other_qn(s)>"; CSV `target_id` = keeper id on each
  removal row.
- **RQ-001 / MT-002** — candidate satisfier: call `mcp__jgs-sysmlv1__impact_analysis({"element_id": "<id>"})`
  and `mcp__jgs-sysmlv1__get_relationships({"element_id": "<id>"})` to find related Blocks, and match Block
  names against the requirement/block name. `fix_preview` = "candidate satisfier: <block_qn>" (top match);
  CSV `target_id` = candidate block id.
- **RQ-002** — candidate verifier: same approach, preferring TestCase/verification-stereotyped elements;
  `fix_preview` = "candidate verifier: <qn>".
- **MT-004** — from the shared `walk_tree` result, match the logical block's name against Blocks in a
  package whose name contains "Physical"; `fix_preview` = "allocate to <qn>".
- **MT-005** — for each untyped port (`mcp__jgs-sysmlv1__get_ports({"element_id": "<block>"})`), enumerate
  InterfaceBlocks from the `walk_tree` result (type filter), rank by longest-common-prefix with the owning
  block name, suggest the top one; if none, name `create_interface_block`. `fix_preview` = "type <port>
  with <IfB_qn>".

If no candidate is found for a finding, keep `fix_kind=candidate` with
`fix_preview="no candidate found — manual choice needed"`.

### Step 2c — Documentation stubs (DC) + native-validation relay
- **DC-*** — draft a documentation stub (**≤2 sentences**) from the element's **name and type only**,
  e.g. "<Name> is a <type> in <owning package>. [Purpose — review and complete.]" Label it verbatim:
  **"suggested draft — drafted from name/type only, not authoritative; review before use."**
  `fix_kind=manual`, `fix_preview` = the labelled stub.
- **Native-validation findings** (any with `domain=="native"` / sourced from `validate_model`, if present
  in the findings JSON): relay the host validator's own remedy text verbatim as `recommended_action` —
  do NOT invent one. `fix_kind=manual` unless the validator names a specific element-level fix.

---

## Step 3 — Write the plan

Group by effort tier mapped from `fix_kind`: **Quick-win = `exact`**, **Moderate = `candidate`**,
**Complex = `manual`**.

**`jgs-v1-fixplan-YYYY-MM-DD.md`** (offer to write; new counter suffix if it exists):
```
# SysML v1 Fix Plan — <project_name>
*Generated: <date> · Source findings: <findings file> (<mtime>) · Safety tier: <tier>*

## Scope summary
N of M fixable findings pre-computed.
- PRO edits: <K> (e.g. renames via rename_element)
- DANGEROUS edits: <J> (removals via delete_element — need enable_dangerous_writes)
- Candidate / manual (need human review): <rest>
Per-tool counts: rename_element <n> · delete_element <n> · add_satisfy <n> · …

## Quick-win (exact)
### [<finding id>] <title>
**Element:** `<element_id>` — `<element_qn>`
**Action:** <recommended_action>
**Apply with:** <apply_tool> (<PRO|DANGEROUS>)
**Fix preview:** <e.g. rename "Use Case 1" → "UseCase1">   (omit if null)

## Moderate (candidate)   ## Complex (manual)
(same per-finding block; Fix preview = the computed candidate / doc stub)
```
Cap each tier's detailed entries at **25** (XR-6) + a rollup line for the remainder. The full edit list
goes to the CSV.

**`jgs-v1-fixplan-YYYY-MM-DD.csv`** — uniform columns, no per-row branching:
`element_id, check_id, fix_kind, apply_tool, tier, action, target_id, new_name`
- `element_id` = subject element; `new_name` = computed name for NM renames (else empty); `target_id` =
  relational target (DU keeper / satisfy / allocate target); empty for plain deletes and manual rows.
- A collision-downgraded NM row has `fix_kind=candidate` with empty `new_name`.

## Step 4 — Read-only confirmation + CTA

Re-check `get_edit_history` latest entry == the Step 1 baseline; state "No model changes made (read-only)."
Close: "These are computed proposals. Applying them needs write access — PRO for renames/links,
DANGEROUS tier for removals. Contact JG Systems Consulting Ltd. — <support@jgsystemsconsulting.com>."

---

## Output Format (terminal)
```
Fix Plan — <project_name> — <date>
  Quick-win (exact):  <n>   (renames <n>, removals <n>)
  Moderate (candidate): <n>
  Complex (manual):     <n>
Files: jgs-v1-fixplan-<date>.md, jgs-v1-fixplan-<date>.csv
Read-only confirmed: edit history unchanged.
```

## Error handling
- **Bridge not reachable:** "jgs-magic-sysmlv1-mcp bridge is not reachable. Is CATIA Magic running with the bridge plugin active?" Stop.
- **Findings file issues:** see Step 0 (missing → run audit; malformed/foreign → halt with named error).
- **A read-only-proof call errors:** still write the plan, but note that the read-only proof could not be captured.

## What not to do
- Do NOT apply any fix or call any write/mutation tool — this skill only proposes.
- Do NOT plan against a findings file whose `root_package_id`/`project_name` differs from the open model.
- Do NOT present a collision-prone NM rename as `exact` — downgrade to candidate.
- Do NOT claim removals are a "PRO" fix — `delete_element` is DANGEROUS tier.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Planning against a stale or foreign findings file | Compare `root_package_id`/`project_name` against `get_root_package`, and check `get_edit_history` mtime — halt or warn rather than planning against the wrong model |
| `walk_tree` truncation ignored | It defaults to `max_elements=200` — pass `max_elements=2000` and caveat any fix derived from a result that equals 2000 |
| Treating a removal as a PRO-tier fix | `delete_element` is DANGEROUS tier, not PRO — label the tier of each write tool correctly in the plan |
| Activity / StateMachine planned as "empty" from the tree | `walk_tree`/`get_element_structure` do NOT enumerate Activity nodes/edges or SM regions/transitions — judge behavioral content from `get_model_metrics` type counts, never the tree |