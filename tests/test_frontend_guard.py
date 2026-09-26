"""The formatting fix must never turn dependency drift into a passing check."""

import json
import sys

import pytest

from scripts.frontend import run_locked


@pytest.fixture
def frontend(tmp_path):
    directory = tmp_path / "reflex.lock"
    directory.mkdir()
    manifest = directory / "package.json"
    manifest.write_text('{\n  "dependencies": {"example": "1.0.0"}\n}\n')
    (directory / "bun.lock").write_bytes(b"original lock bytes")
    return tmp_path, manifest, manifest.read_bytes()


def run(root, script):
    return run_locked([sys.executable, "-c", script], root)


def test_only_whitespace_is_restored(frontend):
    root, manifest, before = frontend
    result = run(
        root,
        "from pathlib import Path; import json; p=Path('reflex.lock/package.json'); "
        "p.write_text(json.dumps(json.loads(p.read_bytes())))",
    )
    assert result == 0
    assert manifest.read_bytes() == before


@pytest.mark.parametrize(
    "change",
    [
        'p.write_text(\'{"dependencies":{"example":"2.0.0"}}\')',
        "Path('reflex.lock/bun.lock').write_text('different lock')",
        "p.write_text('invalid JSON')",
        "p.unlink()",
        "Path('reflex.lock/bun.lock').unlink()",
    ],
)
def test_dependency_drift_is_rejected_without_restoring_it(frontend, change):
    root, manifest, before = frontend
    result = run(root, "from pathlib import Path; p=Path('reflex.lock/package.json'); " + change)
    assert result == 1
    if "2.0.0" in change:
        assert json.loads(manifest.read_bytes())["dependencies"]["example"] == "2.0.0"
    elif "different lock" in change:
        assert (root / "reflex.lock/bun.lock").read_text() == "different lock"
    elif "invalid JSON" in change:
        assert manifest.read_text() == "invalid JSON"
    elif change == "p.unlink()":
        assert not manifest.exists()
    else:
        assert not (root / "reflex.lock/bun.lock").exists()


def test_failed_tool_exit_is_preserved(frontend):
    root, _, _ = frontend
    assert run(root, "raise SystemExit(7)") == 7
