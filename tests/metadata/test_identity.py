"""
DataForge Metadata Identity Tests
"""

from __future__ import annotations

from metadata.identity import dataset_id, new_id, schema_fingerprint


# =========================================================
# dataset_id
# =========================================================


def test_dataset_id_is_deterministic():

    first = dataset_id("bronze", "postgres_orders", "orders")

    second = dataset_id("bronze", "postgres_orders", "orders")

    assert first == second


def test_dataset_id_differs_by_layer():

    bronze = dataset_id("bronze", "postgres_orders", "orders")

    silver = dataset_id("silver", "postgres_orders", "orders")

    assert bronze != silver


def test_dataset_id_differs_by_source():

    first = dataset_id("bronze", "postgres_orders", "orders")

    second = dataset_id("bronze", "mysql_orders", "orders")

    assert first != second


def test_dataset_id_differs_by_table():

    first = dataset_id("bronze", "postgres_orders", "orders")

    second = dataset_id("bronze", "postgres_orders", "customers")

    assert first != second


# =========================================================
# schema_fingerprint
# =========================================================


def test_schema_fingerprint_is_deterministic():

    columns = [
        {"name": "id", "dtype": "int64", "nullable": False},
        {"name": "name", "dtype": "object", "nullable": True},
    ]

    first = schema_fingerprint(columns)

    second = schema_fingerprint(columns)

    assert first == second


def test_schema_fingerprint_ignores_column_order():

    columns_a = [
        {"name": "id", "dtype": "int64", "nullable": False},
        {"name": "name", "dtype": "object", "nullable": True},
    ]

    columns_b = [
        {"name": "name", "dtype": "object", "nullable": True},
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    assert schema_fingerprint(columns_a) == schema_fingerprint(columns_b)


def test_schema_fingerprint_changes_on_new_column():

    columns_a = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    columns_b = [
        {"name": "id", "dtype": "int64", "nullable": False},
        {"name": "name", "dtype": "object", "nullable": True},
    ]

    assert schema_fingerprint(columns_a) != schema_fingerprint(columns_b)


def test_schema_fingerprint_changes_on_dtype_change():

    columns_a = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    columns_b = [
        {"name": "id", "dtype": "object", "nullable": False},
    ]

    assert schema_fingerprint(columns_a) != schema_fingerprint(columns_b)


def test_schema_fingerprint_changes_on_nullable_change():

    columns_a = [
        {"name": "id", "dtype": "int64", "nullable": False},
    ]

    columns_b = [
        {"name": "id", "dtype": "int64", "nullable": True},
    ]

    assert schema_fingerprint(columns_a) != schema_fingerprint(columns_b)


# =========================================================
# new_id
# =========================================================


def test_new_id_is_unique():

    first = new_id()

    second = new_id()

    assert first != second