"""
DataForge Monitoring Module

Registers monitoring and observability services.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer
from pipelines.modules.module import Module
from pipelines.monitoring.pipeline_monitor import PipelineMonitor


class MonitoringModule(Module):
    """
    Monitoring subsystem.

    Responsible for registering monitoring and
    observability services.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Monitoring",
        )

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    def register_services(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register monitoring services.
        """

        container.register_singleton(
            PipelineMonitor,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Initialize monitoring services.
        """

        #
        # Force singleton creation during startup.
        #

        container.resolve(
            PipelineMonitor,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Shutdown monitoring services.

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
