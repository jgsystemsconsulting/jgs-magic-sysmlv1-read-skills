# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-JGSystemsConsulting-Proprietary
"""Release gate (RR-B-15) for the JGS SysML v1 Read Skills pack.

Runs the four check classes against the release-repo root that contains this
script (parent of scripts/): required files, forbidden paths, forbidden
content, headers present. Also asserts version agreement (RR-B-09/RR-S-11)
and BOM-free parser-critical files (RR-B-33). Exits non-zero on any failure.

Works both before and after the release repo gets its own .git: it judges the
files on disk, and when the tree owns its .git it additionally scans the
tracked file list.
"""
import json
import os
import pathlib
import re
import sys


def check_site_version(root, release_re):
    """docs/index.html version strings must equal RELEASE-INFO.txt (ported from jgs-lit-memory)."""
    m = re.search(release_re, (root / "RELEASE-INFO.txt").read_text(encoding="utf-8"), re.M)
    if not m:
        return ["RELEASE-INFO.txt: no version line"]
    expected = m.group(1)
    page = (root / "docs" / "index.html").read_text(encoding="utf-8")
    loci = {
        "softwareVersion": r'"softwareVersion":\s*"(\d+\.\d+\.\d+)"',
        "masthead REV": r"REV <b>(\d+\.\d+\.\d+)</b>",
        "footer Rev": r'<span class="label">Rev</span><b>(\d+\.\d+\.\d+)</b>',
    }
    bad = []
    for name, pat in loci.items():
        v = re.search(pat, page)
        val = v.group(1) if v else None
        if val != expected:
            bad.append(f"{name}={val!r} (expected {expected})")
    if bad:
        return ["site page version mismatch or missing pattern: " + "; ".join(bad)]
    print(f"site page versions agree at {expected}")
    return []


ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)

fails: list[str] = []

# -- 1. Required files -----------------------------------------------------

REQUIRED = [
    "LICENSE", "COPYRIGHT", "NOTICE",
    "README.md", "CHANGELOG.md", "SKILLS.md",
    "RELEASE-INFO.txt", "CITATION.cff", "SECURITY.md", ".gitignore",
    "install.py", "install.sh", "install.ps1",
    "docs/skill-usage.md", "docs/other-agents.md",
    "docs/DISTRIBUTION.md",
    "docs/index.html", "docs/guide.html", "docs/site.css", "docs/.nojekyll",
    "AGENTS.md",
    ".claude-plugin/marketplace.json", ".claude-plugin/plugin.json",
    ".cursor-plugin/marketplace.json", ".cursor-plugin/plugin.json",
    ".agents/plugins/marketplace.json", "gemini-extension.json",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/improvement.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "scripts/check_release.py",
    "skills/jgs-v1-audit/SKILL.md",
    "skills/jgs-v1-feedback/SKILL.md",
]
for f in REQUIRED:
    if not pathlib.Path(f).is_file():
        fails.append(f"required file missing: {f}")

# -- 2. Forbidden paths ----------------------------------------------------

FORBIDDEN_PATH_PARTS = ["__pycache__", ".venv", ".worktrees", ".pytest_cache",
                        ".ruff_cache", ".bak"]


def _tree() -> list[pathlib.Path]:
    return [p for p in pathlib.Path(".").rglob("*")
            if p.is_file() and ".git" not in p.parts]


tracked: list[str] | None = None
if (ROOT / ".git").exists():
    import subprocess
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                             check=True, cwd=ROOT).stdout.splitlines()
    for f in tracked:
        if any(part in pathlib.PurePosixPath(f).parts for part in FORBIDDEN_PATH_PARTS):
            fails.append(f"forbidden tracked path: {f}")

# -- 3. Forbidden content + 4. Headers present -----------------------------

# Gate and CI scripts legitimately list the sentinels as grep targets
# (RR-B-15 / RR-S-12), so the content scan skips their own sources.
CONTENT_SCAN_SKIP = ("scripts/check_release.py", ".github/workflows/")
FORBIDDEN_CONTENT = [re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
                     re.compile(r"CONFIDENTIAL\s+[-\u2014]\s+Not for external distribution"),
                     "JGS_V2_WRITE_SECRET",
                     "JGS_V2_DEV_SECRET"]
HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd."
BINARY_SUFFIXES = {".png", ".jpg", ".ico", ".gif", ".pdf", ".zip", ".jar", ".woff2"}
BOM_SUFFIXES = {".toml", ".json", ".yaml", ".yml", ".cff"}

