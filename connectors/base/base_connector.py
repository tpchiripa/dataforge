"""
DataForge Base Connector

Defines the abstract interface that every DataForge connector must
implement.

All connectors (PostgreSQL, MySQL, Oracle, SAP, REST APIs, Kafka,
S3, Azure, Salesforce, etc.) inherit from this class.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from connectors.config.connector_config import ConnectorConfig


class BaseConnector(ABC):
    """
    Abstract base class for every DataForge connector.
    """

    def __init__(
        self,
        config: ConnectorConfig,
    ) -> None:

        self.config = config

        self._connected = False

    # ---------------------------------------------------------
    # Connection Management
    # ---------------------------------------------------------

    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the connection.
        """

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test connectivity.

        Returns
        -------
        bool
            True if the connection succeeds.
        """

    # ---------------------------------------------------------
    # Data Operations
    # ---------------------------------------------------------

    @abstractmethod
    def read(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Read data from the source.
        """

    @abstractmethod
    def write(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Write data to the source.
        """

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def connected(self) -> bool:
        """
        Returns connection status.
        """

        return self._connected

    # ---------------------------------------------------------

    def __enter__(self):

        self.connect()

        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:

        self.disconnect()

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.config.name}', "
            f"connected={self.connected})"
        )
