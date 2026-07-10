"""
DataForge Connector Scanner

Scans the DataForge connectors directory and discovers connector
implementations.

Responsibilities
----------------
- Walk the connectors directory
- Locate connector.py modules
- Ignore framework directories
- Return discovered connector paths

The scanner performs NO imports.

Importing is handled by the ConnectorLoader.
"""

from __future__ import annotations

from pathlib import Path


class ConnectorScanner:
    """
    Discovers connector modules within the DataForge project.
    """

    IGNORE_DIRECTORIES = {
        "__pycache__",
        "base",
        "discovery",
    }

    def __init__(self, root_directory: str | Path):

        self.root_directory = Path(root_directory).resolve()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(self) -> list[Path]:
        """
        Scan the connectors directory.

        Returns
        -------
        list[Path]
            Sorted list of connector.py files.
        """

        connector_files: list[Path] = []

        if not self.root_directory.exists():
            return connector_files

        for path in self.root_directory.rglob("connector.py"):

            if self._should_ignore(path):
                continue

            connector_files.append(path)

        connector_files.sort()

        return connector_files

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _should_ignore(self, path: Path) -> bool:
        """
        Determine whether a discovered path should be ignored.
        """

        for part in path.parts:

            if part.startswith("."):
                return True

            if part in self.IGNORE_DIRECTORIES:
                return True

        return False
