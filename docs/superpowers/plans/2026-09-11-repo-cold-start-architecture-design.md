<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Repo cold-start architecture pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a user-global `repo-cold-start` skill that projects short root `ARCHITECTURE.md` plus idempotent `AGENTS.md` index markers, reusing BMAD/GSD when present and defaulting to a lightweight scan.

**Architecture:** Stdlib-only Python CLI under `~/.zcode/skills/repo-cold-start/` (house pattern like `onboard-repo`). Skill markdown dispatches the CLI. Structural hash + identity drive freshness. Detection order and AGENTS merge match the spec exactly. This free-skills release clone holds the Superpowers artifacts and is the first dogfood target; the skill body is not a product skill inside `skills/jgs-v1*`.

**Tech Stack:** Python 3 stdlib (`pathlib`, `hashlib`, `argparse`, `re`, `subprocess` for `git rev-parse` only). No new pip deps. Markdown templates in the skill directory.

**Spec:** `docs/superpowers/specs/2026-09-11-repo-cold-start-architecture-design.md`

## Global Constraints

- Do not vendor full BMAD Method into user-global by default.
- Do not delete curated architecture docs.
- Do not hand-edit `SKILLS.md`, `RELEASE-INFO.txt`, or stager HTML in this free-skills pack.
- Do not require `.planning/` on docs-only or pure skills packs (except `--gsd` path).
- Do not invent modules/tools not evidenced in-repo.
- Never copy secrets or machine-local absolute home paths into ARCHITECTURE.md.
- Written Prose Standard on skill-authored durable sections (no em dashes; technical voice).
- Engine enum only: `bmad-quick` | `gsd-map` | `lightweight` | `hub-project` | `manual`.
- Copyright HTML header on new `.md`/`.py` product files the skill writes into repos when those repos require headers (this pack does).

## Research

research: skipped (internal process skill; no external API/version claims)

## Codebase context

- Spec (normative): `docs/superpowers/specs/2026-09-11-repo-cold-start-architecture-design.md`
- Analog skill: `~/.zcode/skills/onboard-repo/` (`SKILL.md` + stdlib `onboard_repo.py`)
- BMAD engine (project-local only): monorepo `.agents/skills/bmad-document-project/`
- GSD engine: `gsd-map-codebase` / `~/.claude/gsd-core/workflows/map-codebase.md`
- Dogfood repo root: this free-skills pack (no root `ARCHITECTURE.md` yet; has `AGENTS.md`, `README.md`, `install.py`)

## File map

| File | Responsibility |
|------|----------------|
| `~/.zcode/skills/repo-cold-start/SKILL.md` | Invoke contract, flags, when to use |
| `~/.zcode/skills/repo-cold-start/repo_cold_start.py` | CLI entry: flags, detection, project, merge, exit codes |
| `~/.zcode/skills/repo-cold-start/hashutil.py` | Structural hash + identity |
| `~/.zcode/skills/repo-cold-start/agents_merge.py` | Marker-based AGENTS merge |
| `~/.zcode/skills/repo-cold-start/freshness.py` | Parse/format Freshness; `is_fresh` on hash+engine |
| `~/.zcode/skills/repo-cold-start/detect.py` | Hub / brownfield / BMAD / GSD / lightweight selection |
| `~/.zcode/skills/repo-cold-start/project.py` | Build root ARCHITECTURE.md body + Freshness block |
| `~/.zcode/skills/repo-cold-start/tests/conftest.py` | Insert skill dir on `sys.path` |
| `~/.zcode/skills/repo-cold-start/tests/test_hashutil.py` | Hash + identity unit tests |
| `~/.zcode/skills/repo-cold-start/tests/test_agents_merge.py` | Idempotent merge tests |
| `~/.zcode/skills/repo-cold-start/tests/test_detect_flags.py` | Flag precedence + hub tie-break |
| `~/.zcode/skills/repo-cold-start/tests/test_freshness.py` | Fresh skip vs force |
| `~/.agents/skills/repo-cold-start/` | Mirror of skill (copy or junction per house habit) |
| Repo root `ARCHITECTURE.md` (dogfood) | Projected cold-start face |
| Repo root `AGENTS.md` (dogfood) | Marker blocks only |

---

### Task 1: Skill skeleton + structural hash helper (TDD)

**Files:**
- Create: `C:/Users/gower/.zcode/skills/repo-cold-start/hashutil.py`
- Create: `C:/Users/gower/.zcode/skills/repo-cold-start/tests/test_hashutil.py`
- Create: `C:/Users/gower/.zcode/skills/repo-cold-start/SKILL.md` (stub)
- Create: `C:/Users/gower/.zcode/skills/repo-cold-start/repo_cold_start.py` (argparse stub only)

**Model:** standard

**Interfaces:**
- Produces:
  - `NOMINATED_MANIFESTS: tuple[str, ...]` exact list from spec
  - `def structural_hash(repo: Path) -> str` → lowercase hex sha256
  - `def identity(repo: Path, struct_hash: str | None = None) -> str` → HEAD sha or `non-git:<full hash>`

- [ ] **Step 0: tests/conftest.py path bootstrap**

```python
# tests/conftest.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

Also works for unittest: same file imported if you run from skill root with `PYTHONPATH=.`.

- [ ] **Step 1: Write failing tests for structural hash**

```python
# tests/test_hashutil.py
from pathlib import Path
import tempfile
from hashutil import structural_hash, identity, NOMINATED_MANIFESTS

def test_nominated_list_matches_spec():
    assert "README.md" in NOMINATED_MANIFESTS
    assert "AGENTS.md" in NOMINATED_MANIFESTS
    assert "install.py" in NOMINATED_MANIFESTS

def test_structural_hash_stable_and_changes_on_toplevel():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "README.md").write_text("a\n", encoding="utf-8")
        h1 = structural_hash(root)
        (root / "extra_dir").mkdir()
        h2 = structural_hash(root)
        assert h1 != h2
        assert len(h1) == 64

def test_identity_non_git_prefix():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "README.md").write_text("x\n", encoding="utf-8")
        h = structural_hash(root)
        assert identity(root, h) == f"non-git:{h}"
