<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Design: repo cold-start architecture pack

**Date:** 2026-09-11  
**Status:** approved for implementation planning  
**Goal:** Every JG repo an agent opens has a short, honest root architecture face plus an AGENTS index, without inventing a fourth documentation engine next to BMAD and GSD.

## Problem

Agents cold-start on many repos. Some monorepos already have BMAD brownfield scans or curated architecture sets. GSD projects can run `gsd-map-codebase` into `.planning/codebase/`. Small release packs often have only README and a thin AGENTS.md. Nothing user-global guarantees a **root** architecture file that every agent finds on first read.

BMAD Method skills exist project-locally (for example under `cameo-sysmlv2-mcp/.agents/skills/bmad-*`) and are not on the default ZCode user-global skill path. GSD map output lives under `.planning/`, which many agents never open. The gap is projection and habit, not missing reverse-engineering ideas.

## Decisions locked in design

| Decision | Choice |
|----------|--------|
| Primary audience | Agent cold-start |
| Root layout | Trio: `README.md` (product) + `AGENTS.md` (rules/index) + `ARCHITECTURE.md` (structure) |
| Reverse-engineer when empty | Auto by repo type (BMAD / GSD / lightweight) |
| Refresh | Structural change or stale freshness fingerprint; `--force` always allowed |
| Engines | Reuse BMAD `document-project` and GSD `map-codebase`; do not build a parallel full scanner |

**Glossary**

- **Fingerprint:** the freshness tuple written into root `ARCHITECTURE.md`: ISO date + identity + structural hash + engine. **Match ignores date** (written-only audit). **Match uses structural hash + engine enum validity.** Identity is always written for humans and skip-line printing. A changed git HEAD alone does **not** force re-project (body commits must not invalidate structure). Non-git identity tracks the hash, so it moves only when the hash moves.
- **Identity:** when `.git` exists, the full git HEAD sha (40 or 64 hex as `git rev-parse HEAD` returns). When no `.git`, the string `non-git:` concatenated with the full structural hash hex (example form `non-git:a1b2…`). Non-git has no bare-hash identity.
- **Structural hash:** SHA-256 over a canonical byte stream of (1) sorted **top-level entry names** (every file and directory name directly under the repo root except `.` and `..`; names only, not file contents of non-nominated entries), then (2) nominated manifest paths that exist, each as `path\0` + file bytes. Nominated manifests (always attempted): `README.md`, `AGENTS.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `install.py`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `CITATION.cff`. Missing nominated paths are omitted, not hashed as empty.
- **Engine values (required enum):** `bmad-quick` | `gsd-map` | `lightweight` | `hub-project` | `manual`.

## Non-goals

- Replace BMAD Method or GSD planning.
- Use `bmad-create-architecture` for brownfield describe-existing work (that skill is greenfield solution design).
- Force ArchiMate or `archify` diagrams as part of the default pack.
- Auto-install BMAD into every bare repo.
- Duplicate long curated architecture sets at root.
- Solve the free-skills four-theme release quality milestone in this design (separate plan under the same `docs/superpowers/` tree).

## File contract

### `README.md`

Human and product face: what ships, install, links into deeper docs. Not the structure deep-dive.

### `AGENTS.md`

First file coding agents should load. Must include:

- What this repo is (one short paragraph or pointer to ARCHITECTURE purpose).
- Edit rules and do-not-hand-edit list.
- Where durable truth lives (markdown vs generated vs upstream/stager).
- Link to root `ARCHITECTURE.md`.
- Short index of key paths and docs.
- Optional: process track hints (GSD vs Superpowers) when the repo uses them.

`AGENTS.md` may already exist with product-specific rules. The skill **merges** only skill-owned blocks; it does not wipe local policy.

**AGENTS merge contract (normative):**

1. Skill-owned blocks are fenced with HTML comments:
   - `<!-- repo-cold-start:index:start -->` … `<!-- repo-cold-start:index:end -->`
   - `<!-- repo-cold-start:arch-link:start -->` … `<!-- repo-cold-start:arch-link:end -->`
2. On every run that updates AGENTS, replace the entire contents between each matching start/end pair (idempotent). If a start marker exists without its end, fail closed and print an error; do not append a second block.
3. If markers are absent, append both blocks once at end of file (after a blank line), never above existing content.
4. Never rewrite text outside the markers. Local policy outside markers wins on conflict.
5. Target headings inside the index block: `## Agent index (repo-cold-start)` and inside the arch-link block a single markdown link line to `./ARCHITECTURE.md`.

### `ARCHITECTURE.md` (repository root)

Cold-start structure only. Target length: short enough that an agent finishes it in one read (rough guide: under ~150 lines for small packs, under ~250 for monorepos before linking out).

**Do not hand-edit the Freshness section.** Body sections may be hand-edited; the skill recomputes structural hash and identity on every run before trusting a stored fingerprint. If stored hash or identity does not match the recomputed values, treat as stale and re-project (same as structural change).

Required sections, in order:

