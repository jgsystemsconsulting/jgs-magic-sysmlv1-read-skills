<!--
Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
See LICENSE for terms.
-->

# Skill Usage Guide: JGS SysML v1 Read Skills

## Entry point

Always start with the dispatcher:

```
/jgs-v1 <your request in plain English>
```

The dispatcher pings the bridge, checks your licence tier, and routes to the right specialist
automatically. It depends on the [jgs-magic-sysmlv1-mcp](https://github.com/jgsystemsconsulting/jgs-magic-sysmlv1-mcp)
bridge being installed and running (FREE tier is enough).

## Direct invocation

Each specialist can also be called directly:

```
/jgs-v1-navigate [<package-name>]
/jgs-v1-impact <element-name>
/jgs-v1-audit [<root-package-id>]
```

Direct invocation skips the dispatcher's liveness check, so you will see raw bridge errors if the bridge is down.

## What requires PRO tier

All skills in this pack are FREE tier (read-only). To make changes to the model, you need:

- **jgs-magic-sysmlv1-mcp PRO licence**
- **jgs-magic-sysmlv1-pro-skills** pack

v1 to v2 **migration** (migrate-read inventory, cross-model compare) is also a PRO capability. It is
read-only but ships in the **jgs-magic-sysmlv1-pro-skills** pack, not here.

The dispatcher will tell you when a request needs PRO access and describe what read-only analysis is available instead.

## Troubleshooting

**"Bridge is not reachable":** ensure CATIA Magic is open with a SysML v1 project loaded and the jgs-magic-sysmlv1-mcp plugin is active.

**Results seem truncated:** some bridge tools cap at 50 results or 2000 elements. Use qualified names for exact lookups, or scope the skill to a specific package.

