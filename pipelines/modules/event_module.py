"""
DataForge Event Module

Registers the DataForge event system.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer

from pipelines.events.event_bus import EventBus
from pipelines.events.event_manager import EventManager
from pipelines.modules.module import Module


class EventModule(Module):
    """
    Event subsystem.

    Responsible for registering the DataForge
    event infrastructure.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Events",
        )

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    def register_services(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register event services.
        """

        container.register_singleton(
            EventBus,
        )

        container.register_singleton(
            EventManager,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Initialize the event subsystem.
        """

        #
        # Resolve the services so they are created
        # during application startup.
        #

        container.resolve(
            EventBus,
        )

        container.resolve(
            EventManager,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Shutdown the event subsystem.

        Placeholder for future cleanup logic.
        """

        return

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )
