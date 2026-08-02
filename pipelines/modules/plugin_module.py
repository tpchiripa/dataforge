"""
DataForge Plugin Module

Registers and initializes the DataForge plugin system.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer

from pipelines.discovery.plugin_discovery import PluginDiscovery

from pipelines.modules.module import Module

from pipelines.plugins.plugin_manager import PluginManager


class PluginModule(Module):
    """
    DataForge Plugin Module.

    Responsible for:

    - Registering the PluginManager
    - Discovering plugins
    - Loading plugins
    - Shutting plugins down
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            "Plugins",
        )

        #
        # Plugin discovery engine.
        #

        self._discovery = PluginDiscovery()

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    def register(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register plugin services.
        """

        #
        # Constructor injection will automatically inject
        # the ServiceContainer.
        #

        container.register_singleton(
            PluginManager,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Discover and load every available plugin.
        """

        manager = container.resolve(
            PluginManager,
        )

        self._discovery.discover(
            manager,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Shutdown every loaded plugin.
        """

        manager = container.resolve(
            PluginManager,
        )

        manager.shutdown_all()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def discovery(
        self,
    ) -> PluginDiscovery:
        """
        Plugin discovery engine.
        """

        return self._discovery

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}')"
        )
