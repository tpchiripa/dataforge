"""
DataForge Pipeline Executor

Responsible for executing pipelines.
"""

from __future__ import annotations

from datetime import datetime

from pipelines.core.pipeline import Pipeline
from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus


class PipelineExecutor:
    """
    Executes DataForge pipelines.

    The executor is responsible for orchestrating pipeline execution.
    Future versions will support retries, scheduling, logging,
    distributed execution and monitoring.
    """

    def __init__(self):

        self.execution_count = 0

        self.last_execution = None

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        pipeline: Pipeline,
    ) -> PipelineResult:
        """
        Execute a pipeline.
        """

        self.execution_count += 1

        self.last_execution = datetime.utcnow()

        return pipeline.execute()

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def execute_many(
        self,
        pipelines: list[Pipeline],
    ) -> list[PipelineResult]:
        """
        Execute multiple pipelines sequentially.
        """

        results = []

        for pipeline in pipelines:

            results.append(
                self.execute(pipeline)
            )

        return results

    # ---------------------------------------------------------

    def execution_summary(
        self,
        result: PipelineResult,
    ) -> dict:
        """
        Return a summary of a pipeline execution.
        """

        return {
            "pipeline": result.pipeline_name,
            "status": result.status.value,
            "success": result.success,
            "duration_seconds": result.duration_seconds,
            "records_read": result.records_read,
            "records_written": result.records_written,
            "records_failed": result.records_failed,
            "errors": len(result.errors),
            "warnings": len(result.warnings),
        }

    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset executor statistics.
        """

        self.execution_count = 0

        self.last_execution = None

    # ---------------------------------------------------------

    @property
    def has_executed(self) -> bool:
        """
        Returns True if at least one execution has occurred.
        """

        return self.execution_count > 0

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"PipelineExecutor("
            f"executions={self.execution_count})"
        )
