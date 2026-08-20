"""
DataForge Extract Step
Pipeline step responsible for extracting data from a connector.
"""
from __future__ import annotations
from connectors.base import BaseConnector
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep
from storage.lakehouse.layer import MedallionLayer
from storage.lakehouse.manager import LakehouseManager
class ExtractStep(BaseStep):
    """
    Extract data from a configured connector.
    The extracted dataset is placed into the execution context
    for downstream pipeline steps. When a LakehouseManager is
    supplied, the raw extracted dataset is also landed in the
    Bronze layer of the lakehouse.
    """
    def __init__(
        self,
        name: str,
        connector: BaseConnector,
        query: str,
        lakehouse: LakehouseManager | None = None,
        source: str | None = None,
        table: str | None = None,
    ) -> None:
        super().__init__(
            name=name,
            description="Extract data from a source connector.",
        )
        self.connector = connector
        self.query = query
        self.lakehouse = lakehouse
        self.source = source
        self.table = table
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
            self.connector.get_metadata()["name"],
        )
        context.add_metadata(
            "extract_query",
            self.query,
        )
        # -----------------------------------------------------
        # Land raw data in the Bronze layer
        # -----------------------------------------------------
        if self.lakehouse is not None:
            filename = f"{context.execution_id}.csv"
            bronze_object = self.lakehouse.write_bytes(
                layer=MedallionLayer.BRONZE,
                source=self.source or self.connector.get_metadata()["name"],
                table=self.table or self.name,
                filename=filename,
                data=dataframe.to_csv(index=False).encode("utf-8"),
                content_type="text/csv",
            )
            context.add_metadata(
                "bronze_key",
                bronze_object.key,
            )