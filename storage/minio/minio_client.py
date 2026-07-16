"""
DataForge MinIO Client

Production-ready MinIO storage backend that mirrors the
FileSystemClient API used throughout DataForge.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from storage.exceptions import (BucketNotFoundError, DeleteError,
                                DownloadError, StorageConnectionError,
                                StorageError, UploadError)
from storage.models.storage_object import StorageObject


class MinIOClient:
    """
    Wrapper around the MinIO SDK.
    """

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
    ) -> None:

        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._secure = secure

        self._client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def access_key(self) -> str:
        return self._access_key

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @property
    def secure(self) -> bool:
        return self._secure

    @property
    def client(self) -> Minio:
        return self._client

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    def test_connection(self) -> bool:
        """
        Verify MinIO connectivity.
        """

        try:
            self._client.list_buckets()
            return True

        except Exception as exc:
            raise StorageConnectionError(str(exc)) from exc

    # ---------------------------------------------------------
    # Bucket Operations
    # ---------------------------------------------------------

    def bucket_exists(self, bucket: str) -> bool:

        return self._client.bucket_exists(bucket)

    # ---------------------------------------------------------

    def create_bucket(self, bucket: str) -> None:

        if not self.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    # ---------------------------------------------------------

    def list_buckets(self) -> list[str]:

        return sorted(
            bucket.name
            for bucket in self._client.list_buckets()
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

        try:

            self.create_bucket(bucket)

            self._client.fput_object(
                bucket,
                object_name,
                str(file_path),
            )

            return self.stat(bucket, object_name)

        except Exception as exc:
            raise UploadError(str(exc)) from exc

    # ---------------------------------------------------------

    def upload_bytes(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:

        try:

            self.create_bucket(bucket)

            stream = BytesIO(data)

            self._client.put_object(
                bucket,
                object_name,
                stream,
                length=len(data),
                content_type=content_type,
            )

            return self.stat(bucket, object_name)

        except Exception as exc:
            raise UploadError(str(exc)) from exc

    # ---------------------------------------------------------

    def upload_stream(
        self,
        bucket: str,
        object_name: str,
        stream: BinaryIO,
        size: int,
        content_type: str = "application/octet-stream",
    ) -> StorageObject:

        try:

            self.create_bucket(bucket)

            self._client.put_object(
                bucket,
                object_name,
                stream,
                length=size,
                content_type=content_type,
            )

            return self.stat(bucket, object_name)

        except Exception as exc:
            raise UploadError(str(exc)) from exc

    # ---------------------------------------------------------
    # Download
    # ---------------------------------------------------------

    def download_file(
        self,
        bucket: str,
        object_name: str,
        destination: str | Path,
    ) -> Path:

        try:

            destination = Path(destination)

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._client.fget_object(
                bucket,
                object_name,
                str(destination),
            )

            return destination

        except Exception as exc:
            raise DownloadError(str(exc)) from exc

    # ---------------------------------------------------------

    def read_bytes(
        self,
        bucket: str,
        object_name: str,
    ) -> bytes:

        try:

            response = self._client.get_object(
                bucket,
                object_name,
            )

            try:
                return response.read()

            finally:
                response.close()
                response.release_conn()

        except Exception as exc:
            raise DownloadError(str(exc)) from exc

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_object(
        self,
        bucket: str,
        object_name: str,
    ) -> None:

        try:

            self._client.remove_object(
                bucket,
                object_name,
            )

        except Exception as exc:
            raise DeleteError(str(exc)) from exc

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def exists(
        self,
        bucket: str,
        object_name: str,
    ) -> bool:

        try:

            self._client.stat_object(
                bucket,
                object_name,
            )

            return True

        except S3Error:
            return False

    # ---------------------------------------------------------

    def stat(
        self,
        bucket: str,
        object_name: str,
    ) -> StorageObject:

        try:

            obj = self._client.stat_object(
                bucket,
                object_name,
            )

            return StorageObject(
                bucket=bucket,
                key=object_name,
                size=obj.size,
                etag=obj.etag,
                content_type=obj.content_type,
                last_modified=obj.last_modified,
                metadata=obj.metadata,
            )

        except S3Error as exc:
            raise StorageError(str(exc)) from exc

    # ---------------------------------------------------------

    def list_objects(
        self,
        bucket: str,
        prefix: str = "",
        recursive: bool = True,
    ) -> list[StorageObject]:

        if not self.bucket_exists(bucket):
            raise BucketNotFoundError(bucket)

        objects = self._client.list_objects(
            bucket,
            prefix=prefix,
            recursive=recursive,
        )

        results: list[StorageObject] = []

        for obj in objects:

            results.append(
                StorageObject(
                    bucket=bucket,
                    key=obj.object_name,
                    size=obj.size,
                    etag=obj.etag,
                    last_modified=obj.last_modified,
                )
            )

        return results

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"endpoint='{self._endpoint}', "
            f"secure={self._secure})"
        )
