#!/usr/bin/env bash
# ==============================================================================
# Shortcut Runner for Live Watch / Foreground Headed Mode
# ==============================================================================
REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
"$SCRIPT_DIR/run_tests.sh" --headed "$@"
