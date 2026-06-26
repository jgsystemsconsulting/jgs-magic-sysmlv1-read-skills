<!--
Copyright (c) 2026 JG Systems Consulting Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# Contributing

Thanks for your interest in the JGS SysML v1 Read Skills. This pack is open source under
Apache-2.0, and contributions are welcome.

## Before you start

These skills are read-only. They drive the FREE tier of the proprietary
[jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp) bridge and
must never modify a model. Any contribution that adds write behaviour, or that calls a write or
`enable_writes` tool, is out of scope here and belongs in the separate PRO pack.

## How to contribute

1. Fork the repository and create a branch from `main`.
2. Make your change. Keep each skill's `SKILL.md` self-contained, with valid frontmatter
   (`name` matching its directory, plus a `description`) and a `## When to use` section.
3. Run the checks the CI runs:
   - `python install.py --dry-run` lists all 17 skills with no error.
   - The content-integrity and frontmatter checks in `.github/workflows/validate.yml` pass.
4. Keep customer-facing prose free of the em dash character, per the project's writing style;
   use a comma, colon, or parentheses instead.
5. Open a pull request describing the change and why.

## Ground rules

- Every source and doc file carries the standard header
  (`Copyright (c) 2026 JG Systems Consulting Ltd.` + `SPDX-License-Identifier: Apache-2.0`).
- By submitting a contribution you agree it is licensed under Apache-2.0, the project licence.
- Do not commit secrets, keys, or internal-only material.

## Reporting issues

For bugs and feature requests, open an issue. For security issues, follow
[SECURITY.md](SECURITY.md) (a private advisory, not a public issue).
