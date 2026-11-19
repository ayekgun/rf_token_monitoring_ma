#!/usr/bin/env bash
# ==============================================================================
# Runner for Automated Mutation Testing & Assertion Sensitivity Verification
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RF_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$RF_DIR"

if [ -f "$RF_DIR/.env" ]; then
  set -a
  source "$RF_DIR/.env"
  set +a
fi

echo "Running Mutation Testing Suite..."
python3 tests/mutation/test_mutation_sensitivity.py
