"""
DataForge Load Step

Pipeline step responsible for loading transformed data
to a destination.
"""

from __future__ import annotations

from pathlib import Path


from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class LoadStep(BaseStep):
    """
    Load transformed data to a destination.

    Currently supports:

    - CSV
    - Parquet

    Future versions will support:

    - PostgreSQL
    - SQL Server
    - MySQL
    - MinIO
    - S3
    - Delta Lake
    - Iceberg
    - Kafka
    """

    def __init__(
        self,
        name: str,
        output_path: str | Path,
        file_format: str = "csv",
        index: bool = False,
    ):

        super().__init__(
            name=name,
            description="Load transformed data.",
        )

        self.output_path = Path(output_path)

        self.file_format = file_format.lower()

        self.index = index

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Load the dataframe.
        """

        dataframe = context.data.get("dataframe")

        if dataframe is None:

            raise ValueError(
                "No dataframe found in pipeline context."
            )

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

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
                f"Unsupported file format: {self.file_format}"
            )

        context.add_metadata(
            "records_loaded",
            len(dataframe),
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
