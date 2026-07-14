"""
DataForge Pipeline Validator Tests
"""

from __future__ import annotations

import pytest

from pipelines.builder.pipeline_builder import PipelineBuilder
from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep
from pipelines.validation.pipeline_validator import PipelineValidator


# ---------------------------------------------------------
# Test Step
# ---------------------------------------------------------


class DummyStep(BaseStep):
    """
    Concrete step used for validator testing.
    """

    def __init__(
        self,
        name: str = "Dummy Step",
    ):

        super().__init__(
            name=name,
            description="Validator test step",
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> None:

        pass


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def build_pipeline():

    builder = PipelineBuilder(
        "Validation Pipeline",
    )

    builder.add_step(
        DummyStep(),
    )

    return builder.build()


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_validator_initialization():

    validator = PipelineValidator()

    assert validator is not None


def test_validate_success():

    validator = PipelineValidator()

    pipeline = build_pipeline()

    assert validator.validate(pipeline) is True


def test_is_valid_returns_true():

    validator = PipelineValidator()

    pipeline = build_pipeline()

    assert validator.is_valid(pipeline) is True


def test_validate_none_pipeline():

    validator = PipelineValidator()

    with pytest.raises(PipelineValidationError):

        validator.validate(None)


def test_pipeline_without_steps():

    validator = PipelineValidator()

    builder = PipelineBuilder(
        "Empty Pipeline",
    )

    pipeline = builder.build()

    with pytest.raises(PipelineValidationError):

        validator.validate(pipeline)


def test_duplicate_step_names():

    validator = PipelineValidator()

    builder = PipelineBuilder(
        "Duplicate Pipeline",
    )

    builder.add_step(
        DummyStep("Duplicate"),
    )

    builder.add_step(
        DummyStep("Duplicate"),
    )

    pipeline = builder.build()

    with pytest.raises(PipelineValidationError):

        validator.validate(pipeline)


def test_empty_step_name():

    validator = PipelineValidator()

    builder = PipelineBuilder(
        "Bad Pipeline",
    )

    builder.add_step(
        DummyStep(""),
    )

    pipeline = builder.build()

    with pytest.raises(PipelineValidationError):

        validator.validate(pipeline)


def test_disabled_step():

    validator = PipelineValidator()

    step = DummyStep()

    step.disable()

    builder = PipelineBuilder(
        "Disabled Step Pipeline",
    )

    builder.add_step(step)

    pipeline = builder.build()

    with pytest.raises(PipelineValidationError):

        validator.validate(pipeline)


def test_invalid_step_object():

    validator = PipelineValidator()

    builder = PipelineBuilder(
        "Invalid Step Pipeline",
    )

    pipeline = builder.build()

    pipeline.steps.append(object())

    with pytest.raises(PipelineValidationError):

        validator.validate(pipeline)


def test_is_valid_returns_false():

    validator = PipelineValidator()

    builder = PipelineBuilder(
        "Invalid Pipeline",
    )

    pipeline = builder.build()

    assert validator.is_valid(pipeline) is False


def test_repr():

    validator = PipelineValidator()

    representation = repr(validator)

    assert "PipelineValidator" in representation
