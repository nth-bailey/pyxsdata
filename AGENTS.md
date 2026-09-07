# AGENTS.md

Instructions and guidelines for AI coding assistants working in the `pyxsdata`
repository.

---

## 1. Project Overview

`pyxsdata` is a modern, high-performance data binding library and code generator for
Python 3.12+ that allows developers to access and use XML and JSON documents as simple
Python objects (standard `dataclasses` or `pydantic` models) rather than dealing
directly with the DOM.

- **Origin**: Modernized successor to `xsdata`, consolidating ecosystem plugins (notably
  `xsdata-pydantic`) into a unified core.
- **Repository**: `nth-bailey/pyxsdata`
- **Supported Python**: `Python >= 3.12` exclusively.

---

## 2. Core Architectural Decisions & Invariants

When contributing or refactoring, strictly maintain the following invariants:

1. **Strict `pyxsdata` CLI (Zero Backwards Compatibility)**:
   - The CLI command is strictly `pyxsdata`.
   - **Do NOT** add `xsdata` aliases, backward compatibility shims, or deprecated
     command fallback.
   - All internal code, tests, docs, and configurations must use the `pyxsdata`
     namespace.

2. **Native Pydantic v2 Support (`pyxsdata.pydantic`)**:
   - The former `xsdata-pydantic` package is consolidated directly into
     `pyxsdata.pydantic`.
   - It is an official, built-in feature, enabled with the `pydantic` extra:
     `pip install "pyxsdata[pydantic]"`.
   - Code generation supports `--output pydantic`.
   - Pre-configured parsers and serializers live in `pyxsdata.pydantic.bindings`
     (`XmlParser`, `XmlSerializer`, etc.).
   - **Do NOT** refer to or add dependencies on external `xsdata-pydantic`.

3. **Modern Python 3.12+ Standards**:
   - Take full advantage of modern Python features: PEP 695 generics
     (`class Foo[T]: ...`), structural pattern matching, `X | Y` union syntax, and
     `kw_only` dataclasses.
   - Do not write code or fallbacks targeting Python 3.11 or older.

---

## 3. Tooling & Development Workflow

### Python Environment

- The virtual environment is located at `.venv/`.
- Virtual environment binaries are at `.venv/bin/`.
- When running commands that spawn subprocesses or expect tools in PATH (e.g. `ruff`,
  `pyxsdata`), make sure `.venv/bin` is in `PATH`:
  ```bash
  PATH="$PWD/.venv/bin:$PATH"
  ```
- Fast package management uses `uv` (`/home/xenah/.local/bin/uv`).

### Static Type Checking: Astral `ty`

- **Static Type Checker**: Astral's `ty` is used across `pyxsdata/`.
- **Mypy is NOT used**: Do not reintroduce `mypy` or `mypy_cache`.
- **Validation Command**:
  ```bash
  .venv/bin/ty check pyxsdata
  ```
  All code in `pyxsdata/` must pass with zero diagnostics: **"All checks passed!"**.
- Type configuration is maintained in `ty.toml`.

### Linting & Formatting: `ruff`

- Configuration is in `ruff.toml` (`target-version = "py312"`), enforcing Google Python
  style guide conventions.
- Note: Subdirectory `pyxsdata/formats/dataclass/ruff.toml` exists for
  dataclass-specific overrides.
- **Commands**:
  ```bash
  .venv/bin/ruff check pyxsdata
  .venv/bin/ruff format --check pyxsdata
  .venv/bin/ruff format pyxsdata
  ```

### Testing: `pytest`

- Full test suite:
  ```bash
  PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --cov=./pyxsdata --cov-report=term-missing:skip-covered
  ```
- Doctests in documentation:
  ```bash
  PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest --doctest-glob="docs/*.md"
  ```
- Ensure test coverage remains high (~99%).

### Documentation: `zensical`

- Documentation is powered by **Zensical** static site generator.
- Configuration is in `zensical.toml`.
- **MkDocs is NOT used**: Do not reintroduce `mkdocs.yml` or `mkdocs*` plugins.
- **Build Command**:
  ```bash
  .venv/bin/zensical build
  ```
  Generates static site into `site/` with zero errors.

### Packaging & Release

- Versioning is declared in `pyproject.toml` and in `pyxsdata/__init__.py` as
  `__version__`.
- Build command:
  ```bash
  uv build
  uv run twine check dist/*
  ```

---

## 4. Repository Structure

```
pyxsdata/
├── pyxsdata/
│   ├── cli.py                     # Click CLI implementation
│   ├── __main__.py                # Main entry point (pyxsdata script)
│   ├── codegen/                   # Schema parsers, AST, mappers, handlers, code writer
│   ├── formats/                   # Dataclass serialization, parsing, handlers, transports
│   ├── models/                    # XSD, WSDL, DTD, and Generator configuration models
│   ├── pydantic/                  # Consolidated Pydantic v2 support
│   │   ├── bindings.py            # Drop-in XmlParser/XmlSerializer for Pydantic
│   │   ├── compat.py              # Pydantic v2 model inspection & ClassType adapter
│   │   ├── fields.py              # Pydantic Field constraint mapping
│   │   └── generator.py           # Pydantic code generation backend
│   └── utils/                     # Namespaces, text, dates, hooks, click helpers
├── tests/
│   ├── codegen/                   # Codegen unit tests
│   ├── formats/                   # Formats & dataclass tests
│   ├── integration/               # End-to-end integration tests & benchmarks
│   ├── models/                    # Model unit tests
│   └── pydantic/                  # Pydantic v2 bindings, compat, and codegen tests
├── docs/                          # Documentation markdown files
├── .github/workflows/             # GitHub Actions CI, test, and docs deploy workflows
├── zensical.toml                  # Zensical SSG configuration
├── ruff.toml                      # Ruff linter and formatter configuration (Google style)
├── ty.toml                        # Astral ty type checker configuration
└── pyproject.toml                 # Dependencies and project packaging metadata
```

---

## 5. Agent Etiquette & Verification Checklist

Before finishing any task:

1. **Linting**: Ensure `.venv/bin/ruff check pyxsdata` passes with 0 errors.
2. **Formatting**: Ensure `.venv/bin/ruff format --check pyxsdata` passes.
3. **Type Checking**: Ensure `.venv/bin/ty check pyxsdata` passes with "All checks
   passed!".
4. **Tests**: Ensure `PATH="$PWD/.venv/bin:$PATH" .venv/bin/pytest` passes without
   regressions.
5. **Docs**: If docs are touched, verify `.venv/bin/zensical build` succeeds.
6. **No Stale Artifacts**: Clean up temporary test directories (`generated/`, scratch
   files).
