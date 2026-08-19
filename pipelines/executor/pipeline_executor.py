"""
DataForge Pipeline Executor

Responsible for executing DataForge pipelines.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer
from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus
from pipelines.execution.execution_timer import ExecutionTimer
from pipelines.lifecycle.lifecycle_manager import LifecycleManager
from pipelines.plugins.plugin_manager import PluginManager


class PipelineExecutor:
    """
    Executes DataForge pipelines.

    The executor is responsible for:

    - Pipeline validation
    - Pipeline lifecycle management
    - Step execution
    - Step execution metrics
    - Execution timing
    - Pipeline finalization
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

        self.lifecycle = (
            lifecycle
            or LifecycleManager()
        )

        self.plugins = (
            plugins
            or PluginManager(
                ServiceContainer(),
            )
        )

    # =========================================================
    # Public API
    # =========================================================

    def execute(
        self,
        pipeline: Pipeline,
    ) -> PipelineResult:
        """
        Execute a pipeline.
        """

        # -----------------------------------------------------
        # Validate pipeline
        # -----------------------------------------------------

        self._validate_pipeline(
            pipeline,
        )

        # -----------------------------------------------------
        # Create execution context
        # -----------------------------------------------------

        context = self._create_context(
            pipeline,
        )

        # -----------------------------------------------------
        # Create execution timer
        # -----------------------------------------------------

        timer = ExecutionTimer()

        # -----------------------------------------------------
        # Initialize execution
        # -----------------------------------------------------

        timer.start()

        context.started_at = timer._started

        context.set_status(
            PipelineStatus.RUNNING,
        )

        # -----------------------------------------------------
        # Initialize step metrics
        # -----------------------------------------------------

        context.start_metrics(
            len(pipeline.steps),
        )

        # -----------------------------------------------------
        # Pipeline lifecycle
        # -----------------------------------------------------

        self.lifecycle.before_pipeline(
            context,
        )

        try:

            # =================================================
            # Execute Pipeline Steps
            # =================================================

            for step in pipeline.steps:

                self.lifecycle.before_step(
                    step,
                    context,
                )

                try:

                    # -----------------------------------------
                    # Execute step
                    # -----------------------------------------

                    step.run(
                        context,
                    )

                    # -----------------------------------------
                    # Record successful step
                    # -----------------------------------------

                    context.step_completed()

                    # -----------------------------------------
                    # Step lifecycle
                    # -----------------------------------------

                    self.lifecycle.after_step(
                        step,
                        context,
                    )

                except Exception as exc:

                    # -----------------------------------------
                    # Record failed step
                    # -----------------------------------------

                    context.step_failed()

                    # -----------------------------------------
                    # Step lifecycle error
                    # -----------------------------------------

                    self.lifecycle.on_step_error(
                        step,
                        context,
                        exc,
                    )

                    raise

            # =================================================
            # Pipeline Completed
            # =================================================

            timer.stop()

            context.finished_at = timer._finished

            context.metrics.duration_seconds = (
                timer.duration
            )

            context.set_status(
                PipelineStatus.COMPLETED,
            )

            self.lifecycle.after_pipeline(
                context,
            )

            return context.finalize(
                success=True,
                message=(
                    "Pipeline completed successfully."
                ),
            )

        # =====================================================
        # Pipeline Failed
        # =====================================================

        except Exception as exc:

            timer.stop()

            context.finished_at = timer._finished

            context.metrics.duration_seconds = (
                timer.duration
            )

            context.set_status(
                PipelineStatus.FAILED,
            )

            self.lifecycle.on_pipeline_error(
                context,
                exc,
            )

            return context.finalize(
                success=False,
                message=(
                    "Pipeline execution failed."
                ),
            )

    # =========================================================
    # Shutdown
    # =========================================================

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown executor plugins.
        """

        self.plugins.shutdown_all()

    # =========================================================
    # Validation
    # =========================================================

    def _validate_pipeline(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Validate the pipeline before execution.
        """

        pipeline.validate()

    # =========================================================
    # Context Creation
    # =========================================================

    def _create_context(
        self,
        pipeline: Pipeline,
    ) -> PipelineContext:
        """
        Create a runtime execution context.
        """

        return PipelineContext(
            config=pipeline.config,
        )

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineExecutor("
            f"plugins={self.plugins.plugin_count})"
        )
