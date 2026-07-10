"""
DataForge Discovery Tests
"""

from connectors.base import ConnectorRegistry
from connectors.discovery.discovery import ConnectorDiscovery


def setup_function():
    """
    Ensure every test starts with a clean registry.
    """
    ConnectorRegistry.clear()


def test_discovery_finds_connectors():

    discovery = ConnectorDiscovery("connectors")

    connectors = discovery.discover()

    assert len(connectors) >= 1


def test_discovery_registers_postgresql():

    discovery = ConnectorDiscovery("connectors")

    discovery.discover()

    assert ConnectorRegistry.exists("postgresql")


def test_discovery_returns_connector_classes():

    discovery = ConnectorDiscovery("connectors")

    connectors = discovery.discover()

    assert connectors[0].__name__ == "PostgreSQLConnector"
