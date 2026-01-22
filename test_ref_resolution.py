#!/usr/bin/env python3
"""
Test the ref resolution logic without actually cloning.

Run: ./test_ref_resolution.py
"""

import os
import subprocess
from pathlib import Path

# Test scenarios
SCENARIOS = [
    {
        "name": "1. Environment variable override",
        "env": {"PYUNDERSTAND_REF": "feature-x"},
        "branch": "main",
        "config_version": "howdy",
        "expected": "feature-x",
    },
    {
        "name": "2. Matching branch (non-main)",
        "env": {},
        "branch": "howdy",  # exists in pyunderstand
        "config_version": "v1.0.0",
        "expected": "howdy",
    },
    {
        "name": "3. Main branch falls through to config.yaml",
        "env": {},
        "branch": "main",
        "config_version": "howdy",
        "expected": "howdy",
    },
    {
        "name": "4. Non-existent branch falls through to config.yaml",
        "env": {},
        "branch": "does-not-exist-xyz",
        "config_version": "howdy",
        "expected": "howdy",
    },
    {
        "name": "5. No config.yaml uses default branch",
        "env": {},
        "branch": "main",
        "config_version": None,
        "expected": None,
    },
]


def resolve_ref_for_test(env: dict, branch: str, config_version: str | None) -> str | None:
    """Simulate ref resolution logic."""
    repo = "kaihendry/pyunderstand"

    # 1. Env override
    if ref := env.get("PYUNDERSTAND_REF"):
        return ref

    # 2. Matching branch (skip main/master)
    if branch not in ("main", "master"):
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", "--heads", f"https://github.com/{repo}.git", branch],
            capture_output=True,
        )
        if result.returncode == 0:
            return branch

    # 3. config.yaml
    if config_version:
        return config_version

    # 4. Default
    return None


def main():
    print("Testing ref resolution logic\n")
    print("=" * 60)

    passed = 0
    failed = 0

    for scenario in SCENARIOS:
        result = resolve_ref_for_test(
            scenario["env"],
            scenario["branch"],
            scenario["config_version"],
        )
        status = "PASS" if result == scenario["expected"] else "FAIL"

        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\n{scenario['name']}")
        print(f"  Branch: {scenario['branch']}")
        print(f"  Env: {scenario['env']}")
        print(f"  Config version: {scenario['config_version']}")
        print(f"  Expected: {scenario['expected']}")
        print(f"  Got: {result}")
        print(f"  [{status}]")

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
