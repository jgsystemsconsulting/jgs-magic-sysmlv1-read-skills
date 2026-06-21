<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS SysML v1 Read Skills

![Licence](https://img.shields.io/badge/licence-proprietary-blue) ![Version](https://img.shields.io/badge/version-0.1.1-green) ![Skills](https://img.shields.io/badge/skills-17-orange) ![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-8A2BE2)

**Version:** 0.1.1  
**Vendor:** JG Systems Consulting Ltd.  
**Contact:** JG Systems Consulting Ltd.  
**Licence:** Free — no licence file required. Requires jgs-magic-sysmlv1-mcp (FREE tier).

---

## What This Is

A free bundle of 17 Claude Code skills for engineers working with SysML v1 models in CATIA Magic Systems of Systems Architect (MSOSA). Every skill is read-only — no write access, no licence key, no model mutation.

Start with `/jgs-v1` and describe what you need in plain English.

---

## Install with your AI agent

Copy everything in the block below and paste it into your coding agent
(Claude Code, Cursor, etc.). It will read this repo and install the pack for you.

```text
You are installing jgs-magic-sysmlv1-read-skills, a free, read-only Claude Code skills pack
(JG Systems Consulting Ltd.) of read-only analysis skills for SysML v1 models in
CATIA Magic. Repository: https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills (version 0.1.1). Do this in order:

1. Read README.md, docs/skill-usage.md, and CHANGELOG.md in this repository so you
   understand what you are installing and its prerequisites.
2. Confirm the prerequisite is in place: the jgs-sysmlv1 MCP bridge must be installed
   and reachable (the FREE/read-only tier is sufficient), with a SysML v1 project open
   in CATIA Magic. These skills are read-only — they never modify the model.
3. Run `python install.py --dry-run` and show me the skill list and target
   (~/.claude/skills/). If it looks right, run `python install.py`.
4. Verify: list the installed jgs-v1* directories and confirm the count matches SKILLS.md.
5. Tell me to restart Claude Code, then start with `/jgs-v1`.
6. This pack is free to use alongside jgs-magic-sysmlv1-mcp; see LICENSE for terms. Do not
   edit anything outside the install target.
```

---

## Skills in This Pack

| Skill | What it does |
|-------|-------------|
| `jgs-v1` | Dispatcher for all jgs-magic-sysmlv1-mcp FREE-tier skills — navigate, inspect, search, impact, audit, repor… |
| `jgs-v1-audit` | JGS Model Audit — free, read-only SysML model health audit |
| `jgs-v1-audit-docs` | JGS Model Audit — documentation coverage specialist |
| `jgs-v1-audit-duplicates` | JGS Model Audit — duplicate elements specialist |
| `jgs-v1-audit-methodology` | JGS Model Audit — SE layer hygiene heuristics specialist |
| `jgs-v1-audit-naming` | JGS Model Audit — naming conventions specialist |
| `jgs-v1-audit-requirements` | JGS Model Audit — requirement coverage and traceability specialist |
| `jgs-v1-audit-unused` | JGS Model Audit — unused types and definitions specialist |
| `jgs-v1-diagrams` | Inventory and export SysML v1 diagrams — build a visual review pack of diagram images, list diagram kinds,… |
| `jgs-v1-fixplan` | Turn a SysML v1 audit's findings into a read-only remediation plan — per-finding recommended action, the ex… |
| `jgs-v1-impact` | Impact analysis for a SysML v1 element — map dependents, diagrams, and requirement links before making a ch… |
| `jgs-v1-inspect` | Deep-dive a single SysML v1 element — type, structure, ports, relationships, allocations, stereotypes, tagg… |
| `jgs-v1-navigate` | Navigate and inspect a SysML v1 model — produce a structured overview of packages, element counts, and diag… |
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
- `--dry-run` — preview what would be installed without writing anything
- `--force` — overwrite existing same-named skills
- `--uninstall` — remove previously installed jgs-v1* skills
- `--agent <name>` — target a specific agent (`claude` default, `openclaw`, `copilot`, `codex`, `gemini`, `cursor`)
- `--agent all` — install for every user-global agent at once
- `--list-agents` — show the supported agents and their install paths

Skills are installed as top-level siblings under `~/.claude/skills/` (short-name discovery —
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

---

## Quick Start

```
/jgs-v1 I just inherited a SysML v1 model — what am I looking at?
/jgs-v1 Run a full health audit
/jgs-v1 What would break if I change the DataBus block?
```

---

## Support & Security

- **Support / questions:** JG Systems Consulting Ltd.
- **Report a security issue:** contact JG Systems Consulting Ltd. privately;
  please do not open public issues for vulnerabilities.

---

## Relationship to Other JGS Products

- **jgs-magic-sysmlv1-mcp** — required bridge; this pack calls its read-only tools
- **jgs-magic-sysmlv1-pro-skills** — the paid companion covering write-tier use cases and v1→v2 migration (migrate-read, cross-model)


