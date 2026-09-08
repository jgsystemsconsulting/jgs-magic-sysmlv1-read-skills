---
name: jgs-v1-feedback
description: "Draft and file a pack or bridge issue on GitHub after one explicit user yes. Trigger: /jgs-v1-feedback"
argument-hint: "[optional gap note]"
---
<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# jgs-v1-feedback

## When to use

User-invoked, or offered by the `/jgs-v1` dispatcher, when a shipped skill or an MCP
contract blocked an outcome that any user of this pack would hit. It is not a modelling
specialist: it never talks to the bridge about model content.

## Prerequisites

- The pack installed (it files against this pack's own tracker).
- GitHub CLI (`gh`) is optional: logged-in `gh` files the issue; otherwise this skill
  prints a pre-filled new-issue URL. No bot token; the issue files as the logged-in user.

## Hard rules

1. File nothing until the user sees the exact draft and says yes.
2. Skill-meta only. No element names, model paths, model content, tokens, or credentials.
3. Origin only if every user of the pack would hit this gap. Local model, org, install,
   or governance pain stays local: say so and stop.
4. No telemetry, no phone-home, no lessons file. It writes only to the issue tracker and
   never stalls the session on a login.

## Filing path

- Default tracker: `jgsystemsconsulting/jgs-magic-sysmlv1-read-skills`.
- If the gap is in the MCP bridge itself (connection, tools, licensing), file on
  `jgsystemsconsulting/jgs-magic-sysmlv1-mcp` instead, and say that you re-routed.
- Logged in: `gh issue create --repo <issues_repo> --title <title> --body <body>`.
- Not logged in: print `https://github.com/<issues_repo>/issues/new?title=...&body=...`
  with the template below URL-encoded, and stop.

## Body template (skill-meta only)

Use this exact markdown as the issue body. It matches the Skill Improvement form fields.

Skill: <skill name, or unknown>
Step: <what you were doing when the gap appeared>
Outcome blocked: <one sentence: what you could not achieve>
Proposed change: <one sentence>
Pack version: <copy Version from RELEASE-INFO.txt, or unknown>
Agent host: <zcode, claude, or other>
Bridge tool or resource: <name only, or none>

This report contains no model content, tokens, or credentials.

## Origin vs local

File only if the proposed change belongs in shipped skill text, the installer, or the
bridge contract, and every other user of the pack would hit the same hole. Environment
pain, private model quirks, and org-specific setup stay local.
