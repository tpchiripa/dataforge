"""
DataForge Discovery Tests
"""

from connectors.base.registry import ConnectorRegistry
from connectors.discovery.discovery import ConnectorDiscovery


def test_discovery_finds_connectors():

    discovery = ConnectorDiscovery("connectors")

    connectors = discovery.discover()

    assert len(connectors) > 0


def test_discovery_registers_postgresql():

    ConnectorRegistry.clear()

    discovery = ConnectorDiscovery("connectors")

    discovery.discover()

    assert ConnectorRegistry.exists("postgresql")


def test_discovery_returns_connector_classes():

    discovery = ConnectorDiscovery("connectors")

    connectors = discovery.discover()

    assert all(isinstance(connector, type) for connector in connectors)


def test_discovery_returns_postgresql_connector():

    discovery = ConnectorDiscovery("connectors")

    connectors = discovery.discover()

    names = [connector.__name__ for connector in connectors]

    assert "PostgreSQLConnector" in names


def test_registry_returns_postgresql_connector():

    ConnectorRegistry.clear()

    discovery = ConnectorDiscovery("connectors")

    discovery.discover()

    connector_class = ConnectorRegistry.get("postgresql")

    assert connector_class.__name__ == "PostgreSQLConnector"
