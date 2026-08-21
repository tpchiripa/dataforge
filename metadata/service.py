"""
DataForge Metadata Service

The single public entry point for the metadata subsystem.
Everything else in metadata/ (repository, models) is an
implementation detail -- callers (MetadataHook, a future REST
API, Mpendulo) should only ever import from this module and
metadata/schemas.py.
"""

from __future__ import annotations

import uuid

from metadata.identity import dataset_id as derive_dataset_id
from metadata.identity import schema_fingerprint
from metadata.models import (
    Dataset,
    DatasetVersion,
    LineageEdge,
    PipelineRun,
    QualityResult,
    SchemaVersion,
    StepRun,
)
from metadata.repository import MetadataRepository
from metadata.schemas import (
    DatasetInfo,
    DatasetVersionInfo,
    LineageEdgeInfo,
    PipelineRunInfo,
    QualityResultInfo,
    SchemaInfo,
    StepRunInfo,
    VersionDiff,
)


class MetadataService:
    """
    Public API for the DataForge metadata subsystem.
    """

    def __init__(
        self,
        repository: MetadataRepository,
    ) -> None:

        self._repository = repository

    # =========================================================
    # Write API
    # =========================================================

    def register_dataset_version(
        self,
        *,
        layer: str,
        source: str,
        table: str,
        storage_bucket: str,
        storage_key: str,
        etag: str | None,
        size_bytes: int | None,
        row_count: int | None,
        columns: list[dict],
        pipeline_run_id: uuid.UUID,
        step_run_id: uuid.UUID,
    ) -> DatasetVersionInfo:
        """
        Register a dataset and its schema (if new), then record
        the version that was just written to the lakehouse.
        """

        dataset = self._repository.upsert_dataset(
            layer=layer,
            source=source,
            table=table,
        )

        schema_version = self._repository.upsert_schema_version(
            dataset_id=dataset.dataset_id,
            fingerprint=schema_fingerprint(columns),
            columns=columns,
        )

        version = self._repository.upsert_dataset_version(
            dataset_id=dataset.dataset_id,
            schema_version_id=schema_version.schema_version_id,
            storage_bucket=storage_bucket,
            storage_key=storage_key,
            etag=etag,
            size_bytes=size_bytes,
            row_count=row_count,
            pipeline_run_id=pipeline_run_id,
            step_run_id=step_run_id,
        )

        return self._to_dataset_version_info(version)

    # ---------------------------------------------------------

    def record_pipeline_run_start(
        self,
        *,
        execution_id: uuid.UUID,
        pipeline_name: str,
        started_at,
    ) -> PipelineRunInfo:

        run = self._repository.start_pipeline_run(
            pipeline_run_id=execution_id,
            pipeline_name=pipeline_name,
            started_at=started_at,
        )

        return self._to_pipeline_run_info(run)

    # ---------------------------------------------------------

    def record_pipeline_run_finish(
        self,
        *,
        execution_id: uuid.UUID,
        status: str,
        finished_at,
        duration_seconds: float | None,
        success: bool,
        message: str | None,
        metadata: dict | None = None,
    ) -> PipelineRunInfo:

        run = self._repository.finish_pipeline_run(
            pipeline_run_id=execution_id,
            status=status,
            finished_at=finished_at,
            duration_seconds=duration_seconds,
            success=success,
            message=message,
            metadata_json=metadata,
        )

        return self._to_pipeline_run_info(run)

    # ---------------------------------------------------------

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
        started_at,
        finished_at,
        error_message: str | None = None,
    ) -> StepRunInfo:

        step_run = self._repository.record_step_run(
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

        return self._to_step_run_info(step_run)

    # ---------------------------------------------------------

    def record_quality_result(
        self,
        *,
        step_run_id: uuid.UUID,
        dataset_version_id: uuid.UUID | None,
        passed: bool,
        total_rules: int,
        passed_rules: int,
        failed_rules: int,
        rule_results: list[dict],
    ) -> QualityResultInfo:

        result = self._repository.record_quality_result(
            step_run_id=step_run_id,
            dataset_version_id=dataset_version_id,
            passed=passed,
            total_rules=total_rules,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            rule_results_json=rule_results,
        )

        return self._to_quality_result_info(result)

    # ---------------------------------------------------------

    def record_lineage_edge(
        self,
        *,
        from_dataset_version_id: uuid.UUID,
        to_dataset_version_id: uuid.UUID,
        pipeline_run_id: uuid.UUID,
        step_run_id: uuid.UUID,
    ) -> LineageEdgeInfo:

        edge = self._repository.record_lineage_edge(
            from_dataset_version_id=from_dataset_version_id,
            to_dataset_version_id=to_dataset_version_id,
            pipeline_run_id=pipeline_run_id,
            step_run_id=step_run_id,
        )

        return self._to_lineage_edge_info(edge)

    # =========================================================
    # Read API
    # =========================================================

    def get_dataset(
        self,
        *,
        layer: str,
        source: str,
        table: str,
    ) -> DatasetInfo:

        dataset = self._repository.get_dataset(
            layer=layer,
            source=source,
            table=table,
        )

        return self._to_dataset_info(dataset)

    # ---------------------------------------------------------

    def get_latest_version(
        self,
        dataset_id: uuid.UUID,
    ) -> DatasetVersionInfo | None:

        version = self._repository.get_latest_version(dataset_id)

        if version is None:

            return None

        return self._to_dataset_version_info(version)

    # ---------------------------------------------------------

    def get_pipeline_run(
        self,
        execution_id: uuid.UUID,
    ) -> PipelineRunInfo:

        run = self._repository.get_pipeline_run(execution_id)

        return self._to_pipeline_run_info(run)

    # ---------------------------------------------------------

    def get_recent_pipeline_runs(
        self,
        *,
        pipeline_name: str | None = None,
        limit: int = 20,
    ) -> list[PipelineRunInfo]:

        runs = self._repository.get_recent_pipeline_runs(
            pipeline_name=pipeline_name,
            limit=limit,
        )

        return [
            self._to_pipeline_run_info(run)
            for run in runs
        ]

    # ---------------------------------------------------------

    def get_quality_results(
        self,
        dataset_id: uuid.UUID,
        *,
        limit: int = 20,
    ) -> list[QualityResultInfo]:

        results = self._repository.get_quality_results(
            dataset_id,
            limit=limit,
        )

        return [
            self._to_quality_result_info(result)
            for result in results
        ]

    # ---------------------------------------------------------

    def get_upstream_dependencies(
        self,
        dataset_version_id: uuid.UUID,
    ) -> list[DatasetVersionInfo]:

        versions = self._repository.get_upstream_versions(
            dataset_version_id,
        )

        return [
            self._to_dataset_version_info(version)
            for version in versions
        ]

    # ---------------------------------------------------------

    def get_downstream_dependencies(
        self,
        dataset_version_id: uuid.UUID,
    ) -> list[DatasetVersionInfo]:

        versions = self._repository.get_downstream_versions(
            dataset_version_id,
        )

        return [
            self._to_dataset_version_info(version)
            for version in versions
        ]

    # ---------------------------------------------------------

    def compare_dataset_versions(
        self,
        version_a: DatasetVersionInfo,
        version_b: DatasetVersionInfo,
    ) -> VersionDiff:
        """
        Compare two dataset versions.

        Schema comparison is based on each version's
        schema_version_id -- a difference in that id means the
        schema changed between the two versions.
        """

        schema_changed = (
            version_a.schema_version_id != version_b.schema_version_id
        )

        row_count_delta = None

        if version_a.row_count is not None and version_b.row_count is not None:

            row_count_delta = version_b.row_count - version_a.row_count

        return VersionDiff(
            version_a=version_a,
            version_b=version_b,
            schema_changed=schema_changed,
            row_count_delta=row_count_delta,
        )

    # =========================================================
    # ORM -> DTO Conversion
    # =========================================================

    @staticmethod
    def _to_dataset_info(dataset: Dataset) -> DatasetInfo:

        return DatasetInfo(
            dataset_id=dataset.dataset_id,
            layer=dataset.layer,
            source=dataset.source,
            table_name=dataset.table_name,
            created_at=dataset.created_at,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_schema_info(schema_version: SchemaVersion) -> SchemaInfo:

        return SchemaInfo(
            schema_version_id=schema_version.schema_version_id,
            dataset_id=schema_version.dataset_id,
            fingerprint=schema_version.fingerprint,
            columns=schema_version.columns,
            first_seen_at=schema_version.first_seen_at,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_dataset_version_info(
        version: DatasetVersion,
    ) -> DatasetVersionInfo:

        return DatasetVersionInfo(
            dataset_version_id=version.dataset_version_id,
            dataset_id=version.dataset_id,
            schema_version_id=version.schema_version_id,
            storage_bucket=version.storage_bucket,
            storage_key=version.storage_key,
            etag=version.etag,
            size_bytes=version.size_bytes,
            row_count=version.row_count,
            pipeline_run_id=version.pipeline_run_id,
            step_run_id=version.step_run_id,
            created_at=version.created_at,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_pipeline_run_info(run: PipelineRun) -> PipelineRunInfo:

        return PipelineRunInfo(
            pipeline_run_id=run.pipeline_run_id,
            pipeline_name=run.pipeline_name,
            status=run.status,
            started_at=run.started_at,
            finished_at=run.finished_at,
            duration_seconds=run.duration_seconds,
            success=run.success,
            message=run.message,
            metadata=run.metadata_json or {},
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_step_run_info(step_run: StepRun) -> StepRunInfo:

        return StepRunInfo(
            step_run_id=step_run.step_run_id,
            pipeline_run_id=step_run.pipeline_run_id,
            step_name=step_run.step_name,
            step_type=step_run.step_type,
            status=step_run.status,
            records_in=step_run.records_in,
            records_out=step_run.records_out,
            records_rejected=step_run.records_rejected,
            started_at=step_run.started_at,
            finished_at=step_run.finished_at,
            error_message=step_run.error_message,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_quality_result_info(
        result: QualityResult,
    ) -> QualityResultInfo:

        return QualityResultInfo(
            quality_result_id=result.quality_result_id,
            step_run_id=result.step_run_id,
            dataset_version_id=result.dataset_version_id,
            passed=result.passed,
            total_rules=result.total_rules,
            passed_rules=result.passed_rules,
            failed_rules=result.failed_rules,
            rule_results=result.rule_results_json,
            created_at=result.created_at,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _to_lineage_edge_info(edge: LineageEdge) -> LineageEdgeInfo:

        return LineageEdgeInfo(
            lineage_edge_id=edge.lineage_edge_id,
            from_dataset_version_id=edge.from_dataset_version_id,
            to_dataset_version_id=edge.to_dataset_version_id,
            pipeline_run_id=edge.pipeline_run_id,
            step_run_id=edge.step_run_id,
            created_at=edge.created_at,
        )

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(repository={self._repository!r})"