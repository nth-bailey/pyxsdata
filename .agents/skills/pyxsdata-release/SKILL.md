---
name: pyxsdata-release
description: >-
  Use this skill when preparing, testing, or publishing a new pyxsdata release, building
  distribution packages, validating wheels with twine, or running pre-release
  verification.
---

# Pyxsdata Release Playbook

This skill outlines the strict pre-release verification, packaging, and distribution
workflow for `pyxsdata`.

## 1. Pre-Release Verification Checklist

Before publishing or tagging a release, all quality gates must pass without exceptions:

```bash
# Quick one-shot automated verification:
./scripts/gate.sh

# Or step-by-step:
# Ensure .venv/bin is in PATH
PATH="$PWD/.venv/bin:$PATH"

# 1. Static Type Checking (Astral ty - Mypy is NOT used)
.venv/bin/ty check pyxsdata

# 2. Linting and Formatting
.venv/bin/ruff check pyxsdata
.venv/bin/ruff format --check pyxsdata

# 3. Full Test Suite with 100% Statement & Branch Coverage
PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --cov=./pyxsdata --cov-branch --cov-report=term-missing:skip-covered

# 4. Documentation Doctests & Site Build
PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --doctest-glob="docs/*.md"
.venv/bin/zensical build
```

## 2. Packaging & Artifact Validation

Use `uv` to build the source distribution (`sdist`) and binary wheel (`bdist_wheel`),
then validate with `twine`:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build packages using uv
uv build

# Validate metadata and artifacts
uv run twine check dist/*
```

Verify the wheel contents:

```bash
# Inspect wheel contents
uv run python -m zipfile -l dist/pyxsdata-*.whl
```

Ensure no test scratch files (`generated/`, `.pytest_cache`, or scratch scripts) leaked
into the wheel.

## 3. Git Status & Release Conventions

- Ensure working directory is clean:
  ```bash
  git status
  ```
- Commit messages must follow Conventional Commits (`feat: ...`, `fix: ...`,
  `chore(release): ...`).
- Release tags follow semantic versioning (`v1.x.y` or `1.x.y`).
