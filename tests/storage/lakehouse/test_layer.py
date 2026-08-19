"""
DataForge Medallion Layer Tests
"""

from __future__ import annotations

from datetime import datetime

import pytest

from storage.lakehouse.layer import LakehousePath, MedallionLayer


# =========================================================
# MedallionLayer
# =========================================================


def test_layer_buckets():

    assert MedallionLayer.STAGING.bucket == "staging"

    assert MedallionLayer.BRONZE.bucket == "bronze"

    assert MedallionLayer.SILVER.bucket == "silver"

    assert MedallionLayer.GOLD.bucket == "gold"


# =========================================================
# LakehousePath.build
# =========================================================


def test_build_key():

    key = LakehousePath.build(
        source="postgres_orders",
        table="orders",
        filename="orders_20260819.parquet",
        as_of=datetime(2026, 8, 19),
    )

    assert key == "postgres_orders/orders/2026/08/19/orders_20260819.parquet"


def test_build_key_defaults_to_now():

    key = LakehousePath.build(
        source="postgres_orders",
        table="orders",
        filename="orders.parquet",
    )

    assert key.startswith("postgres_orders/orders/")

    assert key.endswith("orders.parquet")


def test_build_key_requires_source():

    with pytest.raises(ValueError):

        LakehousePath.build(
            source="",
            table="orders",
            filename="orders.parquet",
        )


def test_build_key_requires_table():

    with pytest.raises(ValueError):

        LakehousePath.build(
            source="postgres_orders",
            table="",
            filename="orders.parquet",
        )


def test_build_key_requires_filename():

    with pytest.raises(ValueError):

        LakehousePath.build(
            source="postgres_orders",
            table="orders",
            filename="",
        )


# =========================================================
# LakehousePath.parse
# =========================================================


def test_parse_key():

    parsed = LakehousePath.parse(
        "postgres_orders/orders/2026/08/19/orders_20260819.parquet"
    )

    assert parsed == {
        "source": "postgres_orders",
        "table": "orders",
        "year": "2026",
        "month": "08",
        "day": "19",
        "filename": "orders_20260819.parquet",
    }


def test_parse_key_invalid():

    with pytest.raises(ValueError):

        LakehousePath.parse("not/a/valid/key")