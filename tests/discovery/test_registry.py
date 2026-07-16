"""
DataForge Registry Tests
"""

import pytest

from connectors.base import (ConnectorNotFoundError,
                             ConnectorRegistrationError, ConnectorRegistry)
from connectors.discovery.discovery import ConnectorDiscovery


def setup_function():
    """
    Reset registry before each test.
    """
    ConnectorRegistry.clear()


def test_registry_registers_connector():

    ConnectorDiscovery("connectors").discover()

    assert ConnectorRegistry.exists("postgresql")


def test_registry_returns_connector():

    ConnectorDiscovery("connectors").discover()

    connector = ConnectorRegistry.get("postgresql")

    assert connector.__name__ == "PostgreSQLConnector"


def test_registry_lists_connectors():

    ConnectorDiscovery("connectors").discover()

    connectors = ConnectorRegistry.list_connectors()

    assert "postgresql" in connectors


def test_registry_prevents_duplicate_registration():

    ConnectorDiscovery("connectors").discover()

    connector = ConnectorRegistry.get("postgresql")

    with pytest.raises(ConnectorRegistrationError):

        ConnectorRegistry.register(
            "postgresql",
            connector,
        )


def test_registry_raises_not_found():

    with pytest.raises(ConnectorNotFoundError):

        ConnectorRegistry.get("mysql")
