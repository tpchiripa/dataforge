"""
DataForge StorageObject Tests
"""

from __future__ import annotations



from storage.models.storage_object import StorageObject

# =========================================================
# Creation
# =========================================================


def test_create_storage_object():

    obj = StorageObject(
        bucket="bronze",
        key="customers/data.csv",
    )

    assert obj.bucket == "bronze"
    assert obj.key == "customers/data.csv"


# =========================================================
# Default Values
# =========================================================


def test_default_values():

    obj = StorageObject(
    bucket="silver",
    key="customers.csv",
)
