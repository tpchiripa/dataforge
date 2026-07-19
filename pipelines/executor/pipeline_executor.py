"""
DataForge Pipeline Executor

Responsible for executing DataForge pipelines.
"""

from __future__ import annotations

from datetime import datetime

from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus

from pipelines.execution import (
    ExecutionEvents,
    ExecutionLogger,
    ExecutionMetrics,
    ExecutionTimer,
)


class PipelineExecutor:
    """
    Executes DataForge pipelines.
    """

    def __init__(self):

        self.logger = ExecutionLogger()

        self.events = ExecutionEvents()

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

        self._validate_pipeline(pipeline)

        context = self._create_context(
            pipeline,
        )

        timer = ExecutionTimer()

        timer.start()

        metrics = ExecutionMetrics()

        metrics.steps_total = len(
            pipeline.steps,
        )

        start = datetime.utcnow()

        context.started_at = start

        context.set_status(
            PipelineStatus.RUNNING,
        )

        self.logger.info(
            f"Starting pipeline "
            f"'{pipeline.config.name}' "
            f"({context.execution_id})"
        )

        self.events.pipeline_started(
            pipeline.config.name,
        )

        try:

            for step in pipeline.steps:

                self.logger.info(
                    f"Executing step: "
                    f"{step.__class__.__name__}"
                )

                self.events.step_started(
                    step.__class__.__name__,
                )

                step.run(context)

                metrics.steps_completed += 1

                self.events.step_completed(
                    step.__class__.__name__,
                )

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.COMPLETED,
            )

            timer.stop()

            metrics.duration_seconds = timer.duration

            duration = (
                context.finished_at - start
            ).total_seconds()

            self.logger.info(
                f"Pipeline "
                f"'{pipeline.config.name}' "
                f"completed successfully."
            )

            self.events.pipeline_completed(
                pipeline.config.name,
            )

            return PipelineResult(
                success=True,
                status=context.status,
                pipeline_name=pipeline.config.name,
                execution_id=context.execution_id,
                message="Pipeline completed successfully.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metrics=metrics,
                metadata=context.metadata,
                warnings=context.warnings,
            )

        except Exception:

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.FAILED,
            )

            timer.stop()

            metrics.duration_seconds = timer.duration

            metrics.steps_failed += 1

            self.logger.error(
                f"Pipeline "
                f"'{pipeline.config.name}' "
                f"failed."
            )

            self.events.pipeline_failed(
                pipeline.config.name,
            )

            duration = (
                context.finished_at - start
            ).total_seconds()

            return PipelineResult(
                success=False,
                status=context.status,
                pipeline_name=pipeline.config.name,
                execution_id=context.execution_id,
                message="Pipeline execution failed.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metrics=metrics,
                metadata=context.metadata,
                errors=context.errors,
                warnings=context.warnings,
            )

    # ---------------------------------------------------------

    def _validate_pipeline(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Validate a pipeline before execution.
        """

        pipeline.validate()

    # ---------------------------------------------------------

    def _create_context(
        self,
        pipeline: Pipeline,
    ) -> PipelineContext:
        """
        Create a fresh execution context.
        """

        return PipelineContext(
            config=pipeline.config,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return "PipelineExecutor()"
