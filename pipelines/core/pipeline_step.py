"""
DataForge Pipeline Step

Defines the base class for every pipeline step.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .pipeline_context import PipelineContext


class PipelineStep(ABC):
    """
    Abstract base class for every DataForge pipeline step.

    Examples
    --------
    - ExtractStep
    - ValidationStep
    - TransformStep
    - LoadStep
    - SparkStep
    - AIInferenceStep
    """

    def __init__(self, name: str):

        self.name = name

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Called immediately before execution.

        Can be overridden by subclasses.
        """

        pass

    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the pipeline step.

        Must be implemented by subclasses.
        """

        ...

    def after_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Called after successful execution.

        Can be overridden by subclasses.
        """

        pass

    def on_error(
        self,
        context: PipelineContext,
        exception: Exception,
    ) -> None:
        """
        Called when execution fails.

        Default behaviour is to record the error
        inside the pipeline context.
        """

        context.add_error(str(exception))

    # ---------------------------------------------------------
    # Runner
    # ---------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the full lifecycle of a pipeline step.
        """

        try:

            self.before_execute(context)

            self.execute(context)

            self.after_execute(context)

        except Exception as exc:

            self.on_error(
                context,
                exc,
            )

            raise

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(name='{self.name}')"
