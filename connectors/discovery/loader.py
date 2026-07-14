"""
DataForge Connector Loader

Dynamically imports connector implementations discovered by the
ConnectorScanner.

Responsibilities
----------------
- Import connector modules
- Locate connector classes
- Return connector classes

The loader performs NO scanning.

Scanning is handled by ConnectorScanner.

Registration is handled by ConnectorDiscovery.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

from connectors.base import BaseConnector


class ConnectorLoader:
    """
    Dynamically loads DataForge connector classes.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def load(
        self,
        connector_path: str | Path,
    ) -> type[BaseConnector]:
        """
        Load a connector class from a Python module.

        Parameters
        ----------
        connector_path
            Path to a connector implementation.

        Returns
        -------
        type[BaseConnector]
        """

        connector_path = Path(
            connector_path
        ).resolve()

        module_name = (
            connector_path.stem
            + "_"
            + str(abs(hash(connector_path)))
        )

        spec = importlib.util.spec_from_file_location(
            module_name,
            connector_path,
        )

        if spec is None or spec.loader is None:

            raise ImportError(
                f"Unable to load module: {connector_path}"
            )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        connector = self._find_connector(module)

        if connector is None:

            raise ValueError(
                f"No BaseConnector implementation found in "
                f"{connector_path.name}"
            )

        return connector

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _find_connector(
        self,
        module,
    ) -> type[BaseConnector] | None:
        """
        Locate the connector class inside a module.
        """

        candidates: list[type[BaseConnector]] = []

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if (
                issubclass(obj, BaseConnector)
                and obj is not BaseConnector
                and obj.__module__ == module.__name__
            ):

                candidates.append(obj)

        if not candidates:

            return None

        if len(candidates) > 1:

            raise ValueError(
                f"Multiple connector classes found in "
                f"module '{module.__name__}'."
            )

        return candidates[0]

    # ---------------------------------------------------------

    def can_load(
        self,
        connector_path: str | Path,
    ) -> bool:
        """
        Determine whether a connector can be loaded.
        """

        try:

            self.load(connector_path)

            return True

        except Exception:

            return False

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return "ConnectorLoader()"
