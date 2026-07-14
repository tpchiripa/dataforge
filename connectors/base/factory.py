"""
DataForge Connector Factory

Responsible for creating connector instances from the
ConnectorRegistry.

The factory decouples the rest of DataForge from concrete
connector implementations.
"""

from __future__ import annotations

from connectors.config.connector_config import ConnectorConfig

from .base_connector import BaseConnector
from .exceptions import ConnectorNotFoundError
from .registry import ConnectorRegistry


class ConnectorFactory:
    """
    Factory responsible for creating DataForge connectors.
    """

    def __init__(
        self,
        registry: ConnectorRegistry | None = None,
    ) -> None:

        # Always use the global registry unless another is supplied.
        self._registry = (
            registry
            if registry is not None
            else ConnectorRegistry
        )

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
        """

        if not self._registry.exists(
            connector_name
        ):
            raise ConnectorNotFoundError(
                f"Connector '{connector_name}' is not registered."
            )

        connector_class = self._registry.get(
            connector_name
        )

        return connector_class(config)

    # ---------------------------------------------------------

    def exists(
        self,
        connector_name: str,
    ) -> bool:
        """
        Determine whether a connector is registered.
        """

        return self._registry.exists(
            connector_name
        )

    # ---------------------------------------------------------

    def available_connectors(
        self,
    ) -> list[str]:
        """
        Return all registered connector names.
        """

        return self._registry.list_connectors()

    # ---------------------------------------------------------

    @property
    def registry(
        self,
    ):
        """
        Return the registry.
        """

        return self._registry

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorFactory("
            f"connectors={self._registry.count()})"
        )
