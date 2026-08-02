"""
DataForge Pipeline Executor

Responsible for executing DataForge pipelines.
"""

from __future__ import annotations

from datetime import datetime

from pipelines.container.service_container import ServiceContainer
from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus
from pipelines.lifecycle.lifecycle_manager import LifecycleManager
from pipelines.plugins.plugin_manager import PluginManager


class PipelineExecutor:
    """
    Executes DataForge pipelines.
    """

    def __init__(
        self,
        lifecycle: LifecycleManager | None = None,
        plugins: PluginManager | None = None,
    ) -> None:
        """
        Create a PipelineExecutor.

        Dependencies may be injected by the runtime.
        If omitted, sensible defaults are created for testing.
        """

        self.lifecycle = lifecycle or LifecycleManager()

        self.plugins = plugins or PluginManager(
            ServiceContainer(),
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def execute(
        self,
        pipeline: Pipeline,
    ) -> PipelineResult:
        """
        Execute a pipeline.
        """

        self._validate_pipeline(
            pipeline,
        )

        context = self._create_context(
            pipeline,
        )

        start = datetime.utcnow()

        context.started_at = start

        context.set_status(
            PipelineStatus.RUNNING,
        )

        self.lifecycle.before_pipeline(
            context,
        )

        try:

            for step in pipeline.steps:

                self.lifecycle.before_step(
                    step,
                    context,
                )

                try:

                    step.run(
                        context,
                    )

                    self.lifecycle.after_step(
                        step,
                        context,
                    )

                except Exception as ex:

                    self.lifecycle.on_step_error(
                        step,
                        context,
                        ex,
                    )

                    raise

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.COMPLETED,
            )

            self.lifecycle.after_pipeline(
                context,
            )

            duration = (
                context.finished_at - start
            ).total_seconds()

            return PipelineResult(
                success=True,
                status=context.status,
                pipeline_name=pipeline.config.name,
                message="Pipeline completed successfully.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metadata=context.metadata,
                warnings=context.warnings,
            )

        except Exception as ex:

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.FAILED,
            )

            self.lifecycle.on_pipeline_error(
                context,
                ex,
            )

            duration = (
                context.finished_at - start
            ).total_seconds()

            return PipelineResult(
                success=False,
                status=context.status,
                pipeline_name=pipeline.config.name,
                message="Pipeline execution failed.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metadata=context.metadata,
                errors=context.errors,
                warnings=context.warnings,
            )

    # ---------------------------------------------------------

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown executor plugins.
        """

        self.plugins.shutdown_all()

    # ---------------------------------------------------------

    def _validate_pipeline(
        self,
        pipeline: Pipeline,
    ) -> None:

        pipeline.validate()

    # ---------------------------------------------------------

    def _create_context(
        self,
        pipeline: Pipeline,
    ) -> PipelineContext:

        return PipelineContext(
            config=pipeline.config,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineExecutor("
            f"plugins={self.plugins.plugin_count})"
        )
