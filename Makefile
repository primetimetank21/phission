UV ?= uv

# Keep downloaded tooling and disposable framework state inside the project.
export UV_CACHE_DIR := $(CURDIR)/.cache/uv
export REFLEX_DIR := $(CURDIR)/.cache/reflex
export XDG_CACHE_HOME := $(CURDIR)/.cache
export BUN_INSTALL_CACHE_DIR := $(CURDIR)/.cache/bun
export NPM_CONFIG_CACHE := $(CURDIR)/.cache/npm
export REFLEX_TELEMETRY_ENABLED := false
export REFLEX_USE_NPM := false
export REFLEX_USE_SYSTEM_BUN := false

.PHONY: setup run test lint format check build frontend-tooling

setup:
	$(UV) sync --frozen
	$(UV) run --frozen --no-sync python scripts/frontend.py setup

# Do not let Reflex silently fall back to npm and replace the Bun lock.
frontend-tooling:
	@test -x "$(REFLEX_DIR)/bun/bin/bun" || { echo "Run make setup to install project-local Bun."; exit 1; }

# Production mode serves the UI and Python backend together on loopback port 3000.
run: frontend-tooling
	$(UV) run --frozen --no-sync reflex run --env prod --backend-host 127.0.0.1

test:
	$(UV) run --frozen --no-sync pytest

lint:
	$(UV) run --frozen --no-sync ruff check .
	$(UV) run --frozen --no-sync ruff format --check .

format:
	$(UV) run --frozen --no-sync ruff format .

check: lint test

# Produces .web/build/client; the interactive app still needs the Python backend.
build: frontend-tooling
	$(UV) run --frozen --no-sync python scripts/frontend.py build
