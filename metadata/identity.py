"""
DataForge Metadata Identity

Deterministic identity helpers for the metadata subsystem.

Dataset identity and schema fingerprints are derived, not
randomly generated, so that registering the same logical
dataset or schema twice is naturally idempotent.
"""

from __future__ import annotations

import hashlib
import uuid
from typing import Any

# =========================================================
# Namespace
# =========================================================

# Fixed namespace UUID for DataForge dataset identity.
# Never change this value once datasets exist in production --
# doing so would change every dataset_id.
DATASET_NAMESPACE = uuid.UUID(
    "6f1c6b2e-6b8a-4b8a-9b8a-1e2d3c4b5a6f",
)


# =========================================================
# Dataset Identity
# =========================================================


def dataset_id(
    layer: str,
    source: str,
    table: str,
) -> uuid.UUID:
    """
    Derive a deterministic dataset identity.

    The same (layer, source, table) always yields the same
    dataset_id, so registering a dataset that already exists
    is naturally idempotent.
    """

    key = f"{layer}:{source}:{table}"

    return uuid.uuid5(
        DATASET_NAMESPACE,
        key,
    )


# =========================================================
# Schema Fingerprint
# =========================================================


def schema_fingerprint(
    columns: list[dict[str, Any]],
) -> str:
    """
    Derive a deterministic fingerprint for a schema.

    Two schemas with the same columns (name, dtype, nullable)
    in any order produce the same fingerprint, so identical
    schemas across separate pipeline runs are deduplicated.

    Parameters
    ----------
    columns:
        A list of dicts, each with at least "name", "dtype",
        and "nullable" keys.
    """

    normalized = sorted(
        (
            str(column["name"]),
            str(column["dtype"]),
            bool(column["nullable"]),
        )
        for column in columns
    )

    payload = "|".join(
        f"{name}:{dtype}:{nullable}"
        for name, dtype, nullable in normalized
    )

    return hashlib.sha256(
        payload.encode("utf-8"),
    ).hexdigest()


# =========================================================
# New Random Identities
# =========================================================


def new_id() -> uuid.UUID:
    """
    Generate a fresh random identity.

    Used for entities that have no natural deterministic key
    (e.g. step_run_id, schema_version_id, lineage_edge_id).
    """

    return uuid.uuid4()