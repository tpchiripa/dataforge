"""
DataForge Plugin

Base class for all DataForge plugins.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pipelines.container.service_container import ServiceContainer


class Plugin(ABC):
    """
    Base class for every DataForge plugin.

    Plugins are automatically discovered by DataForge and then
    initialized by the PluginManager.

    Lifecycle

        __init__()
              ↓
        initialize(container)
              ↓
            Runtime
              ↓
          shutdown()
    """

    #
    # Plugin metadata
    #

    name: str = "Plugin"

    version: str = "1.0.0"

    enabled: bool = True

    description: str = ""

    author: str = "DataForge"

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    @abstractmethod
    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Initialize the plugin.

        Called once after the plugin has been loaded into the
        PluginManager.

        Parameters
        ----------
        container:
            DataForge service container used for dependency
            resolution.
        """

        raise NotImplementedError

    # ---------------------------------------------------------

    def shutdown(
        self,
    ) -> None:
        """
        Optional shutdown hook.

        Override if the plugin owns external resources.
        """

        return

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def id(
        self,
    ) -> str:
        """
        Unique plugin identifier.
        """

        return self.name.lower()

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        """
        Human-readable plugin name.
        """

        return self.name

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"version='{self.version}', "
            f"enabled={self.enabled})"
        )
