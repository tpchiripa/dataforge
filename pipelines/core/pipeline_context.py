"""
DataForge Pipeline Context
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .pipeline_config import PipelineConfig
from .pipeline_status import PipelineStatus


@dataclass(slots=True)
class PipelineContext:
    """
    Runtime context for a pipeline execution.

    Stores shared state that is passed between all
    pipeline steps during execution.
    """

    # ---------------------------------------------------------
    # Pipeline Information
    # ---------------------------------------------------------

    config: PipelineConfig

    status: PipelineStatus = PipelineStatus.CREATED

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # ---------------------------------------------------------
    # Runtime State
    # ---------------------------------------------------------

    data: Any = None

    variables: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Variable Helpers
    # ---------------------------------------------------------

    def set(self, key: str, value: Any) -> None:
        """
        Store a runtime variable.
        """
        self.variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a runtime variable.
        """
        return self.variables.get(key, default)

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Store execution metadata.
        """
        self.metadata[key] = value

    # ---------------------------------------------------------
    # Error Handling
    # ---------------------------------------------------------

    def add_error(self, message: str) -> None:
        """
        Record an execution error.
        """
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """
        Record an execution warning.
        """
        self.warnings.append(message)

    @property
    def has_errors(self) -> bool:
        """
        Returns True if errors exist.
        """
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """
        Returns True if warnings exist.
        """
        return len(self.warnings) > 0

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def set_status(self, status: PipelineStatus) -> None:
        """
        Update the pipeline status.
        """
        self.status = status
