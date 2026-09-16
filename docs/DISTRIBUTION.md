<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
Generated at release time from scripts/release_v1_free_templates/docs/DISTRIBUTION.md.
Under the stager model, edit that source copy: this staged file is regenerated.
-->

# Distribution ledger · JGS SysML v1 Read Skills

One row per place this product is, or could be, distributed and discovered
(`RR-B-36`, release-repo-standard v1.14). Statuses: `submitted` (URL + date, filed by
the maintainer), `in progress`, `deferred`, `deliberate N/A`, `planned`. A
non-submitted row carries the decision and its date so the question stays closed
until its premises change. Revisit at every release; never drop a row silently. An
agent never marks a row `submitted`: filing is the maintainer's action, recorded here.

Last reviewed: 0.3.0 / 2026-09-09

Licence posture: proprietary EULA, free of charge (§0.3: directory eligibility keys
off the licence, not the price).

## In-host marketplaces (manifests shipped, RR-B-29a / RR-S-08)

| Channel | Manifest | Status | Decision / reason | Date |
|---|---|---|---|---|
| Claude Code: Plugin Directory submission form (Console) | `.claude-plugin/` | submitted | Filed 2026-09-09 via platform.claude.com/plugins/submit from the maintainer's Console account; lands in claude-plugins-community after review (`claude plugin validate` passed pre-filing). Contact: support@jgsystemsconsulting.com. | 2026-09-09 |
| Cursor: cursor.com/marketplace/publish + cursor.directory | `.cursor-plugin/` | deliberate N/A | Reviewed marketplace requires an open-source licence; pack is proprietary EULA. Manifest ships for in-repo install. Revisit only if the licence posture changes. | 2026-09-09 |
| OpenAI Codex CLI: Plugin Directory (universal ChatGPT/Codex directory) | root `plugin.json` (agent-plugins 1.0.0) | in progress | Root agent-plugins manifest added 2026-09-16; the portal filing (developers.openai.com/plugins/deploy/submission, OpenAI account) remains. | 2026-09-16 |
| Gemini CLI: geminicli.com/extensions gallery | `gemini-extension.json` | in progress | Auto-index requirements verified but the gallery/extensions.json still excludes the pack after a week; indexing issue filed: google-gemini/gemini-cli#29356 (2026-09-16). | 2026-09-16 |
| ZCode | installer target (`--agent zcode`, flat `~/.zcode/skills`) | deliberate N/A | No marketplace exists; distribution is the installer plus this repository. | 2026-09-09 |

## Web directories & catalogues

| Channel | Artifact | Status | Decision / reason | Date |
|---|---|---|---|---|
| JGSC Labs catalogue (labs.jgsystemsconsulting.com) | site product entry | submitted | Live on the products page (site commit c3bc5a3); blurb matches the repo About description. | 2026-09-09 |
| GitHub About + topics + Release | publish-time `gh` config | submitted | Configured at publish (description, homepage = Pages URL, topics per RR-B-21). | 2026-09-09 |
| mcpservers.org/agent-skills (community skills marketplace) | repo URL | in progress | Checked 2026-09-16: pack not yet listed (skill-URL probes 404). Escalation email to contact [at] mcpservers.org drafted in the submission pack; send it. | 2026-09-16 |
| Community awesome-lists (Claude/agent-skills family) | PR entry | deferred | Same acceptability gate as RR-B-29b: verify each list's licence requirement before a PR. | 2026-09-09 |

## MCP aggregator directories (RR-M-07)

Out of scope for this repository: the MCP surface is the companion bridge
`jgs-magic-sysmlv1-mcp` (Glama/awesome-mcp-servers, Smithery, PulseMCP). Its
distribution ledger lives in that repository's `docs/DISTRIBUTION.md`.
