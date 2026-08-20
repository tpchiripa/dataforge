"""
DataForge Validation Step

Pipeline step responsible for validating extracted data.
"""

from __future__ import annotations

import pandas as pd

from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep
from storage.lakehouse.layer import MedallionLayer
from storage.lakehouse.manager import LakehouseManager


class ValidationStep(BaseStep):
    """
    Validate pipeline data before loading.

    Performs baseline validation and records quality metrics
    for downstream monitoring. When a LakehouseManager is
    supplied, validated data is landed in the Silver layer of
    the lakehouse once validation passes.

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
        lakehouse: LakehouseManager | None = None,
        source: str | None = None,
        table: str | None = None,
    ) -> None:

        super().__init__(
            name=name,
            description="Validate pipeline data.",
        )

        self.lakehouse = lakehouse
        self.source = source
        self.table = table

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Validate the dataframe stored in context.data.
        """

        dataframe = context.data

        if dataframe is None:

            raise PipelineValidationError(
                "No dataframe found in pipeline context.",
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):

            raise PipelineValidationError(
                "Pipeline object is not a pandas DataFrame.",
            )

        if dataframe.empty:

            raise PipelineValidationError(
                "Pipeline dataframe is empty.",
            )

        records = len(dataframe)

        columns = len(dataframe.columns)

        missing_values = int(
            dataframe.isna()
            .sum()
            .sum()
        )

        duplicate_rows = int(
            dataframe.duplicated()
            .sum()
        )

        # -----------------------------------------------------
        # Warnings
        # -----------------------------------------------------

        if missing_values > 0:

            context.add_warning(
                f"{missing_values} missing values detected.",
            )

        if duplicate_rows > 0:

            context.add_warning(
                f"{duplicate_rows} duplicate rows detected.",
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

        context.records_read(
            records,
        )

        # -----------------------------------------------------
        # Land validated data in the Silver layer
        # -----------------------------------------------------

        if self.lakehouse is not None:

            filename = f"{context.execution_id}.csv"

            silver_object = self.lakehouse.write_bytes(
                layer=MedallionLayer.SILVER,
                source=self.source or "pipeline",
                table=self.table or self.name,
                filename=filename,
                data=dataframe.to_csv(index=False).encode("utf-8"),
                content_type="text/csv",
            )

            context.add_metadata(
                "silver_key",
                silver_object.key,
            )