```

- [ ] **Step 2: Run tests (expect fail)**

```bash
cd ~/.zcode/skills/repo-cold-start && python -m pytest tests/test_hashutil.py -v
```

Expected: import/collection failures until implementation exists. If pytest missing, use:

```bash
cd ~/.zcode/skills/repo-cold-start && python -m unittest tests.test_hashutil -v
```

Prefer unittest if pytest not installed house-wide.

- [ ] **Step 3: Implement hashutil.py**

Canonical stream (spec):

1. List top-level entry names with `path.iterdir()`, exclude `.`/`..`, sort lexicographically as Unicode strings, write each name as UTF-8 + `\n`.
2. For each path in `NOMINATED_MANIFESTS` that exists as a file under root, write `relposix + '\0'` then raw file bytes.
3. SHA-256 hex digest of the concatenation.

Identity: if `(repo / '.git').exists()`, run `git -C repo rev-parse HEAD` (capture text strip). On failure (no commits, bad git): fall back to `non-git:` + structural hash and keep a warning string for the CLI. Else `non-git:` + structural hash.

```python
NOMINATED_MANIFESTS = (
    "README.md", "AGENTS.md", "package.json", "pyproject.toml", "Cargo.toml",
    "go.mod", "install.py", ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json", "CITATION.cff",
)
```

- [ ] **Step 4: Re-run tests (expect pass)**

- [ ] **Step 5: Stub SKILL.md + CLI**

`SKILL.md` frontmatter:

```yaml
---
name: repo-cold-start
description: Project root ARCHITECTURE.md and AGENTS index markers from BMAD/GSD/lightweight scan. Use when onboarding a repo or refreshing cold-start architecture docs.
---
```

Body: run `python <skill-dir>/repo_cold_start.py [flags] [repo]` with defaults `repo=.`.

`repo_cold_start.py` argparse: `--force`, `--lightweight`, `--gsd`, positional `repo` default `.`; print `not implemented` and exit 2 for now.

- [ ] **Step 6: Commit skill skeleton in the skill home if it is its own git repo; else leave on disk and note path in dogfood commit later**

House: `~/.zcode` may not be a git repo. Do not force a commit there. Track deliverable as files on disk; dogfood commit lives in this free-skills repo.

---

### Task 2: AGENTS merge (TDD)

**Files:**
- Create: `~/.zcode/skills/repo-cold-start/agents_merge.py`
- Create: `~/.zcode/skills/repo-cold-start/tests/test_agents_merge.py`

**Model:** standard

**Interfaces:**
- Produces: `def merge_agents(agents_path: Path, *, arch_rel: str = "./ARCHITECTURE.md") -> str`  
  Return value one of: `updated` | `unchanged` | `error:orphan-start` | `error:orphan-end`  
  Side effect: write file when updated.
- `def markers_ok(agents_text: str) -> bool` → True iff both pairs present, each start before its end, no orphan end without start.
- Marker constants (exact):

```python
INDEX_START = "<!-- repo-cold-start:index:start -->"
INDEX_END = "<!-- repo-cold-start:index:end -->"
LINK_START = "<!-- repo-cold-start:arch-link:start -->"
LINK_END = "<!-- repo-cold-start:arch-link:end -->"
```

- [ ] **Step 1: Failing tests**

```python
from pathlib import Path
import tempfile
from agents_merge import merge_agents, markers_ok, INDEX_START, INDEX_END, LINK_START, LINK_END

def test_append_when_missing():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "AGENTS.md"
        p.write_text("# Hello\n\nlocal policy\n", encoding="utf-8")
        assert merge_agents(p) == "updated"
        text = p.read_text(encoding="utf-8")
        assert INDEX_START in text and LINK_START in text
        assert "local policy" in text
        assert merge_agents(p) == "unchanged"  # idempotent
        assert markers_ok(text)

def test_orphan_start_fails_closed():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "AGENTS.md"
        p.write_text(INDEX_START + "\nbroken\n", encoding="utf-8")
        assert merge_agents(p).startswith("error:")

def test_one_pair_only_appends_missing_pair():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "AGENTS.md"
        body = f"{INDEX_START}\n## Agent index (repo-cold-start)\n\nx\n{INDEX_END}\n"
        p.write_text(body, encoding="utf-8")
        assert merge_agents(p) == "updated"
        t = p.read_text(encoding="utf-8")
        assert LINK_START in t and INDEX_START in t
```

- [ ] **Step 2: Run fail**

- [ ] **Step 3: Implement replace-between-markers**

Rules:

- If any start without matching end → `error:orphan-start` (do not write).
- If any end without matching start → `error:orphan-end` (do not write).
- For each pair independently: if pair present → replace interior with canonical content; if pair absent → append that block (after ensuring a blank line).
- If neither pair present → append both blocks once.
- Never modify text outside markers.
- Index interior:

```markdown
## Agent index (repo-cold-start)

See root [ARCHITECTURE.md](./ARCHITECTURE.md) for purpose, parts, boundaries, and entry points.
```

- Link interior: single line `[ARCHITECTURE.md](./ARCHITECTURE.md)` (or the `arch_rel` argument).

- [ ] **Step 4: Tests pass**

---

### Task 3: Freshness parse/write + skip path

**Files:**
- Create: `~/.zcode/skills/repo-cold-start/freshness.py`
- Create: `~/.zcode/skills/repo-cold-start/tests/test_freshness.py`
- Modify: `repo_cold_start.py` to call skip logic

**Model:** standard

**Interfaces:**
- `def parse_freshness(arch_text: str) -> dict | None`
- `def format_freshness(*, date: str, identity: str, structural_hash: str, engine: str) -> str`
- `def is_fresh(repo: Path, arch_path: Path) -> bool`  
  Recompute structural hash only; compare to parsed `structural_hash`; require parsed `engine` in enum. **Do not** require identity match (git HEAD may move).

- [ ] **Step 1: Tests**

```python
def test_roundtrip_freshness_block():
    block = format_freshness(date="2026-09-11", identity="non-git:abc", structural_hash="a"*64, engine="lightweight")
    parsed = parse_freshness("# x\n\n## Freshness\n\n" + block)
    assert parsed["engine"] == "lightweight"
    assert parsed["structural_hash"] == "a"*64

