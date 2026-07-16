"""
DataForge PostgreSQL Connector

Provides PostgreSQL connectivity for DataForge.
"""

from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extensions import connection

from connectors.base.base_connector import BaseConnector
from connectors.base.types import ConnectionResult, ConnectionStatus
from connectors.config.connector_config import ConnectorConfig


class PostgreSQLConnector(BaseConnector):
    """
    PostgreSQL connector implementation.

    Supports:

    - Connection management
    - Connection testing
    - Reading data
    - Writing data
    - Metadata discovery

    Future versions will support:

    - Connection pooling
    - Bulk loading
    - COPY operations
    - Transactions
    - DataFrame support
    - Async execution
    """

    VERSION = "1.0.0"

    DISPLAY_NAME = "PostgreSQL"

    def __init__(
        self,
        config: ConnectorConfig,
    ) -> None:

        super().__init__(config)

        self._connection: connection | None = None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @classmethod
    def get_metadata(cls) -> dict:
        """
        Return connector metadata.
        """

        return {
            "name": "postgresql",
            "display_name": cls.DISPLAY_NAME,
            "version": cls.VERSION,
            "description": "PostgreSQL database connector.",
            "supports": {
                "batch": True,
                "streaming": False,
                "incremental": True,
                "transactions": True,
                "schema_discovery": True,
            },
            "capabilities": [
                "connect",
                "disconnect",
                "test_connection",
                "extract",
                "read",
                "write",
            ],
        }

    # ---------------------------------------------------------
    # Connection Management
    # ---------------------------------------------------------

    def connect(self) -> ConnectionResult:
        """
        Establish a PostgreSQL connection.
        """

        if self.connected:

            return ConnectionResult(
                success=True,
                status=ConnectionStatus.CONNECTED,
                message="Already connected.",
            )

        try:

            self._connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                connect_timeout=self.config.timeout,
            )

            self._connected = True

            return ConnectionResult(
                success=True,
                status=ConnectionStatus.CONNECTED,
                message="Connected successfully.",
            )

        except Exception as ex:

            self._connected = False

            return ConnectionResult(
                success=False,
                status=ConnectionStatus.FAILED,
                message=str(ex),
            )

    # ---------------------------------------------------------

    def disconnect(self) -> ConnectionResult:
        """
        Close the PostgreSQL connection.
        """

        if self._connection is not None:

            self._connection.close()

            self._connection = None

        self._connected = False

        return ConnectionResult(
            success=True,
            status=ConnectionStatus.DISCONNECTED,
            message="Disconnected successfully.",
        )

    # ---------------------------------------------------------

    def test_connection(self) -> bool:
        """
        Test database connectivity.
        """

        result = self.connect()

        self.disconnect()

        return result.success

    # ---------------------------------------------------------
    # Data Operations
    # ---------------------------------------------------------

    def extract(
        self,
        query: str,
        parameters: tuple[Any, ...] | None = None,
    ) -> list[tuple]:
        """
        Extract records from PostgreSQL.

        Enterprise ETL alias for read().
        """

        return self.read(
            query,
            parameters,
        )

    # ---------------------------------------------------------

    def read(
        self,
        query: str,
        parameters: tuple[Any, ...] | None = None,
    ) -> list[tuple]:
        """
        Execute a SELECT query.
        """

        if not self.connected:

            result = self.connect()

            if not result.success:
                raise RuntimeError(result.message)

        assert self._connection is not None

        with self._connection.cursor() as cursor:

            cursor.execute(
                query,
                parameters,
            )

            return cursor.fetchall()

    # ---------------------------------------------------------

    def write(
        self,
        query: str,
        parameters: tuple[Any, ...] | None = None,
    ) -> int:
        """
        Execute INSERT, UPDATE or DELETE statements.
        """

        if not self.connected:

            result = self.connect()

            if not result.success:
                raise RuntimeError(result.message)

        assert self._connection is not None

        with self._connection.cursor() as cursor:

            cursor.execute(
                query,
                parameters,
            )

            self._connection.commit()

            return cursor.rowcount

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def connection(self) -> connection | None:
        """
        Active psycopg2 connection.
        """

        return self._connection

    # ---------------------------------------------------------

    @property
    def connected(self) -> bool:
        """
        Whether the connector is connected.
        """

        return (
            self._connected
            and self._connection is not None
            and not self._connection.closed
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:
        """
        String representation of the connector.
        """

        return (
            "PostgreSQLConnector("
            f"database='{self.config.database}', "
            f"host='{self.config.host}', "
            f"connected={self.connected})"
        )
