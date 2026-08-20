"""
DataForge Example: PostgreSQL -> Lakehouse Pipeline

End-to-end example chaining ExtractStep -> ValidationStep -> LoadStep
against real local Docker services (PostgreSQL and MinIO), proving
the full Bronze -> Silver -> Gold Medallion flow.

Usage
-----
python scripts\\postgres_to_lakehouse_pipeline.py
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from connectors.config.connector_config import ConnectorConfig
from connectors.databases.postgresql.connector import PostgreSQLConnector
from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_config import PipelineConfig
from pipelines.executor.pipeline_executor import PipelineExecutor
from pipelines.steps.extract.extract_step import ExtractStep
from pipelines.steps.load.load_step import LoadStep
from pipelines.steps.validate.validation_step import ValidationStep
from storage.lakehouse.manager import LakehouseManager
from storage.manager.storage_manager import StorageManager
from storage.minio.minio_client import MinIOClient


# =========================================================
# Environment
# =========================================================

load_dotenv()


# =========================================================
# Connector Setup
# =========================================================

postgres_config = ConnectorConfig(
    name="postgres_orders",
    host="localhost",
    port=5433,
    database=os.environ["POSTGRES_DB"],
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)

connector = PostgreSQLConnector(postgres_config)


# =========================================================
# Lakehouse Setup
# =========================================================

minio_client = MinIOClient(
    endpoint="localhost:9000",
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False,
)

storage_manager = StorageManager(minio_client)

lakehouse = LakehouseManager(storage_manager)


# =========================================================
# Pipeline Definition
# =========================================================

output_path = Path("data") / "gold" / "orders.csv"

pipeline_config = PipelineConfig(
    name="postgres_to_lakehouse_orders",
    description="Extract synthetic orders from PostgreSQL, validate, "
    "and load through the Bronze/Silver/Gold lakehouse layers.",
)

pipeline = Pipeline(pipeline_config)

pipeline.add_step(
    ExtractStep(
        name="extract_orders",
        connector=connector,
        query=(
            "SELECT * FROM (VALUES "
            "(1, 'Widget', 19.99), "
            "(2, 'Gadget', 29.99), "
            "(3, 'Gizmo', 9.99) "
            ") AS orders(id, product, price)"
        ),
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )
)

pipeline.add_step(
    ValidationStep(
        name="validate_orders",
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )
)

pipeline.add_step(
    LoadStep(
        name="load_orders",
        output_path=output_path,
        file_format="csv",
        lakehouse=lakehouse,
        source="postgres_orders",
        table="orders",
    )
)


# =========================================================
# Execution
# =========================================================

if __name__ == "__main__":

    executor = PipelineExecutor()

    result = executor.execute(pipeline)

    print(f"Success: {result.success}")
    print(f"Status: {result.status.value}")
    print(f"Records read: {result.records_read}")
    print(f"Records written: {result.records_written}")
    print(f"Duration: {result.duration_seconds:.3f}s")
    print()
    print("Bronze key:", result.metadata.get("bronze_key"))
    print("Silver key:", result.metadata.get("silver_key"))
    print("Gold key:", result.metadata.get("gold_key"))

    if result.warnings:
        print()
        print("Warnings:")
        for warning in result.warnings:
            print(" -", warning)

    if not result.success:
        print()
        print("Errors:")
        for error in result.errors:
            print(" -", error)

    connector.disconnect()