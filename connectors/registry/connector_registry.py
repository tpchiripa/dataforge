"""
DataForge Connector Registry

Central registry for DataForge connector classes.
"""

from __future__ import annotations

from typing import Type

from connectors.base.base_connector import BaseConnector
from connectors.exceptions import (
    ConnectorAlreadyRegisteredError,
    ConnectorNotFoundError,
)


class ConnectorRegistry:
    """
    Registry responsible for managing connector classes.

    Connectors are registered by name and later instantiated
    by the ConnectorFactory.
    """

    _connectors: dict[str, Type[BaseConnector]] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        connector: Type[BaseConnector],
    ) -> None:
        """
        Register a connector class.
        """

        key = connector.__name__.lower()

        if key in cls._connectors:

            raise ConnectorAlreadyRegisteredError(
                f"Connector '{connector.__name__}' is already registered."
            )

        cls._connectors[key] = connector

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        connector_name: str,
    ) -> None:
        """
        Remove a connector.
        """

        cls._connectors.pop(
            connector_name.lower(),
            None,
        )

    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        connector_name: str,
    ) -> Type[BaseConnector]:
        """
        Retrieve a connector class.
        """

        connector = cls._connectors.get(
            connector_name.lower(),
        )

        if connector is None:

            raise ConnectorNotFoundError(
                f"Connector '{connector_name}' is not registered."
            )

        return connector

    # ---------------------------------------------------------

    @classmethod
    def exists(
        cls,
        connector_name: str,
    ) -> bool:
        """
        Check whether a connector exists.
        """

        return (
            connector_name.lower()
            in cls._connectors
        )

    # ---------------------------------------------------------
    # Listing
    # ---------------------------------------------------------

    @classmethod
    def list(
        cls,
    ) -> list[Type[BaseConnector]]:
        """
        Return registered connector classes.
        """

        return list(
            cls._connectors.values(),
        )

    # ---------------------------------------------------------

    @classmethod
    def list_names(
        cls,
    ) -> list[str]:
        """
        Return registered connector names.
        """

        return sorted(
            cls._connectors.keys(),
        )

    # ---------------------------------------------------------

    @classmethod
    def connector_count(
        cls,
    ) -> int:
        """
        Number of registered connectors.
        """

        return len(
            cls._connectors,
        )

    # ---------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Remove every registered connector.

        Primarily used during testing.
        """

        cls._connectors.clear()

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._connectors,
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._connectors.values(),
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        connector_name: str,
    ) -> bool:

        return self.exists(
            connector_name,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "ConnectorRegistry("
            f"count={len(self._connectors)})"
        )
