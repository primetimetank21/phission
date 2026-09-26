"""Keep the frontend package-manager choice explicit rather than falling back."""

import subprocess
from pathlib import Path

from rxconfig import config

ROOT = Path(__file__).resolve().parents[1]


def test_frontend_lock_and_config_are_bun_only():
    assert config.frozen_lockfile is True
    assert (ROOT / "reflex.lock" / "bun.lock").is_file()
    assert (ROOT / "reflex.lock" / "package.json").is_file()
    assert not (ROOT / "reflex.lock" / "package-lock.json").exists()


def test_build_preflight_fails_without_local_bun(tmp_path):
    result = subprocess.run(
        ["make", "frontend-tooling", f"REFLEX_DIR={tmp_path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode != 0
    assert "Run make setup to install project-local Bun." in result.stdout


def test_standard_commands_initialize_and_require_the_local_toolchain():
    makefile = (ROOT / "Makefile").read_text()
    assert "python scripts/frontend.py setup" in makefile
    assert "python scripts/frontend.py build" in makefile
    assert "export REFLEX_USE_NPM := false" in makefile
    assert "export REFLEX_USE_SYSTEM_BUN := false" in makefile
    assert "run: frontend-tooling" in makefile
    assert "build: frontend-tooling" in makefile
