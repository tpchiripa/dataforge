"""
DataForge Pipeline Hook

Base class for pipeline lifecycle hooks.
"""

from __future__ import annotations

from abc import ABC


class PipelineHook(ABC):
    """
    Base class for DataForge lifecycle hooks.

    Hooks allow custom logic to be executed during
    pipeline execution without modifying the
    PipelineExecutor itself.

    Examples
    --------
    - LoggingHook
    - MetricsHook
    - AuditHook
    - NotificationHook
    - LineageHook
    """

    # ---------------------------------------------------------
    # Pipeline Events
    # ---------------------------------------------------------

    def before_pipeline(
        self,
        context,
    ) -> None:
        """
        Called before pipeline execution starts.
        """

        pass

    # ---------------------------------------------------------

    def after_pipeline(
        self,
        context,
    ) -> None:
        """
        Called after successful pipeline execution.
        """

        pass

    # ---------------------------------------------------------

    def on_pipeline_error(
        self,
        context,
        exception: Exception,
    ) -> None:
        """
        Called when pipeline execution fails.
        """

        pass

    # ---------------------------------------------------------
    # Step Events
    # ---------------------------------------------------------

    def before_step(
        self,
        step,
        context,
    ) -> None:
        """
        Called before a pipeline step executes.
        """

        pass

    # ---------------------------------------------------------

    def after_step(
        self,
        step,
        context,
    ) -> None:
        """
        Called after a pipeline step executes.
        """

        pass

    # ---------------------------------------------------------

    def on_step_error(
        self,
        step,
        context,
        exception: Exception,
    ) -> None:
        """
        Called when a pipeline step fails.
        """

        pass

    # ---------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Hook name.
        """

        return self.__class__.__name__

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return f"{self.name}()"
