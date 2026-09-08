#!/usr/bin/env bash
# Copyright (c) 2026 JG Systems Consulting Ltd. All Rights Reserved.
# See LICENSE for terms.
#
# Shell wrapper around install.py. Forwards all arguments.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${DIR}/install.py" "$@"
