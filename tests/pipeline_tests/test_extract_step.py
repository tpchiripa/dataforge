"""
DataForge Extract Step Tests
"""
from __future__ import annotations
from unittest.mock import MagicMock
import pandas as pd
import pytest
from pipelines.core.pipeline_config import PipelineConfig
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.extract.extract_step import ExtractStep
from storage.lakehouse.layer import MedallionLayer
# =========================================================
# Fixtures
# =========================================================
@pytest.fixture
def connector():
    connector = MagicMock()
    connector.connected = False
    connector.fetch_dataframe.return_value = pd.DataFrame(
        {"id": [1, 2], "name": ["a", "b"]}
    )
    connector.get_metadata.return_value = {"name": "postgres_orders"}
    return connector
@pytest.fixture
def context():
    return PipelineContext(
        config=PipelineConfig(name="test_pipeline"),
    )
# =========================================================
# Execution — without lakehouse
# =========================================================
def test_execute_extracts_dataframe(connector, context):
    step = ExtractStep(
        name="extract_orders",
        connector=connector,
        query="SELECT * FROM orders",
    )
    step.execute(context)
    connector.connect.assert_called_once()
    assert context.data is not None
    assert len(context.data) == 2
    assert context.metadata["records_extracted"] == 2
    assert context.metadata["extract_query"] == "SELECT * FROM orders"
def test_execute_skips_connect_if_already_connected(connector, context):
    connector.connected = True
    step = ExtractStep(
        name="extract_orders",
        connector=connector,
        query="SELECT * FROM orders",
    )
    step.execute(context)
    connector.connect.assert_not_called()
# =========================================================
# Execution — with lakehouse (Bronze landing)
# =========================================================
def test_execute_writes_to_bronze_when_lakehouse_provided(connector, context):
    lakehouse = MagicMock()
    lakehouse.write_bytes.return_value = MagicMock(
        key="postgres_orders/extract_orders/2026/08/19/exec123.csv"
    )
    step = ExtractStep(
        name="extract_orders",
        connector=connector,
        query="SELECT * FROM orders",
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )
    step.execute(context)
    lakehouse.write_bytes.assert_called_once()
    call_kwargs = lakehouse.write_bytes.call_args.kwargs
    assert call_kwargs["layer"] == MedallionLayer.BRONZE
    assert call_kwargs["source"] == "postgres_orders"
    assert call_kwargs["table"] == "orders"
    assert "bronze_key" in context.metadata
def test_execute_skips_bronze_when_lakehouse_not_provided(connector, context):
    step = ExtractStep(
        name="extract_orders",
        connector=connector,
        query="SELECT * FROM orders",
    )
    step.execute(context)
    assert "bronze_key" not in context.metadata