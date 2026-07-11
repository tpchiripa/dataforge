"""
DataForge Pipeline Monitor

Responsible for monitoring pipeline executions.
"""

from __future__ import annotations

from pipelines.core.pipeline_result import PipelineResult


class PipelineMonitor:
    """
    Monitors DataForge pipeline executions.

    Future versions will integrate with:

    - Prometheus
    - Grafana
    - OpenTelemetry
    - Logging
    - Alerts
    """

    def __init__(self):

        self._history: list[PipelineResult] = []

    # ---------------------------------------------------------
    # Recording
    # ---------------------------------------------------------

    def record(
        self,
        result: PipelineResult,
    ) -> None:
        """
        Record a completed pipeline execution.
        """

        self._history.append(result)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def history(self) -> list[PipelineResult]:
        """
        Return all recorded executions.
        """

        return list(self._history)

    def last_execution(self) -> PipelineResult | None:
        """
        Return the most recent execution.
        """

        if not self._history:
            return None

        return self._history[-1]

    def successful_runs(self) -> list[PipelineResult]:
        """
        Return successful executions.
        """

        return [
            result
            for result in self._history
            if result.success
        ]

    def failed_runs(self) -> list[PipelineResult]:
        """
        Return failed executions.
        """

        return [
            result
            for result in self._history
            if not result.success
        ]

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def execution_count(self) -> int:
        """
        Total number of executions.
        """

        return len(self._history)

    def success_count(self) -> int:
        """
        Number of successful executions.
        """

        return len(self.successful_runs())

    def failure_count(self) -> int:
        """
        Number of failed executions.
        """

        return len(self.failed_runs())

    def success_rate(self) -> float:
        """
        Percentage of successful executions.
        """

        if not self._history:
            return 0.0

        return (
            self.success_count()
            / self.execution_count()
        ) * 100.0

    def average_duration(self) -> float:
        """
        Average pipeline execution duration.
        """

        if not self._history:
            return 0.0

        total = sum(
            result.duration_seconds
            for result in self._history
        )

        return total / len(self._history)

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Clear execution history.
        """

        self._history.clear()

    # ---------------------------------------------------------

    def summary(self) -> dict:
        """
        Return execution statistics.
        """

        return {
            "executions": self.execution_count(),
            "successful": self.success_count(),
            "failed": self.failure_count(),
            "success_rate": self.success_rate(),
            "average_duration": self.average_duration(),
        }

    # ---------------------------------------------------------

    def __len__(self) -> int:

        return len(self._history)

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"PipelineMonitor("
            f"executions={self.execution_count()})"
        )