1. **Purpose:** one paragraph product/job.
2. **Runtime / deliverable shape:** what runs or ships (app, lib, MCP bridge, skills pack, docs-only).
3. **Major parts:** table of path to responsibility.
4. **Boundaries:** what this repo must not own (upstream generators, secrets, sibling products).
5. **Entry points:** install, main CLI, agent invoke, tests/gates if they define how you touch this tree.
6. **Doc map:** curated deep docs, BMAD brownfield paths, GSD `.planning/codebase/`, stager-owned or generated files.
7. **Freshness:** ISO date (written-only); identity (git HEAD sha, or `non-git:<full structural hash hex>`); structural hash (hex SHA-256); engine (`bmad-quick` | `gsd-map` | `lightweight` | `hub-project` | `manual`).

Every structural claim in sections 2 through 5 should be checkable against a path in-repo. Unknown stays `unknown`.

## Detection order (engine selection)

**Flag precedence (evaluated before auto order):**

1. `--force`: ignore freshness skip; still use engine selection below.
2. `--lightweight`: force lightweight path; skip BMAD and GSD engines even if present.
3. `--gsd`: if `.planning/` is missing, create the empty directory `.planning/` when the workspace is writable; if create fails, error and stop (do not fall through to BMAD). Then prefer GSD map path over BMAD for deep scan; still project root.
4. Else: auto order below.

Auto order (first hard match wins for **deep** scan). After the deep path (or lightweight body write), project root `ARCHITECTURE.md` when needed. Run AGENTS merge when markers are missing or incorrect. Skip both only if ARCHITECTURE is fresh and AGENTS markers are present and correct.

1. **Existing root `ARCHITECTURE.md` with matching fingerprint and no structural delta**  
   Recompute structural hash and identity. If they match the Freshness section and engine is one of the enum values: if AGENTS markers are present and correct, report fresh and exit (unless `--force`); if AGENTS markers are missing or broken, run AGENTS merge only, then exit.

2. **Curated architecture hub already authoritative**  
   Collect candidate hub paths (existing on disk only):
   - Fixed path: `docs/catia-magic-mcp-architecture/README.md` (this path is always treated as an authoritative hub when present; no phrase test).
   - Glob: every `docs/**/architecture/README.md` whose first 40 lines contain case-insensitive substring `authoritative`.
   - Pointers: every markdown link in root `README.md` or `AGENTS.md` whose link text or same-line surrounding text matches case-insensitive regex `authoritative.*architecture|architecture.*authoritative`, and whose target resolves to an existing file or directory (if target is a directory, use `README.md` under it when present, else the directory path as the hub root).
   If no candidates: do not take this branch. If several: pick the one with the lexicographically smallest repo-relative path (POSIX separators). Project short root `ARCHITECTURE.md` with engine `hub-project` that **links** that hub; do not regenerate the hub. Always run AGENTS merge after projection.

3. **BMAD brownfield baseline present**  
   If `docs/brownfield/index.md` exists: refresh or reuse per fingerprint; project root from it. Engine: `bmad-quick` if the index body (first 80 lines) matches case-insensitive `bmad` and `document-project` (or `document project`); else `manual`.  
   Fixed paths only in v1: do not read BMAD `_bmad/**/config.yaml` `project_knowledge`. Optional later: `--brownfield-dir PATH`. Always run AGENTS merge after projection.

4. **BMAD wired and no baseline**  
   **Invokable** means at least one of these files exists:
   - `.claude/skills/bmad-document-project/SKILL.md`
   - `.agents/skills/bmad-document-project/SKILL.md`  
   When invokable: host agent loads that skill and runs its **Quick** scan mode (BMAD document-project workflow option Quick / initial scan; not Full or Deep-dive), with output directory `docs/brownfield/` (create if needed). Required projection inputs after scan: `docs/brownfield/index.md` and, if present, `docs/brownfield/project-overview.md` and `docs/brownfield/source-tree-analysis.md`. Engine on root: `bmad-quick`. If Quick cannot complete, fall through to lightweight and set engine `lightweight` with a one-line warning. Always run AGENTS merge after a successful projection.

5. **GSD project**  
   If `.planning/` exists: run or refresh `gsd-map-codebase` into `.planning/codebase/`, then project root `ARCHITECTURE.md` primarily from `.planning/codebase/ARCHITECTURE.md` and `.planning/codebase/STRUCTURE.md`, plus a one-line stack note from `.planning/codebase/STACK.md` when present. Engine: `gsd-map`. Always run AGENTS merge after projection.

6. **Lightweight default**  
   Single inspection pass (tree, README, AGENTS, install scripts, package/plugin manifests, top-level dirs). Write root `ARCHITECTURE.md` and run AGENTS merge. No BMAD install. No mandatory `.planning/`. Engine: `lightweight`.

Parallel note: a repo can be both BMAD-wired and GSD. Under auto order, brownfield index (step 3) or BMAD Quick (step 4) wins before GSD. Under `--gsd`, GSD wins when usable. GSD map may still exist as a deep dump under `.planning/` without copying all seven files to root.

## Projection rules

