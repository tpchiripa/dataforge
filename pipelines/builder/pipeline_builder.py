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
            .tag("etl")
            .tag("customers")
            .owner("data-engineering")
            .add_step(extract)
            .add_step(validate)
            .add_step(transform)
            .add_step(load)
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

    def owner(
        self,
        owner: str,
    ) -> "PipelineBuilder":

        self._config.owner = owner

        return self

    # ---------------------------------------------------------

    def tag(
        self,
        tag: str,
    ) -> "PipelineBuilder":

        if tag not in self._config.tags:
            self._config.tags.append(tag)

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

    def add_steps(
        self,
        *steps: PipelineStep,
    ) -> "PipelineBuilder":

        self._steps.extend(steps)

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
        """
        Build a Pipeline instance.

        NOTE:
        The builder intentionally does NOT validate the pipeline.
        Validation occurs immediately before execution via the
        PipelineExecutor/PipelineValidator. This allows unit tests
        and tooling to construct incomplete pipelines.
        """

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

        return len(
            self._steps,
        )

    # ---------------------------------------------------------

    @property
    def is_empty(
        self,
    ) -> bool:

        return len(
            self._steps,
        ) == 0

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineBuilder("
            f"name='{self._config.name}', "
            f"steps={self.step_count})"
        )
