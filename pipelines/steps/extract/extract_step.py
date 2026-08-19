"""
DataForge Extract Step

Pipeline step responsible for extracting data from a connector.
"""

from __future__ import annotations

from connectors.base import BaseConnector
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class ExtractStep(BaseStep):
    """
    Extract data from a configured connector.

    The extracted dataset is placed into the execution context
    for downstream pipeline steps.
    """

    def __init__(
        self,
        name: str,
        connector: BaseConnector,
        query: str,
    ) -> None:

        super().__init__(
            name=name,
            description="Extract data from a source connector.",
        )

        self.connector = connector
        self.query = query

    # =========================================================
    # Execution
    # =========================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the extraction step.
        """

        # -----------------------------------------------------
        # Connect to source
        # -----------------------------------------------------

        if not self.connector.connected:
            self.connector.connect()

        # -----------------------------------------------------
        # Extract data
        # -----------------------------------------------------

        dataframe = self.connector.fetch_dataframe(
            self.query,
        )

        # -----------------------------------------------------
        # Store extracted dataset
        # -----------------------------------------------------

        context.data = dataframe

        # -----------------------------------------------------
        # Record extraction metrics
        # -----------------------------------------------------

        records = len(dataframe)

        context.records_read(
            records,
        )

        # -----------------------------------------------------
        # Runtime variables
        # -----------------------------------------------------

        context.set(
            "records_extracted",
            records,
        )

        # -----------------------------------------------------
        # Execution metadata
        # -----------------------------------------------------

        context.add_metadata(
            "records_extracted",
            records,
        )

        context.add_metadata(
            "records_read",
            records,
        )

        context.add_metadata(
            "source_connector",
            self.connector.get_metadata().name,
        )

        context.add_metadata(
            "extract_query",
            self.query,
        )
