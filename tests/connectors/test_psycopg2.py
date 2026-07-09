"""
Test psycopg2 connection directly.

Run:

    python tests/connectors/test_psycopg2.py
"""

import psycopg2

print("=" * 70)
print("Testing psycopg2")
print("=" * 70)

try:

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="dataforge",
        user="dataforge",
        password="DataForge2026!",
    )

    print("✓ Connected successfully!")

    cursor = connection.cursor()

    cursor.execute("SELECT current_user, current_database();")

    print(cursor.fetchone())

    cursor.close()
    connection.close()

except Exception as exc:

    print("FAILED")
    print(exc)
