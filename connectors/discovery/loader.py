"""
DataForge Connector Loader

Dynamically imports connector modules discovered by the ConnectorScanner.

Responsibilities
----------------
- Import connector modules from a file path
- Discover connector classes
- Return the connector class

The loader performs NO scanning.

Scanning is handled by the ConnectorScanner.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from connectors.base import BaseConnector


class ConnectorLoader:
    """
    Dynamically loads DataForge connector classes.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, connector_path: str | Path) -> type[BaseConnector]:
        """
        Load a connector class from a connector.py file.

        Parameters
        ----------
        connector_path : str | Path
            Path to connector.py

        Returns
        -------
        type[BaseConnector]
            Connector class

        Raises
        ------
        ImportError
            If the module cannot be imported.

        ValueError
            If no connector class is found.
        """

        connector_path = Path(connector_path).resolve()

        module_name = "_".join(connector_path.parts[-3:]).replace(".py", "")

        spec = importlib.util.spec_from_file_location(
            module_name,
            connector_path,
        )

        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module from {connector_path}")

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        connector_class = self._find_connector(module)

        if connector_class is None:
            raise ValueError(
                f"No BaseConnector implementation found in {connector_path}"
            )

        return connector_class

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _find_connector(self, module) -> type[BaseConnector] | None:
        """
        Locate the connector class within an imported module.
        """

        for obj in module.__dict__.values():

            if (
                isinstance(obj, type)
                and issubclass(obj, BaseConnector)
                and obj is not BaseConnector
            ):
                return obj

        return None
