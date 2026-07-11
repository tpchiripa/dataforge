"""
DataForge Pipeline Builder

Fluent builder for constructing pipelines.
"""

from __future__ import annotations

from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_step import PipelineStep


class PipelineBuilder:
    """
    Fluent builder for DataForge pipelines.

    Example
    -------
    pipeline = (
        PipelineBuilder(config)
        .add_step(step1)
        .add_step(step2)
        .build()
    )
    """

    def __init__(self, config: PipelineConfig):

        self.pipeline = Pipeline(config)

    # ---------------------------------------------------------

    def add_step(
        self,
        step: PipelineStep,
    ) -> "PipelineBuilder":
        """
        Add a pipeline step.
        """

        self.pipeline.add_step(step)

        return self

    # ---------------------------------------------------------

    def remove_step(
        self,
        step_name: str,
    ) -> "PipelineBuilder":
        """
        Remove a pipeline step.
        """

        self.pipeline.remove_step(step_name)

        return self

    # ---------------------------------------------------------

    def clear(self) -> "PipelineBuilder":
        """
        Remove every step.
        """

        self.pipeline.clear_steps()

        return self

    # ---------------------------------------------------------

    def build(self) -> Pipeline:
        """
        Return the finished pipeline.
        """

        return self.pipeline
