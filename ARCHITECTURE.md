<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->
# Architecture

## Purpose

18 free, read-only analysis skills for SysML v1 models in CATIA Magic (MSOSA), driven by the `/jgs-v1` dispatcher over the `jgs-magic-sysmlv1-mcp` bridge (FREE tier). Proprietary of JG Systems Consulting Ltd; free of charge under the product LICENSE.

## Runtime / deliverable shape

Agent skills pack: `skills/jgs-v1*/SKILL.md` installed via `install.py` into user-global agent skill dirs. Optional editor plugin manifests (`.claude-plugin/`, `.cursor-plugin/`). Requires the separate FREE-tier MCP bridge at runtime.

## Major parts

| Path | Role |
|------|------|
| `skills/` | Eighteen FREE read-only skill definitions + dispatcher |
| `install.py` | Multi-agent installer (`--agent`, `--dry-run`, `--list-agents`) |
| `scripts/` | Release gate (`check_release.py`) and helpers |
| `docs/` | Durable invoke guides (`skill-usage.md`, `other-agents.md`); stager HTML is upstream |
| `.github/` | CI validate workflow (inline checks; does not run repo Python) |
| `.claude-plugin/` / `.cursor-plugin/` | Marketplace/plugin metadata |

## Boundaries

- Never hand-edit `SKILLS.md` or `RELEASE-INFO.txt` (generated at release time).
- Do not add model content, machine-local paths, or credentials; release gate scans for leaks.
- Do not open pull requests against this public release clone as the fix channel; report via feedback forms; maintainer applies upstream.
- Do not treat `docs/index.html`, `guide.html`, `site.css`, or `DISTRIBUTION.md` as SSOT here (stager/upstream templates).
- PRO skills pack and bridge runtime changes are out of this repo.

## Entry points

- Install: `python install.py` (wrappers `install.sh`, `install.ps1`)
- Agent invoke after install: `/jgs-v1 <request>`
- Local release gate: `python scripts/check_release.py`
- Agent index: [AGENTS.md](./AGENTS.md)

## Doc map

- [docs/skill-usage.md](./docs/skill-usage.md) — dispatcher, tools, limits
- [docs/other-agents.md](./docs/other-agents.md) — per-agent install targets
- [README.md](./README.md) — product overview and agent-install prompt
- [AGENTS.md](./AGENTS.md) — edit rules and index
- [docs/DISTRIBUTION.md](./docs/DISTRIBUTION.md) — distribution notes (stager-owned product)
- Superpowers artifacts under `docs/superpowers/` (process only)

## Freshness

- Date: 2026-09-11
- Identity: 41aaa640adb7f09513e1896119ded090f2804227
- Structural hash: d5dc63b48544dbb7daa693a1f7b447c56c3fbc3bdd1ad1263f5af203c761f106
- Engine: manual
