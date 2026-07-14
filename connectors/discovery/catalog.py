"""
DataForge Connector Catalog

Builds a searchable catalog of all discovered connectors.
"""

from __future__ import annotations

from pathlib import Path

from connectors.base.registry import ConnectorRegistry
from .discovery import ConnectorDiscovery
from .inspector import ConnectorInspector


class ConnectorCatalog:
    """
    Catalog of discovered DataForge connectors.
    """

    def __init__(
        self,
        connectors_directory: str | Path = "connectors",
    ) -> None:

        self.discovery = ConnectorDiscovery(
            connectors_directory
        )

        self.inspector = ConnectorInspector()

        self._catalog: dict[str, dict] = {}

    # ---------------------------------------------------------
    # Catalog Construction
    # ---------------------------------------------------------

    def build(self) -> dict[str, dict]:
        """
        Build the connector catalog.
        """

        # Ensure connectors are discovered and registered
        self.discovery.discover()

        self._catalog.clear()

        for connector_name in ConnectorRegistry.list_connectors():

            connector_class = ConnectorRegistry.get(
                connector_name
            )

            info = self.inspector.inspect(
                connector_class
            )

            self._catalog[
                connector_name
            ] = info

        return self._catalog

    # ---------------------------------------------------------

    def refresh(self) -> dict[str, dict]:
        """
        Refresh the connector catalog.
        """

        return self.build()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        connector_name: str,
    ) -> dict | None:

        if not self._catalog:
            self.build()

        return self._catalog.get(
            connector_name.lower()
        )

    # ---------------------------------------------------------

    def exists(
        self,
        connector_name: str,
    ) -> bool:

        if not self._catalog:
            self.build()

        return (
            connector_name.lower()
            in self._catalog
        )

    # ---------------------------------------------------------

    def list(self) -> list[str]:

        if not self._catalog:
            self.build()

        return sorted(
            self._catalog.keys()
        )

    # ---------------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> list[dict]:

        if not self._catalog:
            self.build()

        keyword = keyword.lower()

        results = []

        for connector in self._catalog.values():

            if (
                keyword
                in connector["name"].lower()
                or keyword
                in connector["description"].lower()
            ):
                results.append(
                    connector
                )

        return results

    # ---------------------------------------------------------

    def count(self) -> int:

        if not self._catalog:
            self.build()

        return len(
            self._catalog
        )

    # ---------------------------------------------------------
    # Dunder Methods
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.count()

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

        if not self._catalog:
            self.build()

        return iter(
            self._catalog.values()
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorCatalog("
            f"connectors={self.count()})"
        )
