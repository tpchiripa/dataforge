"""
DataForge Lakehouse Manager

Provides layer-aware read/write operations across the Medallion
(Bronze/Silver/Gold) architecture, built on top of StorageManager.
"""

from __future__ import annotations

from pathlib import Path

from storage.lakehouse.layer import LakehousePath, MedallionLayer
from storage.manager.storage_manager import StorageManager
from storage.models.storage_object import StorageObject


class LakehouseManager:
    """
    Layer-aware wrapper around StorageManager.

    Examples
    --------
    lakehouse = LakehouseManager(storage_manager)

    lakehouse.write_bytes(
        layer=MedallionLayer.BRONZE,
        source="postgres_orders",
        table="orders",
        filename="orders_20260819.parquet",
        data=raw_bytes,
    )
    """

    def __init__(self, storage_manager: StorageManager):

        self._storage = storage_manager

    # ---------------------------------------------------------
    # Write
    # ---------------------------------------------------------

    def write_bytes(
        self,
        layer: MedallionLayer,
        source: str,
        table: str,
        filename: str,
        data: bytes,
        content_type: str = "application/octet-stream",
        as_of=None,
    ) -> StorageObject:

        key = LakehousePath.build(
            source=source,
            table=table,
            filename=filename,
            as_of=as_of,
        )

        return self._storage.upload_bytes(
            bucket=layer.bucket,
            object_name=key,
            data=data,
            content_type=content_type,
        )

    # ---------------------------------------------------------

    def write_file(
        self,
        layer: MedallionLayer,
        source: str,
        table: str,
        filename: str,
        file_path: str | Path,
        as_of=None,
    ) -> StorageObject:

        key = LakehousePath.build(
            source=source,
            table=table,
            filename=filename,
            as_of=as_of,
        )

        return self._storage.upload_file(
            bucket=layer.bucket,
            object_name=key,
            file_path=file_path,
        )

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def read_bytes(self, layer: MedallionLayer, key: str) -> bytes:

        return self._storage.read_bytes(
            bucket=layer.bucket,
            object_name=key,
        )

    # ---------------------------------------------------------

    def download_file(
        self,
        layer: MedallionLayer,
        key: str,
        destination: str | Path,
    ) -> Path:

        return self._storage.download_file(
            bucket=layer.bucket,
            object_name=key,
            destination=destination,
        )

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def list_table(
        self,
        layer: MedallionLayer,
        source: str,
        table: str,
    ) -> list[StorageObject]:

        prefix = f"{source}/{table}/"

        return self._storage.list_objects(
            bucket=layer.bucket,
            prefix=prefix,
            recursive=True,
        )

    # ---------------------------------------------------------

    def exists(self, layer: MedallionLayer, key: str) -> bool:

        return self._storage.exists(
            bucket=layer.bucket,
            object_name=key,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(storage={self._storage!r})"