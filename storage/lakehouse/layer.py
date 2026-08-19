"""
DataForge Medallion Architecture

Defines the Bronze / Silver / Gold layers of the lakehouse and the
naming convention used to store objects within each layer.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum


# =========================================================
# Medallion Layer
# =========================================================


class MedallionLayer(str, Enum):
    """
    The layers of the Medallion (Bronze/Silver/Gold) architecture.

    The value of each member is the storage bucket it maps to.
    """

    STAGING = "staging"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    @property
    def bucket(self) -> str:
        """
        Returns the storage bucket backing this layer.
        """

        return self.value


# =========================================================
# Lakehouse Path Convention
# =========================================================


class LakehousePath:
    """
    Builds and parses partitioned object keys for the lakehouse.

    Convention
    ----------
    {source}/{table}/{year}/{month}/{day}/{filename}

    Examples
    --------
    LakehousePath.build(
        source="postgres_orders",
        table="orders",
        filename="orders_20260819.parquet",
    )
    -> "postgres_orders/orders/2026/08/19/orders_20260819.parquet"
    """

    @staticmethod
    def build(
        source: str,
        table: str,
        filename: str,
        as_of: date | datetime | None = None,
    ) -> str:

        if not source:
            raise ValueError("source must not be empty")

        if not table:
            raise ValueError("table must not be empty")

        if not filename:
            raise ValueError("filename must not be empty")

        as_of = as_of or datetime.utcnow()

        return (
            f"{source}/{table}/"
            f"{as_of.year:04d}/{as_of.month:02d}/{as_of.day:02d}/"
            f"{filename}"
        )

    @staticmethod
    def parse(key: str) -> dict[str, str]:
        """
        Parses a lakehouse key back into its components.

        Raises
        ------
        ValueError
            If the key does not match the expected convention.
        """

        parts = key.split("/")

        if len(parts) != 6:
            raise ValueError(
                f"Key does not match lakehouse convention: {key!r}"
            )

        source, table, year, month, day, filename = parts

        return {
            "source": source,
            "table": table,
            "year": year,
            "month": month,
            "day": day,
            "filename": filename,
        }