"""
DataForge Pipeline Context

Runtime context shared by all pipeline steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pipelines.execution.execution_id import ExecutionID
from pipelines.execution.execution_metrics import ExecutionMetrics

from .pipeline_config import PipelineConfig
from .pipeline_result import PipelineResult
from .pipeline_status import PipelineStatus


@dataclass(slots=True)
class PipelineContext:
    """
    Runtime context for a pipeline execution.

    Stores shared state, execution metadata, errors, warnings,
    execution metrics, and the final execution result.
    """

    # =========================================================
    # Pipeline Information
    # =========================================================

    config: PipelineConfig

    execution_id: str = field(
        default_factory=ExecutionID.generate,
    )

    status: PipelineStatus = PipelineStatus.CREATED

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # =========================================================
    # Runtime State
    # =========================================================

    data: Any = None

    variables: dict[str, Any] = field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    errors: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    # =========================================================
    # Execution Metrics
    # =========================================================

    metrics: ExecutionMetrics = field(
        default_factory=ExecutionMetrics,
    )

    # =========================================================
    # Execution Result
    # =========================================================

    result: PipelineResult | None = None

    # =========================================================
    # Variable Helpers
    # =========================================================

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a runtime variable.
        """

        self.variables[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a runtime variable.
        """

        return self.variables.get(
            key,
            default,
        )

    # =========================================================
    # Metadata Helpers
    # =========================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store execution metadata.
        """

        self.metadata[key] = value

    # =========================================================
    # Error Handling
    # =========================================================

    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Record an execution error.
        """

        self.errors.append(
            str(message),
        )

    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Record an execution warning.
        """

        self.warnings.append(
            str(message),
        )

    @property
    def has_errors(
        self,
    ) -> bool:
        """
        Return True when execution errors exist.
        """

        return bool(
            self.errors,
        )

    @property
    def has_warnings(
        self,
    ) -> bool:
        """
        Return True when execution warnings exist.
        """

        return bool(
            self.warnings,
        )

    # =========================================================
    # Status
    # =========================================================

    def set_status(
        self,
        status: PipelineStatus,
    ) -> None:
        """
        Update the pipeline status.
        """

        self.status = status

    # =========================================================
    # Execution Metrics
    # =========================================================

    def start_metrics(
        self,
        total_steps: int,
    ) -> None:
        """
        Initialize execution metrics.
        """

        self.metrics.start_steps(
            total_steps,
        )

    def step_completed(
        self,
    ) -> None:
        """
        Record a successfully completed pipeline step.
        """

        self.metrics.step_completed()

    def step_failed(
        self,
    ) -> None:
        """
        Record a failed pipeline step.
        """

        self.metrics.step_failed()

    def records_read(
        self,
        count: int,
    ) -> None:
        """
        Record records read during execution.
        """

        self.metrics.add_records_read(
            count,
        )

    def records_written(
        self,
        count: int,
    ) -> None:
        """
        Record records written during execution.
        """

        self.metrics.add_records_written(
            count,
        )

    def records_failed(
        self,
        count: int,
    ) -> None:
        """
        Record records that failed during execution.
        """

        self.metrics.add_records_failed(
            count,
        )

    # =========================================================
    # Finalization
    # =========================================================

    def finalize(
        self,
        *,
        success: bool,
        message: str = "",
    ) -> PipelineResult:
        """
        Finalize the pipeline execution.

        Converts the current runtime context into a
        PipelineResult.

        Parameters
        ----------
        success:
            Whether the pipeline execution succeeded.

        message:
            Human-readable execution message.
        """

        # -----------------------------------------------------
        # Finish Timestamp
        # -----------------------------------------------------

        if self.finished_at is None:
            self.finished_at = datetime.utcnow()

        # -----------------------------------------------------
        # Execution Duration
        # -----------------------------------------------------

        if self.started_at is not None:

            duration = (
                self.finished_at
                - self.started_at
            ).total_seconds()

            self.metrics.set_duration(
                duration,
            )

        # -----------------------------------------------------
        # Execution Metadata
        # -----------------------------------------------------

        self.metadata["execution_id"] = (
            self.execution_id
        )

        self.metadata["status"] = (
            self.status.value
        )

        self.metadata["duration_seconds"] = (
            self.metrics.duration_seconds
        )

        # -----------------------------------------------------
        # Construct Pipeline Result
        # -----------------------------------------------------

        result = PipelineResult(
            success=success,
            status=self.status,
            pipeline_name=self.config.name,
            execution_id=self.execution_id,
            message=message,
            started_at=self.started_at,
            finished_at=self.finished_at,
            duration_seconds=self.metrics.duration_seconds,
            metrics=self.metrics,
            records_read=self.metrics.records_read,
            records_written=self.metrics.records_written,
            records_failed=self.metrics.records_failed,
            metadata=dict(self.metadata),
            errors=list(self.errors),
            warnings=list(self.warnings),
        )

        # -----------------------------------------------------
        # Store Final Result
        # -----------------------------------------------------

        self.result = result

        return result

    # =========================================================
    # Representation
    # =========================================================

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineContext("
            f"pipeline='{self.config.name}', "
            f"execution_id='{self.execution_id}', "
            f"status='{self.status.value}')"
        )
