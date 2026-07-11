"""
DataForge Base Step

Base implementation for every executable DataForge pipeline step.
"""

from __future__ import annotations

from abc import abstractmethod
from datetime import datetime

from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_step import PipelineStep


class BaseStep(PipelineStep):
    """
    Base class for every executable DataForge step.

    All Extract, Transform, Validation and Load steps inherit
    from this class.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
    ):

        super().__init__(name)

        self.description = description

        self.enabled = True

        self.started_at = None

        self.finished_at = None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def step_type(self) -> str:
        """
        Return the step type.

        Example:
            extract
            transform
            validation
            load
        """

        return self.__class__.__name__.replace(
            "Step",
            "",
        ).lower()

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:

        self.started_at = datetime.utcnow()

        context.add_metadata(
            f"{self.name}.started_at",
            self.started_at.isoformat(),
        )

    # ---------------------------------------------------------

    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the step.

        Every subclass must implement this.
        """

        ...

    # ---------------------------------------------------------

    def after_execute(
        self,
        context: PipelineContext,
    ) -> None:

        self.finished_at = datetime.utcnow()

        context.add_metadata(
            f"{self.name}.finished_at",
            self.finished_at.isoformat(),
        )

    # ---------------------------------------------------------

    @property
    def duration_seconds(self) -> float:

        if self.started_at is None:

            return 0.0

        if self.finished_at is None:

            return 0.0

        return (
            self.finished_at - self.started_at
        ).total_seconds()

    # ---------------------------------------------------------

    def enable(self) -> None:

        self.enabled = True

    # ---------------------------------------------------------

    def disable(self) -> None:

        self.enabled = False

    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"enabled={self.enabled})"
        )
