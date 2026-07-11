"""
DataForge Pipeline Status
"""

from enum import Enum


class PipelineStatus(str, Enum):
    """
    Execution status of a pipeline.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    VALIDATING = "validating"

    EXTRACTING = "extracting"

    TRANSFORMING = "transforming"

    LOADING = "loading"
