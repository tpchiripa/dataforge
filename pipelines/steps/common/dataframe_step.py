"""
DataForge DataFrame Step

Generic step for applying DataFrame transformations.
"""

from __future__ import annotations

from typing import Callable

import pandas as pd

from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class DataFrameStep(BaseStep):
    """
    Execute a Pandas DataFrame operation.

    The operation receives ``context.data`` and must return
    a transformed DataFrame.
    """

    def __init__(
        self,
        name: str,
        operation: Callable[
            [pd.DataFrame],
            pd.DataFrame,
        ],
        description: str = "",
    ) -> None:

        super().__init__(
            name=name,
            description=(
                description
                or "DataFrame operation."
            ),
        )

        self.operation = operation

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:

        dataframe = context.data

        if dataframe is None:

            raise ValueError(
                "No dataframe found in pipeline context.",
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):

            raise TypeError(
                "Pipeline data must be a pandas DataFrame.",
            )

        transformed = self.operation(
            dataframe,
        )

        if not isinstance(
            transformed,
            pd.DataFrame,
        ):

            raise TypeError(
                "Operation must return a pandas DataFrame.",
            )

        context.data = transformed

        context.add_metadata(
            "dataframe_step",
            self.name,
        )

        context.add_metadata(
            "rows_after_dataframe_step",
            len(transformed),
        )

        context.add_metadata(
            "columns_after_dataframe_step",
            len(transformed.columns),
        )
