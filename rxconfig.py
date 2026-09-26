"""Local-only defaults; this release has no live integrations or persistent state."""

import reflex as rx
from reflex.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="phission",
    backend_host="127.0.0.1",
    state_manager_mode=rx.constants.StateManagerMode.MEMORY,
    telemetry_enabled=False,
    show_built_with_reflex=False,
    frozen_lockfile=True,
    disable_plugins=[SitemapPlugin],
)
