"""
DataForge Metrics Plugin

Registers the MetricsHook with the DataForge lifecycle.
"""

from __future__ import annotations

from pipelines.hooks.metrics_hook import MetricsHook
from pipelines.lifecycle.lifecycle_manager import LifecycleManager
from pipelines.plugins.plugin import Plugin


class MetricsPlugin(Plugin):
    """
    Plugin responsible for collecting execution metrics.

    During initialization the plugin registers the
    MetricsHook with the LifecycleManager.
    """

    name = "Metrics"

    version = "1.0.0"

    # ---------------------------------------------------------

    def __init__(
        self,
        lifecycle: LifecycleManager,
    ) -> None:

        self.lifecycle = lifecycle

        self.hook = MetricsHook()

    # ---------------------------------------------------------

    def initialize(
        self,
    ) -> None:
        """
        Register the metrics hook.
        """

        self.lifecycle.register_hook(
            self.hook,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
    ) -> None:
        """
        Remove the metrics hook.
        """

        self.lifecycle.unregister_hook(
            self.hook,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"MetricsPlugin("
            f"name='{self.name}', "
            f"version='{self.version}')"
        )
