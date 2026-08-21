"""
DataForge Metadata Repository Tests

Runs against the real local Postgres instance (dataforge-postgres),
same as the connector integration tests elsewhere in this suite.
"""

from __future__ import annotations

import uuid

import pytest

from configs.settings import settings
from metadata.exceptions import DatasetNotFoundError, PipelineRunNotFoundError
from metadata.identity import dataset_id, new_id, schema_fingerprint
from metadata.repository import MetadataRepository


# =========================================================
# Fixtures
# =========================================================


@pytest.fixture(scope="module")
def repository():

    repo = MetadataRepository(settings.database.psycopg_uri)

    repo.create_schema_and_tables()

    return repo


@pytest.fixture
def unique_names():
    """
    A fresh, unlikely-to-collide (source, table) pair per test,
    so tests don't interfere with each other's rows.
    """

    suffix = uuid.uuid4().hex[:8]

    return f"test_source_{suffix}", f"test_table_{suffix}"


# =========================================================
# Dataset
# =========================================================


def test_upsert_dataset_creates_row(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    assert dataset.layer == "bronze"

    assert dataset.source == source

    assert dataset.table_name == table

    assert dataset.dataset_id == dataset_id("bronze", source, table)


def test_upsert_dataset_is_idempotent(repository, unique_names):

    source, table = unique_names

    first = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    second = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    assert first.dataset_id == second.dataset_id


def test_get_dataset_raises_when_missing(repository):

    with pytest.raises(DatasetNotFoundError):

        repository.get_dataset(
            layer="bronze",
            source="does_not_exist",
            table="does_not_exist",
        )


# =========================================================
# Schema Version
# =========================================================


def test_upsert_schema_version_creates_row(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    schema_version = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns),
        columns=columns,
    )

    assert schema_version.dataset_id == dataset.dataset_id

    assert schema_version.columns == columns


def test_upsert_schema_version_deduplicates_by_fingerprint(
    repository,
    unique_names,
):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    fingerprint = schema_fingerprint(columns)

    first = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=fingerprint,
        columns=columns,
    )

    second = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=fingerprint,
        columns=columns,
    )

    assert first.schema_version_id == second.schema_version_id


def test_different_schema_creates_new_version(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns_a = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    columns_b = [
        {"name": "id", "dtype": "int64", "nullable": False},
        {"name": "name", "dtype": "object", "nullable": True},
    ]

    first = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns_a),
        columns=columns_a,
    )

    second = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns_b),
        columns=columns_b,
    )

    assert first.schema_version_id != second.schema_version_id


# =========================================================
# Pipeline Run
# =========================================================


def test_start_and_finish_pipeline_run(repository):

    run_id = new_id()

    started = repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    assert started.status == "running"

    finished = repository.finish_pipeline_run(
        pipeline_run_id=run_id,
        status="completed",
        finished_at=None,
        duration_seconds=1.23,
        success=True,
        message="ok",
        metadata_json={"records_read": 3},
    )

    assert finished.status == "completed"

    assert finished.success is True

    assert finished.duration_seconds == 1.23


def test_finish_pipeline_run_raises_when_not_started(repository):

    with pytest.raises(PipelineRunNotFoundError):

        repository.finish_pipeline_run(
            pipeline_run_id=new_id(),
            status="completed",
            finished_at=None,
            duration_seconds=1.0,
            success=True,
            message=None,
            metadata_json=None,
        )


def test_start_pipeline_run_is_idempotent(repository):

    run_id = new_id()

    first = repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    second = repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    assert first.pipeline_run_id == second.pipeline_run_id


def test_get_pipeline_run_raises_when_missing(repository):

    with pytest.raises(PipelineRunNotFoundError):

        repository.get_pipeline_run(new_id())


# =========================================================
# Step Run
# =========================================================


def test_record_step_run(repository):

    run_id = new_id()

    repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    step_run = repository.record_step_run(
        pipeline_run_id=run_id,
        step_name="extract_orders",
        step_type="extract",
        status="completed",
        records_in=None,
        records_out=3,
        records_rejected=None,
        started_at=None,
        finished_at=None,
    )

    assert step_run.step_name == "extract_orders"

    assert step_run.records_out == 3


# =========================================================
# Dataset Version
# =========================================================


def test_upsert_dataset_version_creates_row(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    schema_version = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns),
        columns=columns,
    )

    run_id = new_id()

    repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    step_run = repository.record_step_run(
        pipeline_run_id=run_id,
        step_name="extract",
        step_type="extract",
        status="completed",
        records_in=None,
        records_out=3,
        records_rejected=None,
        started_at=None,
        finished_at=None,
    )

    version = repository.upsert_dataset_version(
        dataset_id=dataset.dataset_id,
        schema_version_id=schema_version.schema_version_id,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/exec1.csv",
        etag="abc123",
        size_bytes=100,
        row_count=3,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    assert version.storage_key == f"{source}/{table}/exec1.csv"

    latest = repository.get_latest_version(dataset.dataset_id)

    assert latest.dataset_version_id == version.dataset_version_id


def test_upsert_dataset_version_is_idempotent(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns = [{"name": "id", "dtype": "int64", "nullable": False}]

    schema_version = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns),
        columns=columns,
    )

    run_id = new_id()

    repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    step_run = repository.record_step_run(
        pipeline_run_id=run_id,
        step_name="extract",
        step_type="extract",
        status="completed",
        records_in=None,
        records_out=3,
        records_rejected=None,
        started_at=None,
        finished_at=None,
    )

    key = f"{source}/{table}/idempotent.csv"

    first = repository.upsert_dataset_version(
        dataset_id=dataset.dataset_id,
        schema_version_id=schema_version.schema_version_id,
        storage_bucket="bronze",
        storage_key=key,
        etag="abc",
        size_bytes=100,
        row_count=3,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    second = repository.upsert_dataset_version(
        dataset_id=dataset.dataset_id,
        schema_version_id=schema_version.schema_version_id,
        storage_bucket="bronze",
        storage_key=key,
        etag="abc",
        size_bytes=100,
        row_count=3,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    assert first.dataset_version_id == second.dataset_version_id


# =========================================================
# Lineage
# =========================================================


def test_lineage_upstream_downstream(repository, unique_names):

    source, table = unique_names

    dataset = repository.upsert_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    columns = [{"name": "id", "dtype": "int64", "nullable": False}]

    schema_version = repository.upsert_schema_version(
        dataset_id=dataset.dataset_id,
        fingerprint=schema_fingerprint(columns),
        columns=columns,
    )

    run_id = new_id()

    repository.start_pipeline_run(
        pipeline_run_id=run_id,
        pipeline_name="test_pipeline",
        started_at=None,
    )

    step_run = repository.record_step_run(
        pipeline_run_id=run_id,
        step_name="extract",
        step_type="extract",
        status="completed",
        records_in=None,
        records_out=3,
        records_rejected=None,
        started_at=None,
        finished_at=None,
    )

    bronze_version = repository.upsert_dataset_version(
        dataset_id=dataset.dataset_id,
        schema_version_id=schema_version.schema_version_id,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/lineage_bronze.csv",
        etag="e1",
        size_bytes=100,
        row_count=3,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    silver_version = repository.upsert_dataset_version(
        dataset_id=dataset.dataset_id,
        schema_version_id=schema_version.schema_version_id,
        storage_bucket="silver",
        storage_key=f"{source}/{table}/lineage_silver.csv",
        etag="e2",
        size_bytes=100,
        row_count=3,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    repository.record_lineage_edge(
        from_dataset_version_id=bronze_version.dataset_version_id,
        to_dataset_version_id=silver_version.dataset_version_id,
        pipeline_run_id=run_id,
        step_run_id=step_run.step_run_id,
    )

    downstream = repository.get_downstream_versions(
        bronze_version.dataset_version_id,
    )

    upstream = repository.get_upstream_versions(
        silver_version.dataset_version_id,
    )

    assert len(downstream) == 1

    assert downstream[0].dataset_version_id == silver_version.dataset_version_id

    assert len(upstream) == 1

    assert upstream[0].dataset_version_id == bronze_version.dataset_version_id