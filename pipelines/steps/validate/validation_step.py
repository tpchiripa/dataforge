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
    Validate pipeline data before loading.

    Performs baseline validation and records
    quality metrics for downstream monitoring.

    Future versions will support:

    - Schema validation
    - Great Expectations
    - Custom validation plugins
    - Business rules
    - Referential integrity
    """

    def __init__(
        self,
        name: str = "Validation",
    ):

        super().__init__(
            name=name,
            description="Validate pipeline data.",
        )

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Validate the dataframe.
        """

        dataframe = context.data.get("dataframe")

        if dataframe is None:
            raise PipelineValidationError(
                "No dataframe found in pipeline context."
            )

        if not isinstance(dataframe, pd.DataFrame):
            raise PipelineValidationError(
                "Pipeline object is not a pandas DataFrame."
            )

        if dataframe.empty:
            raise PipelineValidationError(
                "Pipeline dataframe is empty."
            )

        records = len(dataframe)

        columns = len(dataframe.columns)

        missing_values = int(
            dataframe.isna().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        # -----------------------------------------------------
        # Warnings
        # -----------------------------------------------------

        if missing_values > 0:

            context.add_warning(
                f"{missing_values} missing values detected."
            )

        if duplicate_rows > 0:

            context.add_warning(
                f"{duplicate_rows} duplicate rows detected."
            )

        # -----------------------------------------------------
        # Validation Summary
        # -----------------------------------------------------

        validation_summary = {
            "records": records,
            "columns": columns,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "passed": True,
        }

        context.add_metadata(
            "validation",
            validation_summary,
        )

        context.add_metadata(
            "records_validated",
            records,
        )

        context.add_metadata(
            "validation_passed",
            True,
        )
