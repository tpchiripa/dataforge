"""
DataForge Connector Factory

Creates connector instances from registered connector classes.
"""

from __future__ import annotations

from connectors.base.base_connector import BaseConnector
from connectors.config.connector_config import ConnectorConfig
from connectors.registry.connector_registry import ConnectorRegistry


class ConnectorFactory:
    """
    Factory responsible for creating connector instances.
    """

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------

    @staticmethod
    def create(
        connector_name: str,
        config: ConnectorConfig,
    ) -> BaseConnector:
        """
        Create a connector instance from a registered connector.
        """

        connector_class = ConnectorRegistry.get(
            connector_name,
        )

        return connector_class(
            config,
        )

    # ---------------------------------------------------------

    @staticmethod
    def create_from_config(
        connector_name: str,
        config: ConnectorConfig,
    ) -> BaseConnector:
        """
        Create a connector using its registered name and configuration.
        """

        return ConnectorFactory.create(
            connector_name,
            config,
        )

    # ---------------------------------------------------------

    @staticmethod
    def registered_connectors() -> list[str]:
        """
        Return registered connector names.
        """

        return ConnectorRegistry.list_names()

    # ---------------------------------------------------------

    @staticmethod
    def connector_exists(
        connector_name: str,
    ) -> bool:

        return ConnectorRegistry.exists(
            connector_name,
        )

    # ---------------------------------------------------------

    @staticmethod
    def connector_count() -> int:

        return ConnectorRegistry.connector_count()

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ConnectorFactory("
            f"registered={ConnectorRegistry.connector_count()})"
        )
