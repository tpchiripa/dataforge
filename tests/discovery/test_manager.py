"""
DataForge Manager Tests
"""

from connectors.base import (
    ConnectorConfig,
    ConnectorRegistry,
    ConnectorType,
)
from connectors.discovery.manager import ConnectorManager


def setup_function():
    """
    Reset registry before every test.
    """
    ConnectorRegistry.clear()


def build_config():

    return ConnectorConfig(
        name="Metadata Database",
        connector_type=ConnectorType.DATABASE,
        host="localhost",
        port=5433,
        database="dataforge",
        username="dataforge",
        password="DataForge2026!",
    )


def test_manager_discovers_connectors():

    manager = ConnectorManager("connectors")

    manager.discover()

    assert "postgresql" in manager.registered_connectors()


def test_manager_creates_connector():

    manager = ConnectorManager("connectors")

    manager.discover()

    connector = manager.create(
        "postgresql",
        build_config(),
    )

    assert connector.__class__.__name__ == "PostgreSQLConnector"


def test_manager_catalog():

    manager = ConnectorManager("connectors")

    manager.discover()

    assert manager.count() == 1

    assert manager.exists("postgresql")


def test_manager_inspector():

    manager = ConnectorManager("connectors")

    manager.discover()

    info = manager.inspect("postgresql")

    assert info["display_name"] == "PostgreSQL"

    assert info["version"] == "1.0.0"


def test_manager_clear_registry():

    manager = ConnectorManager("connectors")

    manager.discover()

    assert len(manager.registered_connectors()) == 1

    manager.clear()

    assert len(manager.registered_connectors()) == 0
