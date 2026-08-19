"""
DataForge Lakehouse Manager Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from storage.lakehouse.layer import MedallionLayer
from storage.lakehouse.manager import LakehouseManager


# =========================================================
# Fixtures
# =========================================================


@pytest.fixture
def storage():

    return MagicMock()


@pytest.fixture
def lakehouse(storage):

    return LakehouseManager(storage)


# =========================================================
# Write
# =========================================================


def test_write_bytes(lakehouse, storage):

    lakehouse.write_bytes(
        layer=MedallionLayer.BRONZE,
        source="postgres_orders",
        table="orders",
        filename="orders.parquet",
        data=b"hello",
    )

    storage.upload_bytes.assert_called_once()

    call_kwargs = storage.upload_bytes.call_args.kwargs

    assert call_kwargs["bucket"] == "bronze"

    assert call_kwargs["object_name"].startswith("postgres_orders/orders/")


def test_write_file(lakehouse, storage, tmp_path):

    file = tmp_path / "orders.parquet"

    file.write_text("hello")

    lakehouse.write_file(
        layer=MedallionLayer.SILVER,
        source="postgres_orders",
        table="orders",
        filename="orders.parquet",
        file_path=file,
    )

    storage.upload_file.assert_called_once()

    call_kwargs = storage.upload_file.call_args.kwargs

    assert call_kwargs["bucket"] == "silver"


# =========================================================
# Read
# =========================================================


def test_read_bytes(lakehouse, storage):

    storage.read_bytes.return_value = b"hello"

    result = lakehouse.read_bytes(
        layer=MedallionLayer.GOLD,
        key="postgres_orders/orders/2026/08/19/orders.parquet",
    )

    assert result == b"hello"

    storage.read_bytes.assert_called_once_with(
        bucket="gold",
        object_name="postgres_orders/orders/2026/08/19/orders.parquet",
    )


def test_download_file(lakehouse, storage, tmp_path):

    destination = tmp_path / "orders.parquet"

    lakehouse.download_file(
        layer=MedallionLayer.BRONZE,
        key="postgres_orders/orders/2026/08/19/orders.parquet",
        destination=destination,
    )

    storage.download_file.assert_called_once_with(
        bucket="bronze",
        object_name="postgres_orders/orders/2026/08/19/orders.parquet",
        destination=destination,
    )


# =========================================================
# Discovery
# =========================================================


def test_list_table(lakehouse, storage):

    lakehouse.list_table(
        layer=MedallionLayer.SILVER,
        source="postgres_orders",
        table="orders",
    )

    storage.list_objects.assert_called_once_with(
        bucket="silver",
        prefix="postgres_orders/orders/",
        recursive=True,
    )


def test_exists(lakehouse, storage):

    storage.exists.return_value = True

    assert lakehouse.exists(
        layer=MedallionLayer.GOLD,
        key="postgres_orders/orders/2026/08/19/orders.parquet",
    ) is True


# =========================================================
# Representation
# =========================================================


def test_repr(lakehouse):

    representation = repr(lakehouse)

    assert "LakehouseManager" in representation