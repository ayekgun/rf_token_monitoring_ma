#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

grep -rhoE '@keyword\("([^"]+)"\)' libraries/ 2>/dev/null | \
  sed -E 's/@keyword\("([^"]+)"\)/\1/' | sort -u > /tmp/py_kw.txt || true

grep -rhE '^[A-Z][A-Za-z0-9 _-]+$' resources/keywords/*.robot 2>/dev/null | \
  grep -vE '^\*' | sort -u > /tmp/rf_kw.txt || true

echo "==> Collision (recursion risk):"
colls=$(comm -12 /tmp/py_kw.txt /tmp/rf_kw.txt 2>/dev/null || true)
if [ -n "$colls" ]; then
  echo "$colls" | while read -r kw; do
    [ -n "$kw" ] && echo "  ⚠  $kw"
  done
  exit 1
else
  echo "  OK - Tidak ada benturan nama keyword (bebas infinite recursion)."
fi
