#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

grep -hE '^[A-Z][A-Za-z0-9 _-]+$' resources/keywords/*.robot 2>/dev/null | \
  grep -vE '^\*' | sed 's/ *$//' | sort -u > /tmp/rf_defined.txt || true

python3 - <<'PY'
import re, sys, glob
defined = set()
try:
    with open('/tmp/rf_defined.txt') as f:
        for line in f:
            s = line.strip()
            if s:
                defined.add(s)
except Exception:
    pass

multi = sorted({d for d in defined if ' ' in d}, key=len, reverse=True)
single = {d for d in defined if ' ' not in d}

missing = []
for path in glob.glob('tests/*.robot'):
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            s = line.rstrip()
            if not re.match(r'^ {4}[A-Z]', s):
                continue
            if s.strip().startswith('#') or s.strip().startswith('[Tags]') or s.strip().startswith('[Documentation]') or s.strip().startswith('[Teardown]') or s.strip().startswith('[Setup]'):
                continue
            body = s.strip()
            # Strip BDD prefixes (Given, When, Then, And, But)
            for pfx in ['Given ', 'When ', 'Then ', 'And ', 'But ']:
                if body.startswith(pfx):
                    body = body[len(pfx):].strip()
                    break

            matched = None
            for kw in multi:
                if body == kw or body.startswith(kw + " "):
                    matched = kw
                    break
            if matched is None:
                first = body.split()[0]
                if first in single:
                    matched = first
            if matched is None:
                missing.append((path, lineno, body[:60]))

if missing:
    print("==> Keyword dipanggil tapi tidak terdefinisi:")
    for p, ln, txt in missing:
        print(f"  {p}:{ln}: {txt}")
    sys.exit(1)
else:
    print("==> OK - Semua keyword yang dipanggil di testcase terdefinisi secara valid.")
PY
