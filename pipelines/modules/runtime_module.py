"""
DataForge Runtime Module
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer

from pipelines.validation.pipeline_validator import PipelineValidator

from pipelines.executor.pipeline_executor import PipelineExecutor

from pipelines.lifecycle.lifecycle_manager import LifecycleManager

from pipelines.modules.module import Module


class RuntimeModule(Module):
    """
    Registers the DataForge runtime services.
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            "Runtime",
        )

    # ---------------------------------------------------------
    # Service Registration
    # ---------------------------------------------------------

    def register_services(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register runtime services.
        """

        container.register_singleton(
            LifecycleManager,
        )

        container.register_singleton(
            PipelineValidator,
        )

        container.register_singleton(
            PipelineExecutor,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Initialize runtime services.
        """

        #
        # Force singleton creation during startup.
        #

        container.resolve(
            LifecycleManager,
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
        Shutdown runtime services.
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
