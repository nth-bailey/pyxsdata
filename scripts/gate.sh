#!/usr/bin/env bash
# ==============================================================================
# scripts/gate.sh - Unified Quality Gate for pyxsdata
# ==============================================================================
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# Ensure virtual environment binaries take precedence in PATH
export PATH="${REPO_ROOT}/.venv/bin:${PATH}"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}==> [1/5] Running Astral ty type check...${NC}"
ty check pyxsdata

echo -e "${BLUE}==> [2/5] Running Ruff linter and formatter checks...${NC}"
ruff check pyxsdata
ruff format --check pyxsdata

echo -e "${BLUE}==> [3/5] Running Pytest with 100% statement & branch coverage...${NC}"
pytest --cov=./pyxsdata --cov-branch --cov-fail-under=100 -q

echo -e "${BLUE}==> [4/5] Building documentation with Zensical...${NC}"
zensical build > /dev/null

echo -e "${BLUE}==> [5/5] Running pre-commit hooks check...${NC}"
pre-commit run --all-files

echo -e "${GREEN}✨ All pyxsdata quality gates passed with 100% coverage!${NC}"
