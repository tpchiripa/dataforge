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


class PipelineExecutor:
    """
    Executes DataForge pipelines.
    """

    def __init__(self):

        pass

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

        start = datetime.utcnow()

        context.started_at = start

        context.set_status(
            PipelineStatus.RUNNING,
        )

        try:

            for step in pipeline.steps:

                step.run(context)

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.COMPLETED,
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

        except Exception:

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.FAILED,
            )

            # NOTE:
            # The failing PipelineStep has already recorded the
            # exception via PipelineStep.on_error().
            #
            # We therefore DO NOT add the same error again here,
            # otherwise the PipelineResult would contain duplicate
            # error messages.

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
