#!/usr/bin/env python3
"""
Setup dependencies with smart ref resolution.

Ref resolution order:
1. PYUNDERSTAND_REF environment variable
2. Matching branch (if not main/master and exists in target repo)
3. 'version' field from config.yaml
4. Default branch
"""

import os
import subprocess
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"+ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def get_current_branch() -> str | None:
    result = run(["git", "branch", "--show-current"], check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def branch_exists_in_remote(repo: str, branch: str) -> bool:
    result = run(
        ["git", "ls-remote", "--exit-code", "--heads", f"https://github.com/{repo}.git", branch],
        check=False,
    )
    return result.returncode == 0


def read_config_version(key: str = "version") -> str | None:
    config_path = Path("config.yaml")
    if not config_path.exists():
        return None

    if yaml:
        with open(config_path) as f:
            data = yaml.safe_load(f)
            return data.get(key) if data else None
    else:
        # Fallback: simple parsing without PyYAML
        for line in config_path.read_text().splitlines():
            if line.startswith(f"{key}:"):
                return line.split(":", 1)[1].strip()
    return None


def resolve_ref(repo: str) -> str | None:
    # 1. Environment variable override
    if ref := os.environ.get("PYUNDERSTAND_REF"):
        print(f"Using env override: {ref}")
        return ref

    # 2. Matching branch (skip main/master)
    branch = get_current_branch()
    if branch and branch not in ("main", "master"):
        if branch_exists_in_remote(repo, branch):
            print(f"Using matching branch: {branch}")
            return branch

    # 3. config.yaml version
    if version := read_config_version():
        print(f"Using config.yaml version: {version}")
        return version

    # 4. Default branch
    print("Using default branch")
    return None


def clone_dependency(repo: str, path: str, ref: str | None) -> None:
    if Path(path).exists():
        print(f"Removing existing {path}")
        shutil.rmtree(path)

    cmd = ["git", "clone", "--depth", "1"]
    if ref:
        cmd.extend(["--branch", ref])
    cmd.extend([f"https://github.com/{repo}.git", path])

    run(cmd)


def main():
    repo = "kaihendry/pyunderstand"
    path = "pyunderstand"

    ref = resolve_ref(repo)
    clone_dependency(repo, path, ref)

    run(["uv", "add", "--editable", f"./{path}"])
    run(["uv", "sync"])


if __name__ == "__main__":
    main()
