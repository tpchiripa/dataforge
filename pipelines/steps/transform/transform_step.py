"""
DataForge Transform Step

Pipeline step responsible for transforming data.
"""

from __future__ import annotations

from typing import Callable

import pandas as pd

from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class TransformStep(BaseStep):
    """
    Transform data inside the pipeline.

    A transformation is simply a callable that accepts a
    pandas DataFrame and returns a transformed DataFrame.
    """

    def __init__(
        self,
        name: str,
        transformation: Callable[[pd.DataFrame], pd.DataFrame],
    ):

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

        dataframe = context.data.get("dataframe")

        if dataframe is None:

            raise ValueError(
                "No dataframe found in pipeline context."
            )

        transformed = self.transformation(dataframe)

        context.data["dataframe"] = transformed

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
