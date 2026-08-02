"""
DataForge Logging Hook

Provides lifecycle logging for pipeline execution.
"""

from __future__ import annotations

import logging

from pipelines.core.pipeline_context import PipelineContext
from pipelines.lifecycle.pipeline_hook import PipelineHook


class LoggingHook(PipelineHook):
    """
    Logs pipeline lifecycle events.

    This hook can later be extended to integrate with:

    - Prometheus
    - Grafana
    - OpenTelemetry
    - ELK Stack
    - CloudWatch
    - Azure Monitor
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:

        self.logger = logger or logging.getLogger("dataforge")

    # ---------------------------------------------------------

    def before_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.info(
            "Pipeline '%s' started.",
            context.config.name,
        )

    # ---------------------------------------------------------

    def after_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        self.logger.info(
            "Pipeline '%s' completed successfully.",
            context.config.name,
        )

    # ---------------------------------------------------------

    def on_pipeline_error(
        self,
        context: PipelineContext,
        exception: Exception,
    ) -> None:

        self.logger.exception(
            "Pipeline '%s' failed: %s",
            context.config.name,
            exception,
        )

    # ---------------------------------------------------------

    def before_step(
        self,
        context: PipelineContext,
        step_name: str,
    ) -> None:

        self.logger.info(
            "Executing step '%s'.",
            step_name,
        )

    # ---------------------------------------------------------

    def after_step(
        self,
        context: PipelineContext,
        step_name: str,
    ) -> None:

        self.logger.info(
            "Completed step '%s'.",
            step_name,
        )

    # ---------------------------------------------------------

    def on_step_error(
        self,
        context: PipelineContext,
        step_name: str,
        exception: Exception,
    ) -> None:

        self.logger.exception(
            "Step '%s' failed: %s",
            step_name,
            exception,
        )
