"""Run Reflex tooling without hiding dependency drift or dirtying Git for whitespace.

Reflex init writes compact package.json; Bun writes indented package.json. Preserve
our committed formatting only after proving decoded metadata AND lock bytes match.
Unexpected dependency edits remain on disk for diagnosis and cause a failure.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_locked(command: list[str], root: Path) -> int:
    manifest = root / "reflex.lock" / "package.json"
    lock = root / "reflex.lock" / "bun.lock"
    before_manifest = manifest.read_bytes()
    before_data = json.dumps(json.loads(before_manifest), sort_keys=True, allow_nan=False)
    before_lock = lock.read_bytes()
    result = subprocess.run(command, cwd=root, check=False)
    if result.returncode:
        return result.returncode
    try:
        after_data = json.dumps(json.loads(manifest.read_bytes()), sort_keys=True, allow_nan=False)
        unchanged = (
            lock.read_bytes() == before_lock
            and after_data == before_data
            and not (root / "reflex.lock" / "package-lock.json").exists()
        )
    except (OSError, ValueError):
        unchanged = False
    if not unchanged:
        print(
            "Frontend dependency metadata or Bun lock changed; inspect the diff.", file=sys.stderr
        )
        return 1
    if manifest.read_bytes() != before_manifest:
        manifest.write_bytes(before_manifest)
        print("Restored manifest formatting; dependency metadata and Bun lock are unchanged.")
    return 0


def main() -> int:
    commands = {
        "setup": ["reflex", "init", "--name", "phission", "--no-agents"],
        "build": ["reflex", "export", "--frontend-only", "--no-zip"],
    }
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print("Usage: python scripts/frontend.py <setup|build>", file=sys.stderr)
        return 2
    return run_locked(commands[sys.argv[1]], Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    raise SystemExit(main())
