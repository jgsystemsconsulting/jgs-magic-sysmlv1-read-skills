<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS SysML v1 Free Skills â€” Index

Auto-generated at release time from each skill's frontmatter. 12 skills in this release.

| Skill | Description |
|-------|-------------|
| [`jgs-v1`](skills/jgs-v1/SKILL.md) | Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills — navigate, audit, impact analysis, migration inventory, cross-model compare. Routes any free-tier SysML v1 request to the right specialist skill. |
| [`jgs-v1-audit`](skills/jgs-v1-audit/SKILL.md) | \| JGS Model Audit — free, read-only SysML model health audit. Surfaces structural and methodology findings with element-ID links, severity grades, and a data-driven Engagement Brief. Invocation: /jgs-v1-audit [<root-package-qn-or-id>] Requires the JGS MCP bridge (v1 or v2) running on LicenceTier.FREE or higher. Makes no writes to the model. Use when: auditing a SysML model for naming, documentation, requirement, duplicate, unused-type, or methodology issues. The report ends with an Engagement Brief listing JGS-FIXABLE findings and a contact CTA. |
| [`jgs-v1-audit-docs`](skills/jgs-v1-audit-docs/SKILL.md) | JGS Model Audit — documentation coverage specialist. Checks model elements for missing documentation using check_documentation_coverage. Returns a JSON array of findings conforming to the jgs-model-audit finding schema. |
| [`jgs-v1-audit-duplicates`](skills/jgs-v1-audit-duplicates/SKILL.md) | JGS Model Audit — duplicate elements specialist. Finds duplicate model elements using find_duplicates. Returns JSON findings conforming to the jgs-model-audit finding schema. |
| [`jgs-v1-audit-methodology`](skills/jgs-v1-audit-methodology/SKILL.md) | JGS Model Audit — SE layer hygiene heuristics specialist. Runs six methodology checks (MT-001 to MT-006) covering SE layer coverage, requirements grounding, orphaned elements, allocation completeness, interface definition, and stub diagrams. Returns JSON findings conforming to the jgs-model-audit finding schema. |
| [`jgs-v1-audit-naming`](skills/jgs-v1-audit-naming/SKILL.md) | JGS Model Audit — naming conventions specialist. Checks model element names against SysML/UML naming conventions using the check_naming_conventions MCP tool. Returns a JSON array of findings conforming to the jgs-model-audit finding schema. |
| [`jgs-v1-audit-requirements`](skills/jgs-v1-audit-requirements/SKILL.md) | JGS Model Audit — requirement coverage and traceability specialist. Checks requirement coverage and exports requirements matrix. Returns JSON findings conforming to the jgs-model-audit schema. |
| [`jgs-v1-audit-unused`](skills/jgs-v1-audit-unused/SKILL.md) | JGS Model Audit — unused types and definitions specialist. Detects unused model types using find_unused_types (v1+v2) and find_unused_definitions (v2 only). Returns JSON findings conforming to the jgs-model-audit finding schema. |
| [`jgs-v1-cross-model`](skills/jgs-v1-cross-model/SKILL.md) | Cross-model gap analysis — compare satisfied v1 requirements against element presence in a live v2 model, and surface unsatisfied v1 requirements as traceability gaps. FREE tier on both bridges. Requires jgs-magic-sysmlv1-mcp AND jgs-magic-sysmlv2-mcp both running. |
| [`jgs-v1-impact`](skills/jgs-v1-impact/SKILL.md) | Impact analysis for a SysML v1 element — map dependents, diagrams, and requirement links before making a change. FREE tier. Requires jgs-magic-sysmlv1-mcp. |
| [`jgs-v1-migrate-read`](skills/jgs-v1-migrate-read/SKILL.md) | v1→v2 migration read phase — produce a complete structural inventory of a SysML v1 model as input to a v2 migration plan. FREE tier. Requires jgs-magic-sysmlv1-mcp. |
| [`jgs-v1-navigate`](skills/jgs-v1-navigate/SKILL.md) | Navigate and inspect a SysML v1 model — produce a structured overview of packages, element counts, and diagrams. FREE tier. Requires jgs-magic-sysmlv1-mcp. |
