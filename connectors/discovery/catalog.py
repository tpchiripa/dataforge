"""
DataForge Connector Catalog

Provides access to metadata for all registered connectors.
"""

from __future__ import annotations

from connectors.base import ConnectorRegistry


class ConnectorCatalog:
    """
    Catalog of all registered connectors.
    """

    def __init__(self, registry: ConnectorRegistry | None = None):

        self.registry = registry or ConnectorRegistry()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def list(self) -> list[dict]:
        """
        Return metadata for every registered connector.
        """

        catalog = []

        for connector_name in self.registry.list_connectors():

            connector_class = self.registry.get(connector_name)

            metadata = connector_class.get_metadata()

            catalog.append(
                {
                    "name": connector_name,
                    "display_name": metadata.name,
                    "version": metadata.version,
                    "description": metadata.description,
                    "author": metadata.author,
                    "connector_type": metadata.connector_type.value,
                    "supports_batch": metadata.supports_batch,
                    "supports_streaming": metadata.supports_streaming,
                    "supports_incremental": metadata.supports_incremental,
                    "tags": metadata.tags,
                }
            )

        return sorted(catalog, key=lambda item: item["name"])

    # ---------------------------------------------------------

    def get(self, connector_name: str) -> dict:
        """
        Return metadata for a single connector.
        """

        connector_class = self.registry.get(connector_name)

        metadata = connector_class.get_metadata()

        return {
            "name": connector_name,
            "display_name": metadata.name,
            "version": metadata.version,
            "description": metadata.description,
            "author": metadata.author,
            "connector_type": metadata.connector_type.value,
            "supports_batch": metadata.supports_batch,
            "supports_streaming": metadata.supports_streaming,
            "supports_incremental": metadata.supports_incremental,
            "tags": metadata.tags,
        }

    # ---------------------------------------------------------

    def exists(self, connector_name: str) -> bool:
        """
        Check whether a connector exists.
        """

        return self.registry.exists(connector_name)

    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Return the number of registered connectors.
        """

        return len(self.registry.list_connectors())
