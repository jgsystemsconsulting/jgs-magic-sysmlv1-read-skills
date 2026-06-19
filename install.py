# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
#
# This file is part of the JGS SysML v1 Free Skills distribution.
# Free to use and redistribute alongside jgs-magic-sysmlv1-mcp.
# See LICENSE for the full terms.
#
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Installer for the JGS SysML v1 Free Skills suite — multi-agent.

The pack ships read-only SysML v1 analysis skills as Claude Code `SKILL.md` files.
That format is read natively by several agents and can be transformed into the
prompt/rule conventions of others. This installer targets both kinds.

FLAT-LAYOUT NOTE (deliberate RR-S-03 exception): every skill name in this pack is
prefixed `jgs-v1`, and the product UX is the short-name dispatcher `/jgs-v1`. The
installer therefore writes skills *flat* (top-level siblings, e.g.
`~/.claude/skills/jgs-v1/`), NOT under a vendor-namespace subfolder — so Claude Code
discovers them by their short names. Only `jgs-v1*` items are ever created or removed.

  Native SKILL.md agents (folder is copied unchanged):
    claude    ~/.claude/skills/<skill>/SKILL.md       (default)
    openclaw  ~/.openclaw/skills/<skill>/SKILL.md
    copilot   ~/.copilot/skills/<skill>/SKILL.md       (GitHub Copilot CLI)

  Transform agents (each SKILL.md is converted to that agent's format; any
  references/ files are inlined as an appendix so the result is standalone):
    codex     ~/.codex/prompts/<skill>.md              (OpenAI Codex CLI)
    gemini    ~/.gemini/commands/<skill>.toml          (Gemini CLI)
    cursor    ./.cursor/rules/<skill>.mdc              (Cursor — PROJECT-local)

Usage:
    python install.py                       # install for Claude Code (default)
    python install.py --agent openclaw      # install for a specific agent
    python install.py --agent all           # all user-global agents (not cursor)
    python install.py --list-agents         # show supported agents and paths
    python install.py --dry-run             # show what would be written; no changes
    python install.py --force               # overwrite existing same-named skills
    python install.py --target PATH         # override the install/base directory
    python install.py --uninstall           # remove previously-installed jgs-v1* skills

Prerequisite: the jgs-magic-sysmlv1-mcp bridge (FREE/read-only tier is sufficient),
with a SysML v1 project open in CATIA Magic. These skills never modify the model.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
SKILLS_SRC = HERE / "skills"
# Every shipped skill is prefixed jgs-v1; discovery is by prefix (no fixed list).
SKILL_PREFIX = "jgs-v1"


# --------------------------------------------------------------------------- #
# Base-directory resolvers (one per agent) — FLAT (no vendor namespace)
# --------------------------------------------------------------------------- #
def _home() -> pathlib.Path:
    return pathlib.Path.home()


def claude_base() -> pathlib.Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    root = pathlib.Path(env) if env else _home() / ".claude"
    return root / "skills"


def openclaw_base() -> pathlib.Path:
    return _home() / ".openclaw" / "skills"


def copilot_base() -> pathlib.Path:
    return _home() / ".copilot" / "skills"


def codex_base() -> pathlib.Path:
    # Codex discovers prompts only at the top level of this folder.
    return _home() / ".codex" / "prompts"


def gemini_base() -> pathlib.Path:
    # Flat command files -> /jgs-v1, /jgs-v1-navigate, ... (no namespace subfolder).
    return _home() / ".gemini" / "commands"


def cursor_base() -> pathlib.Path:
    # Cursor rules are project-local; there is no writable user-global rules dir.
    return pathlib.Path.cwd() / ".cursor" / "rules"


