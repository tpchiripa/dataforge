"""
DataForge Pipeline Monitor

Responsible for monitoring pipeline executions.
"""

from __future__ import annotations

from pipelines.core.pipeline_result import PipelineResult


class PipelineMonitor:
    """
    Monitors DataForge pipeline executions.

    Future integrations include:

    - Prometheus
    - Grafana
    - OpenTelemetry
    - Structured Logging
    - Alerting
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
    # History
    # ---------------------------------------------------------

    @property
    def history(self) -> list[PipelineResult]:
        """
        Return execution history.
        """

        return list(self._history)

    @property
    def last_execution(self) -> PipelineResult | None:
        """
        Return the most recent execution.
        """

        if not self._history:
            return None

        return self._history[-1]

    @property
    def successful_runs(self) -> list[PipelineResult]:
        """
        Return successful executions.
        """

        return [
            result
            for result in self._history
            if result.success
        ]

    @property
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

    @property
    def execution_count(self) -> int:
        """
        Total executions.
        """

        return len(self._history)

    @property
    def success_count(self) -> int:
        """
        Successful executions.
        """

        return len(self.successful_runs)

    @property
    def failure_count(self) -> int:
        """
        Failed executions.
        """

        return len(self.failed_runs)

    @property
    def success_rate(self) -> float:
        """
        Success percentage.
        """

        if self.execution_count == 0:
            return 0.0

        return (
            self.success_count
            / self.execution_count
        ) * 100.0

    @property
    def average_duration(self) -> float:
        """
        Average execution duration.
        """

        if self.execution_count == 0:
            return 0.0

        total = sum(
            result.duration_seconds
            for result in self._history
        )

        return total / self.execution_count

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all execution history.
        """

        self._history.clear()

    # ---------------------------------------------------------

    @property
    def summary(self) -> dict:
        """
        Return execution summary.
        """

        return {
            "executions": self.execution_count,
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": self.success_rate,
            "average_duration": self.average_duration,
        }

    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.execution_count

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"PipelineMonitor("
            f"executions={self.execution_count})"
        )
