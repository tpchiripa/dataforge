"""
DataForge Load Step Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pandas as pd
import pytest

from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.load.load_step import LoadStep
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

    return context


# =========================================================
# Execution — without lakehouse
# =========================================================


def test_execute_writes_csv(context, tmp_path):

    output_path = tmp_path / "orders.csv"

    step = LoadStep(
        name="load_orders",
        output_path=output_path,
    )

    step.execute(context)

    assert output_path.exists()

    assert context.metadata["records_loaded"] == 3

    assert context.metadata["output_format"] == "csv"


def test_execute_raises_on_missing_data(context, tmp_path):

    context.data = None

    step = LoadStep(
        name="load_orders",
        output_path=tmp_path / "orders.csv",
    )

    with pytest.raises(ValueError):

        step.execute(context)


def test_execute_raises_on_unsupported_format(context, tmp_path):

    step = LoadStep(
        name="load_orders",
        output_path=tmp_path / "orders.txt",
        file_format="txt",
    )

    with pytest.raises(ValueError):

        step.execute(context)


# =========================================================
# Execution — with lakehouse (Gold landing)
# =========================================================


def test_execute_writes_to_gold_when_lakehouse_provided(context, tmp_path):

    output_path = tmp_path / "orders.csv"

    lakehouse = MagicMock()

    lakehouse.write_bytes.return_value = MagicMock(
        key="pipeline/load_orders/2026/08/19/orders.csv"
    )

    step = LoadStep(
        name="load_orders",
        output_path=output_path,
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )

    step.execute(context)

    lakehouse.write_bytes.assert_called_once()

    call_kwargs = lakehouse.write_bytes.call_args.kwargs

    assert call_kwargs["layer"] == MedallionLayer.GOLD

    assert call_kwargs["source"] == "postgres_orders"

    assert call_kwargs["table"] == "orders"

    assert call_kwargs["filename"] == "orders.csv"

    assert "gold_key" in context.metadata


def test_execute_gold_bytes_match_local_file(context, tmp_path):

    output_path = tmp_path / "orders.csv"

    lakehouse = MagicMock()

    step = LoadStep(
        name="load_orders",
        output_path=output_path,
        lakehouse=lakehouse,
    )

    step.execute(context)

    written_bytes = lakehouse.write_bytes.call_args.kwargs["data"]

    assert written_bytes == output_path.read_bytes()


def test_execute_skips_gold_when_lakehouse_not_provided(context, tmp_path):

    step = LoadStep(
        name="load_orders",
        output_path=tmp_path / "orders.csv",
    )

    step.execute(context)

    assert "gold_key" not in context.metadata