"""
DataForge Storage Manager

Unified interface for object storage.

This class abstracts the underlying storage backend so the rest of
DataForge never needs to know whether data lives in MinIO,
Amazon S3, Azure Blob Storage, Google Cloud Storage,
or the local filesystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from storage.models.storage_object import StorageObject


class StorageManager:
    """
    Unified storage interface.

    Examples
    --------
    manager = StorageManager(minio_client)

    manager.upload_file(...)
    manager.download_file(...)
    manager.delete_object(...)
    """

    def __init__(self, backend):

        self._backend = backend

    # ---------------------------------------------------------
    # Upload
    # ---------------------------------------------------------

    def upload_file(
        self,
        bucket: str,
        object_name: str,
        file_path: str | Path,
    ) -> StorageObject:

        return self._backend.upload_file(
            bucket=bucket,
            object_name=object_name,
            file_path=file_path,
        )

    # ---------------------------------------------------------

    def upload_bytes(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:

        return self._backend.upload_bytes(
            bucket=bucket,
            object_name=object_name,
            data=data,
            content_type=content_type,
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

        return self._backend.upload_stream(
            bucket=bucket,
            object_name=object_name,
            stream=stream,
            size=size,
            content_type=content_type,
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

        return self._backend.download_file(
            bucket=bucket,
            object_name=object_name,
            destination=destination,
        )

    # ---------------------------------------------------------

    def read_bytes(
        self,
        bucket: str,
        object_name: str,
    ) -> bytes:

        return self._backend.read_bytes(
            bucket=bucket,
            object_name=object_name,
        )

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_object(
        self,
        bucket: str,
        object_name: str,
    ) -> None:

        self._backend.delete_object(
            bucket=bucket,
            object_name=object_name,
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def exists(
        self,
        bucket: str,
        object_name: str,
    ) -> bool:

        return self._backend.exists(
            bucket=bucket,
            object_name=object_name,
        )

    # ---------------------------------------------------------

    def stat(
        self,
        bucket: str,
        object_name: str,
    ) -> StorageObject:

        return self._backend.stat(
            bucket=bucket,
            object_name=object_name,
        )

    # ---------------------------------------------------------

    def list_objects(
        self,
        bucket: str,
        prefix: str = "",
        recursive: bool = True,
    ) -> list[StorageObject]:

        return self._backend.list_objects(
            bucket=bucket,
            prefix=prefix,
            recursive=recursive,
        )

    # ---------------------------------------------------------
    # Buckets
    # ---------------------------------------------------------

    def create_bucket(
        self,
        bucket: str,
    ) -> None:

        self._backend.create_bucket(bucket)

    # ---------------------------------------------------------

    def bucket_exists(
        self,
        bucket: str,
    ) -> bool:

        return self._backend.bucket_exists(bucket)

    # ---------------------------------------------------------

    def list_buckets(self):

        return self._backend.list_buckets()

    # ---------------------------------------------------------

    @property
    def backend(self):

        return self._backend

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(backend={self._backend.__class__.__name__})"
        )
