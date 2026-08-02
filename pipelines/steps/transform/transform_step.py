"""
DataForge Transform Step

Pipeline step responsible for transforming pipeline data.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class TransformStep(BaseStep):
    """
    Transform pipeline data.

    A transformation is a callable that accepts the current
    pipeline dataset and returns the transformed dataset.
    """

    def __init__(
        self,
        name: str,
        transformation: Callable[[Any], Any],
    ) -> None:

        super().__init__(
            name=name,
            description="Transform pipeline data.",
        )

        self.transformation = transformation

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the transformation.
        """

        if context.data is None:

            raise ValueError(
                "No input data available for transformation."
            )

        transformed = self.transformation(
            context.data,
        )

        context.data = transformed

        context.set(
            "records_transformed",
            len(transformed),
        )

        context.add_metadata(
            "records_transformed",
            len(transformed),
        )

        context.add_metadata(
            "columns_after_transformation",
            len(transformed.columns),
        )

        context.add_metadata(
            "transformation",
            self.name,
        )
