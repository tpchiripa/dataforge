"""
DataForge Connector Configuration Tests
"""

from __future__ import annotations

import pytest

from connectors.config.connector_config import ConnectorConfig

# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_create_connector_config():

    config = ConnectorConfig(
        name="CSV Connector",
    )

    assert config.name == "CSV Connector"

    assert config.enabled is True

    assert config.timeout == 30

    assert config.retries == 3

    assert config.options == {}


def test_custom_values():

    config = ConnectorConfig(
        name="Postgres",
        enabled=False,
        timeout=60,
        retries=5,
        connection_string="postgres://localhost",
        description="Database connector",
        version="2.0.0",
        options={
            "schema": "public",
        },
    )

    assert config.enabled is False

    assert config.timeout == 60

    assert config.retries == 5

    assert config.connection_string == "postgres://localhost"

    assert config.description == "Database connector"

    assert config.version == "2.0.0"

    assert config.options["schema"] == "public"


def test_empty_name():

    with pytest.raises(ValueError):

        ConnectorConfig(
            name="",
        )


def test_blank_name():

    with pytest.raises(ValueError):

        ConnectorConfig(
            name="     ",
        )


def test_negative_timeout():

    with pytest.raises(ValueError):

        ConnectorConfig(
            name="CSV",
            timeout=-1,
        )


def test_negative_retries():

    with pytest.raises(ValueError):

        ConnectorConfig(
            name="CSV",
            retries=-5,
        )


def test_validate():

    config = ConnectorConfig(
        name="CSV",
    )

    assert config.validate() is None


def test_repr():

    config = ConnectorConfig(
        name="CSV",
    )

    representation = repr(config)

    assert "ConnectorConfig" in representation

    assert "CSV" in representation


def test_options_are_independent():

    first = ConnectorConfig(
        name="CSV",
    )

    second = ConnectorConfig(
        name="JSON",
    )

    first.options["delimiter"] = ","

    assert second.options == {}


def test_default_connection_string():

    config = ConnectorConfig(
        name="CSV",
    )

    assert config.connection_string == ""
