"""
DataForge Metrics Hook

Collects execution metrics during pipeline execution.
"""

from __future__ import annotations

from datetime import datetime

from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_step import PipelineStep
from pipelines.lifecycle.pipeline_hook import PipelineHook


class MetricsHook(PipelineHook):
    """
    Collect execution metrics for pipelines.

    Metrics are stored inside PipelineContext.metadata.
    """

    # ---------------------------------------------------------
    # Pipeline Lifecycle
    # ---------------------------------------------------------

    def before_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        context.metadata["pipeline_started_at"] = datetime.utcnow()

        context.metadata["steps_executed"] = 0

        context.metadata["steps_succeeded"] = 0

        context.metadata["steps_failed"] = 0

    # ---------------------------------------------------------

    def after_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        finished = datetime.utcnow()

        context.metadata["pipeline_finished_at"] = finished

        started = context.metadata.get(
            "pipeline_started_at",
        )

        if started is not None:

            context.metadata["pipeline_duration_seconds"] = (
                finished - started
            ).total_seconds()

    # ---------------------------------------------------------

    def on_pipeline_error(
        self,
        context: PipelineContext,
        exception: Exception,
    ) -> None:

        context.metadata["pipeline_failed"] = True

    # ---------------------------------------------------------
    # Step Lifecycle
    # ---------------------------------------------------------

    def before_step(
        self,
        step: PipelineStep,
        context: PipelineContext,
    ) -> None:

        context.metadata[f"{step.name}_started_at"] = (
            datetime.utcnow()
        )

    # ---------------------------------------------------------

    def after_step(
        self,
        step: PipelineStep,
        context: PipelineContext,
    ) -> None:

        finished = datetime.utcnow()

        started = context.metadata.get(
            f"{step.name}_started_at",
        )

        if started is not None:

            context.metadata[
                f"{step.name}_duration_seconds"
            ] = (
                finished - started
            ).total_seconds()

        context.metadata["steps_executed"] += 1

        context.metadata["steps_succeeded"] += 1

    # ---------------------------------------------------------

    def on_step_error(
        self,
        step: PipelineStep,
        context: PipelineContext,
        exception: Exception,
    ) -> None:

        context.metadata["steps_executed"] += 1

        context.metadata["steps_failed"] += 1
