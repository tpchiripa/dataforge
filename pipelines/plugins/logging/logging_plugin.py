"""
DataForge Logging Plugin
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer
from pipelines.lifecycle.lifecycle_manager import LifecycleManager
from pipelines.plugins.plugin import Plugin

from pipelines.hooks.logging_hook import LoggingHook


class LoggingPlugin(Plugin):
    """
    Registers the LoggingHook with the pipeline lifecycle.
    """

    name = "Logging"

    version = "1.0.0"

    description = "Pipeline execution logging."

    author = "DataForge"

    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Install the logging hook.
        """

        lifecycle = container.resolve(
            LifecycleManager,
        )

        lifecycle.add_hook(
            LoggingHook(),
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown hook.

        Nothing to clean up.
        """

        return
