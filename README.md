<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS SysML v1 Read Skills

![Licence](https://img.shields.io/badge/licence-proprietary-blue) ![Version](https://img.shields.io/badge/version-0.3.0-green) ![Skills](https://img.shields.io/badge/skills-18-orange) ![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-8A2BE2) ![ZCode](https://img.shields.io/badge/ZCode-compatible-8A2BE2)

**Version:** 0.3.0  
**Vendor:** JG Systems Consulting Ltd.  
**Licence:** Free to use under the JGS EULA; see [LICENSE](LICENSE). Requires jgs-magic-sysmlv1-mcp (FREE tier).

---

## What This Is

A free bundle of 18 Claude Code skills for engineers working with SysML v1 models in CATIA Magic Systems of Systems Architect (MSOSA). Every skill is read-only: no write access, no licence key, no model mutation.

Start with `/jgs-v1` and describe what you need in plain English.

---

## Install with your AI agent

Copy everything in the block below and paste it into your coding agent
(Claude Code, Cursor, etc.). It will read this repo and install the pack for you.

```text
You are installing jgs-magic-sysmlv1-read-skills (JGS SysML v1 Read Skills), a free-of-charge skills pack
(JG Systems Consulting Ltd.) of read-only analysis skills for SysML v1 models in
CATIA Magic. Repository: https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills (version 0.3.0). Do this in order:

1. Read README.md and docs/skill-usage.md. Confirm the prerequisite: jgs-magic-sysmlv1-mcp is installed and reachable (FREE/read-only tier is enough), with a SysML v1 project open in CATIA Magic. Skills never modify the model.
2. Run `python install.py --dry-run` and show the skill list and target. If it looks right, run `python install.py` (or `python install.py --agent <name>` / `--agent all` as requested).
3. Verify per install target: count of jgs-v1* entries under that agent’s path matches the skill count in SKILLS.md; tell me to restart or reload the agent.
4. Start with `/jgs-v1`. This pack is free to use under LICENSE; do not edit anything outside the install target.
```

---

## Skills in This Pack

| Skill | What it does |
|-------|-------------|
| `jgs-v1` | Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills: navigate, inspect, search, impact, audit, repor… |
| `jgs-v1-audit` | JGS Model Audit: free, read-only SysML model health audit |
| `jgs-v1-audit-docs` | JGS Model Audit: documentation coverage specialist |
| `jgs-v1-audit-duplicates` | JGS Model Audit: duplicate elements specialist |
| `jgs-v1-audit-methodology` | JGS Model Audit: SE layer hygiene heuristics specialist |
| `jgs-v1-audit-naming` | JGS Model Audit: naming conventions specialist |
| `jgs-v1-audit-requirements` | JGS Model Audit: requirement coverage and traceability specialist |
| `jgs-v1-audit-unused` | JGS Model Audit: unused types and definitions specialist |
| `jgs-v1-diagrams` | Inventory and export SysML v1 diagrams: build a visual review pack of diagram images, list diagram kinds,… |
| `jgs-v1-feedback` | Draft and file a pack or bridge issue on GitHub after one explicit user yes |
| `jgs-v1-fixplan` | Turn a SysML v1 audit's findings into a read-only remediation plan: per-finding recommended action, the ex… |
| `jgs-v1-impact` | Impact analysis for a SysML v1 element: map dependents, diagrams, and requirement links before making a ch… |
| `jgs-v1-inspect` | Deep-dive a single SysML v1 element: type, structure, ports, relationships, allocations, stereotypes, tagg… |
| `jgs-v1-navigate` | Navigate and inspect a SysML v1 model: produce a structured overview of packages, element counts, and diag… |
| `jgs-v1-report` | Produce a shareable model-health report and Requirements Traceability Matrix (RTM) for a SysML v1 model, wr… |
| `jgs-v1-search` | Full-text search across element names in a SysML v1 model and present ranked hits with type, qualified name… |
| `jgs-v1-status` | Report the SysML v1 bridge safety state (tier/mode) and recent model edit history |
| `jgs-v1-units` | Look up units, quantity kinds, and standard-library types in a SysML v1 model |

---

## Prerequisites

- **jgs-magic-sysmlv1-mcp** bridge installed and running (FREE tier sufficient)
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
- `--agent <name>`: target a specific agent (`claude` default, `zcode`, `openclaw`, `copilot`, `codex`, `gemini`, `cursor`)
- `--agent all`: install for every user-global agent at once
- `--list-agents`: show the supported agents and their install paths

Skills are installed as top-level siblings under `~/.claude/skills/` (deliberately flat so
Claude Code discovers them by short name: `/jgs-v1`). The installer honours
`$CLAUDE_CONFIG_DIR`, and `--target PATH` overrides the install directory if you prefer a
different layout. Restart Claude Code after installation.

## Use with other agents

These skills ship in the open `SKILL.md` format. Agents that read it natively (ZCode,
Claude Code, OpenClaw, GitHub Copilot CLI) get the folder copied unchanged; others (OpenAI Codex CLI,
Gemini CLI, Cursor) get an automatic format transform. Pick a target with `--agent`:

```bash
python install.py --list-agents       # show every target and where it installs
python install.py --agent gemini      # e.g. install for Gemini CLI
python install.py --agent all         # all user-global agents (not cursor)
```

See [docs/other-agents.md](docs/other-agents.md) for per-agent paths, invoke syntax, and
limitations.

---

## Usage

Start with the dispatcher and describe what you need:

```
/jgs-v1 I just inherited a SysML v1 model: what am I looking at?
/jgs-v1 Run a full health audit
/jgs-v1 What would break if I change the DataBus block?
```

The full invoke guide, with prerequisites, per-skill walkthroughs, and worked examples,
lives at [docs/skill-usage.md](docs/skill-usage.md).

---

## Licence

This pack is proprietary software of JG Systems Consulting Ltd, free of charge: you may
use it as delivered, but it is not open source, so copying, modifying, or redistributing
it is not permitted. The terms are in [LICENSE](LICENSE).

To request a commercial or academic licence, or if you are unsure which licence you need:
[Labs Licensing](https://labs.jgsystemsconsulting.com/licensing.html)

---

## Support & Feedback

Each kind of report has its own channel:

- **Bug (a skill produced wrong or malformed output):** open an issue with the
  [Bug Report form](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills/issues/new/choose). Include the pack version
  (`RELEASE-INFO.txt`), the skill name, and the exact invocation and output. This is a
  release repo: fixes are applied upstream by the maintainer, so please file an issue
  rather than a pull request.
- **Improvement (an outcome the pack could not enable):** use the
  [Skill Improvement form](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills/issues/new/choose) on the same chooser, or, in an
  agent session, invoke `/jgs-v1-feedback`: it drafts the report (no model content, no
  credentials) and files it after you approve the exact draft.
- **Bridge defects (connection, tools, licensing in jgs-magic-sysmlv1-mcp itself):** file
  them on [the bridge's tracker](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp/issues/new/choose), not here.
- **Security vulnerabilities:** never in a public issue. See
  [SECURITY.md](SECURITY.md) for the private advisory route.
- **Questions and support:** contact JG Systems Consulting Ltd.

---

## Related repositories

The JGS SysML toolchain spans two MCP bridges and two skills packs. This repository is one part; the others:

| Repository | What it is | Access |
|---|---|---|
| [jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp) | MCP bridge for live SysML v1 models in CATIA Magic (MSOSA). FREE tier is read-only; a PRO licence adds write tools, and ENTERPRISE adds administrative tools. | Free; PRO and ENTERPRISE by licence |
| [jgs-magic-sysmlv2-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv2-mcp) | MCP bridge for live SysML v2 models in CATIA Magic. FREE tier is read-only; a PRO licence adds write tools, and ENTERPRISE adds administrative tools. | Free; PRO and ENTERPRISE by licence |
| jgs-magic-sysmlv1-read-skills (this repository) | Free read-only analysis skills for SysML v1. | Free |
| jgs-magic-sysmlv1-pro-skills | Write-capable and migration skills for SysML v1; the paid companion to the read skills. | Proprietary; request access via https://labs.jgsystemsconsulting.com/licensing.html |
