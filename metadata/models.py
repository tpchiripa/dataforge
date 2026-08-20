"""
DataForge Metadata Models

SQLAlchemy ORM models for the metadata subsystem.

All tables live in a dedicated "metadata" Postgres schema,
separate from any source-system schema. Dataset *content*
never lives here -- only pointers into the lakehouse
(storage_bucket / storage_key).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# =========================================================
# Base
# =========================================================


class Base(DeclarativeBase):
    """
    Declarative base for every metadata ORM model.
    """

    metadata_schema = "metadata"


# =========================================================
# Dataset
# =========================================================


class Dataset(Base):

    __tablename__ = "dataset"
    __table_args__ = (
        UniqueConstraint(
            "layer",
            "source",
            "table_name",
            name="uq_dataset_layer_source_table",
        ),
        {"schema": "metadata"},
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    layer: Mapped[str] = mapped_column(String, nullable=False)

    source: Mapped[str] = mapped_column(String, nullable=False)

    table_name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    versions: Mapped[list["DatasetVersion"]] = relationship(
        back_populates="dataset",
    )

    schema_versions: Mapped[list["SchemaVersion"]] = relationship(
        back_populates="dataset",
    )


# =========================================================
# Schema Version
# =========================================================


class SchemaVersion(Base):

    __tablename__ = "schema_version"
    __table_args__ = (
        UniqueConstraint(
            "dataset_id",
            "fingerprint",
            name="uq_schema_version_dataset_fingerprint",
        ),
        {"schema": "metadata"},
    )

    schema_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.dataset.dataset_id"),
        nullable=False,
    )

    fingerprint: Mapped[str] = mapped_column(String, nullable=False)

    columns: Mapped[list] = mapped_column(JSONB, nullable=False)

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    dataset: Mapped["Dataset"] = relationship(
        back_populates="schema_versions",
    )


# =========================================================
# Pipeline Run
# =========================================================


class PipelineRun(Base):

    __tablename__ = "pipeline_run"
    __table_args__ = {"schema": "metadata"}

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    pipeline_name: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    duration_seconds: Mapped[float | None] = mapped_column(Float)

    success: Mapped[bool] = mapped_column(Boolean, nullable=False)

    message: Mapped[str | None] = mapped_column(Text)

    metadata_json: Mapped[dict | None] = mapped_column(JSONB)

    step_runs: Mapped[list["StepRun"]] = relationship(
        back_populates="pipeline_run",
    )


# =========================================================
# Step Run
# =========================================================


class StepRun(Base):

    __tablename__ = "step_run"
    __table_args__ = {"schema": "metadata"}

    step_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.pipeline_run.pipeline_run_id"),
        nullable=False,
    )

    step_name: Mapped[str] = mapped_column(String, nullable=False)

    step_type: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)

    records_in: Mapped[int | None] = mapped_column(Integer)

    records_out: Mapped[int | None] = mapped_column(Integer)

    records_rejected: Mapped[int | None] = mapped_column(Integer)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    error_message: Mapped[str | None] = mapped_column(Text)

    pipeline_run: Mapped["PipelineRun"] = relationship(
        back_populates="step_runs",
    )


# =========================================================
# Dataset Version
# =========================================================


class DatasetVersion(Base):

    __tablename__ = "dataset_version"
    __table_args__ = (
        UniqueConstraint(
            "storage_bucket",
            "storage_key",
            name="uq_dataset_version_storage",
        ),
        {"schema": "metadata"},
    )

    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.dataset.dataset_id"),
        nullable=False,
    )

    schema_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.schema_version.schema_version_id"),
        nullable=False,
    )

    storage_bucket: Mapped[str] = mapped_column(String, nullable=False)

    storage_key: Mapped[str] = mapped_column(String, nullable=False)

    etag: Mapped[str | None] = mapped_column(String)

    size_bytes: Mapped[int | None] = mapped_column(Integer)

    row_count: Mapped[int | None] = mapped_column(Integer)

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.pipeline_run.pipeline_run_id"),
        nullable=False,
    )

    step_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.step_run.step_run_id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    dataset: Mapped["Dataset"] = relationship(
        back_populates="versions",
    )


# =========================================================
# Quality Result
# =========================================================


class QualityResult(Base):

    __tablename__ = "quality_result"
    __table_args__ = {"schema": "metadata"}

    quality_result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    step_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.step_run.step_run_id"),
        nullable=False,
    )

    dataset_version_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.dataset_version.dataset_version_id"),
    )

    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    total_rules: Mapped[int] = mapped_column(Integer, nullable=False)

    passed_rules: Mapped[int] = mapped_column(Integer, nullable=False)

    failed_rules: Mapped[int] = mapped_column(Integer, nullable=False)

    rule_results_json: Mapped[list] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# =========================================================
# Lineage Edge
# =========================================================


class LineageEdge(Base):

    __tablename__ = "lineage_edge"
    __table_args__ = {"schema": "metadata"}

    lineage_edge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    from_dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.dataset_version.dataset_version_id"),
        nullable=False,
    )

    to_dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.dataset_version.dataset_version_id"),
        nullable=False,
    )

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.pipeline_run.pipeline_run_id"),
        nullable=False,
    )

    step_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("metadata.step_run.step_run_id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )