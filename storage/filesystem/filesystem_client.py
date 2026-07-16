"""
DataForge Local Filesystem Client

Provides a storage backend using the local filesystem.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

from storage.exceptions import StorageError
from storage.models.storage_object import StorageObject


class FileSystemClient:
    """
    Local filesystem storage backend.
    """

    def __init__(
        self,
        root_directory: str | Path,
    ) -> None:

        self._root = Path(root_directory)

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _bucket_path(
        self,
        bucket: str,
    ) -> Path:

        return self._root / bucket

    # ---------------------------------------------------------

    def _object_path(
        self,
        bucket: str,
        object_name: str,
    ) -> Path:

        return self._bucket_path(bucket) / object_name

    # ---------------------------------------------------------
    # Buckets
    # ---------------------------------------------------------

    def create_bucket(
        self,
        bucket: str,
    ) -> None:

        self._bucket_path(bucket).mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------

    def bucket_exists(
        self,
        bucket: str,
    ) -> bool:

        return self._bucket_path(bucket).exists()

    # ---------------------------------------------------------

    def list_buckets(
        self,
    ) -> list[str]:

        return sorted(
            directory.name
            for directory in self._root.iterdir()
            if directory.is_dir()
        )

    # ---------------------------------------------------------
    # Upload
    # ---------------------------------------------------------

    def upload_file(
        self,
        bucket: str,
        object_name: str,
        file_path: str | Path,
    ) -> StorageObject:

        self.create_bucket(bucket)

        destination = self._object_path(
            bucket,
            object_name,
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            file_path,
            destination,
        )

        return self.stat(
            bucket,
            object_name,
        )

    # ---------------------------------------------------------

    def upload_bytes(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:

        self.create_bucket(bucket)

        destination = self._object_path(
            bucket,
            object_name,
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(data)

        return self.stat(
            bucket,
            object_name,
        )

    # ---------------------------------------------------------

    def upload_stream(
        self,
        bucket: str,
        object_name: str,
        stream: BinaryIO,
        size: int,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:

        self.create_bucket(bucket)

        destination = self._object_path(
            bucket,
            object_name,
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with destination.open("wb") as output:

            shutil.copyfileobj(
                stream,
                output,
            )

        return self.stat(
            bucket,
            object_name,
        )

    # ---------------------------------------------------------
    # Download
    # ---------------------------------------------------------

    def download_file(
        self,
        bucket: str,
        object_name: str,
        destination: str | Path,
    ) -> Path:

        source = self._object_path(
            bucket,
            object_name,
        )

        if not source.exists():

            raise StorageError(
                f"Object '{object_name}' not found."
            )

        destination = Path(destination)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            destination,
        )

        return destination

    # ---------------------------------------------------------

    def read_bytes(
        self,
        bucket: str,
        object_name: str,
    ) -> bytes:

        source = self._object_path(
            bucket,
            object_name,
        )

        if not source.exists():

            raise StorageError(
                f"Object '{object_name}' not found."
            )

        return source.read_bytes()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_object(
        self,
        bucket: str,
        object_name: str,
    ) -> None:

        path = self._object_path(
            bucket,
            object_name,
        )

        if path.exists():

            path.unlink()

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def exists(
        self,
        bucket: str,
        object_name: str,
    ) -> bool:

        return self._object_path(
            bucket,
            object_name,
        ).exists()

    # ---------------------------------------------------------

    def stat(
        self,
        bucket: str,
        object_name: str,
    ) -> StorageObject:

        path = self._object_path(
            bucket,
            object_name,
        )

        if not path.exists():

            raise StorageError(
                f"Object '{object_name}' not found."
            )

        stats = path.stat()

        return StorageObject(
            bucket=bucket,
            key=object_name,
            size=stats.st_size,
            etag=None,
            content_type=None,
        )

    # ---------------------------------------------------------

    def list_objects(
        self,
        bucket: str,
        prefix: str = "",
        recursive: bool = True,
    ) -> list[StorageObject]:

        bucket_path = self._bucket_path(bucket)

        if not bucket_path.exists():

            return []

        pattern = "**/*" if recursive else "*"

        objects = []

        for file in bucket_path.glob(pattern):

            if not file.is_file():

                continue

            relative = file.relative_to(bucket_path)

            if not str(relative).startswith(prefix):

                continue

            objects.append(
                self.stat(
                    bucket,
                    str(relative),
                )
            )

        return objects

    # ---------------------------------------------------------

    @property
    def root_directory(
        self,
    ) -> Path:

        return self._root

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(root='{self._root}')"
        )
