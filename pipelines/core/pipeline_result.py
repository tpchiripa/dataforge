"""
DataForge Pipeline Result
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pipelines.execution.execution_metrics import ExecutionMetrics

from .pipeline_status import PipelineStatus


@dataclass(slots=True)
class PipelineResult:
    """
    Represents the outcome of a pipeline execution.
    """

    success: bool

    status: PipelineStatus

    pipeline_name: str

    execution_id: str = ""

    message: str = ""

    started_at: datetime | None = None

    finished_at: datetime | None = None

    duration_seconds: float = 0.0

    metrics: ExecutionMetrics = field(
        default_factory=ExecutionMetrics,
    )

    records_read: int = 0

    records_written: int = 0

    records_failed: int = 0

    output_location: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------

    def add_error(self, message: str) -> None:
        """
        Add an execution error.
        """
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """
        Add an execution warning.
        """
        self.warnings.append(message)

    @property
    def has_errors(self) -> bool:
        """
        Return True if execution contains errors.
        """
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """
        Return True if execution contains warnings.
        """
        return len(self.warnings) > 0
