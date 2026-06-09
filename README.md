<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# JGS SysML v1 Free Skills

**Version:** 0.1.0  
**Vendor:** JG Systems Consulting Ltd.  
**Contact:** JG Systems Consulting Ltd.  
**Licence:** Free â€” no licence file required. Requires jgs-magic-sysmlv1-mcp (FREE tier).

---

## What This Is

A free bundle of 12 Claude Code skills for engineers working with SysML v1 models in CATIA Magic Systems of Systems Architect (MSOSA). Every skill is read-only â€” no write access, no licence key, no model mutation.

Start with `/jgs-v1` and describe what you need in plain English.

---

## Install with your AI agent

Copy everything in the block below and paste it into your coding agent
(Claude Code, Cursor, etc.). It will read this repo and install the pack for you.

```text
You are installing jgs-magic-sysmlv1-free-skills, a FREE Claude Code skills pack
(JG Systems Consulting Ltd.) of read-only analysis skills for SysML v1 models in
CATIA Magic. Repository: https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-free-skills (version 0.1.0). Do this in order:

1. Read README.md, docs/skill-usage.md, and CHANGELOG.md in this repository so you
   understand what you are installing and its prerequisites.
2. Confirm the prerequisite is in place: the jgs-sysmlv1 MCP bridge must be installed
   and reachable (the FREE/read-only tier is sufficient), with a SysML v1 project open
   in CATIA Magic. These skills are read-only â€” they never modify the model.
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
| `jgs-v1` | Dispatcher â€” routes any free-tier request to the right specialist |
| `jgs-v1-navigate` | Structured model overview â€” packages, block counts, diagram inventory |
| `jgs-v1-impact` | Blast-radius analysis before changing a shared element |
| `jgs-v1-migrate-read` | v1â†’v2 migration inventory document |
| `jgs-v1-cross-model` | Cross-model migration progress report (requires jgs-magic-sysmlv2-mcp too) |
| `jgs-v1-audit` | Full audit orchestrator â€” runs all 6 specialists, writes report |
| `jgs-v1-audit-naming` | Naming convention violations |
| `jgs-v1-audit-docs` | Documentation coverage gaps |
| `jgs-v1-audit-requirements` | Requirement coverage + traceability matrix export |
| `jgs-v1-audit-duplicates` | Duplicate element detection |
| `jgs-v1-audit-unused` | Unused type detection |
| `jgs-v1-audit-methodology` | BDD/IBD/parametric heuristics; model validation; diagram export |

---

## Prerequisites

- **jgs-magic-sysmlv1-mcp** bridge installed and running (FREE tier sufficient)
- **Claude Code** with MCP configured for `jgs-magic-sysmlv1-mcp`
- A SysML v1.x project open in CATIA Magic
- For `jgs-v1-cross-model` only: **jgs-magic-sysmlv2-mcp** also running on a separate port

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
- `--dry-run` â€” preview what would be installed without writing anything
- `--force` â€” overwrite existing same-named skills
- `--uninstall` â€” remove previously installed jgs-v1* skills

Skills are installed as top-level siblings under `~/.claude/skills/`. Restart Claude Code after installation.

---

## Quick Start

```
/jgs-v1 I just inherited a SysML v1 model â€” what am I looking at?
/jgs-v1 Run a full health audit
/jgs-v1 What would break if I change the DataBus block?
/jgs-v1 Give me a migration inventory for v2
```

---

## Support & Security

- **Support / questions:** JG Systems Consulting Ltd.
- **Report a security issue:** contact JG Systems Consulting Ltd. privately;
  please do not open public issues for vulnerabilities.

---

## Relationship to Other JGS Products

- **jgs-magic-sysmlv1-mcp** â€” required bridge; this pack calls its read-only tools
- **jgs-magic-sysmlv1-pro-skills** â€” the paid companion covering write-tier use cases
- **jgs-magic-sysmlv2-mcp** â€” optional; required only for `jgs-v1-cross-model`


