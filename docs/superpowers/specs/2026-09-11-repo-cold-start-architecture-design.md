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

`AGENTS.md` may already exist with product-specific rules. The skill **merges** index and architecture pointer sections; it does not wipe local policy.

### `ARCHITECTURE.md` (repository root)

Cold-start structure only. Target length: short enough that an agent finishes it in one read (rough guide: under ~150 lines for small packs, under ~250 for monorepos before linking out).

Required sections, in order:

1. **Purpose:** one paragraph product/job.
2. **Runtime / deliverable shape:** what runs or ships (app, lib, MCP bridge, skills pack, docs-only).
3. **Major parts:** table of path to responsibility.
4. **Boundaries:** what this repo must not own (upstream generators, secrets, sibling products).
5. **Entry points:** install, main CLI, agent invoke, tests/gates if they define how you touch this tree.
6. **Doc map:** curated deep docs, BMAD brownfield paths, GSD `.planning/codebase/`, stager-owned or generated files.
7. **Freshness:** ISO date, git HEAD (or tree fingerprint for non-git), and which engine produced or last projected the body (`bmad-quick` | `gsd-map` | `lightweight` | `manual`).

Every structural claim in sections 2 through 5 should be checkable against a path in-repo. Unknown stays `unknown`.

## Detection order (engine selection)

Run top-down; first hard match wins for **deep** scan. Projection to root always runs after the chosen path.

1. **Existing root `ARCHITECTURE.md` with fresh fingerprint and no structural delta**  
   Report fresh; exit (unless `--force`).

2. **Curated architecture hub already authoritative**  
   Detect known hubs (for example `docs/catia-magic-mcp-architecture/`, explicit "authoritative architecture" pointers in README/AGENTS).  
   Project a short root `ARCHITECTURE.md` that **links** the hub; do not regenerate the hub.

3. **BMAD brownfield baseline present**  
   If `docs/brownfield/index.md` (or configured `project_knowledge` brownfield tree) exists: refresh or reuse per fingerprint; project root from it.

4. **BMAD wired and no baseline**  
   If project-local `bmad-document-project` is invokable (`.claude/skills/` or `.agents/skills/` with skill body): run **Quick** scan into the repo's BMAD knowledge path (prefer `docs/brownfield/` when that is the established convention), then project root.

5. **GSD project**  
   If `.planning/` exists (or user passed `--gsd`): run or refresh `gsd-map-codebase` into `.planning/codebase/`, then project root `ARCHITECTURE.md` primarily from `ARCHITECTURE.md` + `STRUCTURE.md` (+ STACK one-liner).

6. **Lightweight default**  
   Single inspection pass (tree, README, AGENTS, install scripts, package/plugin manifests, top-level dirs). Write root `ARCHITECTURE.md` + merge `AGENTS.md` index. No BMAD install. No mandatory `.planning/`.

Parallel note: a repo can be both BMAD-wired and GSD. Prefer BMAD brownfield for the **narrative** cold-start when a brownfield index already exists; still allow GSD map as the deep dump under `.planning/` without copying all seven files to root.

## Projection rules

- Root file is a **projection**, not a second full dump of engine output.
- Prefer tables and paths over essay.
- If BMAD or GSD already state a fact, cite the path to that doc in **Doc map** rather than restating pages of detail.
- Never invent tools, services, or modules not evidenced in-repo.
- Never copy secrets, machine-local paths, or credential-shaped strings into architecture docs (same class of leak rules as release gates).
- Written Prose Standard applies to durable sections the skill authors or rewrites.

## Refresh policy

**Rewrite or re-project when any of:**

- Top-level directory set changed in a way that affects Major parts.
- Documented entry points or install surface changed (README install block, `install.py`, package entry points, plugin manifests).
- Ownership / do-not-edit rules changed.
- Freshness fingerprint older than policy default (default: no automatic time expiry if HEAD unchanged; structural hash is the main signal). Compare stored HEAD + structural hash in the Freshness section to current repo.
- User passes `--force`.

**Do not rewrite when:**

- Only file body churn inside existing modules with the same top-level shape.
- Only process logs under `docs/superpowers/` or equivalent scratch trees.
- Only dependency lockfile noise without stack change (optional STACK touch inside GSD map is out of band unless user forced refresh).

On skip: print one line (`ARCHITECTURE.md fresh @ <HEAD>`) and exit 0.

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

- Exact structural hash algorithm (top-level dirs + nominated manifest paths).
- Whether freshness policy default gains a max-age even when HEAD matches (recommend no in v1).
- Skill short-name vs `jgs-` prefix for public packs.
- Whether release-repo-standard gains an RR-B requirement for root ARCHITECTURE later.

## Approval record

- Audience: agent cold-start.
- Layout: root trio.
- Engine: auto by repo type.
- Refresh: structural + fingerprint; `--force` allowed.
- Human approval: 2026-09-11 (design dialogue).
)
