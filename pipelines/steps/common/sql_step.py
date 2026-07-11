"""
DataForge SQL Step

Execute SQL transformations against the pipeline DataFrame.
"""

from __future__ import annotations

import duckdb
import pandas as pd

from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class SQLStep(BaseStep):
    """
    Execute SQL against the pipeline DataFrame.

    The incoming DataFrame is exposed as a table named
    'dataframe'.

    Example
    -------
    SELECT *
    FROM dataframe
    WHERE amount > 100
    """

    def __init__(
        self,
        name: str,
        query: str,
    ):

        super().__init__(
            name=name,
            description="Execute SQL transformation.",
        )

        self.query = query

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the SQL query.
        """

        dataframe = context.data.get("dataframe")

        if dataframe is None:

            raise ValueError(
                "No dataframe found in pipeline context."
            )

        if not isinstance(dataframe, pd.DataFrame):

            raise TypeError(
                "Context object is not a pandas DataFrame."
            )

        connection = duckdb.connect()

        try:

            connection.register(
                "dataframe",
                dataframe,
            )

            result = connection.execute(
                self.query
            ).fetchdf()

        finally:

            connection.close()

        context.data["dataframe"] = result

        context.add_metadata(
            "sql_step",
            self.name,
        )

        context.add_metadata(
            "sql_query",
            self.query,
        )

        context.add_metadata(
            "rows_after_sql",
            len(result),
        )

        context.add_metadata(
            "columns_after_sql",
            len(result.columns),
        )
