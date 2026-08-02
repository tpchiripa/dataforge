"""
DataForge Plugin Manager

Responsible for discovering, loading,
initializing and shutting down plugins.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer

from pipelines.plugins.plugin import Plugin
from pipelines.plugins.plugin_registry import PluginRegistry


class PluginManager:
    """
    Manages the lifecycle of DataForge plugins.
    """

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self._container = container

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load(
        self,
        plugin: Plugin,
    ) -> None:
        """
        Load a plugin.
        """

        if not plugin.enabled:

            return

        plugin.initialize(
            self._container,
        )

        PluginRegistry.register(
            plugin,
        )

    # ---------------------------------------------------------

    def load_many(
        self,
        *plugins: Plugin,
    ) -> None:
        """
        Load multiple plugins.
        """

        for plugin in plugins:

            self.load(
                plugin,
            )

    # ---------------------------------------------------------
    # Unloading
    # ---------------------------------------------------------

    def unload(
        self,
        plugin_name: str,
    ) -> None:
        """
        Unload a plugin.
        """

        plugin = PluginRegistry.get(
            plugin_name,
        )

        plugin.shutdown()

        PluginRegistry.unregister(
            plugin_name,
        )

    # ---------------------------------------------------------

    def shutdown_all(
        self,
    ) -> None:
        """
        Shutdown every loaded plugin.
        """

        for plugin in PluginRegistry.plugins():

            plugin.shutdown()

        PluginRegistry.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        plugin_name: str,
    ) -> Plugin:

        return PluginRegistry.get(
            plugin_name,
        )

    # ---------------------------------------------------------

    def exists(
        self,
        plugin_name: str,
    ) -> bool:

        return PluginRegistry.exists(
            plugin_name,
        )

    # ---------------------------------------------------------

    @property
    def plugin_count(
        self,
    ) -> int:

        return PluginRegistry.count()

    # ---------------------------------------------------------

    @property
    def container(
        self,
    ) -> ServiceContainer:

        return self._container

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PluginManager("
            f"plugins={self.plugin_count})"
        )
