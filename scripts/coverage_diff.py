#!/usr/bin/env python3
"""Coverage Diff Inspector.

Runs pytest with coverage or inspects the existing .coverage database to identify
and display exclusively the missing statements and missing branch transitions with
file line snippets.
"""

from __future__ import annotations

import argparse
import linecache
import os
import subprocess
import sys
from pathlib import Path

# Ensure .venv/bin is in PATH
venv_bin = str(Path(__file__).resolve().parent.parent / ".venv" / "bin")
if venv_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{venv_bin}:{os.environ.get('PATH', '')}"

from coverage import Coverage


def run_pytest(test_args: list[str]) -> int:
    """Run pytest with coverage instrumentation."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=./pyxsdata",
        "--cov-branch",
        *test_args,
    ]
    print(f"==> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def inspect_coverage(data_file: Path | None = None) -> int:
    """Inspect coverage data and report only unhit lines and branches."""
    cov = Coverage(data_file=str(data_file) if data_file else None)
    cov.load()

    total_missing = 0
    repo_root = Path(__file__).resolve().parent.parent

    print("\n" + "=" * 80)
    print("Zero-Fluff Coverage Diff Inspector")
    print("=" * 80)

    for filename in sorted(cov.get_data().measured_files()):
        rel_path = Path(filename).resolve()
        try:
            rel_str = str(rel_path.relative_to(repo_root))
        except ValueError:
            continue

        if not rel_str.startswith("pyxsdata/"):
            continue

        analysis = cov._analyze(filename)
        missing_statements = sorted(analysis.missing)
        missing_branches = sorted(analysis.missing_branch_arcs())

        if not missing_statements and not missing_branches:
            continue

        total_missing += len(missing_statements) + len(missing_branches)
        num_statements = len(analysis.statements)
        covered_statements = num_statements - len(missing_statements)
        pct = (covered_statements / num_statements * 100) if num_statements else 100.0

        print(f"\n📄 \033[1;31m{rel_str}\033[0m ({pct:.1f}% covered)")

        if missing_statements:
            print("  ❌ Missing Statements:")
            for line_no in missing_statements:
                line_content = linecache.getline(filename, line_no).rstrip()
                print(f"     Line {line_no:4d}: {line_content}")

        if missing_branches:
            print("  🔀 Missing Branch Transitions:")
            for src, dst in missing_branches:
                line_content = linecache.getline(filename, src).rstrip()
                dst_label = "exit" if dst < 0 else str(dst)
                print(f"     Line {src} -> {dst_label}: {line_content}")

    print("\n" + "=" * 80)
    if total_missing == 0:
        print("✅ 100.00% statement and branch coverage achieved across all files!")
        return 0
    else:
        print(f"❌ Total unhit items: {total_missing}")
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect missing coverage lines and branches.")
    parser.add_argument(
        "--no-run",
        action="store_true",
        help="Do not run pytest; inspect existing .coverage file directly.",
    )
    parser.add_argument(
        "pytest_args",
        nargs="*",
        help="Optional arguments passed to pytest (e.g. tests/pydantic/).",
    )

    args = parser.parse_args()

    if not args.no_run:
        test_args = args.pytest_args or ["-q"]
        run_pytest(test_args)

    sys.exit(inspect_coverage())


if __name__ == "__main__":
    main()
