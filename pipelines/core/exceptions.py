"""
DataForge Pipeline Exceptions

Exception hierarchy for the Pipeline Engine.
"""

from __future__ import annotations


class PipelineError(Exception):
    """
    Base exception for all pipeline-related errors.
    """

    pass


class PipelineConfigurationError(PipelineError):
    """
    Raised when a pipeline configuration is invalid.
    """

    pass


class PipelineValidationError(PipelineError):
    """
    Raised when pipeline validation fails.
    """

    pass


class PipelineExecutionError(PipelineError):
    """
    Raised when pipeline execution fails.
    """

    pass


class PipelineTimeoutError(PipelineExecutionError):
    """
    Raised when a pipeline exceeds its execution timeout.
    """

    pass


class PipelineCancelledError(PipelineExecutionError):
    """
    Raised when a pipeline is cancelled.
    """

    pass


class PipelineStepError(PipelineExecutionError):
    """
    Raised when a pipeline step fails.

    Attributes
    ----------
    step_name:
        Name of the step that failed.
    """

    def __init__(
        self,
        step_name: str,
        message: str,
    ):

        self.step_name = step_name

        super().__init__(f"[{step_name}] {message}")


class PipelineNotFoundError(PipelineError):
    """
    Raised when a requested pipeline cannot be found.
    """

    pass


class DuplicatePipelineError(PipelineError):
    """
    Raised when attempting to register an existing pipeline.
    """

    pass
