"""
DataForge Execution Metrics
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionMetrics:

    steps_total: int = 0

    steps_completed: int = 0

    steps_failed: int = 0

    records_read: int = 0

    records_written: int = 0

    records_failed: int = 0

    duration_seconds: float = 0.0