# kind: "native" copies the SKILL.md folder; otherwise a transform key.
# global_: included in --agent all (cursor is project-local, so excluded).
AGENTS: dict[str, dict] = {
    "claude":   {"label": "Claude Code",        "kind": "native", "base": claude_base,   "global_": True,
                 "invoke": "/jgs-v1"},
    "openclaw": {"label": "OpenClaw",            "kind": "native", "base": openclaw_base, "global_": True,
                 "invoke": "/jgs-v1"},
    "copilot":  {"label": "GitHub Copilot CLI",  "kind": "native", "base": copilot_base,  "global_": True,
                 "invoke": "reference the /jgs-v1 skill in a prompt; run /skills reload"},
    "codex":    {"label": "OpenAI Codex CLI",    "kind": "codex",  "base": codex_base,    "global_": True,
                 "invoke": "/prompts:jgs-v1"},
    "gemini":   {"label": "Gemini CLI",          "kind": "gemini", "base": gemini_base,   "global_": True,
                 "invoke": "/jgs-v1  (run /commands reload first)"},
    "cursor":   {"label": "Cursor (project-local)", "kind": "cursor", "base": cursor_base, "global_": False,
                 "invoke": "@jgs-v1, or let the agent auto-apply by rule description"},
}


# --------------------------------------------------------------------------- #
# SKILL.md parsing + format transforms
# --------------------------------------------------------------------------- #
def parse_skill(skill_md: pathlib.Path) -> tuple[str, str, str]:
    """Return (name, description, body) from a SKILL.md file."""
    text = skill_md.read_text(encoding="utf-8")
    name = skill_md.parent.name
    description = ""
    body = text

    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            for ln in lines[1:end]:
                key, sep, val = ln.partition(":")
                if not sep:
                    continue
                key, val = key.strip(), val.strip()
                if key == "name" and val:
                    name = val
                elif key == "description" and val:
                    description = val
            body = "".join(lines[end + 1:]).lstrip("\n")
    return name, description, body


def references_appendix(skill_dir: pathlib.Path) -> str:
    """Inline any references/ files so transform targets stay self-contained."""
    refs = skill_dir / "references"
    if not refs.is_dir():
        return ""
    parts: list[str] = []
    for f in sorted(p for p in refs.rglob("*") if p.is_file()):
        rel = f.relative_to(skill_dir).as_posix()
        parts.append(f"\n\n---\n\n## Appendix — {rel}\n\n{f.read_text(encoding='utf-8')}")
    return "".join(parts)


