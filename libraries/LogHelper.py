"""
Helper logging terstandarisasi untuk Robot Framework 5.0.1+.
Complies with Global QA SDET & RF Constitution:
- Chunk size 4000 characters to prevent log message truncation in RF 5.0.1
- Pretty-printed JSON snapshots (indent=2)
- Transparent PASS and FAIL comparison logging (Expected vs Actual field-by-field)
- Strict Deep Compare: Automatically computes differences between Expected and Actual payloads
  with strict type checking (int vs str vs bool vs float).
"""
import json
import re
from robot.api import logger

CHUNK_SIZE = 4000
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]+")

def mask_sensitive(text: str) -> str:
    """Masks JWT tokens to protect credentials in automation logs."""
    if not isinstance(text, str):
        return text
    return JWT_PATTERN.sub("[MASKED_JWT_TOKEN]", text)

def _log_chunked(title, content, chunk_size=CHUNK_SIZE):
    """
    Logs large payloads, HTTP responses, and database queries in chunks
    to avoid truncation in Robot Framework 5.0.1.
    """
    if isinstance(content, (dict, list)):
        content_str = json.dumps(content, indent=2, ensure_ascii=False)
    else:
        content_str = str(content)

    content_str = mask_sensitive(content_str)

    if len(content_str) <= chunk_size:
        logger.info(f"--- START {title} | Length={len(content_str)} chars ---")
        logger.info(content_str)
        logger.info(f"--- END {title} ---")
        return

    parts = [content_str[i:i+chunk_size] for i in range(0, len(content_str), chunk_size)]
    logger.info(f"--- START {title} | Length={len(content_str)} chars | Parts={len(parts)} ---")
    for idx, part in enumerate(parts, 1):
        logger.info(f"[{title} | PART {idx}/{len(parts)}]\n" + str(part))
    logger.info(f"--- END {title} ---")

def deep_compare(expected, actual, path=""):
    """
    Recursively compares expected vs actual values (dicts, lists, scalars).
    Enforces STRICT type differentiation:
    - (None vs non-None): Mismatch
    - (bool vs int/str): Mismatch (bool strictly checked before int)
    - (int vs str): Mismatch (never treats "12843" as equal to 12843)
    - (int vs float): Equivalent numeric comparison (tolerance 1e-4)
    - (str vs str): String comparison with whitespace stripping
    - (dict vs non-dict, list vs non-list): Mismatch
    Returns a list of human-readable mismatch strings.
    """
    mismatches = []
    current_path = path if path else "root"

    # None check
    if (expected is None) != (actual is None):
        mismatches.append(f"At '{current_path}': expected {expected}, got {actual}")
        return mismatches
    if expected is None and actual is None:
        return mismatches

    # Boolean check (must precede int/float because in Python bool is subclass of int)
    if isinstance(expected, bool) or isinstance(actual, bool):
        if type(expected) is not type(actual) or expected != actual:
            mismatches.append(f"At '{current_path}': expected boolean {expected}, got {type(actual).__name__} ({actual})")
        return mismatches

    # Numeric equivalence check (int and float allowed, but NOT str or other types)
    is_exp_num = isinstance(expected, (int, float))
    is_act_num = isinstance(actual, (int, float))
    if is_exp_num != is_act_num:
        mismatches.append(f"At '{current_path}': type mismatch. Expected {type(expected).__name__} ({expected}), got {type(actual).__name__} ({actual})")
        return mismatches

    if is_exp_num and is_act_num:
        if abs(float(expected) - float(actual)) > 1e-4:
            mismatches.append(f"At '{current_path}': expected numeric {expected}, got {actual}")
        return mismatches

    # Dict comparison
    if isinstance(expected, dict) or isinstance(actual, dict):
        if type(expected) is not type(actual):
            mismatches.append(f"At '{current_path}': type mismatch. Expected {type(expected).__name__}, got {type(actual).__name__}")
            return mismatches
        all_keys = sorted(set(expected.keys()) | set(actual.keys()))
        for k in all_keys:
            subpath = f"{current_path}.{k}" if path else str(k)
            if k not in expected:
                mismatches.append(f"At '{subpath}': unexpected extra key in actual payload (value: {actual[k]})")
            elif k not in actual:
                mismatches.append(f"At '{subpath}': expected key missing from actual payload (expected: {expected[k]})")
            else:
                mismatches.extend(deep_compare(expected[k], actual[k], subpath))
        return mismatches

    # List comparison
    if isinstance(expected, list) or isinstance(actual, list):
        if type(expected) is not type(actual):
            mismatches.append(f"At '{current_path}': type mismatch. Expected {type(expected).__name__}, got {type(actual).__name__}")
            return mismatches
        if len(expected) != len(actual):
            mismatches.append(f"At '{current_path}': array length mismatch. Expected {len(expected)} items, got {len(actual)} items.")
        min_len = min(len(expected), len(actual))
        for i in range(min_len):
            subpath = f"{current_path}[{i}]"
            mismatches.extend(deep_compare(expected[i], actual[i], subpath))
        return mismatches

    # String & other scalar comparison
    if type(expected) is not type(actual):
        mismatches.append(f"At '{current_path}': type mismatch. Expected {type(expected).__name__} ({expected}), got {type(actual).__name__} ({actual})")
        return mismatches

    if str(expected).strip() != str(actual).strip():
        mismatches.append(f"At '{current_path}': expected '{expected}', got '{actual}'")
    return mismatches

def log_transparent_comparison(title, expected, actual, mismatches=None, raise_on_mismatch=False):
    """
    Logs full snapshots of Expected and Actual payloads plus field-by-field verification.
    Automatically computes deep_compare(expected, actual) if mismatches is None.
    MANDATORY: Must be logged for BOTH PASS and FAIL outcomes to ensure auditable logs.
    """
    if mismatches is None:
        mismatches = deep_compare(expected, actual)

    logger.info("================================================================================")
    logger.info(" TRANSPARENT PAYLOAD AUDIT: " + str(title))
    logger.info("================================================================================")
    _log_chunked("[EXPECTED PAYLOAD] " + str(title), expected)
    _log_chunked("[ACTUAL PAYLOAD] " + str(title), actual)

    if mismatches:
        logger.error("--- [COMPARISON RESULT: " + str(title) + "] FAIL - " + str(len(mismatches)) + " MISMATCH(ES) FOUND ---")
        for idx, diff in enumerate(mismatches, 1):
            logger.error("  [" + str(idx) + "] " + str(diff))
        if raise_on_mismatch:
            raise AssertionError("Audit komparasi gagal (" + str(title) + "): " + str(mismatches[0]))
    else:
        logger.info("--- [COMPARISON RESULT: " + str(title) + "] PASS - 100% MATCH (All fields identical) ---")
    logger.info("================================================================================")
    return mismatches
