#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

declare -A seen
dupes=0
for f in resources/keywords/*.robot; do
  [ -e "$f" ] || continue
  while IFS= read -r kw; do
    [ -z "$kw" ] && continue
    [ "${kw:0:1}" = "*" ] && continue
    if [ -n "${seen[$kw]:-}" ]; then
      echo "  ⚠  '$kw' di: ${seen[$kw]} + $f"
      dupes=$((dupes+1))
    else
      seen[$kw]="$f"
    fi
  done < <(grep -E '^[A-Z][A-Za-z0-9 _-]+$' "$f" | sed 's/ *$//' | sort -u)
done

if [ "$dupes" -eq 0 ]; then
  echo "==> OK - Tidak ada keyword duplikat antar file resource."
  exit 0
else
  exit 1
fi