def _toml_basic(s: str) -> str:
    """Escape a string for a TOML basic (double-quoted) value."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def render_transform(kind: str, name: str, description: str, body: str) -> tuple[str, str]:
    """Return (relative_path, file_contents) for a transform agent."""
    if kind == "codex":
        front = f"---\ndescription: {description}\n---\n" if description else ""
        return f"{name}.md", f"{front}{body}"

    if kind == "gemini":
        esc = body.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        contents = f'description = "{_toml_basic(description)}"\nprompt = """\n{esc}\n"""\n'
        return f"{name}.toml", contents

    if kind == "cursor":
        front = (
            "---\n"
            f"description: {description}\n"
            "globs:\n"
            "alwaysApply: false\n"
            "---\n"
        )
        return f"{name}.mdc", f"{front}{body}"

    raise ValueError(f"unknown transform kind: {kind}")


# --------------------------------------------------------------------------- #
# Source discovery
# --------------------------------------------------------------------------- #
def list_source_skills() -> list[pathlib.Path]:
    if not SKILLS_SRC.is_dir():
        return []
    return sorted(
        p for p in SKILLS_SRC.iterdir()
        if p.is_dir() and p.name.startswith(SKILL_PREFIX)
    )


# --------------------------------------------------------------------------- #
# Install / uninstall
# --------------------------------------------------------------------------- #
def install_native(target: pathlib.Path, skills: list[pathlib.Path],
                   force: bool, dry_run: bool) -> tuple[int, int, int]:
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
    installed = skipped = overwritten = 0
    for src in skills:
        dst = target / src.name
        if dst.exists():
            if not force:
                print(f"  SKIP  {src.name} (exists — use --force)")
                skipped += 1
                continue
            if not dry_run:
                shutil.rmtree(dst)
            overwritten += 1
        if dry_run:
            print(f"  +     {src.name}/")
        else:
            shutil.copytree(src, dst)
            print(f"  OK    {src.name}/")
        installed += 1
    return installed, skipped, overwritten


def install_transform(kind: str, base: pathlib.Path, skills: list[pathlib.Path],
                      force: bool, dry_run: bool) -> tuple[int, int, int]:
    installed = skipped = overwritten = 0
    for src in skills:
        name, description, body = parse_skill(src / "SKILL.md")
        body = body + references_appendix(src)
        rel, contents = render_transform(kind, name, description, body)
        dst = base / rel
        if dst.exists():
            if not force:
                print(f"  SKIP  {rel} (exists — use --force)")
                skipped += 1
                continue
            overwritten += 1
        if dry_run:
            print(f"  +     {rel}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(contents, encoding="utf-8")
            print(f"  OK    {rel}")
        installed += 1
    return installed, skipped, overwritten


def install_for_agent(agent: str, override: pathlib.Path | None,
                      force: bool, dry_run: bool) -> int:
    cfg = AGENTS[agent]
    skills = list_source_skills()
    if not skills:
        print(f"ERROR: no '{SKILL_PREFIX}*' skills found in {SKILLS_SRC}")
        return 1

    base = override if override is not None else cfg["base"]()
    print(f"\n== {cfg['label']} ({agent}) ==")
    print(f"Target: {base}")
    if dry_run:
        print("(dry run — no files written)")

    if cfg["kind"] == "native":
        installed, skipped, overwritten = install_native(base, skills, force, dry_run)
    else:
        installed, skipped, overwritten = install_transform(cfg["kind"], base, skills, force, dry_run)

    if dry_run:
        print(f"Would install {installed}; would skip {skipped}.")
    else:
        print(f"Installed {installed}. Overwrote {overwritten}. Skipped {skipped}.")
        print(f"Invoke: {cfg['invoke']}")
    return 0


def uninstall_for_agent(agent: str, override: pathlib.Path | None, dry_run: bool) -> int:
    cfg = AGENTS[agent]
    base = override if override is not None else cfg["base"]()
    names = [p.name for p in list_source_skills()]
    print(f"\n== {cfg['label']} ({agent}) ==")
    print(f"Target: {base}")
    if dry_run:
        print("(dry run — no files removed)")

    removed = 0
    if cfg["kind"] == "native":
        for name in names:
            p = base / name
            if p.is_dir():
                print(f"  {'-' if dry_run else 'RM'}    {name}/")
                if not dry_run:
                    shutil.rmtree(p)
                removed += 1
    elif cfg["kind"] == "gemini":
        for name in names:
            p = base / f"{name}.toml"
            if p.is_file():
                print(f"  {'-' if dry_run else 'RM'}    {p.name}")
                if not dry_run:
                    p.unlink()
                removed += 1
    else:
        ext = {"codex": ".md", "cursor": ".mdc"}[cfg["kind"]]
        for name in names:
            p = base / f"{name}{ext}"
            if p.is_file():
                print(f"  {'-' if dry_run else 'RM'}    {p.name}")
                if not dry_run:
                    p.unlink()
                removed += 1

    print(f"{'Would remove' if dry_run else 'Removed'} {removed} item(s).")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def resolve_agents(choice: str) -> list[str]:
    if choice == "all":
        return [a for a, c in AGENTS.items() if c["global_"]]
    return [choice]


def print_agents() -> int:
    print("Supported agents:\n")
    for key, cfg in AGENTS.items():
        scope = "user-global" if cfg["global_"] else "PROJECT-local"
        print(f"  {key:9} {cfg['label']:24} [{cfg['kind']:7}] {scope}")
        print(f"            -> {cfg['base']()}")
    print("\n'all' targets every user-global agent (cursor is project-local; request it explicitly).")
    print("Skills install flat (short-name discovery): /jgs-v1 and friends.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--agent", default="claude",
                        choices=list(AGENTS) + ["all"],
                        help="Target agent (default: claude)")
    parser.add_argument("--target", type=pathlib.Path, default=None,
                        help="Override the install/base directory")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing same-named skills")
    parser.add_argument("--dry-run", action="store_true",
                        help="List changes without making them")
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove previously-installed jgs-v1* skills")
    parser.add_argument("--list-agents", action="store_true",
                        help="Show supported agents and their install paths")
    args = parser.parse_args()

    if args.list_agents:
        return print_agents()

    agents = resolve_agents(args.agent)
    if args.target is not None and len(agents) > 1:
        print("ERROR: --target cannot be combined with --agent all.")
        return 2

    rc = 0
    for agent in agents:
        if args.uninstall:
            rc |= uninstall_for_agent(agent, args.target, args.dry_run)
        else:
            rc |= install_for_agent(agent, args.target, args.force, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
