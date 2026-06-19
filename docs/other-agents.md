<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Using the pack with other agents

These skills are read-only SysML v1 analysis workflows that drive the
`jgs-magic-sysmlv1-mcp` bridge. They ship in Claude Code's `SKILL.md` format, which
**several agents read natively** and others can consume after a small format transform.
`install.py` handles both — pick a target with `--agent`.

```bash
python install.py --list-agents          # show every target and where it installs
python install.py --agent <name>          # install for one agent
python install.py --agent all             # all user-global agents (not cursor)
python install.py --agent <name> --dry-run --force --uninstall   # the usual flags
```

> **Flat layout (deliberate).** Every skill is prefixed `jgs-v1` and the product UX is the
> short-name dispatcher `/jgs-v1`. The installer therefore writes skills **flat** — top-level
> siblings, not under a vendor-namespace subfolder — so each agent discovers them by their
> short names. Only `jgs-v1*` items are ever created or removed.

## Supported targets

| Agent | `--agent` | Install path | Format | Invoke as |
|---|---|---|---|---|
| Claude Code | `claude` *(default)* | `~/.claude/skills/<skill>/SKILL.md` | SKILL.md (copied) | `/jgs-v1` |
| OpenClaw | `openclaw` | `~/.openclaw/skills/<skill>/SKILL.md` | SKILL.md (copied) | `/jgs-v1` |
| GitHub Copilot CLI | `copilot` | `~/.copilot/skills/<skill>/SKILL.md` | SKILL.md (copied) | reference `/jgs-v1` in a prompt; `/skills reload` |
| OpenAI Codex CLI | `codex` | `~/.codex/prompts/<skill>.md` | Markdown + `description` frontmatter | `/prompts:jgs-v1` |
| Gemini CLI | `gemini` | `~/.gemini/commands/<skill>.toml` | TOML (`prompt = """…"""`) | `/jgs-v1` (run `/commands reload`) |
| Cursor | `cursor` | `./.cursor/rules/<skill>.mdc` **(project-local)** | `.mdc` rule + frontmatter | `@jgs-v1`, or auto-applied by rule description |

### Native SKILL.md agents — `claude`, `openclaw`, `copilot`
These read the `SKILL.md` format directly, so the installer copies each skill folder
unchanged — references and all.

### Transform agents — `codex`, `gemini`, `cursor`
These use prompt/rule conventions rather than skills, so the installer converts each
`SKILL.md` into the agent's format. To keep the result self-contained, any `references/`
files are **inlined into the prompt as an appendix**.

## Notes & limitations

- **Cursor is project-local.** Cursor has no programmatically-writable user-global rules
  directory, so the installer writes `./.cursor/rules/*.mdc` under the **current directory**.
  Run it from your project root. For that reason `cursor` is *not* included in `--agent all`.
- **Codex prompts vs. skills.** Codex's custom-prompts directory is the stable, widely
  supported target today; that's what the installer writes.
- **Restart / reload.** After installing, restart the agent or run its reload command
  (`/skills reload` for Copilot, `/commands reload` for Gemini) so it picks up the files.
- **`--target`** overrides the install directory for a single agent (it cannot be combined
  with `--agent all`).

## What stays the same everywhere

Regardless of agent, the prerequisite is identical: the `jgs-magic-sysmlv1-mcp` bridge must be
installed and reachable (FREE/read-only tier is sufficient), with a SysML v1 project open in
CATIA Magic. The skills never modify the model. See [skill-usage.md](skill-usage.md) for what
each skill does.
