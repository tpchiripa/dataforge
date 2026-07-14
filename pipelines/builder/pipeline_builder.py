"""
DataForge Pipeline Builder

Provides a fluent interface for constructing DataForge pipelines.
"""

from __future__ import annotations

from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_step import PipelineStep


class PipelineBuilder:
    """
    Fluent builder for constructing DataForge pipelines.

    Example
    -------
    pipeline = (
        PipelineBuilder("Customer ETL")
            .description("Loads customer records")
            .version("1.0.0")
            .add_step(step1)
            .add_step(step2)
            .build()
    )
    """

    def __init__(
        self,
        name: str,
    ):

        self._config = PipelineConfig(
            name=name,
        )

        self._steps: list[PipelineStep] = []

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def description(
        self,
        description: str,
    ) -> "PipelineBuilder":

        self._config.description = description

        return self

    # ---------------------------------------------------------

    def version(
        self,
        version: str,
    ) -> "PipelineBuilder":

        self._config.version = version

        return self

    # ---------------------------------------------------------

    def enabled(
        self,
        enabled: bool = True,
    ) -> "PipelineBuilder":

        self._config.enabled = enabled

        return self

    # ---------------------------------------------------------
    # Steps
    # ---------------------------------------------------------

    def add_step(
        self,
        step: PipelineStep,
    ) -> "PipelineBuilder":

        self._steps.append(step)

        return self

    # ---------------------------------------------------------

    def clear_steps(
        self,
    ) -> "PipelineBuilder":

        self._steps.clear()

        return self

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(
        self,
    ) -> Pipeline:

        pipeline = Pipeline(
            config=self._config,
        )

        for step in self._steps:

            pipeline.add_step(step)

        return pipeline

    # ---------------------------------------------------------

    def reset(
        self,
    ) -> "PipelineBuilder":

        name = self._config.name

        self._config = PipelineConfig(
            name=name,
        )

        self._steps.clear()

        return self

    # ---------------------------------------------------------

    @property
    def step_count(
        self,
    ) -> int:

        return len(self._steps)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineBuilder("
            f"name='{self._config.name}', "
            f"steps={len(self._steps)})"
        )
