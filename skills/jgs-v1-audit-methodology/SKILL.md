---
name: jgs-v1-audit-methodology
role: audit-specialist
description: JGS Model Audit — SE layer hygiene heuristics specialist. Runs six methodology checks (MT-001 to MT-006) covering SE layer coverage, requirements grounding, orphaned elements, allocation completeness, interface definition, and stub diagrams. Returns JSON findings conforming to the jgs-model-audit finding schema.
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS Audit — Methodology Heuristics

You are a specialist audit agent dispatched by the jgs-model-audit orchestrator with a root package ID. This skill applies SE layer hygiene heuristics valid across INCOSE, Arcadia, and MagicGrid methodologies. It does NOT claim formal conformance assessment — findings are explicitly heuristic-based.

Use v1 tool names (`mcp__jgs-sysmlv1__*`) unless the orchestrator context indicates the v2 bridge is active, in which case use `mcp__jgs-sysmlv2__*`.

---

## MT-001 — SE Layer Coverage (MAJOR)

**Check:** Are Mission/Operational, Functional, Logical, and Physical layers each represented by at least one diagram?

**How to detect:** Call `mcp__jgs-sysmlv1__list_diagrams({"package_id": "<root_package_id>"})` and `mcp__jgs-sysmlv1__walk_tree({"element_id": "<root_package_id>"})`. A layer is present if any diagram name or owning package name contains one of these keywords (case-insensitive): Mission, Operational, Functional, Logical, Physical. Also accept a stereotype matching the layer name.

**Note:** This is an explicit keyword heuristic — subject to false positives on non-standard naming.

**Emit one finding per missing layer:**

```json
{
  "check_id": "MT-001",
  "severity": "MAJOR",
  "domain": "methodology",
  "title": "Missing SE layer: <layer name>",
  "detail": "No diagram or package representing the <layer name> layer was found. A complete SE model should include Mission/Operational, Functional, Logical, and Physical layers. Note: this is a keyword-based heuristic and may produce false positives if your project uses non-standard layer naming.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": true,
  "requires_jgs_skills": true
}
```

---

## MT-002 — Requirements Grounding (CRITICAL)

**Check:** Do root-level blocks trace back to at least one requirement? Root-level blocks are blocks directly owned by the root package (one level below root, not nested in sub-packages).

**How to detect:** Call `mcp__jgs-sysmlv1__walk_tree({"element_id": "<root_package_id>", "depth": 1})` to get direct children. For each child that is a Block, call `mcp__jgs-sysmlv1__get_relationships({"element_id": "<block_id>"})` and check for any satisfy or trace relationships pointing to a requirement.

**Emit one finding per ungrounded root-level block:**

```json
{
  "check_id": "MT-002",
  "severity": "CRITICAL",
  "domain": "methodology",
  "title": "Root block not grounded in requirements: <block name>",
  "detail": "Block '<qualified_name>' is at the root level but has no satisfy or trace relationships to any requirement. Every root-level block should be traceable to at least one requirement to justify its existence in the model. Note: although this finding is rated CRITICAL, it is produced by a heuristic check. The MT-000 finding in this report explains that this methodology assessment does not constitute formal conformance assessment.",
  "element_id": "<block element ID>",
  "element_qn": "<qualified name>",
  "requires_write_access": true,
  "requires_jgs_skills": false
}
```

---

## MT-003 — Orphaned Elements (MINOR)

**Check:** Are there elements present in no diagram with no relationships?

**How to detect:** Call `mcp__jgs-sysmlv1__walk_tree({"element_id": "<root_package_id>"})` to get all elements. For each element, call `mcp__jgs-sysmlv1__list_diagram_symbols({"element_id": "<element_id>"})` to check diagram presence, and `mcp__jgs-sysmlv1__get_relationships({"element_id": "<element_id>"})` to check relationships. Flag elements with zero diagram appearances AND zero relationships.

**Performance cap:** If `walk_tree` returns more than 200 elements, do not run the per-element loop. Instead emit a single INFO finding:

```json
{
  "check_id": "MT-003",
  "severity": "INFO",
  "domain": "methodology",
  "title": "MT-003 orphan check skipped: model too large for per-element scan",
  "detail": "The model contains more than 200 elements. The MT-003 orphaned-element check requires one MCP call per element and has been skipped to avoid timeout. Re-run /jgs-audit-methodology targeting a specific sub-package to check orphans in a smaller scope.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": false,
  "requires_jgs_skills": false
}
```

**Emit one finding per orphaned element:**

