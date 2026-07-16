"""
DataForge MinIO Client Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from storage.exceptions import BucketNotFoundError
from storage.minio.minio_client import MinIOClient
from storage.models.storage_object import StorageObject

# =========================================================
# Fixtures
# =========================================================


@pytest.fixture
def client():

    client = MinIOClient(
        endpoint="localhost:9000",
        access_key="dataforge",
        secret_key="password",
        secure=False,
    )

    client._client = MagicMock()

    return client


# =========================================================
# Initialization
# =========================================================


def test_initialization(client):

    assert client.endpoint == "localhost:9000"

    assert client.access_key == "dataforge"

    assert client.secret_key == "password"

    assert client.secure is False


# =========================================================
# Connection
# =========================================================


def test_test_connection(client):

    client._client.list_buckets.return_value = []

    assert client.test_connection() is True


# =========================================================
# Bucket Operations
# =========================================================


def test_bucket_exists(client):

    client._client.bucket_exists.return_value = True

    assert client.bucket_exists("bronze")


def test_create_bucket(client):

    client._client.bucket_exists.return_value = False

    client.create_bucket("bronze")

    client._client.make_bucket.assert_called_once_with(
        "bronze",
    )


def test_list_buckets(client):

    bucket = MagicMock()

    bucket.name = "bronze"

    client._client.list_buckets.return_value = [bucket]

    buckets = client.list_buckets()

    assert buckets == ["bronze"]


# =========================================================
# Upload
# =========================================================


def test_upload_file(client, tmp_path):

    file = tmp_path / "customers.csv"

    file.write_text("hello")

    client.upload_file(
        bucket="bronze",
        object_name="customers.csv",
        file_path=file,
    )

    client._client.fput_object.assert_called_once()


# =========================================================
# Download
# =========================================================


def test_download_file(client, tmp_path):

    destination = tmp_path / "customers.csv"

    client.download_file(
        bucket="bronze",
        object_name="customers.csv",
        destination=destination,
    )

    client._client.fget_object.assert_called_once()


# =========================================================
# Delete
# =========================================================


def test_delete_object(client):

    client.delete_object(
        bucket="bronze",
        object_name="customers.csv",
    )

    client._client.remove_object.assert_called_once_with(
        "bronze",
        "customers.csv",
    )


# =========================================================
# List Objects
# =========================================================


def test_list_objects(client):

    obj = MagicMock()

    obj.object_name = "customers.csv"
    obj.size = 100
    obj.etag = "abc123"
    obj.last_modified = None

    client._client.bucket_exists.return_value = True

    client._client.list_objects.return_value = [obj]

    objects = client.list_objects("bronze")

    assert len(objects) == 1

    assert isinstance(
        objects[0],
        StorageObject,
    )

    assert objects[0].bucket == "bronze"

    assert objects[0].key == "customers.csv"


def test_list_objects_bucket_missing(client):

    client._client.bucket_exists.return_value = False

    with pytest.raises(BucketNotFoundError):

        client.list_objects("missing")


# =========================================================
# Representation
# =========================================================


def test_repr(client):

    representation = repr(client)

    assert "MinIOClient" in representation

    assert "localhost:9000" in representation
