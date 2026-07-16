"""
DataForge Connector Manager Tests
"""

from __future__ import annotations

import pytest

from connectors.base.base_connector import BaseConnector
from connectors.base.manager import ConnectorManager
from connectors.base.registry import ConnectorRegistry
from connectors.config.connector_config import ConnectorConfig

# ---------------------------------------------------------
# Dummy Connector
# ---------------------------------------------------------


class DummyConnector(BaseConnector):
    """
    Dummy connector used for testing.
    """

    def connect(self) -> None:

        self._connected = True

    def disconnect(self) -> None:

        self._connected = False

    def read(self):

        return []

    def write(
        self,
        data,
    ) -> None:

        pass

    def test_connection(self) -> bool:

        return True


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_registry():

    ConnectorRegistry.clear()

    yield

    ConnectorRegistry.clear()


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def make_config() -> ConnectorConfig:

    return ConnectorConfig(
        name="dummy",
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_manager_initialization():

    manager = ConnectorManager()

    assert manager.count == 0


# ---------------------------------------------------------


def test_create_connector():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    connector = manager.create(
        "dummy",
        make_config(),
    )

    assert isinstance(
        connector,
        DummyConnector,
    )

    assert manager.count == 1


# ---------------------------------------------------------


def test_get_connector():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    created = manager.create(
        "dummy",
        make_config(),
    )

    retrieved = manager.get(
        "dummy",
    )

    assert retrieved is created


# ---------------------------------------------------------


def test_exists():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    assert manager.exists("dummy")

    assert not manager.exists("postgres")


# ---------------------------------------------------------


def test_remove_connector():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    manager.remove("dummy")

    assert manager.count == 0


# ---------------------------------------------------------


def test_connect_all():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    connector = manager.create(
        "dummy",
        make_config(),
    )

    manager.connect_all()

    assert connector.connected


# ---------------------------------------------------------


def test_disconnect_all():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    connector = manager.create(
        "dummy",
        make_config(),
    )

    manager.connect_all()

    manager.disconnect_all()

    assert not connector.connected


# ---------------------------------------------------------


def test_connected():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    connector = manager.create(
        "dummy",
        make_config(),
    )

    manager.connect_all()

    connected = manager.connected()

    assert connector in connected

    assert len(connected) == 1


# ---------------------------------------------------------


def test_disconnected():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    connector = manager.create(
        "dummy",
        make_config(),
    )

    disconnected = manager.disconnected()

    assert connector in disconnected

    assert len(disconnected) == 1


# ---------------------------------------------------------


def test_list():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    assert manager.list() == [
        "dummy",
    ]


# ---------------------------------------------------------


def test_clear():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    manager.clear()

    assert manager.count == 0


# ---------------------------------------------------------


def test_len():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    assert len(manager) == 1


# ---------------------------------------------------------


def test_repr():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy",
        make_config(),
    )

    representation = repr(manager)

    assert "ConnectorManager" in representation

    assert "1" in representation


# ---------------------------------------------------------


def test_multiple_connectors():

    ConnectorRegistry.register(
        "dummy1",
        DummyConnector,
    )

    ConnectorRegistry.register(
        "dummy2",
        DummyConnector,
    )

    manager = ConnectorManager()

    manager.create(
        "dummy1",
        ConnectorConfig(name="dummy1"),
    )

    manager.create(
        "dummy2",
        ConnectorConfig(name="dummy2"),
    )

    assert manager.count == 2

    assert manager.list() == [
        "dummy1",
        "dummy2",
    ]
