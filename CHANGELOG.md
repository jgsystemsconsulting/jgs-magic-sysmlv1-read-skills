<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# Changelog: JGS SysML v1 Read Skills

## 0.2.0 (2026-06-26)

Relicensed the pack from the JG Systems Consulting proprietary EULA to **Apache-2.0**. These
read-only skills are now open source: free to use, fork, and redistribute under Apache-2.0. The
`jgs-magic-sysmlv1-mcp` bridge they drive, and the PRO skills pack, stay proprietary and are
distributed separately.

What this changes:

- `LICENSE` is now the Apache-2.0 text; every source and doc header carries
  `SPDX-License-Identifier: Apache-2.0`; `COPYRIGHT` and `NOTICE` reflect the open-source posture
  (the `NOTICE` file keeps the trademark and third-party attributions, as Apache-2.0 requires).
- Added `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).
- The pack is now listed in the public agent directories for searchable discovery (Anthropic's
  `claude-plugins-official` for Claude Code, and Cursor's public plugin marketplace), in addition
  to the in-repo `.claude-plugin/` and `.cursor-plugin/` manifests.

The skills themselves are unchanged: same 17 read-only workflows, same `/jgs-v1` entry point.

## 0.1.2 (2026-06-26)

Renamed the product from **JGS SysML v1 Free Skills** to **JGS SysML v1 Read Skills** to
describe what the pack does (read-only model analysis) rather than its price. The GitHub
repository moved from `jgs-magic-sysmlv1-free-skills` to `jgs-magic-sysmlv1-read-skills` (the
old URL redirects). The pack remains free to use, and the bridge licence tier (FREE / PRO /
ENTERPRISE) is unchanged: these skills still run on the bridge's FREE / read-only tier.

This release also made the dependency on the **jgs-magic-sysmlv1-mcp** bridge explicit across
the README and landing page, added a "Related products" map linking the free bridge and the PRO
upgrade path, switched security reporting to GitHub security advisories (no email address), and
removed the em dash from all customer-facing prose.

Added a `.cursor-plugin/` manifest so Cursor (2.5+) can install the pack from the repository,
alongside the existing Claude Code `.claude-plugin/` marketplace manifests. As a proprietary
pack, it is not submitted to the open-source-only public directories; discovery is through this
repository and the project landing page.

## 0.1.1 (2026-06-19)

Expanded the pack to 17 read-only skills. Added `jgs-v1-inspect`, `jgs-v1-search`,
`jgs-v1-report`, `jgs-v1-diagrams`, `jgs-v1-units`, `jgs-v1-status`, and `jgs-v1-fixplan`
alongside the original navigate / impact / audit suite. The dispatcher (`jgs-v1`) now routes
across the full free-tier toolset and flags PRO-only capabilities.

## 0.1.0 (2026-05-18)

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
