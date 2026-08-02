"""
DataForge Pipeline Registry

Central registry for managing DataForge pipelines.
"""

from __future__ import annotations

from collections import Counter

from pipelines.core.exceptions import (
    DuplicatePipelineError,
    PipelineNotFoundError,
)
from pipelines.core.pipeline import Pipeline


class PipelineRegistry:
    """
    Global registry responsible for storing DataForge pipelines.
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

        key = pipeline.config.name.lower()

        if key in cls._pipelines:
            raise DuplicatePipelineError(
                f"Pipeline '{pipeline.config.name}' already exists."
            )

        cls._pipelines[key] = pipeline

    # ---------------------------------------------------------

    @classmethod
    def update(
        cls,
        pipeline: Pipeline,
    ) -> None:
        """
        Replace an existing pipeline.
        """

        key = pipeline.config.name.lower()

        if key not in cls._pipelines:
            raise PipelineNotFoundError(
                pipeline.config.name
            )

        cls._pipelines[key] = pipeline

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        pipeline_name: str,
    ) -> None:

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

        pipeline = cls._pipelines.get(
            pipeline_name.lower()
        )

        if pipeline is None:
            raise PipelineNotFoundError(
                pipeline_name
            )

        return pipeline

    # ---------------------------------------------------------

    @classmethod
    def exists(
        cls,
        pipeline_name: str,
    ) -> bool:

        return pipeline_name.lower() in cls._pipelines

    # ---------------------------------------------------------
    # Listing
    # ---------------------------------------------------------

    @classmethod
    def list(
        cls,
    ) -> list[Pipeline]:

        return list(cls._pipelines.values())

    # ---------------------------------------------------------

    @classmethod
    def list_names(
        cls,
    ) -> list[str]:
        """
        Return display names.
        """

        return sorted(
            pipeline.config.name
            for pipeline in cls._pipelines.values()
        )

    # ---------------------------------------------------------

    @classmethod
    def list_pipelines(
        cls,
    ) -> list[str]:
        """
        Backwards-compatible alias.

        Returns the registry keys (lowercase names)
        expected by the legacy unit tests.
        """

        return sorted(
            cls._pipelines.keys()
        )

    # ---------------------------------------------------------
    # Searching
    # ---------------------------------------------------------

    @classmethod
    def find_by_owner(
        cls,
        owner: str,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if pipeline.config.owner.lower()
            == owner.lower()
        ]

    # ---------------------------------------------------------

    @classmethod
    def find_by_tag(
        cls,
        tag: str,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if tag.lower()
            in {
                t.lower()
                for t in pipeline.config.tags
            }
        ]

    # ---------------------------------------------------------

    @classmethod
    def find_by_source(
        cls,
        connector: str,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if pipeline.config.source_connector.lower()
            == connector.lower()
        ]

    # ---------------------------------------------------------

    @classmethod
    def find_by_destination(
        cls,
        connector: str,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if pipeline.config.destination_connector.lower()
            == connector.lower()
        ]

    # ---------------------------------------------------------

    @classmethod
    def enabled_pipelines(
        cls,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if pipeline.config.enabled
        ]

    # ---------------------------------------------------------

    @classmethod
    def scheduled_pipelines(
        cls,
    ) -> list[Pipeline]:

        return [
            pipeline
            for pipeline in cls.list()
            if pipeline.config.schedule
        ]

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @classmethod
    def statistics(
        cls,
    ) -> dict:

        owners = Counter()
        sources = Counter()
        destinations = Counter()

        for pipeline in cls.list():

            if pipeline.config.owner:
                owners[pipeline.config.owner] += 1

            if pipeline.config.source_connector:
                sources[
                    pipeline.config.source_connector
                ] += 1

            if pipeline.config.destination_connector:
                destinations[
                    pipeline.config.destination_connector
                ] += 1

        return {
            "registered": len(cls._pipelines),
            "enabled": len(cls.enabled_pipelines()),
            "disabled": len(cls._pipelines)
            - len(cls.enabled_pipelines()),
            "scheduled": len(
                cls.scheduled_pipelines()
            ),
            "owners": dict(owners),
            "source_connectors": dict(sources),
            "destination_connectors": dict(
                destinations
            ),
        }

    # ---------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._pipelines.clear()

    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:

        return len(self._pipelines)

    # ---------------------------------------------------------

    def __len__(
        self,
    ):

        return len(self._pipelines)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(self._pipelines.values())

    # ---------------------------------------------------------

    def __contains__(
        self,
        pipeline_name: str,
    ) -> bool:

        return self.exists(
            pipeline_name,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ):

        return (
            f"PipelineRegistry("
            f"count={len(self._pipelines)})"
        )
