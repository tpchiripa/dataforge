"""
DataForge Connector Inspector

Inspects registered connectors and exposes their
metadata and capabilities.
"""

from __future__ import annotations

from inspect import getmembers, isfunction

from connectors.base import ConnectorRegistry


class ConnectorInspector:
    """
    Inspects registered DataForge connectors.
    """

    def __init__(self, registry: ConnectorRegistry | None = None):

        self.registry = registry or ConnectorRegistry()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def inspect(self, connector_name: str) -> dict:
        """
        Inspect a registered connector.

        Parameters
        ----------
        connector_name
            Registered connector name.

        Returns
        -------
        dict
            Connector information.
        """

        connector_class = self.registry.get(connector_name)

        metadata = connector_class.get_metadata()

        methods = self._public_methods(connector_class)

        return {
            "name": connector_name,
            "display_name": metadata.name,
            "version": metadata.version,
            "description": metadata.description,
            "author": metadata.author,
            "connector_type": metadata.connector_type.value,
            "supports": {
                "batch": metadata.supports_batch,
                "streaming": metadata.supports_streaming,
                "incremental": metadata.supports_incremental,
            },
            "tags": metadata.tags,
            "methods": methods,
        }

    # ---------------------------------------------------------

    def inspect_all(self) -> list[dict]:
        """
        Inspect every registered connector.
        """

        results = []

        for connector_name in self.registry.list_connectors():

            results.append(
                self.inspect(connector_name)
            )

        return results

    # ---------------------------------------------------------

    @staticmethod
    def _public_methods(connector_class) -> list[str]:
        """
        Return all public methods implemented
        by the connector.
        """

        excluded = {
            "__init__",
            "__repr__",
            "__str__",
        }

        methods = []

        for name, member in getmembers(connector_class):

            if (
                isfunction(member)
                and not name.startswith("_")
                and name not in excluded
            ):
                methods.append(name)

        return sorted(methods)
