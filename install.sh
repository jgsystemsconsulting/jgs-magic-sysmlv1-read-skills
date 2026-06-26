#!/usr/bin/env bash
# Copyright (c) 2026 JG Systems Consulting Ltd.
# SPDX-License-Identifier: Apache-2.0
#
# Shell wrapper around install.py. Forwards all arguments.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${DIR}/install.py" "$@"
