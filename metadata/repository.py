"""
DataForge Metadata Repository

All SQLAlchemy session handling and SQL for the metadata
subsystem lives here and nowhere else. MetadataService is the
only caller.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session, sessionmaker

from metadata.exceptions import (
    DatasetNotFoundError,
    PipelineRunNotFoundError,
)
from metadata.identity import dataset_id as derive_dataset_id
from metadata.identity import new_id
from metadata.models import (
    Base,
    Dataset,
    DatasetVersion,
    LineageEdge,
    PipelineRun,
    QualityResult,
    SchemaVersion,
    StepRun,
)


class MetadataRepository:
    """
    Repository layer for the metadata subsystem.

    Owns the SQLAlchemy engine/session and every table
    operation. All writes are idempotent per the identity
    strategy in metadata/identity.py -- callers do not need to
    check existence before writing.
    """

    def __init__(
        self,
        connection_string: str,
    ) -> None:

        self._engine = create_engine(
            connection_string,
            future=True,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            future=True,
        )

    # =========================================================
    # Schema Management
    # =========================================================

    def create_schema_and_tables(self) -> None:
        """
        Create the "metadata" Postgres schema and every table.

        Intended for local/dev use and tests. Production
        deployments should use the Alembic migration instead.
        """

        with self._engine.begin() as connection:

            connection.exec_driver_sql(
                "CREATE SCHEMA IF NOT EXISTS metadata",
            )

            Base.metadata.create_all(connection)

    # =========================================================
    # Session Helper
    # =========================================================

    def _session(self) -> Session:

        return self._session_factory()

    # =========================================================
    # Dataset
    # =========================================================

    def upsert_dataset(
        self,
        *,
        layer: str,
        source: str,
        table: str,
    ) -> Dataset:
        """
        Idempotently register a dataset.

        Same (layer, source, table) always resolves to the same
        row -- re-registering is a no-op.
        """

        identity = derive_dataset_id(layer, source, table)

        with self._session() as session:

            statement = (
                pg_insert(Dataset)
                .values(
                    dataset_id=identity,
                    layer=layer,
                    source=source,
                    table_name=table,
                )
                .on_conflict_do_nothing(
                    index_elements=["layer", "source", "table_name"],
                )
            )

            session.execute(statement)

            session.commit()

            return session.get(Dataset, identity)

    # =========================================================
    # Schema Version
    # =========================================================

    def upsert_schema_version(
        self,
        *,
        dataset_id: uuid.UUID,
        fingerprint: str,
        columns: list[dict],
    ) -> SchemaVersion:
        """
        Idempotently register a schema version.

        Same (dataset_id, fingerprint) always resolves to the
        same row -- an unchanged schema across runs does not
        create a new row.
        """

        with self._session() as session:

            existing = session.scalar(
                select(SchemaVersion).where(
                    SchemaVersion.dataset_id == dataset_id,
                    SchemaVersion.fingerprint == fingerprint,
                )
            )

            if existing is not None:

                return existing

            schema_version = SchemaVersion(
                schema_version_id=new_id(),
                dataset_id=dataset_id,
                fingerprint=fingerprint,
                columns=columns,
            )

            session.add(schema_version)

            session.commit()

            session.refresh(schema_version)

            return schema_version

    # =========================================================
    # Pipeline Run
    # =========================================================

    def start_pipeline_run(
        self,
        *,
        pipeline_run_id: uuid.UUID,
        pipeline_name: str,
        started_at: datetime | None,
    ) -> PipelineRun:
        """
        Record the start of a pipeline run.

        pipeline_run_id is the pipeline's execution_id -- calling
        this twice for the same run is safe (second call is a
        no-op update of the same row).
        """

        with self._session() as session:

            existing = session.get(PipelineRun, pipeline_run_id)

            if existing is not None:

                return existing

            run = PipelineRun(
                pipeline_run_id=pipeline_run_id,
                pipeline_name=pipeline_name,
                status="running",
                started_at=started_at,
                success=False,
            )

            session.add(run)

            session.commit()

            session.refresh(run)

            return run

    # ---------------------------------------------------------

    def finish_pipeline_run(
        self,
        *,
        pipeline_run_id: uuid.UUID,
        status: str,
        finished_at: datetime | None,
        duration_seconds: float | None,
        success: bool,
        message: str | None,
        metadata_json: dict | None,
    ) -> PipelineRun:
        """
        Record the completion of a pipeline run.

        Safe to call more than once for the same run -- always
        updates the same row rather than inserting a new one.
        """

        with self._session() as session:

            run = session.get(PipelineRun, pipeline_run_id)

            if run is None:

                raise PipelineRunNotFoundError(
                    f"Pipeline run '{pipeline_run_id}' was never started.",
                )

            run.status = status

            run.finished_at = finished_at

            run.duration_seconds = duration_seconds

            run.success = success

            run.message = message

            run.metadata_json = metadata_json

            session.commit()

            session.refresh(run)

            return run

    # ---------------------------------------------------------

    def get_pipeline_run(
        self,
        pipeline_run_id: uuid.UUID,
    ) -> PipelineRun:

        with self._session() as session:

            run = session.get(PipelineRun, pipeline_run_id)

            if run is None:

                raise PipelineRunNotFoundError(
                    f"Pipeline run '{pipeline_run_id}' not found.",
                )

            return run

    # ---------------------------------------------------------

    def get_recent_pipeline_runs(
        self,
        *,
        pipeline_name: str | None = None,
        limit: int = 20,
    ) -> list[PipelineRun]:

        with self._session() as session:

            statement = select(PipelineRun).order_by(
                PipelineRun.started_at.desc(),
            ).limit(limit)

            if pipeline_name is not None:

                statement = statement.where(
                    PipelineRun.pipeline_name == pipeline_name,
                )

            return list(session.scalars(statement))

    # =========================================================
    # Step Run
    # =========================================================

    def record_step_run(
        self,
        *,
        pipeline_run_id: uuid.UUID,
        step_name: str,
        step_type: str,
        status: str,
        records_in: int | None,
        records_out: int | None,
        records_rejected: int | None,
        started_at: datetime | None,
        finished_at: datetime | None,
        error_message: str | None = None,
    ) -> StepRun:

        with self._session() as session:

            step_run = StepRun(
                step_run_id=new_id(),
                pipeline_run_id=pipeline_run_id,
                step_name=step_name,
                step_type=step_type,
                status=status,
                records_in=records_in,
                records_out=records_out,
                records_rejected=records_rejected,
                started_at=started_at,
                finished_at=finished_at,
                error_message=error_message,
            )

            session.add(step_run)

            session.commit()

            session.refresh(step_run)

            return step_run

    # =========================================================
    # Dataset Version
    # =========================================================

    def upsert_dataset_version(
        self,
        *,
        dataset_id: uuid.UUID,
        schema_version_id: uuid.UUID,
        storage_bucket: str,
        storage_key: str,
        etag: str | None,
        size_bytes: int | None,
        row_count: int | None,
        pipeline_run_id: uuid.UUID,
        step_run_id: uuid.UUID,
    ) -> DatasetVersion:
        """
        Idempotently register a dataset version.

        Same (storage_bucket, storage_key) always resolves to
        the same row -- re-registering the exact same physical
        object (e.g. a retried step) is a no-op.
        """

        with self._session() as session:

            existing = session.scalar(
                select(DatasetVersion).where(
                    DatasetVersion.storage_bucket == storage_bucket,
                    DatasetVersion.storage_key == storage_key,
                )
            )

            if existing is not None:

                return existing

            version = DatasetVersion(
                dataset_version_id=new_id(),
                dataset_id=dataset_id,
                schema_version_id=schema_version_id,
                storage_bucket=storage_bucket,
                storage_key=storage_key,
                etag=etag,
                size_bytes=size_bytes,
                row_count=row_count,
                pipeline_run_id=pipeline_run_id,
                step_run_id=step_run_id,
            )

            session.add(version)

            session.commit()

            session.refresh(version)

            return version

    # ---------------------------------------------------------

    def get_latest_version(
        self,
        dataset_id: uuid.UUID,
    ) -> DatasetVersion | None:

        with self._session() as session:

            return session.scalar(
                select(DatasetVersion)
                .where(DatasetVersion.dataset_id == dataset_id)
                .order_by(DatasetVersion.created_at.desc())
                .limit(1)
            )

    # ---------------------------------------------------------

    def get_dataset(
        self,
        *,
        layer: str,
        source: str,
        table: str,
    ) -> Dataset:

        identity = derive_dataset_id(layer, source, table)

        with self._session() as session:

            dataset = session.get(Dataset, identity)

            if dataset is None:

                raise DatasetNotFoundError(
                    f"Dataset '{layer}/{source}/{table}' not found.",
                )

            return dataset

    # =========================================================
    # Quality Result
    # =========================================================

    def record_quality_result(
        self,
        *,
        step_run_id: uuid.UUID,
        dataset_version_id: uuid.UUID | None,
        passed: bool,
        total_rules: int,
        passed_rules: int,
        failed_rules: int,
        rule_results_json: list[dict],
    ) -> QualityResult:

        with self._session() as session:

            result = QualityResult(
                quality_result_id=new_id(),
                step_run_id=step_run_id,
                dataset_version_id=dataset_version_id,
                passed=passed,
                total_rules=total_rules,
                passed_rules=passed_rules,
                failed_rules=failed_rules,
                rule_results_json=rule_results_json,
            )

            session.add(result)

            session.commit()

            session.refresh(result)

            return result

    # ---------------------------------------------------------

    def get_quality_results(
        self,
        dataset_id: uuid.UUID,
        *,
        limit: int = 20,
    ) -> list[QualityResult]:

        with self._session() as session:

            statement = (
                select(QualityResult)
                .join(
                    DatasetVersion,
                    QualityResult.dataset_version_id
                    == DatasetVersion.dataset_version_id,
                )
                .where(DatasetVersion.dataset_id == dataset_id)
                .order_by(QualityResult.created_at.desc())
                .limit(limit)
            )

            return list(session.scalars(statement))

    # =========================================================
    # Lineage
    # =========================================================

    def record_lineage_edge(
        self,
        *,
        from_dataset_version_id: uuid.UUID,
        to_dataset_version_id: uuid.UUID,
        pipeline_run_id: uuid.UUID,
        step_run_id: uuid.UUID,
    ) -> LineageEdge:

        with self._session() as session:

            edge = LineageEdge(
                lineage_edge_id=new_id(),
                from_dataset_version_id=from_dataset_version_id,
                to_dataset_version_id=to_dataset_version_id,
                pipeline_run_id=pipeline_run_id,
                step_run_id=step_run_id,
            )

            session.add(edge)

            session.commit()

            session.refresh(edge)

            return edge

    # ---------------------------------------------------------

    def get_upstream_versions(
        self,
        dataset_version_id: uuid.UUID,
    ) -> list[DatasetVersion]:

        with self._session() as session:

            statement = (
                select(DatasetVersion)
                .join(
                    LineageEdge,
                    LineageEdge.from_dataset_version_id
                    == DatasetVersion.dataset_version_id,
                )
                .where(
                    LineageEdge.to_dataset_version_id == dataset_version_id,
                )
            )

            return list(session.scalars(statement))

    # ---------------------------------------------------------

    def get_downstream_versions(
        self,
        dataset_version_id: uuid.UUID,
    ) -> list[DatasetVersion]:

        with self._session() as session:

            statement = (
                select(DatasetVersion)
                .join(
                    LineageEdge,
                    LineageEdge.to_dataset_version_id
                    == DatasetVersion.dataset_version_id,
                )
                .where(
                    LineageEdge.from_dataset_version_id == dataset_version_id,
                )
            )

            return list(session.scalars(statement))

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(engine={self._engine.url})"