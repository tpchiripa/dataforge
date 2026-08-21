"""
DataForge Metadata Service Tests

Runs against the real local Postgres instance, exercising the
full MetadataService write/read/DTO round trip on top of
MetadataRepository.
"""

from __future__ import annotations

import uuid

import pytest

from configs.settings import settings
from metadata.identity import new_id, schema_fingerprint
from metadata.repository import MetadataRepository
from metadata.service import MetadataService


# =========================================================
# Fixtures
# =========================================================


@pytest.fixture(scope="module")
def service():

    repository = MetadataRepository(settings.database.psycopg_uri)

    repository.create_schema_and_tables()

    return MetadataService(repository)


@pytest.fixture
def unique_names():

    suffix = uuid.uuid4().hex[:8]

    return f"svc_source_{suffix}", f"svc_table_{suffix}"


@pytest.fixture
def columns():

    return [
        {"name": "id", "dtype": "int64", "nullable": False},
        {"name": "name", "dtype": "object", "nullable": True},
    ]


# =========================================================
# Full Round Trip
# =========================================================


def test_full_pipeline_round_trip(service, unique_names, columns):

    source, table = unique_names

    run_id = new_id()

    started_run = service.record_pipeline_run_start(
        execution_id=run_id,
        pipeline_name="svc_test_pipeline",
        started_at=None,
    )

    assert started_run.status == "running"

    extract_step = service.record_step_run(
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

    bronze_version = service.register_dataset_version(
        layer="bronze",
        source=source,
        table=table,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/round_trip.csv",
        etag="e1",
        size_bytes=200,
        row_count=3,
        columns=columns,
        pipeline_run_id=run_id,
        step_run_id=extract_step.step_run_id,
    )

    validate_step = service.record_step_run(
        pipeline_run_id=run_id,
        step_name="validate_orders",
        step_type="validation",
        status="completed",
        records_in=3,
        records_out=3,
        records_rejected=0,
        started_at=None,
        finished_at=None,
    )

    quality_result = service.record_quality_result(
        step_run_id=validate_step.step_run_id,
        dataset_version_id=bronze_version.dataset_version_id,
        passed=True,
        total_rules=2,
        passed_rules=2,
        failed_rules=0,
        rule_results=[
            {"rule_name": "not_null", "passed": True},
            {"rule_name": "no_duplicates", "passed": True},
        ],
    )

    silver_version = service.register_dataset_version(
        layer="silver",
        source=source,
        table=table,
        storage_bucket="silver",
        storage_key=f"{source}/{table}/round_trip_silver.csv",
        etag="e2",
        size_bytes=200,
        row_count=3,
        columns=columns,
        pipeline_run_id=run_id,
        step_run_id=validate_step.step_run_id,
    )

    edge = service.record_lineage_edge(
        from_dataset_version_id=bronze_version.dataset_version_id,
        to_dataset_version_id=silver_version.dataset_version_id,
        pipeline_run_id=run_id,
        step_run_id=validate_step.step_run_id,
    )

    finished_run = service.record_pipeline_run_finish(
        execution_id=run_id,
        status="completed",
        finished_at=None,
        duration_seconds=0.5,
        success=True,
        message="ok",
        metadata={"records_read": 3},
    )

    # -----------------------------------------------------
    # Assertions
    # -----------------------------------------------------

    assert finished_run.success is True

    assert quality_result.passed is True

    assert edge.from_dataset_version_id == bronze_version.dataset_version_id

    assert edge.to_dataset_version_id == silver_version.dataset_version_id

    dataset = service.get_dataset(
        layer="bronze",
        source=source,
        table=table,
    )

    latest = service.get_latest_version(dataset.dataset_id)

    assert latest.dataset_version_id == bronze_version.dataset_version_id

    downstream = service.get_downstream_dependencies(
        bronze_version.dataset_version_id,
    )

    assert len(downstream) == 1

    assert downstream[0].dataset_version_id == silver_version.dataset_version_id

    upstream = service.get_upstream_dependencies(
        silver_version.dataset_version_id,
    )

    assert len(upstream) == 1

    assert upstream[0].dataset_version_id == bronze_version.dataset_version_id

    quality_results = service.get_quality_results(dataset.dataset_id)

    assert len(quality_results) == 1

    assert quality_results[0].passed is True

    fetched_run = service.get_pipeline_run(run_id)

    assert fetched_run.status == "completed"

    recent_runs = service.get_recent_pipeline_runs(
        pipeline_name="svc_test_pipeline",
    )

    assert any(
        run.pipeline_run_id == run_id
        for run in recent_runs
    )


# =========================================================
# compare_dataset_versions
# =========================================================


def test_compare_dataset_versions_detects_schema_change(
    service,
    unique_names,
    columns,
):

    source, table = unique_names

    run_id = new_id()

    service.record_pipeline_run_start(
        execution_id=run_id,
        pipeline_name="svc_test_pipeline",
        started_at=None,
    )

    step = service.record_step_run(
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

    version_a = service.register_dataset_version(
        layer="bronze",
        source=source,
        table=table,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/v1.csv",
        etag="a",
        size_bytes=100,
        row_count=3,
        columns=columns,
        pipeline_run_id=run_id,
        step_run_id=step.step_run_id,
    )

    changed_columns = columns + [
        {"name": "email", "dtype": "object", "nullable": True},
    ]

    version_b = service.register_dataset_version(
        layer="bronze",
        source=source,
        table=table,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/v2.csv",
        etag="b",
        size_bytes=150,
        row_count=5,
        columns=changed_columns,
        pipeline_run_id=run_id,
        step_run_id=step.step_run_id,
    )

    diff = service.compare_dataset_versions(version_a, version_b)

    assert diff.schema_changed is True

    assert diff.row_count_delta == 2


def test_compare_dataset_versions_no_schema_change(
    service,
    unique_names,
    columns,
):

    source, table = unique_names

    run_id = new_id()

    service.record_pipeline_run_start(
        execution_id=run_id,
        pipeline_name="svc_test_pipeline",
        started_at=None,
    )

    step = service.record_step_run(
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

    version_a = service.register_dataset_version(
        layer="bronze",
        source=source,
        table=table,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/same_v1.csv",
        etag="a",
        size_bytes=100,
        row_count=3,
        columns=columns,
        pipeline_run_id=run_id,
        step_run_id=step.step_run_id,
    )

    version_b = service.register_dataset_version(
        layer="bronze",
        source=source,
        table=table,
        storage_bucket="bronze",
        storage_key=f"{source}/{table}/same_v2.csv",
        etag="b",
        size_bytes=100,
        row_count=3,
        columns=columns,
        pipeline_run_id=run_id,
        step_run_id=step.step_run_id,
    )

    diff = service.compare_dataset_versions(version_a, version_b)

    assert diff.schema_changed is False

    assert diff.row_count_delta == 0