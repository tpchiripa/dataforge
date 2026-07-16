"""
DataForge Connector Registry

Central registry for all DataForge connector implementations.

The registry maintains a mapping between connector names and
their implementation classes.

Example
-------
>>> ConnectorRegistry.register("postgresql", PostgresConnector)
>>> ConnectorRegistry.get("postgresql")
<class 'PostgresConnector'>
"""

from __future__ import annotations

from typing import Type

from .base_connector import BaseConnector
from .exceptions import ConnectorNotFoundError, ConnectorRegistrationError


class ConnectorRegistry:
    """
    Registry responsible for storing connector implementations.
    """

    _connectors: dict[str, Type[BaseConnector]] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        name: str,
        connector: Type[BaseConnector],
    ) -> None:
        """
        Register a connector class.
        """

        key = name.strip().lower()

        if not key:
            raise ValueError(
                "Connector name cannot be empty."
            )

        if key in cls._connectors:
            raise ConnectorRegistrationError(
                f"Connector '{name}' is already registered."
            )

        if not issubclass(connector, BaseConnector):
            raise TypeError(
                "Connector must inherit from BaseConnector."
            )

        cls._connectors[key] = connector

    # ---------------------------------------------------------
    # Removal
    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        """
        Remove a connector from the registry.
        """

        cls._connectors.pop(
            name.lower(),
            None,
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Type[BaseConnector]:
        """
        Retrieve a registered connector class.
        """

        connector = cls._connectors.get(
            name.lower()
        )

        if connector is None:
            raise ConnectorNotFoundError(
                f"Connector '{name}' is not registered."
            )

        return connector

    # ---------------------------------------------------------

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:
        """
        Check whether a connector is registered.
        """

        return (
            name.lower()
            in cls._connectors
        )

    # ---------------------------------------------------------

    @classmethod
    def list_connectors(
        cls,
    ) -> list[str]:
        """
        Return connector names.
        """

        return sorted(
            cls._connectors.keys()
        )

    # ---------------------------------------------------------

    @classmethod
    def list(
        cls,
    ) -> list[Type[BaseConnector]]:
        """
        Return connector classes.
        """

        return list(
            cls._connectors.values()
        )

    # ---------------------------------------------------------

    @classmethod
    def count(cls) -> int:
        """
        Number of registered connectors.
        """

        return len(cls._connectors)

    # ---------------------------------------------------------

    @classmethod
    def clear(cls) -> None:
        """
        Remove every registered connector.

        Primarily used by unit tests.
        """

        cls._connectors.clear()

    # ---------------------------------------------------------
    # Dunder Methods
    # ---------------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.count()

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self.list()
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorRegistry("
            f"connectors={self.count()})"
        )
