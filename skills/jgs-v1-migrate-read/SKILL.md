---
name: jgs-v1-migrate-read
description: v1→v2 migration read phase — produce a complete structural inventory of a SysML v1 model as input to a v2 migration plan. FREE tier. Requires jgs-magic-sysmlv1-mcp.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-migrate-read — v1→v2 Migration Read Phase (UC-V1-08)

Produce a complete structural inventory of a SysML v1 model to drive a v2 migration plan. Read-only — the actual v2 model build is a separate step.

**Invocation:** `/jgs-v1-migrate-read [<root-package>]`

---

## Step 1 — Locate the model root

Call `mcp__jgs-sysmlv1__get_root_package`.

If a `<root-package>` argument was provided, instead call `mcp__jgs-sysmlv1__find_by_name` with that name to resolve the scoped package — bridge cap: 50 results.
- **Zero results:** Report "Package '<name>' not found. Use /jgs-v1-migrate-read with no argument to use the model root."
- **One result:** Proceed — use the returned element ID as the scoped root.
- **Multiple results (2–49):** Present them as a numbered list using the format `[N] TypeName — QualifiedName (ID: ...)` and ask "Which package did you mean?" Wait for user selection.
- **Exactly 50 results:** Present the list and add: "The result list may be truncated at 50. If your target package is not shown, provide its fully-qualified name and use `mcp__jgs-sysmlv1__find_by_qualified_name` instead."

Store the resolved element ID as `root_id`.

---

## Step 2 — Walk the model tree

Call `mcp__jgs-sysmlv1__walk_tree` with:
- `root_id = root_id`
- `max_depth = 10`
- `max_elements = 2000`

From the returned list, count Block elements by filtering entries where `type = "Block"`. Store this as `block_count`. Store the full list of Block IDs as `block_ids` — these are the IDs step 6 will iterate.

**Truncation warning:** If the number of returned elements equals 2000, add this note to the output: "Inventory may be incomplete — walk_tree was truncated at 2000 elements. Re-run scoped to individual packages for complete data."

---

## Step 3 — Model-wide metrics

Call `mcp__jgs-sysmlv1__get_model_metrics`.

Use the returned statistics for accurate model-wide counts in the summary section. Do not use these counts for the Block-count threshold in step 5 — use the walk_tree Block count from step 2.

---

## Step 4 — Requirement coverage

Call `mcp__jgs-sysmlv1__check_requirement_coverage`.

Extract the total requirement count and the count of unsatisfied requirements for the summary and gap table.

---

## Step 5 — Relationship fetch gate

**Block count for this check = `block_count` from step 2** (Block-typed entries in the walk_tree result — not the model-wide metric from step 3).

If `block_count >= 50`:

> Present this exact prompt to the user:
> "This model has N Blocks in scope. Fetching relationships will make N sequential bridge calls and may take several minutes. Proceed? (y/n)"
> (Replace N with the actual block_count.)

- **User answers y:** proceed to step 6.
- **User answers n or does not respond:** skip step 6. In the output, mark the "Relationship count" column as `—` and add the note: "Relationship inventory skipped by user. Re-run with a scoped package, or accept the delay on the full model." Omit the migration order ranking section. Continue to step 7 with partial data.

If `block_count < 50`: proceed directly to step 6 without prompting.

---

## Step 6 — Per-Block relationship collection

For each Block ID in `block_ids`, call `mcp__jgs-sysmlv1__get_relationships` with that element ID.

Collect all relationship types and their targets. Group by relationship kind (e.g. Association, Generalization, Dependency, ItemFlow). Deduplicate relationship entries for the same pair.

For each package, count the relationships where the target element's qualified name has a different immediate-child-of-root package prefix than the source Block. This is the cross-package dependency count used in step 7's migration ranking.

**Package prefix rule:** The immediate-child-of-root prefix is the first segment of the qualified name after the root package name. For example:
- `SensorsPackage::Sub::X` and `SensorsPackage::Y` share prefix `SensorsPackage` — same package.
- `SensorsPackage::X` and `ThermalPackage::Y` have different prefixes — cross-package dependency.

---

## Step 7 — Produce migration inventory document

Output the following structured markdown document. Replace all bracketed placeholders with actual data.

```markdown
## v1 Migration Inventory — [model root name]
*Generated: [date]*

### Summary
- [block_count] Blocks across [package_count] packages
- [relationship_count] relationship types found [or: relationship inventory skipped]
- [unsatisfied_count] unsatisfied requirements (of [total_count] total)
- [diagram_count] diagrams (will require manual re-creation in v2 — diagram migration is not automated)

### Package inventory

| Package | Block count | Relationship count |
|---------|------------|-------------------|
| [package name] | [n] | [n or —] |
| ... | | |

### Requirement gaps

| Requirement ID | Requirement text | Satisfied |
|---------------|-----------------|-----------|
| [REQ-ID] | [text] | [Yes / No] |
| ... | | |

### Recommended v2 migration order
[Include only if step 6 was NOT skipped]

Packages ranked by ascending cross-package dependency count (fewer external dependencies = safer to migrate first):

| Rank | Package | Cross-package dependencies |
|------|---------|--------------------------|
| 1 | [package name] | [count] |
| ... | | |

### Next steps
To build the v2 model: use jgs-magic-sysmlv2-mcp PRO tier with the above inventory as input.
```

If step 6 was skipped, omit the "Recommended v2 migration order" section entirely and include this note in its place:

> Migration order unavailable — relationship data was not collected. Re-run with relationships enabled to generate a ranked migration plan.

---

## Output delivery

After displaying the inventory document, offer: "Would you like me to write this to a file? (e.g. `v1-migration-inventory-[model-name].md`)"

If the user says yes, use the filesystem write tools available to the agent (Read/Write/Edit) to save the file. Do NOT call any write tools on the `jgs-sysmlv1` bridge — all v1 bridge calls in this skill are read-only.

---

## Error handling

- **Bridge unreachable:** If any `mcp__jgs-sysmlv1__*` call returns a connection error, report: "jgs-magic-sysmlv1-mcp bridge is not reachable. Is the CATIA Magic instance running with its bridge plugin active?" and stop.
- **Empty walk_tree result:** If walk_tree returns zero elements, report: "walk_tree returned no elements for root ID [root_id]. Verify the model is loaded and the root package ID is correct."
- **get_relationships errors on individual Blocks:** Log the Block ID and continue iterating — do not abort the full loop. Note at the end: "Relationship fetch failed for [n] Block(s): [list of IDs]. These are excluded from relationship counts."
