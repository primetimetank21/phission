"""Credential-free runtime boundaries, including a fresh application import."""

import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

from phission.demo import load_inbox

ROOT = Path(__file__).resolve().parents[1]


def test_fresh_import_and_all_demo_actions_without_network_tokens_or_legacy_clients():
    script = r"""
import builtins
import io
import os
import socket
from pathlib import Path

original_import = builtins.__import__
def guarded_import(name, *args, **kwargs):
    if name.split(".")[0] in {
        "email_lib", "phishing_lib", "tts_lib", "googleapiclient",
        "google_auth_oauthlib", "pyttsx3", "pynecone"
    }:
        raise AssertionError(f"Retired integration imported: {name}")
    return original_import(name, *args, **kwargs)
builtins.__import__ = guarded_import

def block_network(*args, **kwargs):
    raise AssertionError("Demo attempted outbound network access")
socket.socket.connect = block_network
socket.create_connection = block_network
socket.getaddrinfo = block_network

original_open = builtins.open
original_io_open = io.open
def guard_open(original):
    def opened(file, *args, **kwargs):
        if isinstance(file, (str, bytes, os.PathLike)):
            name = os.fsdecode(file).split("/")[-1].lower()
            if name.startswith(("token", "credentials", ".env")):
                raise AssertionError("Demo attempted to read private configuration")
        return original(file, *args, **kwargs)
    return opened
builtins.open = guard_open(original_open)
io.open = guard_open(original_io_open)

import reflex as rx

def block_compile(*args, **kwargs):
    raise AssertionError("App compiled at import time or during a demo action")
rx.App._compile = block_compile

from rxconfig import config
from phission.phission import app, index
from phission.state import DemoState
assert config.state_manager_mode == rx.constants.StateManagerMode.MEMORY
assert config.telemetry_enabled is False
assert config.db_url is None
assert config.redis_url is None
assert config.backend_host == "127.0.0.1"
index()
state = DemoState(_reflex_internal_init=True)
list(state.load())
for message in state.messages:
    state.select_message(message.id)
    for link in state.links:
        state.select_link(link.url)
        list(state.analyze())
        assert state.result_visible
print("Synthetic-only import and runtime verified")
"""
    env = {
        **os.environ,
        "REFLEX_DIR": str(ROOT / ".cache" / "reflex"),
        "REFLEX_TELEMETRY_ENABLED": "false",
    }
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Synthetic-only import and runtime verified" in result.stdout


def test_every_fixture_destination_uses_reserved_domains():
    for message in load_inbox():
        for link in message.links:
            host = urlsplit(link.url).hostname
            assert host.endswith((".example", ".test")) or host == "example.org"


def test_maintained_tree_has_no_retired_modules_or_sensitive_artifacts():
    for name in [
        "email_lib/__init__.py",
        "phishing_lib/__init__.py",
        "tts_lib/__init__.py",
        "pcconfig.py",
        "requirements.txt",
        "pynecone.db",
        "panas_calc.py",
        "phission_PANAS_results.xlsx",
        ".github/add_github_hooks.sh",
    ]:
        assert not (ROOT / name).exists(), name


def test_ui_does_not_create_email_navigation_or_html_injection():
    # Behavioral state tests above cover the actions. This guard also catches
    # accidentally wiring an email destination into an active browser link.
    source = (ROOT / "phission" / "phission.py").read_text()
    assert "href=link" not in source
    assert "href=State.selected_url" not in source
    assert "rx.html(" not in source
    assert "dangerouslySetInnerHTML" not in source
    assert "app.compile(" not in source
    assert '"aria-live": "polite"' in source
    assert 'type="button"' in source
    css = (ROOT / "assets" / "styles.css").read_text()
    assert "https://" not in css
    assert "@import" not in css
    assert "prefers-reduced-motion" in css
    assert ":focus-visible" in css
