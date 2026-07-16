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
    Extract data from a connector.

    The extracted data is stored in the pipeline context for
    downstream steps.
    """

    def __init__(
        self,
        name: str,
        connector: BaseConnector,
        query: str,
    ):

        super().__init__(
            name=name,
            description="Extract data from a source connector.",
        )

        self.connector = connector

        self.query = query

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the extraction step.
        """

        if not self.connector.connected:

            self.connector.connect()

        dataframe = self.connector.fetch_dataframe(
            self.query
        )

        context.data["dataframe"] = dataframe

        context.add_metadata(
            "records_extracted",
            len(dataframe),
        )

        context.add_metadata(
            "source_connector",
            self.connector.get_metadata().name,
        )
