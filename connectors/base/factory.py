"""
DataForge Connector Factory

Responsible for creating connector instances from the registry.

Example:

factory = ConnectorFactory()

connector = factory.create(
    "postgres",
    host="localhost",
    port=5432,
    database="sales",
    username="admin",
    password="secret",
)

connector.connect()
"""

from __future__ import annotations

from typing import Any

from .exceptions import ConnectorNotFoundError
from .registry import ConnectorRegistry


class ConnectorFactory:
    """
    Creates connector instances.

    The factory hides connector implementation details from the rest
    of the platform.

    Other DataForge modules only interact with this factory.
    """

    def __init__(self, registry: ConnectorRegistry | None = None):
        self.registry = registry or ConnectorRegistry()

    def create(self, connector_name: str, **kwargs: Any):
        """
        Create a connector instance.

        Parameters
        ----------
        connector_name:
            Registered connector name.

        kwargs:
            Configuration passed directly to connector constructor.
        """

        connector_class = self.registry.get(connector_name)

        if connector_class is None:
            raise ConnectorNotFoundError(
                f"Connector '{connector_name}' is not registered."
            )

        return connector_class(**kwargs)

    def available_connectors(self) -> list[str]:
        """
        Return registered connector names.
        """

        return sorted(self.registry.list_connectors())