- Root file is a **projection**, not a second full dump of engine output.
- Prefer tables and paths over essay.
- If BMAD or GSD already state a fact, cite the path to that doc in **Doc map** rather than restating pages of detail.
- Never invent tools, services, or modules not evidenced in-repo.
- Never copy secrets, machine-local paths, or credential-shaped strings into architecture docs (same class of leak rules as release gates).
- Written Prose Standard applies to durable sections the skill authors or rewrites (user AGENTS.md: load avoid-ai-writing; no em dashes; technical voice).

## Refresh policy

**Rewrite or re-project when any of:**

- Recomputed structural hash differs from Freshness (covers top-level layout and nominated manifests, including `README.md`, `AGENTS.md`, and install/plugin manifests listed in the glossary).
- Stored engine is missing or not in the engine enum.
- User passes `--force`.

Do **not** treat a changed git HEAD alone as stale. Always rewrite the Identity line on a successful project so the printed HEAD stays current, but skip body re-projection when hash and engine still match.

Entry-point, install-surface, and ownership-rule changes are **not** separate triggers; they are covered when those files are in the nominated manifest set (`README.md`, `AGENTS.md`, `install.py`, plugin manifests). Do not claim extra triggers the hash cannot see.

**Do not rewrite when:**

- Only file body churn inside existing modules with the same top-level shape and unchanged nominated manifests.
- Only process logs under `docs/superpowers/` or equivalent scratch trees.
- Only dependency lockfile noise without a nominated-manifest change (lockfiles are not in the v1 hash set).

On skip: print one line. Git: `ARCHITECTURE.md fresh @ <HEAD>`. Non-git: `ARCHITECTURE.md fresh @ non-git:<structural-hash-prefix12>`. Exit 0.

## Skill shape (implementation target)

**Working name:** `repo-cold-start` (final name bikeshed allowed at plan time).

**Home:** user-global skill under `~/.zcode/skills/` with mirrors to Claude/agents paths per existing skill-distribution habit.

**Invocation:**

- `/repo-cold-start`: detect, maybe scan, project, merge AGENTS index.
- `/repo-cold-start --force`: ignore freshness skip.
- `/repo-cold-start --lightweight`: skip BMAD/GSD even if present.
- `/repo-cold-start --gsd`: prefer GSD map path when available.

**Hooks (optional, same plan or follow-on):**

- Call from `onboard-repo` after planning root exists (or instead of leaving architecture empty).
- Suggest from ship / `document-release` when root ARCHITECTURE is missing or fingerprint stale.
- Do not block ship on architecture freshness in v1 unless release-repo-standard gains an explicit RR requirement later.

## Hard limits

- Do not vendor full BMAD Method into user-global by default.
- Do not delete curated architecture docs.
- Do not hand-edit generated release artifacts the host repo forbids (example: this free-skills pack's `SKILLS.md`, `RELEASE-INFO.txt`, stager HTML).
- Do not require `.planning/` on docs-only or pure skills packs.
- Do not treat Superpowers `theme` candidates as architecture content.

## Relationship to existing skills

| Skill | Role relative to this design |
|-------|------------------------------|
| `bmad-document-project` | Brownfield reverse-engineer engine when wired |
| `bmad-create-architecture` | Out of scope for describe-existing; greenfield decisions only |
| `bmad-generate-project-context` | Optional lean AI rules file; link from Doc map if present |
| `bmad-index-docs` | Folder indexes only; not a substitute for root ARCHITECTURE |
| `gsd-map-codebase` | Deep seven-doc dump under `.planning/codebase/` |
| `deepinit` | Hierarchical AGENTS trees; complementary, not required for v1 |
| `document-release` | Post-ship doc sync; can call or remind cold-start |
| `context-loop` | Topic evidence for Superpowers; not whole-repo living arch |
| `archify` / `archi-*` | Visual or ArchiMate; optional later, not default |
| `onboard-repo` | Natural bootstrap hook |

## Success criteria

1. Bare small repo: one skill run produces root `ARCHITECTURE.md` with all seven sections and an AGENTS pointer/index merge.
2. Monorepo with BMAD brownfield: root file projects from brownfield and links curated hubs without duplicating them.
3. GSD repo: map exists under `.planning/codebase/`; root ARCHITECTURE stays short and points at the map.
4. Second run with no structural change: no file rewrite (fresh exit).
5. Agent reading only `AGENTS.md` + `ARCHITECTURE.md` can state purpose, parts, boundaries, and entry points without opening the full tree.

## Open points for the implementation plan (not design blockers)

- Exact canonicalization of the structural hash byte stream (line endings, path separators): pin in plan tests.
- Whether freshness policy default gains a max-age even when HEAD matches (recommend no in v1).
- Skill short-name vs `jgs-` prefix for public packs.
- Whether release-repo-standard gains an RR-B requirement for root ARCHITECTURE later.

## Approval record

- Audience: agent cold-start.
- Layout: root trio.
- Engine: auto by repo type; flag precedence `--lightweight` then `--gsd` then auto.
- Refresh: structural hash + identity fingerprint; `--force` allowed.
- Human approval: 2026-09-11 (design dialogue).
- ARL Round 1 genuine fixes applied: 2026-09-11.