for path in _tree():
    rel = path.as_posix()
    if any(part in path.parts for part in FORBIDDEN_PATH_PARTS):
        fails.append(f"forbidden path: {rel}")
    if path.suffix.lower() in BINARY_SUFFIXES:
        continue
    raw = path.read_bytes()
    if path.suffix.lower() in BOM_SUFFIXES and raw.startswith(b"\xef\xbb\xbf"):
        fails.append(f"UTF-8 BOM in parser-critical file: {rel}")
    text = raw.decode("utf-8", errors="ignore")
    if not rel.startswith(CONTENT_SCAN_SKIP):
        for rx in FORBIDDEN_CONTENT:
            if isinstance(rx, str):
                if rx in text:
                    fails.append(f"forbidden content in {rel}: {rx!r}")
            elif rx.search(text):
                fails.append(f"forbidden content in {rel}: {rx.pattern}")
    if path.suffix.lower() in {".md", ".py", ".sh", ".ps1"}:
        if rel.startswith(("docs/superpowers/", ".superpowers/")):
            pass  # process artifacts; header not required
        elif HEADER_SENTINEL not in text[:4096]:
            fails.append(f"header missing: {rel}")

for path in _tree():
    if path.suffix == ".py":
        head = path.read_text(encoding="utf-8", errors="ignore")[:600]
        if "SPDX-License-Identifier:" not in head:
            fails.append(f"SPDX missing: {path.as_posix()}")

# -- Site structure (RR-B-30): shared stylesheet, anchors, no leaks -------

ALLOWED_HOSTS = ("github.com", "jgsystemsconsulting.github.io", "labs.jgsystemsconsulting.com")
pages = {p.name: p.read_text(encoding="utf-8", errors="ignore")
         for p in pathlib.Path("docs").glob("*.html")}
ids = {name: set(re.findall(r'id="([^"]+)"', text)) for name, text in pages.items()}
for name, text in sorted(pages.items()):
    body = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    if 'href="site.css"' not in body:
        fails.append(f"site: {name} does not link the shared stylesheet")
    if "—" in body:
        fails.append(f"site: {name} has an em dash outside comments")
    for m in re.finditer(r'(?:src|href)="(https?://[^"/]+)', body):
        if not any(h in m.group(1) for h in ALLOWED_HOSTS):
            fails.append(f"site: {name} references third-party host {m.group(1)}")
    for m in re.finditer(r'href="([^"#]*)(#[^"]+)?', body):
        target, frag = m.group(1), m.group(2)
        if not frag:
            continue
        page_ids = ids.get(target if target else name, None)
        if page_ids is None:
            if not target.startswith(("http", "{{")):
                fails.append(f"site: {name} anchors to missing page {target}")
            continue
        if frag[1:] not in page_ids:
            fails.append(f"site: {name} anchor {frag} not on {target or name}")

# -- Version agreement (RR-B-09 / RR-S-11) ---------------------------------

VERSION = "0.3.0"
rel_text = pathlib.Path("RELEASE-INFO.txt").read_text(encoding="utf-8",
                                                      errors="ignore") if pathlib.Path("RELEASE-INFO.txt").is_file() else ""
m_rel = re.search(r"(?m)^Version:\s*(\S+)", rel_text)
if not m_rel:
    fails.append("RELEASE-INFO.txt has no Version:")
elif m_rel.group(1) != VERSION:
    fails.append(f"version mismatch: RELEASE-INFO.txt={m_rel.group(1)!r} != {VERSION!r}")

cl = pathlib.Path("CHANGELOG.md")
if cl.is_file():
    m_cl = re.search(r"(?m)^##\s+\[?(\d+\.\d+\.\d+)\]?", cl.read_text(encoding="utf-8",
                                                                      errors="ignore"))
    if not m_cl:
        fails.append("CHANGELOG.md has no semver heading")
    elif m_cl.group(1) != VERSION:
        fails.append(f"version mismatch: CHANGELOG top {m_cl.group(1)!r} != {VERSION!r}")

pj = pathlib.Path(".claude-plugin/plugin.json")
if pj.is_file():
    try:
        v = json.loads(pj.read_text(encoding="utf-8")).get("version")
        if v != VERSION:
            fails.append(f"version mismatch: plugin.json={v!r} != {VERSION!r}")
    except Exception as exc:
        fails.append(f"plugin.json unreadable: {exc}")

cff = pathlib.Path("CITATION.cff")
if cff.is_file():
    m_cff = re.search(r'(?m)^version:\s*["\']?([^"\'\s]+)', cff.read_text(encoding="utf-8", errors="ignore"))
    if not m_cff:
        fails.append("CITATION.cff has no version:")
    elif m_cff.group(1) != VERSION:
        fails.append(f"version mismatch: CITATION.cff={m_cff.group(1)!r} != {VERSION!r}")

cpj = pathlib.Path(".cursor-plugin/plugin.json")
if cpj.is_file():
    try:
        v = json.loads(cpj.read_text(encoding="utf-8")).get("version")
        if v != VERSION:
            fails.append(f"version mismatch: .cursor-plugin/plugin.json={v!r} != {VERSION!r}")
    except Exception as exc:
        fails.append(f".cursor-plugin/plugin.json unreadable: {exc}")

fails += check_site_version(pathlib.Path("."), r"^Version:\s*(\d+\.\d+\.\d+)")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("release gate: PASS")
