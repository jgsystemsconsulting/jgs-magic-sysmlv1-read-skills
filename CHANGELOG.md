<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Changelog · JGS SysML v1 Read Skills

## 0.3.0 - 2026-09-09

New generation of the read-skills pack, superseding the pre-0.3 releases in this
repository's history. Rebranded to JGS SysML v1 Read Skills; the licence reverts to
the JGS EULA (the pack remains free of charge); the earlier releases stay under
their existing tags as the Apache-2.0 record.

- 18 read-only skills: the audit specialists (naming, docs, requirements,
  duplicates, unused, methodology), navigate, inspect, search, impact, report,
  diagrams, units, status, fixplan, and the in-pack `/jgs-v1-feedback` reporter.
- Installers for seven agent hosts: ZCode, Claude Code (default), OpenClaw,
  GitHub Copilot CLI, OpenAI Codex CLI, Gemini CLI, and Cursor (project-local).
- Marketplace manifests for Claude Code, Cursor, Codex, and Gemini CLI.
- Shipped release gate (`scripts/check_release.py`), bug and skill-improvement
  issue forms, private-advisory security policy, `CITATION.cff`, and a
  distribution ledger (`docs/DISTRIBUTION.md`).
- Two-page documentation site (landing plus guide) on a shared stylesheet, with
  structural checks in CI.

## 0.1.1 - 2026-06-19

Expanded the pack to 18 read-only skills: added `jgs-v1-inspect`,
`jgs-v1-search`, `jgs-v1-report`, `jgs-v1-diagrams`, `jgs-v1-units`, `jgs-v1-status`,
and `jgs-v1-fixplan` alongside the original navigate/impact/audit suite. The dispatcher
(`jgs-v1`) now routes across the full free-tier toolset and flags PRO-only capabilities.

## 0.1.0 - 2026-05-18

Initial release.

**Skills included (10):**

- `jgs-v1`: dispatcher / entry point
- `jgs-v1-navigate`: model navigation and overview (UC-V1-01)
- `jgs-v1-impact`: blast-radius analysis before a change (UC-V1-10)
- `jgs-v1-audit`: full audit orchestrator
- `jgs-v1-audit-naming`: naming convention violations (UC-V1-06)
- `jgs-v1-audit-docs`: documentation coverage gaps
- `jgs-v1-audit-requirements`: requirement coverage + RTM export (UC-V1-02, UC-V1-14)
- `jgs-v1-audit-duplicates`: duplicate element detection
- `jgs-v1-audit-unused`: unused type detection (UC-V1-13)
- `jgs-v1-audit-methodology`: BDD/IBD/parametric heuristics; validation; diagram export (UC-V1-05, UC-V1-09)
