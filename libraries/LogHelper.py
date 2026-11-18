"""
LogHelper.py - Anti-Truncation & Transparent Payload Logging for Robot Framework 5.0.1+
Complies with Global QA SDET & RF Constitution:
- Chunk size 4000 characters to prevent log message truncation in RF 5.0.1
- Pretty-printed JSON snapshots (indent=2)
- Transparent PASS and FAIL comparison logging (Expected vs Actual field-by-field)
- Strict Deep Compare: Automatically computes differences between Expected and Actual payloads.
"""
import json
import re
from robot.api import logger

CHUNK_SIZE = 4000
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]+")

def mask_sensitive(text: str) -> str:
    """Masks JWT tokens to protect credentials in automation logs."""
    if not isinstance(text, str):
        text = str(text)
    return JWT_PATTERN.sub(lambda m: m.group(0)[:10] + "...[REDACTED_JWT_TOKEN]", text)

def _format_content(content):
    if isinstance(content, (dict, list)):
        raw = json.dumps(content, indent=2, ensure_ascii=False, default=str)
    else:
        raw = str(content)
    return mask_sensitive(raw)

def _log_chunked(title, content, chunk_size=CHUNK_SIZE):
    """
    Emits chunked log messages into Robot Framework log.html.
    Prevents truncation in RF 5.0.1 without relying on --maxlogmessage.
    """
    text = _format_content(content)
    total_len = len(text)
    total_parts = max(1, (total_len + chunk_size - 1) // chunk_size)

    logger.info(f"--- START {title} | Length={total_len} chars | Parts={total_parts} ---")
    if total_len <= chunk_size:
        logger.info(text)
    else:
        for idx in range(total_parts):
            start = idx * chunk_size
            end = start + chunk_size
            logger.info(f"[{title} | PART {idx + 1}/{total_parts}]\n{text[start:end]}")
    logger.info(f"--- END {title} ---")

def deep_compare(expected, actual, path=""):
    """
    Recursively compares expected vs actual values (dicts, lists, scalars).
    Handles numeric equality between int and float (tolerance 1e-4).
    Returns a list of human-readable mismatch strings.
    """
    mismatches = []
    current_path = path if path else "root"

    # None check
    if (expected is None) != (actual is None):
        mismatches.append("At '" + current_path + "': expected " + str(expected) + ", got " + str(actual))
        return mismatches
    if expected is None and actual is None:
        return mismatches

    # Boolean check (must precede int/float because bool is subclass of int)
    if isinstance(expected, bool) or isinstance(actual, bool):
        if type(expected) is not type(actual) or expected != actual:
            mismatches.append("At '" + current_path + "': expected boolean " + str(expected) + ", got " + str(actual))
        return mismatches

    # Numeric equivalence check
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if abs(float(expected) - float(actual)) > 1e-4:
            mismatches.append("At '" + current_path + "': expected numeric " + str(expected) + ", got " + str(actual))
        return mismatches

    # Dict comparison
    if isinstance(expected, dict) and isinstance(actual, dict):
        all_keys = sorted(set(expected.keys()) | set(actual.keys()))
        for k in all_keys:
            subpath = (current_path + "." + str(k)) if path else str(k)
            if k not in expected:
                mismatches.append("At '" + subpath + "': unexpected extra key in actual payload (value: " + str(actual[k]) + ")")
            elif k not in actual:
                mismatches.append("At '" + subpath + "': expected key missing from actual payload (expected: " + str(expected[k]) + ")")
            else:
                mismatches.extend(deep_compare(expected[k], actual[k], subpath))
        return mismatches

    # List comparison
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            mismatches.append("At '" + current_path + "': array length mismatch. Expected " + str(len(expected)) + " items, got " + str(len(actual)) + " items.")
        min_len = min(len(expected), len(actual))
        for i in range(min_len):
            subpath = current_path + "[" + str(i) + "]"
            mismatches.extend(deep_compare(expected[i], actual[i], subpath))
        return mismatches

    # String & other scalar comparison
    if str(expected).strip() != str(actual).strip():
        mismatches.append("At '" + current_path + "': expected '" + str(expected) + "', got '" + str(actual) + "'")
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
