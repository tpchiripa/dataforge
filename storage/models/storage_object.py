"""
DataForge Storage Object
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class StorageObject:
    """
    Represents a file or object stored in any storage backend.
    """

    bucket: str
    key: str

    size: int = 0

    content_type: Optional[str] = None

    etag: Optional[str] = None

    last_modified: Optional[datetime] = None

    version_id: Optional[str] = None

    metadata: dict[str, str] | None = None

    @property
    def filename(self) -> str:
        """
        Returns only the filename.
        """
        return Path(self.key).name

    @property
    def extension(self) -> str:
        """
        Returns the file extension.
        """
        return Path(self.key).suffix

    @property
    def parent(self) -> str:
        """
        Returns the parent directory.
        """
        return str(Path(self.key).parent)

    @property
    def uri(self) -> str:
        """
        Returns a storage URI.
        """
        return f"{self.bucket}/{self.key}"

    def __repr__(self) -> str:
        return (
            f"StorageObject("
            f"bucket='{self.bucket}', "
            f"key='{self.key}', "
            f"size={self.size})"
        )
