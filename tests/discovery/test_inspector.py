"""
DataForge Inspector Tests
"""

from connectors.base import ConnectorRegistry
from connectors.discovery.discovery import ConnectorDiscovery
from connectors.discovery.inspector import ConnectorInspector


def setup_function():
    """
    Reset registry before every test.
    """
    ConnectorRegistry.clear()


def test_inspector_returns_connector_information():

    ConnectorDiscovery("connectors").discover()

    inspector = ConnectorInspector()

    info = inspector.inspect("postgresql")

    assert info["name"] == "postgresql"

    assert info["display_name"] == "PostgreSQL"

    assert info["version"] == "1.0.0"


def test_inspector_lists_methods():

    ConnectorDiscovery("connectors").discover()

    inspector = ConnectorInspector()

    info = inspector.inspect("postgresql")

    methods = info["methods"]

    assert "connect" in methods

    assert "disconnect" in methods

    assert "extract" in methods


def test_inspector_lists_capabilities():

    ConnectorDiscovery("connectors").discover()

    inspector = ConnectorInspector()

    info = inspector.inspect("postgresql")

    assert info["supports"]["batch"] is True

    assert info["supports"]["streaming"] is False

    assert info["supports"]["incremental"] is True


def test_inspector_inspects_all():

    ConnectorDiscovery("connectors").discover()

    inspector = ConnectorInspector()

    connectors = inspector.inspect_all()

    assert len(connectors) == 1

    assert connectors[0]["name"] == "postgresql"
