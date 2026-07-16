"""
DataForge Storage Manager Tests
"""

from __future__ import annotations

from pathlib import Path

import pytest

from storage.manager.storage_manager import StorageManager
from storage.models.storage_object import StorageObject

# =========================================================
# Dummy Backend
# =========================================================


class DummyBackend:

    def upload_file(
        self,
        bucket,
        object_name,
        file_path,
    ):

        return StorageObject(
            bucket=bucket,
            key=object_name,
            size=Path(file_path).stat().st_size,
        )

    def upload_bytes(
        self,
        bucket,
        object_name,
        data,
        content_type="application/octet-stream",
    ):

        return StorageObject(
            bucket=bucket,
            key=object_name,
            size=len(data),
        )

    def upload_stream(
        self,
        bucket,
        object_name,
        stream,
        size,
        content_type="application/octet-stream",
    ):

        return StorageObject(
            bucket=bucket,
            key=object_name,
            size=size,
        )

    def download_file(
        self,
        bucket,
        object_name,
        destination,
    ):

        return Path(destination)

    def read_bytes(
        self,
        bucket,
        object_name,
    ):

        return b"hello"

    def delete_object(
        self,
        bucket,
        object_name,
    ):

        return None

    def exists(
        self,
        bucket,
        object_name,
    ):

        return True

    def stat(
        self,
        bucket,
        object_name,
    ):

        return StorageObject(
            bucket=bucket,
            key=object_name,
            size=123,
        )

    def list_objects(
        self,
        bucket,
        prefix="",
        recursive=True,
    ):

        return [
            StorageObject(
                bucket=bucket,
                key="a.csv",
            ),
            StorageObject(
                bucket=bucket,
                key="b.csv",
            ),
        ]

    def create_bucket(
        self,
        bucket,
    ):

        return None

    def bucket_exists(
        self,
        bucket,
    ):

        return True

    def list_buckets(self):

        return [
            "bronze",
            "silver",
        ]


# =========================================================
# Fixtures
# =========================================================


@pytest.fixture
def backend():

    return DummyBackend()


@pytest.fixture
def manager(backend):

    return StorageManager(backend)


# =========================================================
# Initialization
# =========================================================


def test_manager_initialization(manager):

    assert manager.backend is not None


# =========================================================
# Upload File
# =========================================================


def test_upload_file(manager, tmp_path):

    file = tmp_path / "sales.csv"

    file.write_text("hello")

    obj = manager.upload_file(
        bucket="bronze",
        object_name="sales.csv",
        file_path=file,
    )

    assert obj.bucket == "bronze"

    assert obj.key == "sales.csv"


# =========================================================
# Upload Bytes
# =========================================================


def test_upload_bytes(manager):

    obj = manager.upload_bytes(
        bucket="bronze",
        object_name="customers.csv",
        data=b"hello",
    )

    assert obj.size == 5


# =========================================================
# Read Bytes
# =========================================================


def test_read_bytes(manager):

    data = manager.read_bytes(
        "bronze",
        "customers.csv",
    )

    assert data == b"hello"


# =========================================================
# Exists
# =========================================================


def test_exists(manager):

    assert manager.exists(
        "bronze",
        "customers.csv",
    )


# =========================================================
# Delete
# =========================================================


def test_delete_object(manager):

    manager.delete_object(
        "bronze",
        "customers.csv",
    )


# =========================================================
# Metadata
# =========================================================


def test_stat(manager):

    obj = manager.stat(
        "bronze",
        "customers.csv",
    )

    assert obj.size == 123


# =========================================================
# List Objects
# =========================================================


def test_list_objects(manager):

    objects = manager.list_objects("bronze")

    assert len(objects) == 2

    assert objects[0].key == "a.csv"


# =========================================================
# Buckets
# =========================================================


def test_bucket_operations(manager):

    manager.create_bucket("bronze")

    assert manager.bucket_exists("bronze")

    assert manager.list_buckets() == [
        "bronze",
        "silver",
    ]


# =========================================================
# Representation
# =========================================================


def test_repr(manager):

    representation = repr(manager)

    assert "StorageManager" in representation
