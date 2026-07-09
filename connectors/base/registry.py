"""
DataForge Connector Registry

Central registry for all DataForge connectors.
"""

from __future__ import annotations

from typing import Type

from .connector import BaseConnector
from .exceptions import (
    ConnectorNotFoundError,
    ConnectorRegistrationError,
)


class ConnectorRegistry:
    """
    Registry responsible for storing and retrieving
    connector implementations.
    """

    _connectors: dict[str, Type[BaseConnector]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        connector: Type[BaseConnector],
    ) -> None:
        """
        Register a connector.

        Example:
            ConnectorRegistry.register(
                "postgres",
                PostgreSQLConnector
            )
        """

        key = name.lower()

        if key in cls._connectors:
            raise ConnectorRegistrationError(
                f"Connector '{name}' is already registered."
            )

        cls._connectors[key] = connector

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Remove a connector from the registry.
        """

        cls._connectors.pop(name.lower(), None)

    @classmethod
    def get(cls, name: str) -> Type[BaseConnector]:
        """
        Retrieve a connector class.
        """

        connector = cls._connectors.get(name.lower())

        if connector is None:
            raise ConnectorNotFoundError(
                f"Connector '{name}' is not registered."
            )

        return connector

    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Check whether a connector exists.
        """

        return name.lower() in cls._connectors

    @classmethod
    def list_connectors(cls) -> list[str]:
        """
        Return all registered connector names.
        """

        return sorted(cls._connectors.keys())

    @classmethod
    def clear(cls) -> None:
        """
        Remove all registered connectors.

        Mainly useful for testing.
        """

        cls._connectors.clear()
