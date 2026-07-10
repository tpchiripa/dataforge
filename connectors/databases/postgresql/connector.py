"""
DataForge PostgreSQL Connector
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from sqlalchemy import URL, create_engine, inspect, text

from connectors.base import (
    BaseConnector,
    ConnectionFailedError,
    ConnectionResult,
    ConnectionStatus,
    ConnectorConfig,
    ConnectorMetadata,
    ConnectorType,
    DatasetInfo,
    ExtractionResult,
)


class PostgreSQLConnector(BaseConnector):
    """
    PostgreSQL implementation of the DataForge Connector SDK.
    """

    def __init__(self, config: ConnectorConfig):
        super().__init__(config)
        self.engine = None

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    def connect(self) -> ConnectionResult:

        try:

            url = URL.create(
                drivername="postgresql+psycopg2",
                username=self.config.username,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
            )

            print("\n" + "=" * 80)
            print("DataForge PostgreSQL Connector")
            print("=" * 80)
            print(f"Host      : {self.config.host}")
            print(f"Port      : {self.config.port}")
            print(f"Database  : {self.config.database}")
            print(f"Username  : {self.config.username}")
            print(f"Password  : {self.config.password}")
            print(f"URL       : {url}")
            print("=" * 80 + "\n")

            self.engine = create_engine(
                url,
                pool_pre_ping=True,
                future=True,
            )

            self.connection = self.engine.connect()

            self.connected = True

            return ConnectionResult(
                success=True,
                status=ConnectionStatus.CONNECTED,
                message="Successfully connected to PostgreSQL.",
            )

        except Exception as exc:

            self.connected = False

            raise ConnectionFailedError(str(exc))

    # ---------------------------------------------------------

    def disconnect(self):

        if self.connection is not None:
            self.connection.close()

        if self.engine is not None:
            self.engine.dispose()

        self.connected = False

    # ---------------------------------------------------------

    def test_connection(self):

        return self.connect()

    # ---------------------------------------------------------

    def validate(self):

        required = [
            self.config.host,
            self.config.port,
            self.config.database,
            self.config.username,
            self.config.password,
        ]

        return all(required)

    # ---------------------------------------------------------

    @staticmethod
    def get_metadata() -> ConnectorMetadata:
        """
        Return metadata describing this connector.
        """

        return ConnectorMetadata(
            name="PostgreSQL",
            version="1.0.0",
            description="PostgreSQL Database Connector",
            author="DataForge",
            connector_type=ConnectorType.DATABASE,
            supports_batch=True,
            supports_streaming=False,
            supports_incremental=True,
            tags=[
                "postgresql",
                "database",
                "sql",
            ],
        )

    # ---------------------------------------------------------

    def list_datasets(self):

        if not self.connected:
            self.connect()

        inspector = inspect(self.engine)

        datasets = []

        for table in inspector.get_table_names():

            datasets.append(
                DatasetInfo(
                    name=table,
                    schema="public",
                )
            )

        return datasets

    # ---------------------------------------------------------

    def fetch_dataframe(self, query: str):

        if not self.connected:
            self.connect()

        return pd.read_sql(text(query), self.engine)

    # ---------------------------------------------------------

    def extract(
        self,
        query: str,
        output_location: str = "",
    ):

        start = datetime.utcnow()

        df = self.fetch_dataframe(query)

        duration = (datetime.utcnow() - start).total_seconds()

        return ExtractionResult(
            success=True,
            records=len(df),
            duration_seconds=duration,
            output_location=output_location,
            metadata={
                "columns": list(df.columns),
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