def test_is_fresh_false_when_missing_arch(tmp_path):
    assert is_fresh(tmp_path, tmp_path / "ARCHITECTURE.md") is False

def test_is_fresh_ignores_identity_drift(tmp_path):
    from hashutil import structural_hash, identity
    from freshness import format_freshness, is_fresh
    (tmp_path / "README.md").write_text("hi\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    h = structural_hash(tmp_path)
    arch = tmp_path / "ARCHITECTURE.md"
    arch.write_text(
        "# A\n\n## Freshness\n\n"
        + format_freshness(date="2026-09-11", identity="deadbeef", structural_hash=h, engine="lightweight"),
        encoding="utf-8",
    )
    (tmp_path / "pkg" / "x.py").write_text("1\n", encoding="utf-8")  # non-nominated body churn
    assert is_fresh(tmp_path, arch) is True
    assert identity(tmp_path, h) != "deadbeef" or True  # identity may differ; freshness still True
```

Freshness section body format (pin):

```markdown
- Date: 2026-09-11
- Identity: non-git:…
- Structural hash: …
- Engine: lightweight
```

- [ ] **Step 2: Implement**

- [ ] **Step 3: Wire CLI early exit**

Order after resolving `repo` path:

1. Parse flags (`--force` disables skip).
2. If not force and `ARCHITECTURE.md` exists and `is_fresh(repo, arch)`:
   - Ensure `AGENTS.md` exists (create empty file if missing).
   - If `markers_ok(AGENTS.md text)`: print skip line and exit 0.
   - Else: run `merge_agents` only; on success print repair line + skip line; exit 0. On merge error: exit 1 (do not re-project body).
3. Skip line format: git repos `ARCHITECTURE.md fresh @ <full HEAD sha>`; non-git `ARCHITECTURE.md fresh @ non-git:<first 12 hex chars of structural hash>` (storage in Freshness still uses full `non-git:<full hash>` identity).
4. Else continue to full project path.

- [ ] **Step 4: Tests pass**

---

### Task 4: Detection + flag precedence

**Files:**
- Create: `~/.zcode/skills/repo-cold-start/detect.py`
- Create: `~/.zcode/skills/repo-cold-start/tests/test_detect_flags.py`

**Model:** standard

**Interfaces:**
- `Engine = Literal["bmad-quick","gsd-map","lightweight","hub-project","manual"]`
- `class DetectError(Exception): ...`  # used for --gsd create failure
- `def choose_engine(repo: Path, *, lightweight: bool, gsd: bool) -> tuple[Engine, dict]`  
  Note: `force` is CLI-only (freshness skip); not an engine selector.  
  Context dict keys: `hub_path: Path | None`, `brownfield_index: Path | None`, `warnings: list[str]`.

**Algorithm (implement exactly):**

1. If `lightweight`: return `("lightweight", {hub_path: None, brownfield_index: None, warnings: []})`.
2. If `gsd`:
   - If `(repo/".planning").exists()` is False: `mkdir` it; on OSError raise `DetectError("cannot create .planning")`.
   - Return `("gsd-map", …)` (even if brownfield or hub also exist).
3. Else auto:
   - Collect hub candidates (existing paths only):
     - Fixed: `docs/catia-magic-mcp-architecture/README.md` if file exists.
     - Glob: every `docs/**/architecture/README.md` whose first 40 lines contain substring `authoritative` (casefold).
     - Pointers: markdown links in root `README.md`/`AGENTS.md` where link text or same line matches regex `(?i)authoritative.*architecture|architecture.*authoritative`; resolve target; if dir, prefer `README.md` under it.
     - If candidates: pick lexicographically smallest POSIX relative path → engine `hub-project`.
   - Else if `docs/brownfield/index.md` exists → engine `bmad-quick` if first 80 lines casefold-match both `bmad` and (`document-project` or `document project`), else `manual`; set `brownfield_index`.
   - Else if either `.claude/skills/bmad-document-project/SKILL.md` or `.agents/skills/bmad-document-project/SKILL.md` exists → engine `bmad-quick` (index missing).
   - Else if `(repo/".planning").exists()` → engine `gsd-map`.
   - Else → `lightweight`.

**v1 CLI pragmatism (pin):** Do not shell out to an LLM. Compute `effective_engine` for Freshness and body: when chosen engine is `bmad-quick` and brownfield index missing: print host instruction, warning, set `effective_engine = "lightweight"`. When chosen engine is `gsd-map` and `.planning/codebase/ARCHITECTURE.md` missing: print host instruction, set `effective_engine = "lightweight"`. Otherwise `effective_engine = chosen`. Always write Freshness `Engine:` as `effective_engine`.
- [ ] **Step 1: Tests for precedence**

```python
def test_lightweight_beats_gsd(tmp_path):
    (tmp_path / ".planning").mkdir()
    eng, _ = choose_engine(tmp_path, lightweight=True, gsd=True)
    assert eng == "lightweight"

def test_gsd_beats_brownfield(tmp_path):
    (tmp_path / "docs" / "brownfield").mkdir(parents=True)
    (tmp_path / "docs" / "brownfield" / "index.md").write_text("bmad document-project\n", encoding="utf-8")
    eng, _ = choose_engine(tmp_path, lightweight=False, gsd=True)
    assert eng == "gsd-map"
    assert (tmp_path / ".planning").is_dir()

def test_gsd_creates_planning(tmp_path):
    eng, _ = choose_engine(tmp_path, lightweight=False, gsd=True)
    assert eng == "gsd-map"
    assert (tmp_path / ".planning").is_dir()

def test_hub_fixed_path(tmp_path):
    p = tmp_path / "docs" / "catia-magic-mcp-architecture"
    p.mkdir(parents=True)
    (p / "README.md").write_text("# hub\n", encoding="utf-8")
    eng, ctx = choose_engine(tmp_path, lightweight=False, gsd=False)
    assert eng == "hub-project"
    assert "catia-magic-mcp-architecture" in str(ctx["hub_path"])

def test_hub_tie_break_lex_smallest(tmp_path):
    a = tmp_path / "docs" / "aaa" / "architecture"
    b = tmp_path / "docs" / "zzz" / "architecture"
    for p in (a, b):
        p.mkdir(parents=True)
        (p / "README.md").write_text("authoritative hub\n", encoding="utf-8")
    eng, ctx = choose_engine(tmp_path, lightweight=False, gsd=False)
    assert eng == "hub-project"
    assert "aaa" in str(ctx["hub_path"]).replace("\\", "/")
```

- [ ] **Step 2: Implement hub candidate collection + lex smallest path + algorithm above**

- [ ] **Step 3: Tests pass**

---

### Task 5: Lightweight projector + full CLI write path

**Files:**
- Create: `~/.zcode/skills/repo-cold-start/project.py`
- Modify: `repo_cold_start.py` full flow
- Modify: `SKILL.md` complete procedure

**Model:** deep

**Interfaces:**
- `def main(argv: list[str] | None = None) -> int`
- `def build_architecture_md(repo: Path, *, engine: str, hub_path: Path | None, brownfield_index: Path | None) -> str`  
  When brownfield_index set, read that file and optional sibling `project-overview.md` in the same directory.

- Section H2 titles exact order:
  1. `## Purpose`
  2. `## Runtime / deliverable shape`
  3. `## Major parts`
  4. `## Boundaries`
  5. `## Entry points`
  6. `## Doc map`
  7. `## Freshness`
- Include copyright HTML header if `AGENTS.md` starts with `<!--` copyright block (copy first comment block).
- `def scrub_leaks(text: str, repo: Path) -> str` before write:
  - Replace `str(Path.home())` and `Path.home().as_posix()` with `unknown`.
  - Regex replace (case-insensitive) assignments like `(api[_-]?key|secret|token|password)\s*[:=]\s*\S+` → `\1: unknown`.
  - Regex replace `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `glpat-[A-Za-z0-9_-]{20,}` → `unknown`.


- [ ] **Step 1: Implement lightweight body**

From repo:

- Purpose: first non-empty paragraph of README.md after the H1 (strip badge lines) or `unknown`
- Runtime shape: infer from presence of `install.py`, `skills/`, `package.json`, etc.
- Major parts: top-level dirs (skip `.git`) as markdown table path | role guess
- Boundaries: bullet lines from AGENTS containing "do not" / "never" (casefold), else `unknown`
- Entry points: README install fenced commands first line + `install.py` if present
- Doc map: list top-level `docs/*.md` names + brownfield/GSD paths if exist
- Freshness: `format_freshness` + `datetime.date.today().isoformat()` + identity + hash + engine
- Run `scrub_leaks` on full body

- [ ] **Step 2: Hub / brownfield / GSD projection**

- hub-project: purpose from hub README first para; Doc map links hub; engine `hub-project`
- brownfield: read `docs/brownfield/index.md` (+ overview if present); engine already chosen (`bmad-quick` or `manual`)
- gsd-map: if `.planning/codebase/ARCHITECTURE.md` exists, take Purpose/Major parts from it and STRUCTURE.md when present; one-line stack from STACK.md; Doc map links `.planning/codebase/`; engine `gsd-map`. If map missing, CLI already fell through to lightweight before calling build.

- [ ] **Step 3: CLI end-to-end on temp repo test**

```python
from repo_cold_start import main

def test_cli_writes_arch(tmp_path):
    (tmp_path / "README.md").write_text("# P\n\nPurpose here.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# A\n", encoding="utf-8")
    assert main([str(tmp_path), "--lightweight"]) == 0
    assert (tmp_path / "ARCHITECTURE.md").exists()
    assert "Engine: lightweight" in (tmp_path / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert main([str(tmp_path), "--lightweight"]) == 0  # fresh

def test_scrub_home_path(tmp_path, monkeypatch):
    home = str(Path.home())
    (tmp_path / "README.md").write_text(f"# P\n\nUses {home}/secret\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# A\n", encoding="utf-8")
    main([str(tmp_path), "--lightweight"])
    body = (tmp_path / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert home not in body
```

- [ ] **Step 4: Second run exits fresh without rewrite** (content of sections 1–6 unchanged; Freshness identity may update only if you choose to rewrite Freshness on skip — v1: on full skip, do not touch file at all)

- [ ] **Step 5: Update SKILL.md procedure** to match CLI flags and host BMAD/GSD notes

- [ ] **Step 6: Em-dash scan** on skill-authored `ARCHITECTURE.md` in unit test fixture (assert `"—"` not in body and `" -- "` not in prose lines)

---

### Task 6: Dogfood on free-skills pack + AGENTS merge

**Files:**
- Modify (repo): `ARCHITECTURE.md` (create)
- Modify (repo): `AGENTS.md` (markers only)
- Test: run CLI from this repo root

**Model:** standard

**Interfaces:** consumes Task 5 CLI

- [ ] **Step 1: Run lightweight cold-start**

```bash
python ~/.zcode/skills/repo-cold-start/repo_cold_start.py --lightweight \
  "C:/Users/gower/OneDrive/Documents/GitHub/cameo-sysmlv2-mcp/releases/jgs-magic-sysmlv1-free-skills"
```

Expected: creates `ARCHITECTURE.md`; merges AGENTS markers; exit 0.

- [ ] **Step 2: Human-grade pass on ARCHITECTURE.md**

- Fix purpose/boundaries if lightweight inference is weak (allowed hand edit of body; not Freshness).
- Re-run CLI without `--force`; expect fresh skip (or AGENTS-only if markers broken).
- Ensure no edits to `SKILLS.md` / `RELEASE-INFO.txt`.

- [ ] **Step 3: Run unit tests once more**

```bash
cd ~/.zcode/skills/repo-cold-start && python -m unittest discover -s tests -v
```

- [ ] **Step 4: Commit in free-skills repo**

```bash
git add ARCHITECTURE.md AGENTS.md
git add docs/superpowers/specs/2026-09-11-repo-cold-start-architecture-design.md
git add docs/superpowers/specs/2026-09-11-repo-cold-start-architecture-design-triage-log.md
git add docs/superpowers/specs/2026-09-11-repo-cold-start-architecture-design-fcl-triage-log.md
git add docs/superpowers/plans/2026-09-11-repo-cold-start-architecture-design.md
git add docs/superpowers/plans/2026-09-11-repo-cold-start-architecture-design-triage-log.md
git add docs/superpowers/plans/2026-09-11-repo-cold-start-architecture-design-fcl-triage-log.md
git status --short
git commit -m "docs: root ARCHITECTURE cold-start + repo-cold-start plan/spec"
```

Only add paths that exist. Do not use `|| true` to hide failures.

---

### Task 7: Mirror skill to agents path + invoke smoke

**Files:**
- Create/sync: `~/.agents/skills/repo-cold-start/` (copy tree)
- Optional: `~/.claude/skills/repo-cold-start/` symlink or copy if house mirrors skills there

**Model:** flash

**Interfaces:** same CLI

- [ ] **Step 1: Copy skill tree**

```bash
rm -rf ~/.agents/skills/repo-cold-start
cp -R ~/.zcode/skills/repo-cold-start ~/.agents/skills/repo-cold-start
```

- [ ] **Step 2: Smoke**

```bash
python ~/.agents/skills/repo-cold-start/repo_cold_start.py --help
```

- [ ] **Step 3: Document in SKILL.md** that after install, new chat may be required for skill discovery; invoke `/repo-cold-start` or run the python entry.

---

## Spec coverage checklist

| Spec requirement | Task |
|------------------|------|
| Root trio layout | 5–6 |
| AGENTS merge markers / fail-closed | 2 |
| Freshness fields + structural hash + identity | 1, 3 |
| Flag precedence | 4 |
| Hub detection + tie-break | 4–5 |
| BMAD paths fixed; host Quick note; fallthrough | 4–5 |
| GSD paths full; create `.planning` on `--gsd` | 4–5 |
| Hash-only refresh | 3 |
| Lightweight default | 5 |
| Dogfood success criteria 1 and 4 | 6 |
| Success criteria 2, 3, 5 | Accepted by inspection / manual (no automated monorepo BMAD/GSD dogfood in this plan) |
| User-global home + mirrors | 1, 7 |
| No BMAD vendor / no stager edits | Global + 6 |
| Secrets / home-path scrub | 5 |
| `--gsd` creates `.planning` | 4 |
| GSD body projection | 5 |
| Fresh match = hash + engine (not HEAD) | 3 + spec amendment |

## Open points closed in plan

- Hash byte stream: Task 1 pins names + `\n` and `path\0` + bytes.
- BMAD/GSD inside CLI: host-agent instruction + lightweight fallthrough (deterministic v1).
- Section-to-source mapping table: deferred (spec advisory-skipped).
- Git HEAD alone must not force rewrite: spec + Task 3 match on structural hash + engine only.

author-leaf: fallback (inline)
