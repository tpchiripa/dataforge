"""
DataForge Execution Metrics

Runtime metrics collected during pipeline execution.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionMetrics:
    """
    Metrics collected during a pipeline execution.

    The metrics object belongs to the PipelineContext while a
    pipeline is executing and is transferred to PipelineResult
    when execution is finalized.
    """

    # ---------------------------------------------------------
    # Step Metrics
    # ---------------------------------------------------------

    steps_total: int = 0

    steps_completed: int = 0

    steps_failed: int = 0

    # ---------------------------------------------------------
    # Record Metrics
    # ---------------------------------------------------------

    records_read: int = 0

    records_written: int = 0

    records_failed: int = 0

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    duration_seconds: float = 0.0

    # ---------------------------------------------------------
    # Step Helpers
    # ---------------------------------------------------------

    def start_steps(
        self,
        total: int,
    ) -> None:
        """
        Set the total number of pipeline steps.
        """

        self.steps_total = total

    def step_completed(
        self,
    ) -> None:
        """
        Record a successfully completed pipeline step.
        """

        self.steps_completed += 1

    def step_failed(
        self,
    ) -> None:
        """
        Record a failed pipeline step.
        """

        self.steps_failed += 1

    # ---------------------------------------------------------
    # Record Helpers
    # ---------------------------------------------------------

    def add_records_read(
        self,
        count: int,
    ) -> None:
        """
        Add records read during execution.
        """

        self.records_read += max(
            0,
            int(count),
        )

    def add_records_written(
        self,
        count: int,
    ) -> None:
        """
        Add records written during execution.
        """

        self.records_written += max(
            0,
            int(count),
        )

    def add_records_failed(
        self,
        count: int,
    ) -> None:
        """
        Add records that failed processing.
        """

        self.records_failed += max(
            0,
            int(count),
        )

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    def set_duration(
        self,
        duration_seconds: float,
    ) -> None:
        """
        Set total execution duration.
        """

        self.duration_seconds = max(
            0.0,
            float(duration_seconds),
        )

    # ---------------------------------------------------------
    # Derived Metrics
    # ---------------------------------------------------------

    @property
    def steps_pending(
        self,
    ) -> int:
        """
        Return the number of steps not yet completed or failed.
        """

        return max(
            0,
            self.steps_total
            - self.steps_completed
            - self.steps_failed,
        )

    @property
    def is_complete(
        self,
    ) -> bool:
        """
        Return True when all pipeline steps have finished.
        """

        return (
            self.steps_completed
            + self.steps_failed
            >= self.steps_total
        )

    @property
    def success_rate(
        self,
    ) -> float:
        """
        Return the percentage of successfully completed steps.

        Returns 0 when no steps have completed or failed.
        """

        completed = (
            self.steps_completed
            + self.steps_failed
        )

        if completed == 0:
            return 0.0

        return (
            self.steps_completed
            / completed
        ) * 100

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, int | float]:
        """
        Convert metrics into a serializable dictionary.
        """

        return {
            "steps_total": self.steps_total,
            "steps_completed": self.steps_completed,
            "steps_failed": self.steps_failed,
            "records_read": self.records_read,
            "records_written": self.records_written,
            "records_failed": self.records_failed,
            "duration_seconds": self.duration_seconds,
        }

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ExecutionMetrics("
            f"steps_total={self.steps_total}, "
            f"steps_completed={self.steps_completed}, "
            f"steps_failed={self.steps_failed}, "
            f"records_read={self.records_read}, "
            f"records_written={self.records_written}, "
            f"records_failed={self.records_failed}, "
            f"duration_seconds={self.duration_seconds}"
            ")"
        )
