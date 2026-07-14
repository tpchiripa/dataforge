"""
DataForge Discovery Manager

High-level interface for the DataForge Connector Discovery
subsystem.
"""

from __future__ import annotations

from pathlib import Path

from connectors.base.factory import ConnectorFactory
from connectors.base.registry import ConnectorRegistry
from connectors.config.connector_config import ConnectorConfig

from .catalog import ConnectorCatalog
from .discovery import ConnectorDiscovery
from .inspector import ConnectorInspector


class DiscoveryManager:
    """
    High-level manager for connector discovery.
    """

    def __init__(
        self,
        connectors_directory: str | Path = "connectors",
    ) -> None:

        self.discovery = ConnectorDiscovery(
            connectors_directory
        )

        self.catalog = ConnectorCatalog(
            connectors_directory
        )

        self.inspector = ConnectorInspector()

        self.factory = ConnectorFactory()

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(self):

        return self.discovery.discover()

    def refresh(self):

        ConnectorRegistry.clear()

        self.discovery.discover()

        return self.catalog.refresh()

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def create(
        self,
        connector_name: str,
        config: ConnectorConfig,
    ):

        return self.factory.create(
            connector_name,
            config,
        )

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    def registered_connectors(
        self,
    ) -> list[str]:

        return ConnectorRegistry.list_connectors()

    def clear_registry(
        self,
    ) -> None:

        ConnectorRegistry.clear()

    # ---------------------------------------------------------
    # Backwards Compatibility
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Backwards-compatible alias for clear_registry().
        """

        self.clear_registry()

    # ---------------------------------------------------------
    # Catalog
    # ---------------------------------------------------------

    def connectors(
        self,
    ) -> list[str]:

        return self.catalog.list()

    def connector(
        self,
        name: str,
    ) -> dict | None:

        return self.catalog.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.catalog.exists(name)

    def search(
        self,
        keyword: str,
    ):

        return self.catalog.search(keyword)

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    def inspect(
        self,
        connector,
    ):

        return self.inspector.inspect(
            connector
        )

    # ---------------------------------------------------------

    def count(
        self,
    ) -> int:

        return self.catalog.count()

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.count()

    def __contains__(
        self,
        connector_name: str,
    ) -> bool:

        return self.exists(
            connector_name
        )

    def __iter__(
        self,
    ):

        return iter(self.catalog)

    def __repr__(
        self,
    ) -> str:

        return (
            "DiscoveryManager("
            f"connectors={self.count()})"
        )


# ==========================================================
# Backwards Compatibility
# ==========================================================

ConnectorManager = DiscoveryManager

__all__ = [
    "DiscoveryManager",
    "ConnectorManager",
]
