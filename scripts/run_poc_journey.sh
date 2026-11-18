#!/usr/bin/env bash
# ==============================================================================
# Full 7-Step Interactive Spotlight & HUD POC Journey Runner (Foreground)
# ==============================================================================
REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
RF_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$RF_DIR"
export DISPLAY="${DISPLAY:-:0}"
python3 automation/spotlight_hud_runner.py --headed "$@"
