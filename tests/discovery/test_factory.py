"""
DataForge Factory Tests
"""

from connectors.base import (ConnectorConfig, ConnectorFactory,
                             ConnectorRegistry, ConnectorType)
from connectors.discovery.discovery import ConnectorDiscovery


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


def test_factory_lists_connectors():

    ConnectorDiscovery("connectors").discover()

    factory = ConnectorFactory()

    available = factory.available_connectors()

    assert "postgresql" in available


def test_factory_creates_connector():

    ConnectorDiscovery("connectors").discover()

    factory = ConnectorFactory()

    connector = factory.create(
        "postgresql",
        build_config(),
    )

    assert connector.__class__.__name__ == "PostgreSQLConnector"


def test_factory_connects_to_database():

    ConnectorDiscovery("connectors").discover()

    factory = ConnectorFactory()

    connector = factory.create(
        "postgresql",
        build_config(),
    )

    result = connector.connect()

    assert result.success is True

    connector.disconnect()
