"""
DataForge Connector Manager

High-level interface for the DataForge Connector Discovery
subsystem.

The ConnectorManager coordinates:

- Discovery
- Registry
- Factory
- Catalog
- Inspector

It provides a single entry point for interacting with
connectors throughout the platform.
"""

from __future__ import annotations

from pathlib import Path

from connectors.base import (
    ConnectorConfig,
    ConnectorFactory,
    ConnectorRegistry,
)

from connectors.discovery.catalog import ConnectorCatalog
from connectors.discovery.discovery import ConnectorDiscovery
from connectors.discovery.inspector import ConnectorInspector


class ConnectorManager:
    """
    High-level interface for the Connector SDK.

    Other DataForge modules should interact with this class
    instead of using Discovery, Registry, Factory or Catalog
    directly.
    """

    def __init__(self, connectors_directory: str | Path):

        self.registry = ConnectorRegistry()

        self.discovery = ConnectorDiscovery(connectors_directory)

        self.factory = ConnectorFactory(self.registry)

        self.catalog = ConnectorCatalog(self.registry)

        self.inspector = ConnectorInspector(self.registry)

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(self):
        """
        Discover and register all connectors.
        """

        return self.discovery.discover()

    # ---------------------------------------------------------
    # Catalog
    # ---------------------------------------------------------

    def list(self):
        """
        Return metadata for every registered connector.
        """

        return self.catalog.list()

    def get(self, connector_name: str):
        """
        Return metadata for a connector.
        """

        return self.catalog.get(connector_name)

    def exists(self, connector_name: str):
        """
        Check whether a connector exists.
        """

        return self.catalog.exists(connector_name)

    def count(self):
        """
        Return the number of registered connectors.
        """

        return self.catalog.count()

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    def inspect(self, connector_name: str):
        """
        Inspect a connector.
        """

        return self.inspector.inspect(connector_name)

    def inspect_all(self):
        """
        Inspect every connector.
        """

        return self.inspector.inspect_all()

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def create(
        self,
        connector_name: str,
        config: ConnectorConfig,
    ):
        """
        Create a connector instance.
        """

        return self.factory.create(
            connector_name,
            config,
        )

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    def registered_connectors(self):
        """
        Return all registered connector names.
        """

        return self.registry.list_connectors()

    def clear(self):
        """
        Clear the connector registry.

        Mainly useful during testing.
        """

        self.registry.clear()
