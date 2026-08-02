"""
DataForge Module

Base class for all DataForge modules.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pipelines.container.service_container import ServiceContainer


class Module(ABC):
    """
    Base class for every DataForge module.

    Every DataForge subsystem (Pipelines, Plugins,
    Events, Monitoring, Connectors, Storage, Runtime, etc.)
    derives from this class.

    Modules are responsible for registering their services
    into the dependency injection container and optionally
    participating in application startup and shutdown.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self._name = name

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    @abstractmethod
    def register_services(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register every service owned by this module.
        """

        raise NotImplementedError

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Optional startup hook.

        Called after every module has registered its services.
        """

        return

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Optional shutdown hook.

        Override to release resources.
        """

        return

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Module name.
        """

        return self._name

    # ---------------------------------------------------------

    @property
    def id(
        self,
    ) -> str:
        """
        Unique module identifier.
        """

        return self.name.lower()

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}')"
        )
