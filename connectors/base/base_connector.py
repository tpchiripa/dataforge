"""
DataForge Base Connector

Defines the abstract interface that every DataForge connector must
implement.

All connectors (PostgreSQL, MySQL, Oracle, SAP, REST APIs, Kafka,
S3, Azure, Salesforce, etc.) inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
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
    def connect(
        self,
    ) -> None:
        """
        Establish a connection.
        """

    @abstractmethod
    def disconnect(
        self,
    ) -> None:
        """
        Close the connection.
        """

    @abstractmethod
    def test_connection(
        self,
    ) -> bool:
        """
        Test connectivity.
        """

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @abstractmethod
    def validate_configuration(
        self,
    ) -> None:
        """
        Validate connector configuration.
        """

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        return self.config.name

    # ---------------------------------------------------------

    @property
    def connector_type(
        self,
    ) -> str:
        return self.__class__.__name__

    # ---------------------------------------------------------

    @property
    def connected(
        self,
    ) -> bool:
        return self._connected

    # ---------------------------------------------------------

    @property
    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Capabilities supported by the connector.
        """

        return {
            "read": True,
            "write": True,
            "streaming": False,
            "transactions": False,
            "schema_discovery": False,
        }

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
        Read data.
        """

    @abstractmethod
    def write(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Write data.
        """

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_connect(
        self,
    ) -> None:
        """
        Hook executed before connect().
        """
        return

    # ---------------------------------------------------------

    def after_connect(
        self,
    ) -> None:
        """
        Hook executed after connect().
        """
        return

    # ---------------------------------------------------------

    def before_disconnect(
        self,
    ) -> None:
        """
        Hook executed before disconnect().
        """
        return

    # ---------------------------------------------------------

    def after_disconnect(
        self,
    ) -> None:
        """
        Hook executed after disconnect().
        """
        return

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Connector health information.
        """

        return {
            "name": self.name,
            "type": self.connector_type,
            "connected": self.connected,
        }

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(
        self,
    ):
        self.before_connect()
        self.connect()
        self.after_connect()
        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        self.before_disconnect()
        self.disconnect()
        self.after_disconnect()

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.connector_type}("
            f"name='{self.name}', "
            f"connected={self.connected})"
        )
