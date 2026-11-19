#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Mutation Testing & Assertion Sensitivity Verification Suite.
Proves that the Robot Framework suite strictly FAILS (exit code 1)
when values, types, or contracts are intentionally inverted/mutated.
Zero False Positive Protocol Compliant.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LIB_FILE = BASE_DIR / "libraries" / "TokenMonitoringLibrary.py"
RESULTS_DIR = BASE_DIR / "results"
REPORT_FILE = RESULTS_DIR / "mutation_audit_report.json"

def run_rf_test(test_pattern: str) -> Tuple[int, str]:
    res = subprocess.run(
        [
            sys.executable, "-m", "robot",
            "--pythonpath", "libraries",
            "--maxassignlength", "0",
            "--outputdir", "results/mutation_runs",
            "-t", test_pattern,
            "tests"
        ],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True
    )
    return res.returncode, res.stdout + res.stderr

def run_mutation_tests():
    print("========================================================================")
    print(" STARTING AUTOMATED MUTATION TESTING (PROVEN SENSITIVITY)")
    print(f" Target Library: {LIB_FILE}")
    print("========================================================================")

    with open(LIB_FILE, "r", encoding="utf-8") as f:
        orig_code = f.read()

    results = []

    try:
        # ----------------------------------------------------------------------
        # Mutation 1: TC-011 Numeric Inversion (60.56 -> 999.0 / floored 999)
        # ----------------------------------------------------------------------
        print("\n[MUTATION 1] TC-011: Numeric Inversion (Daily Token 60 -> 999)...")
        mutated_code_1 = orig_code.replace(
            "expected_floored = int(raw_usage / TOKEN_FIXED_PRICE)",
            "expected_floored = 999  # INJECTED MUTATION"
        )
        assert mutated_code_1 != orig_code, "Failed to inject Mutation 1!"
        with open(LIB_FILE, "w", encoding="utf-8") as f:
            f.write(mutated_code_1)

        code1, out1 = run_rf_test("TC-011*")
        has_failed_1 = (code1 != 0) and ("FAIL" in out1 or "AssertionError" in out1)
        print(f"  Result: ReturnCode={code1}, Sensitivity Proven={has_failed_1}")
        assert has_failed_1, "MUTATION 1 FAILED: Test should have failed but passed!"
        results.append({
            "mutation_id": "MUT-001",
            "target": "TC-011 Daily Tooltip Tokens",
            "injected": "expected_floored = 999 (was 60)",
            "expected_outcome": "FAIL (AssertionError)",
            "actual_return_code": code1,
            "passed_sensitivity_check": has_failed_1
        })

        # ----------------------------------------------------------------------
        # Mutation 2: TC-001 Type Mismatch (int 12 -> str "12")
        # ----------------------------------------------------------------------
        print("\n[MUTATION 2] TC-001: Strict Type Mismatch (int 12 -> str '12')...")
        mutated_code_2 = orig_code.replace(
            '"history_window_months": 12,',
            '"history_window_months": "12",  # INJECTED TYPE MUTATION'
        )
        assert mutated_code_2 != orig_code, "Failed to inject Mutation 2!"
        with open(LIB_FILE, "w", encoding="utf-8") as f:
            f.write(mutated_code_2)

        code2, out2 = run_rf_test("TC-001*")
        has_failed_2 = (code2 != 0) and ("type mismatch" in out2.lower() or "fail" in out2.lower())
        print(f"  Result: ReturnCode={code2}, Sensitivity Proven={has_failed_2}")
        assert has_failed_2, "MUTATION 2 FAILED: Test should have failed on type mismatch!"
        results.append({
            "mutation_id": "MUT-002",
            "target": "TC-001 Strict Type Check deep_compare",
            "injected": 'history_window_months: "12" (str) vs 12 (int)',
            "expected_outcome": "FAIL (Type Mismatch)",
            "actual_return_code": code2,
            "passed_sensitivity_check": has_failed_2
        })

        # ----------------------------------------------------------------------
        # Mutation 3: TC-012 Empty State Reason Mutation
        # ----------------------------------------------------------------------
        print("\n[MUTATION 3] TC-012: Empty State Reason Mutation...")
        mutated_code_3 = orig_code.replace(
            '"api_empty_reason": "NO_TRANSACTIONS_IN_SELECTED_MONTH",',
            '"api_empty_reason": "INVALID_EMPTY_REASON",  # INJECTED MUTATION'
        )
        assert mutated_code_3 != orig_code, "Failed to inject Mutation 3!"
        with open(LIB_FILE, "w", encoding="utf-8") as f:
            f.write(mutated_code_3)

        code3, out3 = run_rf_test("TC-012*")
        has_failed_3 = (code3 != 0) and ("FAIL" in out3 or "AssertionError" in out3)
        print(f"  Result: ReturnCode={code3}, Sensitivity Proven={has_failed_3}")
        assert has_failed_3, "MUTATION 3 FAILED: Test should have failed but passed!"
        results.append({
            "mutation_id": "MUT-003",
            "target": "TC-012 Empty State Reason Contract",
            "injected": 'api_empty_reason: "INVALID_EMPTY_REASON"',
            "expected_outcome": "FAIL (AssertionError)",
            "actual_return_code": code3,
            "passed_sensitivity_check": has_failed_3
        })

    finally:
        # Always restore original library file
        with open(LIB_FILE, "w", encoding="utf-8") as f:
            f.write(orig_code)
        print("\nOriginal TokenMonitoringLibrary.py restored cleanly.")

    # Save report
    os.makedirs(RESULTS_DIR, exist_ok=True)
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_mutations": len(results),
        "all_sensitivity_proven": all(r["passed_sensitivity_check"] for r in results),
        "results": results
    }
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print("========================================================================")
    print(f" MUTATION TESTING COMPLETE: {len(results)}/{len(results)} SENSITIVITY CHECKS PROVEN")
    print(f" Report saved: {REPORT_FILE}")
    print("========================================================================")

if __name__ == "__main__":
    from typing import Tuple
    run_mutation_tests()
