"""
DataForge Load Step
Pipeline step responsible for loading transformed data
to a destination.
"""
from __future__ import annotations
from pathlib import Path
from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep
from storage.lakehouse.layer import MedallionLayer
from storage.lakehouse.manager import LakehouseManager
class LoadStep(BaseStep):
    """
    Load transformed data to a destination.
    Currently supports:
    - CSV
    - Parquet
    When a LakehouseManager is supplied, the written output is
    also landed in the Gold layer of the lakehouse.
    Future versions will support:
    - PostgreSQL
    - SQL Server
    - MySQL
    - MinIO
    - S3
    - Delta Lake
    - Apache Iceberg
    - Kafka
    """
    _CONTENT_TYPES = {
        "csv": "text/csv",
        "parquet": "application/octet-stream",
    }
    def __init__(
        self,
        name: str,
        output_path: str | Path,
        file_format: str = "csv",
        index: bool = False,
        lakehouse: LakehouseManager | None = None,
        source: str | None = None,
        table: str | None = None,
    ):
        super().__init__(
            name=name,
            description="Load transformed data.",
        )
        self.output_path = Path(
            output_path,
        )
        self.file_format = (
            file_format.lower()
        )
        self.index = index
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
        Load the dataframe.
        """
        dataframe = context.data
        if dataframe is None:
            raise ValueError(
                "No dataframe found in pipeline context."
            )
        # -----------------------------------------------------
        # Validate dataframe interface
        # -----------------------------------------------------
        if not hasattr(dataframe, "to_csv"):
            raise TypeError(
                "Pipeline data does not support dataframe output."
            )
        # -----------------------------------------------------
        # Create output directory
        # -----------------------------------------------------
        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        # -----------------------------------------------------
        # Write output
        # -----------------------------------------------------
        if self.file_format == "csv":
            dataframe.to_csv(
                self.output_path,
                index=self.index,
            )
        elif self.file_format == "parquet":
            dataframe.to_parquet(
                self.output_path,
                index=self.index,
            )
        else:
            raise ValueError(
                f"Unsupported file format: "
                f"{self.file_format}"
            )
        # -----------------------------------------------------
        # Record load metrics
        # -----------------------------------------------------
        records = len(dataframe)
        context.records_written(
            records,
        )
        # -----------------------------------------------------
        # Execution Metadata
        # -----------------------------------------------------
        context.add_metadata(
            "records_loaded",
            records,
        )
        context.add_metadata(
            "records_written",
            records,
        )
        context.add_metadata(
            "output_format",
            self.file_format,
        )
        context.add_metadata(
            "output_location",
            str(self.output_path),
        )
        context.add_metadata(
            "load_completed",
            True,
        )
        # -----------------------------------------------------
        # Land loaded data in the Gold layer
        # -----------------------------------------------------
        if self.lakehouse is not None:

            data = self.output_path.read_bytes()

            gold_object = self.lakehouse.write_bytes(
                layer=MedallionLayer.GOLD,
                source=self.source or "pipeline",
                table=self.table or self.name,
                filename=self.output_path.name,
                data=data,
                content_type=self._CONTENT_TYPES.get(
                    self.file_format,
                    "application/octet-stream",
                ),
            )

            context.add_metadata(
                "gold_key",
                gold_object.key,
            )