# Contributing to pyxsdata

Thank you for your interest in contributing to `pyxsdata`! We welcome contributions, bug
reports, and feature proposals from the community.

---

## Code of Conduct

By participating in this project, you agree to abide by the terms of the
[Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to
[bailey.tan.nguyen@gmail.com](mailto:bailey.tan.nguyen@gmail.com).

---

## Getting Started

### Prerequisites

- **Python**: Python >= 3.12 exclusively.
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv) is recommended for fast
  virtual environment and dependency management.

### Setting Up the Development Environment

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/nth-bailey/pyxsdata.git
   cd pyxsdata
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev,pydantic,cli,lxml]"
   ```

3. Install pre-commit hooks:
   ```bash
   uv pip install pre-commit
   pre-commit install
   ```

---

## Development Workflow & Standards

### 1. Code Style & Formatting: `ruff`

All code must adhere to the Google Python Style Guide, enforced by `ruff`:

```bash
.venv/bin/ruff check pyxsdata
.venv/bin/ruff format --check pyxsdata
```

To automatically format files:

```bash
.venv/bin/ruff format pyxsdata
```

### 2. Static Type Checking: Astral `ty`

Static typing is enforced using Astral's `ty`. All code in `pyxsdata/` must pass with
zero diagnostics:

```bash
.venv/bin/ty check pyxsdata
```

_(Note: `mypy` is not used in this repository)._

### 3. Testing & Coverage: `pytest`

`pyxsdata` maintains **100% statement and branch test coverage** (`fail_under = 100`):

```bash
PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --cov=./pyxsdata --cov-report=term-missing:skip-covered
```

To run doctests in documentation:

```bash
PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --doctest-glob="docs/*.md"
```

### 4. Documentation: `zensical`

Documentation is built using [Zensical](https://zensical.org):

```bash
.venv/bin/zensical build
```

---

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) to enable automated
semantic releases:

- `feat:` A new feature (triggers a minor version bump).
- `fix:` A bug fix (triggers a patch version bump).
- `docs:` Documentation changes.
- `refactor:` Code refactoring with no behavior changes.
- `perf:` Performance improvements.
- `test:` Adding or updating tests.
- `chore:` Maintenance, dependencies, build configs.

Example:

```bash
git commit -m "feat(pydantic): map XSD restrictions to native Pydantic v2 constraints"
```

---

## Submitting a Pull Request

1. Create a new topic branch:
   ```bash
   git checkout -b my-feature-name
   ```
2. Make your changes with appropriate tests and documentation.
3. Verify that all checks pass locally:
   - Linting: `.venv/bin/ruff check pyxsdata`
   - Formatting: `.venv/bin/ruff format --check pyxsdata`
   - Type checking: `.venv/bin/ty check pyxsdata`
   - Test suite: `pytest --cov=./pyxsdata` (100% coverage required)
4. Push your branch and open a Pull Request against the `main` branch.
