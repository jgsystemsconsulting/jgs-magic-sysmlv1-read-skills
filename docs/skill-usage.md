<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Skill Usage Guide · JGS SysML v1 Read Skills

## Entry point

Always start with the dispatcher:

```
/jgs-v1 <your request in plain English>
```

The dispatcher pings the bridge, checks your licence tier, and routes to the right specialist automatically.

## Direct invocation

Each specialist can also be called directly:

```
/jgs-v1-navigate [<package-name>]
/jgs-v1-impact <element-name>
/jgs-v1-audit [<root-package-id>]
```

Direct invocation skips the dispatcher's liveness check, so you'll see raw bridge errors if the bridge is down.

## What requires PRO tier

All skills in this pack are FREE tier (read-only). To make changes to the model, you need:

- **jgs-magic-sysmlv1-mcp PRO licence**
- **jgs-magic-sysmlv1-pro-skills** pack

v1→v2 **migration** (migrate-read inventory, cross-model compare) is also a PRO capability: it is
read-only but ships in the **jgs-magic-sysmlv1-pro-skills** pack, not here.

The dispatcher will tell you when a request needs PRO access and describe what read-only analysis is available instead.

## FREE-tier tools this pack uses

These are the `jgs-sysmlv1` MCP tools referenced by skills in this pack. Short names omit the `mcp__jgs-sysmlv1__` prefix. Purpose phrases come from skill step text; do not treat this as a live bridge `tools/list`.

Catalogue as consumed by this pack version (see README / `RELEASE-INFO.txt`). Bridge tool sets may change over time.

| Tool | Purpose | Example skill(s) |
|------|---------|------------------|
| ping | Bridge liveness | jgs-v1, jgs-v1-audit |
| get_licence | Licence / tier | jgs-v1 |
| get_root_package | Model root package | jgs-v1-audit, jgs-v1-diagrams, jgs-v1-fixplan |
| get_model_metrics | Model-wide metrics / counts | jgs-v1-audit, jgs-v1-navigate, jgs-v1-report |
| walk_tree | Package/element tree walk | jgs-v1-navigate, jgs-v1-diagrams, jgs-v1-fixplan |
| list_children | Direct children of a node | jgs-v1-inspect |
| find_by_name | Name search (capped) | jgs-v1-navigate, jgs-v1-impact, jgs-v1-inspect |
| find_by_qualified_name | Exact qualified-name lookup | jgs-v1-impact, jgs-v1-inspect |
| search | Full-text name search | jgs-v1-search |
| get_element | Element by id | jgs-v1-inspect |
| describe_element | Element description | jgs-v1-inspect |
| get_element_structure | Structural breakdown | jgs-v1-inspect |
| get_ports | Ports on element | jgs-v1-inspect, jgs-v1-fixplan |
| get_relationships | Relationships | jgs-v1-impact, jgs-v1-inspect, jgs-v1-fixplan |
| get_allocations | Allocations | jgs-v1-inspect, jgs-v1-audit-methodology |
| get_qualified_name | Qualified name for id | jgs-v1-inspect |
| list_applied_stereotypes | Stereotypes on element | jgs-v1-inspect |
| impact_analysis | Dependent / impact map | jgs-v1-impact, jgs-v1-fixplan |
| list_diagrams | Diagrams under parent_id | jgs-v1-navigate, jgs-v1-diagrams |
| list_diagram_kinds | Diagram kind inventory | jgs-v1-diagrams |
| list_diagram_symbols | Symbols on a diagram | jgs-v1-diagrams, jgs-v1-audit-methodology |
| list_layout_styles | Layout styles | jgs-v1-diagrams |
| compare_layout_styles | Compare layout styles | jgs-v1-diagrams |
| export_diagram_image | Export diagram image | jgs-v1-diagrams |
| check_naming_conventions | Naming audit | jgs-v1-audit-naming |
| check_documentation_coverage | Docs coverage audit | jgs-v1-audit-docs |
| check_requirement_coverage | Requirement coverage | jgs-v1-audit-requirements, jgs-v1-report |
| find_duplicates | Duplicate detection | jgs-v1-audit-duplicates |
| find_unused_types | Unused types | jgs-v1-audit-unused |
| validate_model | Model validation | jgs-v1-audit, jgs-v1-report |
| generate_model_summary | Model summary | jgs-v1-report |
| export_requirements_matrix | RTM export | jgs-v1-report, jgs-v1-audit-requirements |
| trace_requirement | Requirement trace | jgs-v1-report, jgs-v1-inspect |
| find_unit | Unit lookup | jgs-v1-units |
| find_quantity_kind | Quantity kind lookup | jgs-v1-units |
| get_standard_library_types | Standard library types | jgs-v1-units |
| get_safety_state | Bridge safety state | jgs-v1-status, jgs-v1-fixplan |
| get_edit_history | Recent edit history | jgs-v1-status, jgs-v1-fixplan |

## Result limits

Known bridge caps that skills must respect (from navigate/impact guidance). Rows may name tools skills **warn against** (e.g. `find_by_type`) even when those tools are not in the FREE tools catalogue above.

| Tool / behavior | Limit | Guidance |
|-----------------|-------|----------|
| `find_by_name` | 50 results; silent truncate | Prefer `find_by_qualified_name`; warn when count equals 50 |
| `find_by_type` | 50; model-wide | Do not call `find_by_type` for counts (and do not add it to the FREE tools catalogue). Use `get_model_metrics` for counts instead. |
| `walk_tree` | default `max_elements=200`; skills pass `2000` | Warn when returned count equals 2000 |
| `list_diagrams` | requires `parent_id`; no model-wide call | If `walk_tree` returned more than ~40 packages, diagrams for top two package levels only, or omit with an explicit note |

## Documentation ownership

Stager vs durable edit rules live under **Rules** in [AGENTS.md](../AGENTS.md). Do not hand-edit `SKILLS.md`, `RELEASE-INFO.txt`, or restage-generated HTML in this clone.

## Troubleshooting

**"Bridge is not reachable"**: ensure CATIA Magic is open with a SysML v1 project loaded and the jgs-magic-sysmlv1-mcp plugin is active.

**Results seem truncated**: some bridge tools cap at 50 results or 2000 elements. Use qualified names for exact lookups, or scope the skill to a specific package. See **Result limits** above.

