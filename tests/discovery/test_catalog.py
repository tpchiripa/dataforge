"""
DataForge Catalog Tests
"""

from connectors.base import ConnectorRegistry
from connectors.discovery.catalog import ConnectorCatalog
from connectors.discovery.discovery import ConnectorDiscovery


def setup_function():
    """
    Reset registry before each test.
    """
    ConnectorRegistry.clear()


def test_catalog_lists_connectors():

    ConnectorDiscovery("connectors").discover()

    catalog = ConnectorCatalog()

    connectors = catalog.list()

    assert len(connectors) == 1


def test_catalog_returns_postgresql():

    ConnectorDiscovery("connectors").discover()

    catalog = ConnectorCatalog()

    connector = catalog.get("postgresql")

    assert connector["display_name"] == "PostgreSQL"

    assert connector["version"] == "1.0.0"


def test_catalog_exists():

    ConnectorDiscovery("connectors").discover()

    catalog = ConnectorCatalog()

    assert catalog.exists("postgresql")

    assert not catalog.exists("mysql")


def test_catalog_count():

    ConnectorDiscovery("connectors").discover()

    catalog = ConnectorCatalog()

    assert catalog.count() == 1
