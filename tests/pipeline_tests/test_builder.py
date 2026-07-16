"""
DataForge PipelineBuilder Tests
"""

from __future__ import annotations

from pipelines.builder.pipeline_builder import PipelineBuilder
from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class DummyStep(BaseStep):
    """
    Concrete implementation used for testing PipelineBuilder.
    """

    def __init__(self):

        super().__init__(
            name="Dummy Step",
            description="Testing PipelineBuilder",
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> None:

        context.add_metadata(
            "executed",
            True,
        )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_builder_initialization():

    builder = PipelineBuilder(
        "Customer Pipeline",
    )

    assert builder.step_count == 0


def test_description():

    builder = (
        PipelineBuilder("Pipeline")
        .description("Customer ETL")
    )

    pipeline = builder.build()

    assert pipeline.config.description == "Customer ETL"


def test_version():

    builder = (
        PipelineBuilder("Pipeline")
        .version("2.0.0")
    )

    pipeline = builder.build()

    assert pipeline.config.version == "2.0.0"


def test_enabled():

    builder = (
        PipelineBuilder("Pipeline")
        .enabled(False)
    )

    pipeline = builder.build()

    assert pipeline.config.enabled is False


def test_add_step():

    builder = PipelineBuilder("Pipeline")

    builder.add_step(DummyStep())

    assert builder.step_count == 1


def test_clear_steps():

    builder = PipelineBuilder("Pipeline")

    builder.add_step(DummyStep())

    builder.add_step(DummyStep())

    builder.clear_steps()

    assert builder.step_count == 0


def test_build_pipeline():

    builder = PipelineBuilder("Pipeline")

    builder.add_step(DummyStep())

    pipeline = builder.build()

    assert isinstance(
        pipeline,
        Pipeline,
    )

    assert pipeline.step_count == 1


def test_reset():

    builder = (
        PipelineBuilder("Pipeline")
        .description("Test")
        .version("2.0.0")
    )

    builder.add_step(DummyStep())

    builder.reset()

    assert builder.step_count == 0

    pipeline = builder.build()

    assert pipeline.config.name == "Pipeline"

    assert pipeline.config.description == ""

    assert pipeline.config.version == "1.0.0"


def test_repr():

    builder = PipelineBuilder("Pipeline")

    representation = repr(builder)

    assert "PipelineBuilder" in representation

    assert "Pipeline" in representation
