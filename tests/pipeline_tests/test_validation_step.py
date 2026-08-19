"""
DataForge Validation Step Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pandas as pd
import pytest

from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.validate.validation_step import ValidationStep
from storage.lakehouse.layer import MedallionLayer


# =========================================================
# Fixtures
# =========================================================


@pytest.fixture
def context():

    context = PipelineContext(
        config=PipelineConfig(name="test_pipeline"),
    )

    context.data = pd.DataFrame(
        {"id": [1, 2, 3], "name": ["a", "b", "c"]}
    )

    context.result = MagicMock(records_read=0)

    return context


# =========================================================
# Execution — without lakehouse
# =========================================================


def test_execute_passes_valid_dataframe(context):

    step = ValidationStep()

    step.execute(context)

    assert context.metadata["validation_passed"] is True

    assert context.metadata["records_validated"] == 3


def test_execute_raises_on_missing_data(context):

    context.data = None

    step = ValidationStep()

    with pytest.raises(PipelineValidationError):

        step.execute(context)


def test_execute_raises_on_non_dataframe(context):

    context.data = {"not": "a dataframe"}

    step = ValidationStep()

    with pytest.raises(PipelineValidationError):

        step.execute(context)


def test_execute_raises_on_empty_dataframe(context):

    context.data = pd.DataFrame()

    step = ValidationStep()

    with pytest.raises(PipelineValidationError):

        step.execute(context)


def test_execute_warns_on_missing_values(context):

    context.data = pd.DataFrame(
        {"id": [1, None, 3], "name": ["a", "b", "c"]}
    )

    step = ValidationStep()

    step.execute(context)

    assert any(
        "missing values" in warning
        for warning in context.warnings
    )


# =========================================================
# Execution — with lakehouse (Silver landing)
# =========================================================


def test_execute_writes_to_silver_when_lakehouse_provided(context):

    lakehouse = MagicMock()

    lakehouse.write_bytes.return_value = MagicMock(
        key="pipeline/Validation/2026/08/19/exec123.csv"
    )

    step = ValidationStep(
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )

    step.execute(context)

    lakehouse.write_bytes.assert_called_once()

    call_kwargs = lakehouse.write_bytes.call_args.kwargs

    assert call_kwargs["layer"] == MedallionLayer.SILVER

    assert call_kwargs["source"] == "postgres_orders"

    assert call_kwargs["table"] == "orders"

    assert "silver_key" in context.metadata


def test_execute_skips_silver_when_lakehouse_not_provided(context):

    step = ValidationStep()

    step.execute(context)

    assert "silver_key" not in context.metadata


def test_execute_does_not_write_to_silver_on_validation_failure(context):

    context.data = pd.DataFrame()

    lakehouse = MagicMock()

    step = ValidationStep(lakehouse=lakehouse)

    with pytest.raises(PipelineValidationError):

        step.execute(context)

    lakehouse.write_bytes.assert_not_called()