"""
DataForge PostgreSQL Connector Test

Run:

    python tests/connectors/test_postgres.py
"""

from pathlib import Path
import sys

# ---------------------------------------------------------------------
# Add the DataForge project root to Python's import path
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------

from connectors.base import (
    ConnectorConfig,
    ConnectorType,
)
from connectors.databases.postgresql import PostgreSQLConnector


def main():

    config = ConnectorConfig(
        name="DataForge Metadata Database",
        connector_type=ConnectorType.DATABASE,
        host="localhost",
        port=5433,
        database="dataforge",
        username="dataforge",
        password="DataForge2026!",
    )

    connector = PostgreSQLConnector(config)

    print("=" * 60)
    print("DataForge PostgreSQL Connector Test")
    print("=" * 60)

    # ---------------------------------------------------------
    # Validate Configuration
    # ---------------------------------------------------------

    print("\n[1] Validating configuration...")

    if connector.validate():
        print("✓ Configuration is valid")
    else:
        print("✗ Configuration is invalid")
        return

    # ---------------------------------------------------------
    # Connect
    # ---------------------------------------------------------

    print("\n[2] Connecting to PostgreSQL...")

    try:

        result = connector.connect()

        print(f"✓ {result.message}")

    except Exception as exc:

        print("✗ Connection failed")
        print(exc)
        return

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    print("\n[3] Connector Metadata")

    metadata = connector.get_metadata()

    print(f"Name        : {metadata.name}")
    print(f"Version     : {metadata.version}")
    print(f"Type        : {metadata.connector_type}")
    print(f"Batch       : {metadata.supports_batch}")
    print(f"Streaming   : {metadata.supports_streaming}")

    # ---------------------------------------------------------
    # Tables
    # ---------------------------------------------------------

    print("\n[4] Discovering Tables...")

    tables = connector.list_datasets()

    print(f"Found {len(tables)} tables\n")

    for table in tables:
        print(f" - {table.name}")

    # ---------------------------------------------------------
    # SQL Query
    # ---------------------------------------------------------

    print("\n[5] Running SQL Query...")

    df = connector.fetch_dataframe(
        """
        SELECT
            dag_id,
            is_paused
        FROM dag;
        """
    )

    print(df)

    # ---------------------------------------------------------
    # Disconnect
    # ---------------------------------------------------------

    print("\n[6] Disconnecting...")

    connector.disconnect()

    print("✓ Connection closed")

    print("\n🎉 All tests completed successfully.")


if __name__ == "__main__":
    main()
