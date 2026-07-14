"""
DataForge Connector Factory Tests
"""

from __future__ import annotations

import pytest

from connectors.base.base_connector import BaseConnector
from connectors.base.exceptions import ConnectorNotFoundError
from connectors.base.factory import ConnectorFactory
from connectors.base.registry import ConnectorRegistry
from connectors.config.connector_config import ConnectorConfig


# ---------------------------------------------------------
# Dummy Connector
# ---------------------------------------------------------


class DummyConnector(BaseConnector):
    """
    Minimal connector used for factory testing.
    """

    def connect(self) -> None:

        self._connected = True

    def disconnect(self) -> None:

        self._connected = False

    def read(self, *args, **kwargs):

        return []

    def write(
        self,
        data,
        *args,
        **kwargs,
    ) -> None:

        return None

    def test_connection(self) -> bool:

        return True


# ---------------------------------------------------------
# Test Fixture
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


def test_factory_initialization():

    factory = ConnectorFactory()

    assert factory.registry is not None


# ---------------------------------------------------------


def test_create_connector():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    connector = factory.create(
        "dummy",
        make_config(),
    )

    assert isinstance(
        connector,
        DummyConnector,
    )


# ---------------------------------------------------------


def test_connector_configuration():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    config = make_config()

    factory = ConnectorFactory()

    connector = factory.create(
        "dummy",
        config,
    )

    assert connector.config is config


# ---------------------------------------------------------


def test_connector_not_found():

    factory = ConnectorFactory()

    with pytest.raises(
        ConnectorNotFoundError,
    ):

        factory.create(
            "missing",
            make_config(),
        )


# ---------------------------------------------------------


def test_available_connectors():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    ConnectorRegistry.register(
        "another",
        DummyConnector,
    )

    factory = ConnectorFactory()

    assert factory.available_connectors() == [
        "another",
        "dummy",
    ]


# ---------------------------------------------------------


def test_exists():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    assert factory.exists("dummy")

    assert not factory.exists("postgres")


# ---------------------------------------------------------


def test_registry_property():

    factory = ConnectorFactory()

    assert factory.registry is ConnectorRegistry


# ---------------------------------------------------------


def test_create_multiple_instances():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    connector1 = factory.create(
        "dummy",
        make_config(),
    )

    connector2 = factory.create(
        "dummy",
        make_config(),
    )

    assert connector1 is not connector2


# ---------------------------------------------------------


def test_connector_type():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    connector = factory.create(
        "dummy",
        make_config(),
    )

    assert isinstance(
        connector,
        BaseConnector,
    )


# ---------------------------------------------------------


def test_repr():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    representation = repr(factory)

    assert "ConnectorFactory" in representation

    assert "1" in representation


# ---------------------------------------------------------


def test_factory_uses_custom_registry():

    registry = ConnectorRegistry()

    registry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory(
        registry,
    )

    connector = factory.create(
        "dummy",
        make_config(),
    )

    assert isinstance(
        connector,
        DummyConnector,
    )


# ---------------------------------------------------------


def test_factory_returns_new_connector_each_time():

    ConnectorRegistry.register(
        "dummy",
        DummyConnector,
    )

    factory = ConnectorFactory()

    first = factory.create(
        "dummy",
        make_config(),
    )

    second = factory.create(
        "dummy",
        make_config(),
    )

    assert first != second
