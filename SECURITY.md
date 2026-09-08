<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Security Policy

## Reporting a vulnerability

If you discover a security issue in this software, please report it **privately**. Do
**not** open a public GitHub issue for security vulnerabilities.

- **Preferred:** open a [private security advisory](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-read-skills/security/advisories/new)
  on this repository. This reaches the maintainer directly and keeps the report
  confidential while a fix is prepared.
- **Alternatively:** a pull request with the fix and a description of the issue, marked
  as security-related in the description. Do not include exploit details in the PR body.
- **General contact (non-security):** support@jgsystemsconsulting.com. JG Systems
  Consulting Ltd operates this inbox for general enquiries; vulnerability reports should
  still come through the private advisory above so they are tracked as security items.
- Include: a description, reproduction steps, and the affected version (see `RELEASE-INFO.txt`).

## What to expect

- Private disclosure: reports are kept confidential until a fix is available.
- Acknowledgement within **5 business days**.
- An assessment and, where applicable, a remediation plan.
- Coordinated disclosure once a fix is available; reporters who request credit get it.

This is proprietary software licensed by JG Systems Consulting Ltd. There is no paid
bug-bounty program, but we appreciate responsible disclosure.

## Scope

These skills are **read-only**: they call the FREE/read-only tier of the
`jgs-magic-sysmlv1-mcp` bridge and never modify your model. Reports about the bridge
itself belong on the bridge: see its repository (`jgs-magic-sysmlv1-mcp`) and file there
or via its own security policy.
