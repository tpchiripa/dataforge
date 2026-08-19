"""
DataForge PipelineExecutor Tests
"""

from __future__ import annotations

from pipelines.builder.pipeline_builder import PipelineBuilder
from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus
from pipelines.executor.pipeline_executor import PipelineExecutor
from pipelines.steps.base.base_step import BaseStep


# ---------------------------------------------------------
# Dummy Steps
# ---------------------------------------------------------


class DummyStep(BaseStep):
    """
    Simple successful pipeline step used for testing.
    """

    def __init__(
        self,
        name: str = "Dummy Step",
    ) -> None:
        super().__init__(
            name=name,
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        context.add_metadata(
            "executed",
            True,
        )


class FailingStep(BaseStep):
    """
    Pipeline step that deliberately fails.
    """

    def __init__(
        self,
        name: str = "Failing Step",
    ) -> None:
        super().__init__(
            name=name,
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        raise RuntimeError(
            "Boom!"
        )


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def build_pipeline():
    """
    Build a simple pipeline containing one successful step.
    """

    builder = PipelineBuilder(
        "Test Pipeline",
    )

    builder.add_step(
        DummyStep(),
    )

    return builder.build()


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_executor_initialization():
    executor = PipelineExecutor()

    assert executor is not None


def test_create_context():
    executor = PipelineExecutor()

    pipeline = build_pipeline()

    context = executor._create_context(
        pipeline,
    )

    assert context.config == pipeline.config


def test_validate_pipeline():
    executor = PipelineExecutor()

    pipeline = build_pipeline()

    executor._validate_pipeline(
        pipeline,
    )


def test_execute_returns_result():
    executor = PipelineExecutor()

    pipeline = build_pipeline()

    result = executor.execute(
        pipeline,
    )

    assert isinstance(
        result,
        PipelineResult,
    )


def test_execute_success():
    executor = PipelineExecutor()

    pipeline = build_pipeline()

    result = executor.execute(
        pipeline,
    )

    assert result.success is True

    assert (
        result.status
        == PipelineStatus.COMPLETED
    )


def test_execute_records_metadata():
    executor = PipelineExecutor()

    pipeline = build_pipeline()

    result = executor.execute(
        pipeline,
    )

    assert (
        result.metadata["executed"]
        is True
    )


def test_execute_failure():
    builder = PipelineBuilder(
        "Failure Pipeline",
    )

    builder.add_step(
        FailingStep(),
    )

    pipeline = builder.build()

    executor = PipelineExecutor()

    result = executor.execute(
        pipeline,
    )

    assert result.success is False

    assert (
        result.status
        == PipelineStatus.FAILED
    )


def test_execute_collects_errors():
    builder = PipelineBuilder(
        "Failure Pipeline",
    )

    builder.add_step(
        FailingStep(),
    )

    pipeline = builder.build()

    executor = PipelineExecutor()

    result = executor.execute(
        pipeline,
    )

    assert len(result.errors) == 1

    assert "Boom!" in result.errors[0]


# ---------------------------------------------------------
# Execution Metrics
# ---------------------------------------------------------


def test_execution_metrics_track_successful_steps():
    """
    Verify that successful pipeline steps update execution metrics.
    """

    executor = PipelineExecutor()

    builder = PipelineBuilder(
        "Metrics Pipeline",
    )

    builder.add_step(
        DummyStep(
            name="Dummy Step 1",
        ),
    )

    builder.add_step(
        DummyStep(
            name="Dummy Step 2",
        ),
    )

    pipeline = builder.build()

    result = executor.execute(
        pipeline,
    )

    assert result.success is True

    assert (
        result.metrics.steps_total
        == 2
    )

    assert (
        result.metrics.steps_completed
        == 2
    )

    assert (
        result.metrics.steps_failed
        == 0
    )


def test_execution_metrics_track_failed_steps():
    """
    Verify that failed pipeline steps update execution metrics.
    """

    executor = PipelineExecutor()

    builder = PipelineBuilder(
        "Metrics Failure Pipeline",
    )

    builder.add_step(
        DummyStep(
            name="Successful Step",
        ),
    )

    builder.add_step(
        FailingStep(
            name="Failing Step",
        ),
    )

    pipeline = builder.build()

    result = executor.execute(
        pipeline,
    )

    assert result.success is False

    assert (
        result.metrics.steps_total
        == 2
    )

    assert (
        result.metrics.steps_completed
        == 1
    )

    assert (
        result.metrics.steps_failed
        == 1
    )


# ---------------------------------------------------------
# Representation
# ---------------------------------------------------------


def test_repr():
    executor = PipelineExecutor()

    representation = repr(executor)

    assert "PipelineExecutor" in representation

    assert "plugins=" in representation
