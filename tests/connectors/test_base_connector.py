"""
DataForge Base Connector Tests
"""

from __future__ import annotations

import pytest

from connectors.base.base_connector import BaseConnector
from connectors.config.connector_config import ConnectorConfig


# ---------------------------------------------------------
# Dummy Connector
# ---------------------------------------------------------

class DummyConnector(BaseConnector):
    """
    Concrete implementation used for testing.
    """

    def connect(self) -> None:

        self._connected = True

    def disconnect(self) -> None:

        self._connected = False

    def test_connection(self) -> bool:

        return self.connected

    def read(self, *args, **kwargs):

        return {"message": "read"}

    def write(self, data, *args, **kwargs):

        self._last_write = data


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def make_config() -> ConnectorConfig:

    return ConnectorConfig(
        name="Dummy Connector",
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_create_connector():

    connector = DummyConnector(make_config())

    assert connector.config.name == "Dummy Connector"

    assert connector.connected is False


def test_connect():

    connector = DummyConnector(make_config())

    connector.connect()

    assert connector.connected is True


def test_disconnect():

    connector = DummyConnector(make_config())

    connector.connect()

    connector.disconnect()

    assert connector.connected is False


def test_test_connection():

    connector = DummyConnector(make_config())

    assert connector.test_connection() is False

    connector.connect()

    assert connector.test_connection() is True


def test_read():

    connector = DummyConnector(make_config())

    result = connector.read()

    assert result == {
        "message": "read",
    }


def test_write():

    connector = DummyConnector(make_config())

    connector.write({"id": 1})

    assert connector._last_write == {
        "id": 1,
    }


def test_context_manager():

    with DummyConnector(make_config()) as connector:

        assert connector.connected is True

    assert connector.connected is False


def test_validate_configuration():

    config = ConnectorConfig(
        name="Dummy",
    )

    connector = DummyConnector(config)

    assert connector.config is config


def test_repr():

    connector = DummyConnector(make_config())

    representation = repr(connector)

    assert "DummyConnector" in representation

    assert "Dummy Connector" in representation


def test_connected_property():

    connector = DummyConnector(make_config())

    assert connector.connected is False

    connector.connect()

    assert connector.connected is True
