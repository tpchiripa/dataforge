"""
DataForge Connector Factory

Creates connector instances from the ConnectorRegistry.

Example
-------

from connectors.base import ConnectorConfig, ConnectorFactory

config = ConnectorConfig(
    name="Metadata Database",
    connector_type=ConnectorType.DATABASE,
    host="localhost",
    port=5433,
    database="dataforge",
    username="dataforge",
    password="DataForge2026!",
)

factory = ConnectorFactory()

connector = factory.create(
    "postgresql",
    config,
)

connector.connect()
"""

from __future__ import annotations

from .connector import BaseConnector
from .exceptions import ConnectorNotFoundError
from .registry import ConnectorRegistry
from .types import ConnectorConfig


class ConnectorFactory:
    """
    Factory responsible for creating connector instances.

    The factory isolates the rest of DataForge from concrete
    connector implementations.

    Connectors are created dynamically from the registry.
    """

    def __init__(self, registry: ConnectorRegistry | None = None):

        self.registry = registry or ConnectorRegistry()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def create(
        self,
        connector_name: str,
        config: ConnectorConfig,
    ) -> BaseConnector:
        """
        Create a connector instance.

        Parameters
        ----------
        connector_name
            Registered connector name.

        config
            Connector configuration.

        Returns
        -------
        BaseConnector
        """

        connector_class = self.registry.get(connector_name)

        if connector_class is None:

            raise ConnectorNotFoundError(
                f"Connector '{connector_name}' is not registered."
            )

        return connector_class(config)

    # ---------------------------------------------------------

    def available_connectors(self) -> list[str]:
        """
        Return all registered connectors.
        """

        return self.registry.list_connectors()
