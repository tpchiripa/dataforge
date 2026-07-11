"""
DataForge Validation Step

Pipeline step responsible for validating extracted data.
"""

from __future__ import annotations

import pandas as pd

from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class ValidationStep(BaseStep):
    """
    Validate extracted data before transformation.

    This step performs generic validation checks.

    Future versions will support:

    - Schema validation
    - Data quality rules
    - Great Expectations
    - Custom validation plugins
    """

    def __init__(
        self,
        name: str = "Validation",
    ):

        super().__init__(
            name=name,
            description="Validate extracted data.",
        )

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Validate the extracted dataframe.
        """

        dataframe = context.data.get("dataframe")

        if dataframe is None:

            raise PipelineValidationError(
                "No dataframe found in pipeline context."
            )

        if not isinstance(dataframe, pd.DataFrame):

            raise PipelineValidationError(
                "Context object is not a pandas DataFrame."
            )

        if dataframe.empty:

            raise PipelineValidationError(
                "Extracted dataframe is empty."
            )

        records = len(dataframe)

        columns = len(dataframe.columns)

        missing_values = int(
            dataframe.isna().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        context.add_metadata(
            "records_validated",
            records,
        )

        context.add_metadata(
            "column_count",
            columns,
        )

        context.add_metadata(
            "missing_values",
            missing_values,
        )

        context.add_metadata(
            "duplicate_rows",
            duplicate_rows,
        )

        context.add_metadata(
            "validation_passed",
            True,
        )
