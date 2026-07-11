"""
DataForge Pipeline

Core pipeline implementation.
"""

from __future__ import annotations

from datetime import datetime

from .exceptions import (
    PipelineExecutionError,
    PipelineValidationError,
)
from .pipeline_config import PipelineConfig
from .pipeline_context import PipelineContext
from .pipeline_result import PipelineResult
from .pipeline_status import PipelineStatus
from .pipeline_step import PipelineStep


class Pipeline:
    """
    Represents an executable DataForge pipeline.
    """

    def __init__(
        self,
        config: PipelineConfig,
    ):

        self.config = config

        self.steps: list[PipelineStep] = []

    # ---------------------------------------------------------
    # Steps
    # ---------------------------------------------------------

    def add_step(
        self,
        step: PipelineStep,
    ) -> None:
        """
        Add a pipeline step.
        """

        self.steps.append(step)

    def remove_step(
        self,
        step_name: str,
    ) -> None:
        """
        Remove a pipeline step by name.
        """

        self.steps = [
            step
            for step in self.steps
            if step.name != step_name
        ]

    def clear_steps(self) -> None:
        """
        Remove every pipeline step.
        """

        self.steps.clear()

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate pipeline before execution.
        """

        if not self.config.enabled:
            raise PipelineValidationError(
                "Pipeline is disabled."
            )

        if not self.steps:
            raise PipelineValidationError(
                "Pipeline contains no steps."
            )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(self) -> PipelineResult:
        """
        Execute the pipeline.
        """

        self.validate()

        context = PipelineContext(
            config=self.config,
        )

        start = datetime.utcnow()

        context.started_at = start

        context.set_status(
            PipelineStatus.RUNNING
        )

        try:

            for step in self.steps:

                step.run(context)

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.COMPLETED
            )

            duration = (
                context.finished_at - start
            ).total_seconds()

            return PipelineResult(
                success=True,
                status=context.status,
                pipeline_name=self.config.name,
                message="Pipeline completed successfully.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metadata=context.metadata,
                warnings=context.warnings,
            )

        except Exception as exc:

            context.finished_at = datetime.utcnow()

            context.set_status(
                PipelineStatus.FAILED
            )

            duration = (
                context.finished_at - start
            ).total_seconds()

            context.add_error(str(exc))

            return PipelineResult(
                success=False,
                status=context.status,
                pipeline_name=self.config.name,
                message="Pipeline execution failed.",
                started_at=start,
                finished_at=context.finished_at,
                duration_seconds=duration,
                metadata=context.metadata,
                errors=context.errors,
                warnings=context.warnings,
            )

    # ---------------------------------------------------------

    @property
    def step_count(self) -> int:
        """
        Return the number of pipeline steps.
        """

        return len(self.steps)

    # ---------------------------------------------------------

    def __len__(self) -> int:

        return len(self.steps)

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Pipeline("
            f"name='{self.config.name}', "
            f"steps={len(self.steps)})"
        )
