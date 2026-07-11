"""
DataForge BaseStep Tests
"""

from __future__ import annotations

from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class DummyStep(BaseStep):
    """
    Concrete implementation used for testing BaseStep.
    """

    def __init__(self):

        super().__init__(
            name="Dummy Step",
            description="Testing BaseStep",
        )

    def execute(self, context: PipelineContext):

        context.add_metadata(
            "executed",
            True,
        )


# ---------------------------------------------------------
# Test Helpers
# ---------------------------------------------------------


def create_context() -> PipelineContext:
    """
    Create a valid PipelineContext for testing.
    """

    return PipelineContext(
        config=PipelineConfig(
            name="Test Pipeline",
        )
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_base_step_initialization():

    step = DummyStep()

    assert step.name == "Dummy Step"

    assert step.description == "Testing BaseStep"

    assert step.enabled is True


def test_enable_disable():

    step = DummyStep()

    step.disable()

    assert step.enabled is False

    step.enable()

    assert step.enabled is True


def test_step_type():

    step = DummyStep()

    assert step.step_type == "dummy"


def test_before_execute():

    context = create_context()

    step = DummyStep()

    step.before_execute(context)

    assert step.started_at is not None

    assert (
        "Dummy Step.started_at"
        in context.metadata
    )


def test_after_execute():

    context = create_context()

    step = DummyStep()

    step.before_execute(context)

    step.after_execute(context)

    assert step.finished_at is not None

    assert (
        "Dummy Step.finished_at"
        in context.metadata
    )


def test_duration():

    context = create_context()

    step = DummyStep()

    step.before_execute(context)

    step.after_execute(context)

    assert step.duration_seconds >= 0


def test_run_executes_step():

    context = create_context()

    step = DummyStep()

    step.run(context)

    assert context.metadata["executed"] is True


def test_repr():

    step = DummyStep()

    representation = repr(step)

    assert "DummyStep" in representation

    assert "Dummy Step" in representation
