"""
DataForge Connector Inspector

Inspects connector implementations and exposes metadata.
"""

from __future__ import annotations

from connectors.base import BaseConnector
from connectors.base.registry import ConnectorRegistry


class ConnectorInspector:
    """
    Inspects DataForge connector implementations.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def inspect(
        self,
        connector: str | type[BaseConnector],
    ) -> dict:
        """
        Inspect a connector class or connector name.
        """

        if isinstance(connector, str):

            connector_class = ConnectorRegistry.get(
                connector
            )

        else:

            connector_class = connector

        #
        # Connector metadata
        #

        metadata = {}

        if hasattr(
            connector_class,
            "get_metadata",
        ):

            try:

                metadata = (
                    connector_class.get_metadata()
                )

            except Exception:

                metadata = {}

        #
        # Connector name
        #

        connector_name = metadata.get(
            "name",
            connector_class.__name__
            .replace("Connector", "")
            .lower(),
        )

        #
        # Public methods
        #

        methods = sorted(

            name

            for name, member in connector_class.__dict__.items()

            if callable(member)
            and not name.startswith("_")

        )

        #
        # Capabilities
        #

        capabilities = metadata.get(
            "capabilities",
            [],
        )

        if not capabilities:

            for capability in (
                "connect",
                "disconnect",
                "test_connection",
                "extract",
                "read",
                "write",
            ):

                if hasattr(
                    connector_class,
                    capability,
                ):

                    capabilities.append(
                        capability
                    )

        return {

            "name": connector_name,

            "display_name": metadata.get(
                "display_name",
                connector_name.capitalize(),
            ),

            "version": metadata.get(
                "version",
                "Unknown",
            ),

            "module": connector_class.__module__,

            "class": connector_class.__name__,

            "description": metadata.get(
                "description",
                connector_class.__doc__.strip()
                if connector_class.__doc__
                else "",
            ),

            "methods": methods,

            "capabilities": capabilities,

            "supports": metadata.get(
                "supports",
                {},
            ),

            "metadata": metadata,

        }

    # ---------------------------------------------------------

    def inspect_all(
        self,
    ) -> list[dict]:
        """
        Inspect every registered connector.
        """

        return [

            self.inspect(name)

            for name in ConnectorRegistry.list_connectors()

        ]

    # ---------------------------------------------------------

    def validate(
        self,
        connector_class: type,
    ) -> bool:

        return (

            isinstance(
                connector_class,
                type,
            )

            and issubclass(
                connector_class,
                BaseConnector,
            )

            and connector_class is not BaseConnector

        )

    # ---------------------------------------------------------

    def supports_metadata(
        self,
        connector_class: type[BaseConnector],
    ) -> bool:

        return hasattr(
            connector_class,
            "get_metadata",
        )

    # ---------------------------------------------------------

    def connector_name(
        self,
        connector_class: type[BaseConnector],
    ) -> str:

        return connector_class.__name__

    # ---------------------------------------------------------

    def module_name(
        self,
        connector_class: type[BaseConnector],
    ) -> str:

        return connector_class.__module__

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return "ConnectorInspector()"
