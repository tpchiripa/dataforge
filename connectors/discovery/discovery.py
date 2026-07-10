"""
DataForge Connector Discovery Engine

Coordinates connector discovery by combining the
ConnectorScanner, ConnectorLoader and ConnectorRegistry.

Responsibilities
----------------
- Scan the connectors directory
- Load connector classes
- Register connectors
- Return discovered connector classes
"""

from __future__ import annotations

from pathlib import Path

from connectors.base import ConnectorRegistry
from connectors.discovery.loader import ConnectorLoader
from connectors.discovery.scanner import ConnectorScanner


class ConnectorDiscovery:
    """
    Discovers and registers DataForge connectors.
    """

    def __init__(self, connectors_directory: str | Path):

        self.connectors_directory = Path(connectors_directory)

        self.scanner = ConnectorScanner(self.connectors_directory)

        self.loader = ConnectorLoader()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def discover(self) -> list[type]:
        """
        Discover all connectors and register them.

        Returns
        -------
        list[type]
            List of discovered connector classes.
        """

        discovered: list[type] = []

        connector_files = self.scanner.scan()

        for connector_file in connector_files:

            connector_class = self.loader.load(connector_file)

            # Folder containing connector.py
            connector_name = connector_file.parent.name.lower()

            ConnectorRegistry.register(
                connector_name,
                connector_class,
            )

            discovered.append(connector_class)

        return discovered

    # ------------------------------------------------------------------

    def registry(self) -> ConnectorRegistry:
        """
        Return the registry.
        """

        return ConnectorRegistry
