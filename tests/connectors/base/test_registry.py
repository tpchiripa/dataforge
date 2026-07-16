"""
DataForge Connector Registry Tests
"""

from __future__ import annotations

import pytest

from connectors.base.base_connector import BaseConnector
from connectors.base.exceptions import (ConnectorNotFoundError,
                                        ConnectorRegistrationError)
from connectors.base.registry import ConnectorRegistry
from connectors.config.connector_config import ConnectorConfig

# ---------------------------------------------------------
# Dummy Connector
# ---------------------------------------------------------


class DummyConnector(BaseConnector):
    """
    Minimal connector used for registry testing.
    """

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def read(self, *args, **kwargs):
        """
        Dummy read implementation.
        """
        return []

    def write(self, data, *args, **kwargs):
        """
        Dummy write implementation.
        """
        return None

    def test_connection(self) -> bool:
        return True


# ---------------------------------------------------------
# Test Fixture
# ---------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_registry():
    """
    Ensure every test starts with a clean registry.
    """

    ConnectorRegistry.clear()

    yield

    ConnectorRegistry.clear()


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_registry_initialization():

    registry = ConnectorRegistry()

    assert registry.count() == 0


# ---------------------------------------------------------


def test_register_connector():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    assert registry.count() == 1

    assert registry.exists("dummy")


# ---------------------------------------------------------


def test_duplicate_registration():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    with pytest.raises(
        ConnectorRegistrationError,
    ):

        registry.register(
            "dummy",
            DummyConnector,
        )


# ---------------------------------------------------------


def test_get_connector():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    connector = registry.get("dummy")

    assert connector is DummyConnector


# ---------------------------------------------------------


def test_connector_not_found():

    registry = ConnectorRegistry()

    with pytest.raises(
        ConnectorNotFoundError,
    ):

        registry.get("missing")


# ---------------------------------------------------------


def test_unregister_connector():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    registry.unregister("dummy")

    assert registry.count() == 0

    assert not registry.exists("dummy")


# ---------------------------------------------------------


def test_list_connectors():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    registry.register(
        "another",
        DummyConnector,
    )

    assert registry.list_connectors() == [
        "another",
        "dummy",
    ]


# ---------------------------------------------------------


def test_list_connector_classes():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    connectors = registry.list()

    assert connectors == [DummyConnector]


# ---------------------------------------------------------


def test_clear_registry():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    registry.clear()

    assert registry.count() == 0


# ---------------------------------------------------------


def test_iteration():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    connectors = [
        connector
        for connector in registry
    ]

    assert connectors == [DummyConnector]


# ---------------------------------------------------------


def test_len():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    assert len(registry) == 1


# ---------------------------------------------------------


def test_contains():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    assert "dummy" in registry

    assert "postgres" not in registry


# ---------------------------------------------------------


def test_repr():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    representation = repr(registry)

    assert "ConnectorRegistry" in representation

    assert "1" in representation


# ---------------------------------------------------------


def test_registry_returns_registered_class():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    connector_class = registry.get("dummy")

    config = ConnectorConfig(
        name="dummy",
    )

    connector = connector_class(config)

    assert isinstance(
        connector,
        DummyConnector,
    )
