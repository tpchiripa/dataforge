"""
DataForge Pipeline

Core pipeline implementation.
"""

from __future__ import annotations

from collections.abc import Iterator

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
    ) -> "Pipeline":
        """
        Add a pipeline step.
        """

        self.steps.append(step)

        return self

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

    def get_step(
        self,
        step_name: str,
    ) -> PipelineStep | None:
        """
        Retrieve a pipeline step.
        """

        for step in self.steps:

            if step.name == step_name:

                return step

        return None

    def has_step(
        self,
        step_name: str,
    ) -> bool:
        """
        Return True if the pipeline contains a step.
        """

        return self.get_step(step_name) is not None

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

        if not self.config.name.strip():

            raise PipelineValidationError(
                "Pipeline name cannot be empty."
            )

        if not self.steps:

            raise PipelineValidationError(
                "Pipeline contains no steps."
            )

        names: set[str] = set()

        for step in self.steps:

            if not step.enabled:

                raise PipelineValidationError(
                    f"Pipeline step '{step.name}' is disabled."
                )

            key = step.name.lower()

            if key in names:

                raise PipelineValidationError(
                    f"Duplicate pipeline step '{step.name}'."
                )

            names.add(key)

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
    ):
        """
        Execute the pipeline.
        """

        from pipelines.executor.pipeline_executor import (
            PipelineExecutor,
        )

        return PipelineExecutor().execute(
            self,
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def step_count(
        self,
    ) -> int:

        return len(
            self.steps,
        )

    @property
    def is_empty(
        self,
    ) -> bool:

        return len(
            self.steps,
        ) == 0

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[PipelineStep]:

        return iter(
            self.steps,
        )

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
            f"steps={self.step_count})"
        )
