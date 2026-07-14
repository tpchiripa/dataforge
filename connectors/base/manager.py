"""
DataForge Connector Manager

Responsible for managing live connector instances.

The ConnectorManager sits above the ConnectorFactory and provides
a central place for creating, retrieving, connecting and
disconnecting connectors.

Example
-------
>>> manager = ConnectorManager()
>>> manager.create("postgresql", config)
>>> manager.connect_all()
>>> connector = manager.get("postgresql")
>>> manager.disconnect_all()
"""

from __future__ import annotations

from connectors.config.connector_config import ConnectorConfig

from .base_connector import BaseConnector
from .factory import ConnectorFactory


class ConnectorManager:
    """
    Manages DataForge connector instances.
    """

    def __init__(
        self,
        factory: ConnectorFactory | None = None,
    ) -> None:

        self._factory = factory or ConnectorFactory()

        self._connectors: dict[str, BaseConnector] = {}

    # ---------------------------------------------------------
    # Connector Creation
    # ---------------------------------------------------------

    def create(
        self,
        connector_name: str,
        config: ConnectorConfig,
    ) -> BaseConnector:
        """
        Create and store a connector.
        """

        connector = self._factory.create(
            connector_name,
            config,
        )

        self._connectors[
            connector_name.lower()
        ] = connector

        return connector

    # ---------------------------------------------------------

    def get(
        self,
        connector_name: str,
    ) -> BaseConnector | None:
        """
        Return an existing connector.
        """

        return self._connectors.get(
            connector_name.lower()
        )

    # ---------------------------------------------------------

    def exists(
        self,
        connector_name: str,
    ) -> bool:
        """
        Check whether a connector exists.
        """

        return (
            connector_name.lower()
            in self._connectors
        )

    # ---------------------------------------------------------

    def remove(
        self,
        connector_name: str,
    ) -> None:
        """
        Remove a connector.
        """

        connector = self._connectors.pop(
            connector_name.lower(),
            None,
        )

        if connector is not None and connector.connected:

            connector.disconnect()

    # ---------------------------------------------------------
    # Connection Management
    # ---------------------------------------------------------

    def connect_all(self) -> None:
        """
        Connect every managed connector.
        """

        for connector in self._connectors.values():

            if not connector.connected:

                connector.connect()

    # ---------------------------------------------------------

    def disconnect_all(self) -> None:
        """
        Disconnect every managed connector.
        """

        for connector in self._connectors.values():

            if connector.connected:

                connector.disconnect()

    # ---------------------------------------------------------
    # Collection Helpers
    # ---------------------------------------------------------

    def list(self) -> list[str]:
        """
        Return connector names.
        """

        return sorted(
            self._connectors.keys()
        )

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all connectors.
        """

        self.disconnect_all()

        self._connectors.clear()

    # ---------------------------------------------------------

    def connected(self) -> list[BaseConnector]:
        """
        Return connected connector instances.
        """

        return [
            connector
            for connector in self._connectors.values()
            if connector.connected
        ]

    # ---------------------------------------------------------

    def disconnected(self) -> list[BaseConnector]:
        """
        Return disconnected connector instances.
        """

        return [
            connector
            for connector in self._connectors.values()
            if not connector.connected
        ]

    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        """
        Number of managed connectors.
        """

        return len(self._connectors)

    # ---------------------------------------------------------
    # Dunder Methods
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.count

    # ---------------------------------------------------------

    def __contains__(
        self,
        connector_name: str,
    ) -> bool:

        return self.exists(
            connector_name
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._connectors.values()
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorManager("
            f"connectors={self.count}, "
            f"connected={len(self.connected())})"
        )
