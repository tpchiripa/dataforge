"""
DataForge Filesystem Client Tests
"""

from __future__ import annotations

import pytest

from storage.exceptions import StorageError
from storage.filesystem.filesystem_client import FileSystemClient

# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def client(tmp_path):
    return FileSystemClient(
        root_directory=tmp_path,
    )


# =========================================================
# Initialization
# =========================================================

def test_initialization(client, tmp_path):
    assert client.root_directory == tmp_path


# =========================================================
# Bucket Operations
# =========================================================

def test_create_bucket(client):
    client.create_bucket("bronze")

    assert client.bucket_exists("bronze")


def test_list_buckets(client):
    client.create_bucket("bronze")
    client.create_bucket("silver")

    buckets = client.list_buckets()

    assert buckets == ["bronze", "silver"]


# =========================================================
# Upload / Download Bytes
# =========================================================

def test_upload_bytes(client):
    obj = client.upload_bytes(
        bucket="bronze",
        object_name="customers.csv",
        data=b"hello",
    )

    assert obj.bucket == "bronze"
    assert obj.key == "customers.csv"


def test_read_bytes(client):
    client.upload_bytes(
        bucket="bronze",
        object_name="customers.csv",
        data=b"hello world",
    )

    data = client.read_bytes(
        "bronze",
        "customers.csv",
    )

    assert data == b"hello world"


# =========================================================
# Exists
# =========================================================

def test_exists_true(client):
    client.upload_bytes(
        "bronze",
        "customers.csv",
        b"abc",
    )

    assert client.exists(
        "bronze",
        "customers.csv",
    )


def test_exists_false(client):
    assert not client.exists(
        "bronze",
        "missing.csv",
    )


# =========================================================
# Delete
# =========================================================

def test_delete_object(client):
    client.upload_bytes(
        "bronze",
        "customers.csv",
        b"abc",
    )

    client.delete_object(
        "bronze",
        "customers.csv",
    )

    assert not client.exists(
        "bronze",
        "customers.csv",
    )


# =========================================================
# Metadata
# =========================================================

def test_stat(client):
    obj = client.upload_bytes(
        "bronze",
        "customers.csv",
        b"abcdef",
    )

    metadata = client.stat(
        "bronze",
        "customers.csv",
    )

    assert metadata.bucket == obj.bucket
    assert metadata.key == obj.key
    assert metadata.size == 6


# =========================================================
# List Objects
# =========================================================

def test_list_objects(client):
    client.upload_bytes(
        "bronze",
        "a.csv",
        b"a",
    )

    client.upload_bytes(
        "bronze",
        "b.csv",
        b"b",
    )

    objects = client.list_objects(
        "bronze",
    )

    assert len(objects) == 2

    keys = sorted(obj.key for obj in objects)

    assert keys == [
        "a.csv",
        "b.csv",
    ]


# =========================================================
# Missing Object
# =========================================================

def test_read_missing_object(client):
    with pytest.raises(StorageError):
        client.read_bytes(
            "bronze",
            "missing.csv",
        )


# =========================================================
# Representation
# =========================================================

def test_repr(client):
    representation = repr(client)

    assert "FileSystemClient" in representation
