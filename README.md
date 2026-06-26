<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# JGS SysML v1 Read Skills

![Licence](https://img.shields.io/badge/licence-Apache--2.0-blue) ![Version](https://img.shields.io/badge/version-0.2.0-green) ![Skills](https://img.shields.io/badge/skills-17-orange) ![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-8A2BE2)

**Version:** 0.2.0  
**Vendor:** JG Systems Consulting Ltd.  
**Licence:** Apache-2.0 (free and open source). Requires the proprietary jgs-magic-sysmlv1-mcp bridge (FREE tier).

> [!IMPORTANT]
> **Requires the free [jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp) bridge.**
> These skills do nothing on their own. They drive the bridge's read-only (FREE tier) tools to
> analyse a live SysML v1 model in CATIA Magic. Install the bridge first; its FREE tier is all
> this pack needs. See [Related products](#related-products) for the bridge and the PRO upgrade.

---

## What this is

A free bundle of 17 Claude Code skills for engineers working with SysML v1 models in CATIA Magic
Systems of Systems Architect (MSOSA). Every skill is read-only: no write access, no licence key,
no model mutation.

Start with `/jgs-v1` and describe what you need in plain English.

New here? The [Skill Usage Guide](docs/skill-usage.md) walks through the entry point, direct
invocation, and troubleshooting.

---

## Install with your AI agent

Copy everything in the block below and paste it into your coding agent
(Claude Code, Cursor, etc.). It will read this repo and install the pack for you.

```text
You are installing jgs-magic-sysmlv1-read-skills, a free, read-only Claude Code skills pack
(JG Systems Consulting Ltd.) of read-only analysis skills for SysML v1 models in
CATIA Magic. Repository: https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills (version 0.2.0). Do this in order:

1. Read README.md, docs/skill-usage.md, and CHANGELOG.md in this repository so you
   understand what you are installing and its prerequisites.
2. Confirm the prerequisite is in place: the jgs-magic-sysmlv1-mcp bridge must be installed
   and reachable (the FREE/read-only tier is sufficient), with a SysML v1 project open
   in CATIA Magic. These skills are read-only and never modify the model.
3. Run `python install.py --dry-run` and show me the skill list and target
   (~/.claude/skills/). If it looks right, run `python install.py`.
4. Verify: list the installed jgs-v1* directories and confirm the count matches SKILLS.md.
5. Tell me to restart Claude Code, then start with `/jgs-v1`.
6. This pack is open source (Apache-2.0) and free to use alongside jgs-magic-sysmlv1-mcp; see
   LICENSE. Do not edit anything outside the install target.
```

---

## Skills in this pack

| Skill | What it does |
|-------|-------------|
| `jgs-v1` | Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills: navigate, inspect, search, impact, audit, report. |
| `jgs-v1-audit` | JGS Model Audit: free, read-only SysML model health audit. |
| `jgs-v1-audit-docs` | JGS Model Audit: documentation coverage specialist. |
| `jgs-v1-audit-duplicates` | JGS Model Audit: duplicate elements specialist. |
| `jgs-v1-audit-methodology` | JGS Model Audit: SE layer hygiene heuristics specialist. |
| `jgs-v1-audit-naming` | JGS Model Audit: naming conventions specialist. |
| `jgs-v1-audit-requirements` | JGS Model Audit: requirement coverage and traceability specialist. |
| `jgs-v1-audit-unused` | JGS Model Audit: unused types and definitions specialist. |
| `jgs-v1-diagrams` | Inventory and export SysML v1 diagrams: build a visual review pack, list diagram kinds, compare layouts. |
| `jgs-v1-fixplan` | Turn a SysML v1 audit's findings into a read-only remediation plan with per-finding recommended actions. |
| `jgs-v1-impact` | Impact analysis for a SysML v1 element: map dependents, diagrams, and requirement links before a change. |
| `jgs-v1-inspect` | Deep-dive a single SysML v1 element: type, structure, ports, relationships, allocations, stereotypes. |
| `jgs-v1-navigate` | Navigate a SysML v1 model: a structured overview of packages, element counts, and diagrams. |
| `jgs-v1-report` | Produce a shareable model-health report and Requirements Traceability Matrix (RTM), written to a file. |
| `jgs-v1-search` | Full-text search across element names, with ranked hits by type, qualified name, and ID. |
| `jgs-v1-status` | Report the SysML v1 bridge safety state (tier/mode) and recent model edit history. |
| `jgs-v1-units` | Look up units, quantity kinds, and standard-library types in a SysML v1 model. |

---

## Prerequisites

- **[jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp)** bridge installed and running (FREE tier sufficient)
- **Claude Code** with MCP configured for `jgs-magic-sysmlv1-mcp`
- A SysML v1.x project open in CATIA Magic

---

## Installation

```bash
# Python (cross-platform)
python install.py

# Bash / macOS / Linux
bash install.sh

# Windows PowerShell
.\install.ps1
```

Options:
- `--dry-run`: preview what would be installed without writing anything
- `--force`: overwrite existing same-named skills
- `--uninstall`: remove previously installed jgs-v1* skills
- `--agent <name>`: target a specific agent (`claude` default, `openclaw`, `copilot`, `codex`, `gemini`, `cursor`)
- `--agent all`: install for every user-global agent at once
- `--list-agents`: show the supported agents and their install paths

Skills are installed as top-level siblings under `~/.claude/skills/` (short-name discovery,
`/jgs-v1`). Restart Claude Code after installation.

## Use with other agents

These skills ship in the open `SKILL.md` format. Agents that read it natively (Claude Code,
OpenClaw, GitHub Copilot CLI) get the folder copied unchanged; others (OpenAI Codex CLI,
Gemini CLI, Cursor) get an automatic format transform. Pick a target with `--agent`:

```bash
python install.py --list-agents       # show every target and where it installs
python install.py --agent gemini      # e.g. install for Gemini CLI
python install.py --agent all         # all user-global agents (not cursor)
```

See [docs/other-agents.md](docs/other-agents.md) for per-agent paths, invoke syntax, and
limitations.

## Install from a marketplace

The pack ships host-native plugin manifests, so you can add it from inside your agent without
cloning first:

- **Claude Code:** `/plugin marketplace add jgsystemsconsulting/jgs-magic-sysmlv1-read-skills`,
  then install **jgs-magic-sysmlv1-read-skills** from the list.
- **Cursor (2.5+):** the repo carries a `.cursor-plugin/` manifest; point Cursor at this
  repository to discover and install the pack. Cursor reads the `skills/` tree directly.

> [!NOTE]
> This pack is open source (Apache-2.0), so it is also listed in the public agent directories
> for searchable discovery: Anthropic's `claude-plugins-official` for Claude Code and Cursor's
> public plugin marketplace. The bridge it drives, **jgs-magic-sysmlv1-mcp**, stays proprietary
> and is distributed separately.

---

## Quick start

```
/jgs-v1 I just inherited a SysML v1 model. What am I looking at?
/jgs-v1 Run a full health audit
/jgs-v1 What would break if I change the DataBus block?
```

Full walkthrough: [docs/skill-usage.md](docs/skill-usage.md).

---

## Support & security

- **Support / questions:** open an issue on this repository.
- **Report a security issue:** please report privately through a
  [GitHub security advisory](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills/security/advisories/new),
  or open a pull request with a fix. Do not open a public issue for vulnerabilities.
  See [SECURITY.md](SECURITY.md).

---

## Related products

This pack is the free, read-only entry point to the JGS SysML v1 line. It sits on top of a
free bridge, and a PRO upgrade unlocks write access:

| Product | What it is | Cost |
|---------|------------|------|
| **[jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp)** | The MCP bridge these skills depend on. Its FREE tier serves the read-only tools this pack calls. A **PRO licence** on the same bridge unlocks model writes (create, edit, fix). | Free bridge; PRO licence for writes |
| **jgs-magic-sysmlv1-read-skills** *(this pack)* | 17 read-only analysis skills driven by `/jgs-v1`. Runs on the bridge's FREE tier. | Free |
| **jgs-magic-sysmlv1-pro-skills** | The paid companion: write-tier skills (apply audit fixes, author requirements and allocations) plus v1→v2 migration (migrate-read, cross-model). | PRO |

**The upgrade path:** install the free bridge, add these free read skills, and analyse your
model at no cost. When you want the agent to *act* on what it finds, add a PRO licence to the
bridge and the **jgs-magic-sysmlv1-pro-skills** pack. Same local, air-gapped setup; full write
access. [Compare tiers](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp/blob/main/docs/licensing.md).
