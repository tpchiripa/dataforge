"""
DataForge Pipeline Module
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer

from pipelines.core.pipeline import Pipeline
from pipelines.validation.pipeline_validator import PipelineValidator

from pipelines.executor.pipeline_executor import PipelineExecutor

from pipelines.registry.pipeline_registry import PipelineRegistry

from pipelines.modules.module import Module


class PipelineModule(Module):
    """
    Registers all pipeline-related services.
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            "Pipeline",
        )

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    def register_services(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register pipeline services.
        """

        container.register_singleton(
            PipelineRegistry,
        )

        container.register_singleton(
            PipelineValidator,
        )

        container.register_singleton(
            PipelineExecutor,
        )

        container.register_transient(
            Pipeline,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Initialize pipeline services.
        """

        #
        # Force singleton creation during startup.
        #

        container.resolve(
            PipelineRegistry,
        )

        container.resolve(
            PipelineValidator,
        )

        container.resolve(
            PipelineExecutor,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Shutdown pipeline subsystem.
        """

        return

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}')"
        )
