"""
DataForge Pipeline Registry

Central registry for DataForge pipelines.
"""

from __future__ import annotations

from pipelines.core.exceptions import (
    DuplicatePipelineError,
    PipelineNotFoundError,
)
from pipelines.core.pipeline import Pipeline


class PipelineRegistry:
    """
    Registry responsible for storing and managing pipelines.
    """

    _pipelines: dict[str, Pipeline] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        pipeline: Pipeline,
    ) -> None:
        """
        Register a pipeline.
        """

        name = pipeline.config.name.lower()

        if name in cls._pipelines:
            raise DuplicatePipelineError(
                f"Pipeline '{pipeline.config.name}' is already registered."
            )

        cls._pipelines[name] = pipeline

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        pipeline_name: str,
    ) -> None:
        """
        Remove a pipeline from the registry.
        """

        cls._pipelines.pop(
            pipeline_name.lower(),
            None,
        )

    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        pipeline_name: str,
    ) -> Pipeline:
        """
        Retrieve a registered pipeline.
        """

        pipeline = cls._pipelines.get(
            pipeline_name.lower()
        )

        if pipeline is None:
            raise PipelineNotFoundError(
                f"Pipeline '{pipeline_name}' is not registered."
            )

        return pipeline

    # ---------------------------------------------------------

    @classmethod
    def exists(
        cls,
        pipeline_name: str,
    ) -> bool:
        """
        Check whether a pipeline exists.
        """

        return pipeline_name.lower() in cls._pipelines

    # ---------------------------------------------------------

    @classmethod
    def list_pipelines(cls) -> list[str]:
        """
        Return all registered pipeline names.
        """

        return sorted(cls._pipelines.keys())

    # ---------------------------------------------------------

    @classmethod
    def list(cls) -> list[Pipeline]:
        """
        Return all registered pipeline objects.
        """

        return list(cls._pipelines.values())

    # ---------------------------------------------------------

    @classmethod
    def count(cls) -> int:
        """
        Return the number of registered pipelines.
        """

        return len(cls._pipelines)

    # ---------------------------------------------------------

    @classmethod
    def clear(cls) -> None:
        """
        Remove every registered pipeline.

        Primarily useful for testing.
        """

        cls._pipelines.clear()

    # ---------------------------------------------------------

    @classmethod
    def __contains__(
        cls,
        pipeline_name: str,
    ) -> bool:

        return cls.exists(pipeline_name)
