"""
DataForge Connector Manager

Responsible for creating, managing, and disposing connector instances.
"""

from __future__ import annotations

from connectors.base.base_connector import BaseConnector
from connectors.config.connector_config import ConnectorConfig
from connectors.exceptions import ConnectorNotFoundError
from connectors.factory.connector_factory import ConnectorFactory


class ConnectorManager:
    """
    Manages DataForge connector instances.

    The manager is responsible for:

    - Creating connectors
    - Opening connections
    - Closing connections
    - Reusing connector instances
    - Cleaning up resources
    """

    def __init__(self) -> None:

        self._connectors: dict[str, BaseConnector] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def create(
        self,
        connector_name: str,
        config: ConnectorConfig,
    ) -> BaseConnector:
        """
        Create and register a connector.
        """

        connector = ConnectorFactory.create_from_config(
            connector_name,
            config,
        )

        self._connectors[
            config.name.lower()
        ] = connector

        return connector

    # ---------------------------------------------------------

    def add(
        self,
        connector: BaseConnector,
    ) -> None:
        """
        Register an existing connector instance.
        """

        self._connectors[
            connector.name.lower()
        ] = connector

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    def get(
        self,
        connector_name: str,
    ) -> BaseConnector:
        """
        Retrieve a managed connector.
        """

        connector = self._connectors.get(
            connector_name.lower(),
        )

        if connector is None:

            raise ConnectorNotFoundError(
                f"Connector '{connector_name}' is not managed."
            )

        return connector

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
    # Connection Management
    # ---------------------------------------------------------

    def connect(
        self,
        connector_name: str,
    ) -> None:
        """
        Connect a managed connector.
        """

        connector = self.get(
            connector_name,
        )

        if not connector.connected:

            connector.connect()

    # ---------------------------------------------------------

    def disconnect(
        self,
        connector_name: str,
    ) -> None:
        """
        Disconnect a managed connector.
        """

        connector = self.get(
            connector_name,
        )

        if connector.connected:

            connector.disconnect()

    # ---------------------------------------------------------

    def connect_all(
        self,
    ) -> None:
        """
        Connect every managed connector.
        """

        for connector in self._connectors.values():

            if not connector.connected:

                connector.connect()

    # ---------------------------------------------------------

    def disconnect_all(
        self,
    ) -> None:
        """
        Disconnect every managed connector.
        """

        for connector in self._connectors.values():

            if connector.connected:

                connector.disconnect()

    # ---------------------------------------------------------
    # Removal
    # ---------------------------------------------------------

    def remove(
        self,
        connector_name: str,
    ) -> None:
        """
        Remove a managed connector.
        """

        connector = self.get(
            connector_name,
        )

        if connector.connected:

            connector.disconnect()

        self._connectors.pop(
            connector_name.lower(),
        )

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove every connector.
        """

        self.disconnect_all()

        self._connectors.clear()

    # ---------------------------------------------------------
    # Listing
    # ---------------------------------------------------------

    def list(
        self,
    ) -> list[BaseConnector]:
        """
        Return managed connectors.
        """

        return list(
            self._connectors.values(),
        )

    # ---------------------------------------------------------

    def list_names(
        self,
    ) -> list[str]:
        """
        Return managed connector names.
        """

        return sorted(
            self._connectors.keys(),
        )

    # ---------------------------------------------------------

    @property
    def connector_count(
        self,
    ) -> int:
        """
        Number of managed connectors.
        """

        return len(
            self._connectors,
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._connectors,
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._connectors.values(),
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        connector_name: str,
    ) -> bool:

        return self.exists(
            connector_name,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorManager("
            f"connectors={self.connector_count})"
        )