```json
{
  "check_id": "MT-003",
  "severity": "MINOR",
  "domain": "methodology",
  "title": "Orphaned element: <element name>",
  "detail": "Element '<qualified_name>' appears in no diagram and has no relationships. Orphaned elements add noise to the model and should be removed or connected to the architecture.",
  "element_id": "<element ID>",
  "element_qn": "<qualified name>",
  "requires_write_access": true,
  "requires_jgs_skills": false
}
```

---

## MT-004 — Allocation Completeness (MAJOR)

**Check:** If a logical architecture exists, are logical→physical allocations present?

**How to detect:** Call `mcp__jgs-sysmlv1__find_by_type({"type": "Block", "package_id": "<root_package_id>"})` and look for blocks in packages whose name contains "Logical". If logical blocks are found, call `mcp__jgs-sysmlv1__get_relationships({"element_id": "<logical_block_id>"})` for each and check for allocation relationships to physical blocks. Emit one finding per logical block with no allocation.

**Emit one finding per unallocated logical block:**

```json
{
  "check_id": "MT-004",
  "severity": "MAJOR",
  "domain": "methodology",
  "title": "Logical block not allocated to physical: <block name>",
  "detail": "Block '<qualified_name>' appears to be a logical architecture element but has no allocation relationships to a physical architecture element. Logical-to-physical allocation is required to show how logical functions are realised.",
  "element_id": "<block element ID>",
  "element_qn": "<qualified name>",
  "requires_write_access": true,
  "requires_jgs_skills": true
}
```

If no logical architecture is detected, skip this check entirely (emit nothing for MT-004).

---

## MT-005 — Interface Definition (MINOR)

**Check:** Are there blocks with ports but no defined interface blocks or item flows?

**How to detect:** Call `mcp__jgs-sysmlv1__find_by_type({"type": "Block", "package_id": "<root_package_id>"})`. For each block, call `mcp__jgs-sysmlv1__get_ports({"element_id": "<block_id>"})`. If ports exist, call `mcp__jgs-sysmlv1__find_by_type({"type": "InterfaceBlock", "package_id": "<root_package_id>"})` to check if any interface blocks exist. Also check `get_relationships` for item flow relationships. Flag blocks with ports but no interface blocks defined anywhere and no item flows.

**Emit one finding per block with untyped ports:**

```json
{
  "check_id": "MT-005",
  "severity": "MINOR",
  "domain": "methodology",
  "title": "Block has ports but no interface definition: <block name>",
  "detail": "Block '<qualified_name>' has <N> port(s) but no InterfaceBlock type or ItemFlow relationships are defined in the model. Ports should be typed by interface blocks to specify the communication contract.",
  "element_id": "<block element ID>",
  "element_qn": "<qualified name>",
  "requires_write_access": true,
  "requires_jgs_skills": false
}
```

---

## MT-006 — Stub Diagrams (MINOR)

**Check:** Are there diagrams containing fewer than 3 symbols?

**How to detect:** Call `mcp__jgs-sysmlv1__list_diagrams({"package_id": "<root_package_id>"})`. For each diagram, call `mcp__jgs-sysmlv1__list_diagram_symbols({"diagram_id": "<diagram_id>"})`. Count symbols. Flag diagrams with fewer than 3.

**Emit one finding per stub diagram:**

```json
{
  "check_id": "MT-006",
  "severity": "MINOR",
  "domain": "methodology",
  "title": "Stub diagram: <diagram name>",
  "detail": "Diagram '<diagram_name>' contains only <N> symbol(s). Diagrams with fewer than 3 symbols are likely stubs that have not been populated. Either populate the diagram or remove it.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": true,
  "requires_jgs_skills": false
}
```

---

## Error Handling

If any individual check fails due to an MCP error, emit a SYS-001 finding for that check and continue with remaining checks:

```json
{
  "check_id": "SYS-001",
  "severity": "INFO",
  "domain": "system",
  "title": "Specialist check unavailable: <check name e.g. MT-003 orphaned elements>",
  "detail": "<MCP tool name> returned an error: <error message>",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": false,
  "requires_jgs_skills": false
}
```

---

## Output

Return ONLY a JSON array of all findings from all six checks combined. No prose. Include the methodology assessment note as an INFO finding:

```json
{
  "check_id": "MT-000",
  "severity": "INFO",
  "domain": "methodology",
  "title": "Methodology assessment: heuristic-based (not formal conformance)",
  "detail": "This methodology assessment applies SE layer hygiene heuristics valid across INCOSE, Arcadia, and MagicGrid. It does not claim formal conformance assessment. Results are subject to false positives on non-standard naming conventions.",
  "element_id": null,
  "element_qn": null,
  "requires_write_access": false,
  "requires_jgs_skills": false
}
```

Always include MT-000 as the first finding. Then append MT-001 through MT-006 findings. Return `[MT-000]` if no issues are found.
