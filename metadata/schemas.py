"""
DataForge Metadata Schemas

Plain, ORM-independent data transfer objects returned by
MetadataService. Nothing outside metadata/ should ever need
to import a SQLAlchemy model directly -- this is the stable
shape that a future REST API, UI, or Mpendulo consumes.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# =========================================================
# Dataset
# =========================================================


@dataclass(slots=True)
class DatasetInfo:

    dataset_id: uuid.UUID

    layer: str

    source: str

    table_name: str

    created_at: datetime


# =========================================================
# Schema
# =========================================================


@dataclass(slots=True)
class SchemaInfo:

    schema_version_id: uuid.UUID

    dataset_id: uuid.UUID

    fingerprint: str

    columns: list[dict[str, Any]]

    first_seen_at: datetime


# =========================================================
# Dataset Version
# =========================================================


@dataclass(slots=True)
class DatasetVersionInfo:

    dataset_version_id: uuid.UUID

    dataset_id: uuid.UUID

    schema_version_id: uuid.UUID

    storage_bucket: str

    storage_key: str

    etag: str | None

    size_bytes: int | None

    row_count: int | None

    pipeline_run_id: uuid.UUID

    step_run_id: uuid.UUID

    created_at: datetime


@dataclass(slots=True)
class VersionDiff:

    version_a: DatasetVersionInfo

    version_b: DatasetVersionInfo

    schema_changed: bool

    added_columns: list[str] = field(default_factory=list)

    removed_columns: list[str] = field(default_factory=list)

    row_count_delta: int | None = None


# =========================================================
# Pipeline Run
# =========================================================


@dataclass(slots=True)
class PipelineRunInfo:

    pipeline_run_id: uuid.UUID

    pipeline_name: str

    status: str

    started_at: datetime | None

    finished_at: datetime | None

    duration_seconds: float | None

    success: bool

    message: str | None

    metadata: dict[str, Any] = field(default_factory=dict)


# =========================================================
# Step Run
# =========================================================


@dataclass(slots=True)
class StepRunInfo:

    step_run_id: uuid.UUID

    pipeline_run_id: uuid.UUID

    step_name: str

    step_type: str

    status: str

    records_in: int | None

    records_out: int | None

    records_rejected: int | None

    started_at: datetime | None

    finished_at: datetime | None

    error_message: str | None = None


# =========================================================
# Quality Result
# =========================================================


@dataclass(slots=True)
class QualityResultInfo:

    quality_result_id: uuid.UUID

    step_run_id: uuid.UUID

    dataset_version_id: uuid.UUID | None

    passed: bool

    total_rules: int

    passed_rules: int

    failed_rules: int

    rule_results: list[dict[str, Any]]

    created_at: datetime


# =========================================================
# Lineage
# =========================================================


@dataclass(slots=True)
class LineageEdgeInfo:

    lineage_edge_id: uuid.UUID

    from_dataset_version_id: uuid.UUID

    to_dataset_version_id: uuid.UUID

    pipeline_run_id: uuid.UUID

    step_run_id: uuid.UUID

    created_at: datetime