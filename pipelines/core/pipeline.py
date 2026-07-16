"""
DataForge Pipeline

Core pipeline implementation.
"""

from __future__ import annotations

from .exceptions import PipelineValidationError
from .pipeline_config import PipelineConfig
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

    def clear_steps(
        self,
    ) -> None:
        """
        Remove every pipeline step.
        """

        self.steps.clear()

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
    ) -> None:
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

    def execute(self):
        """
        Execute the pipeline.

        Delegates execution to PipelineExecutor.
        """

        from pipelines.executor.pipeline_executor import PipelineExecutor

        executor = PipelineExecutor()

        return executor.execute(
            self,
        )

    # ---------------------------------------------------------

    @property
    def step_count(
        self,
    ) -> int:
        """
        Return the number of pipeline steps.
        """

        return len(
            self.steps,
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.steps,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"Pipeline("
            f"name='{self.config.name}', "
            f"steps={len(self.steps)})"
        )
