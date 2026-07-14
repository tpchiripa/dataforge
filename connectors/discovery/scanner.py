"""
DataForge Connector Scanner

Scans the DataForge connectors directory and discovers connector
implementations.
"""

from __future__ import annotations

from pathlib import Path


class ConnectorScanner:
    """
    Discovers connector implementation files.
    """

    IGNORE_DIRECTORIES = {
        "__pycache__",
        "base",
        "discovery",
    }

    def __init__(
        self,
        root_directory: str | Path,
    ):

        self.root_directory = Path(
            root_directory
        ).resolve()

    # ---------------------------------------------------------

    def scan(self) -> list[Path]:
        """
        Return every connector implementation.

        Supports both:

        connector.py
        *_connector.py
        """

        connector_files: list[Path] = []

        if not self.root_directory.exists():
            return connector_files

        for path in self.root_directory.rglob("*.py"):

            if self._should_ignore(path):
                continue

            if path.name == "__init__.py":
                continue

            if (
                path.name == "connector.py"
                or path.name.endswith("_connector.py")
            ):
                connector_files.append(path)

        connector_files.sort()

        return connector_files

    # ---------------------------------------------------------

    def _should_ignore(
        self,
        path: Path,
    ) -> bool:

        for part in path.parts:

            if part.startswith("."):
                return True

            if part in self.IGNORE_DIRECTORIES:
                return True

        return False

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ConnectorScanner("
            f"root_directory='{self.root_directory}')"
        )
