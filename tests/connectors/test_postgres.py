"""
DataForge PostgreSQL Connector Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from connectors.config.connector_config import ConnectorConfig
from connectors.databases.postgresql.connector import PostgreSQLConnector

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def make_config() -> ConnectorConfig:

    return ConnectorConfig(
        name="postgres",
        host="localhost",
        port=5432,
        database="dataforge",
        username="postgres",
        password="password",
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_connector_initialization():

    connector = PostgreSQLConnector(make_config())

    assert connector.connection is None

    assert connector.connected is False


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_connect(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    connector.connect()

    assert connector.connected is True

    assert connector.connection is mock_connection

    mock_connect.assert_called_once()


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_disconnect(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    connector.connect()

    connector.disconnect()

    mock_connection.close.assert_called_once()

    assert connector.connection is None

    assert connector.connected is False


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_reconnect(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    connector.connect()

    connector.connect()

    mock_connect.assert_called_once()


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_test_connection_success(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    assert connector.test_connection() is True


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_test_connection_failure(mock_connect):

    mock_connect.side_effect = Exception("Connection failed")

    connector = PostgreSQLConnector(make_config())

    assert connector.test_connection() is False


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_connection_property(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    connector.connect()

    assert connector.connection is mock_connection


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_connected_property(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    assert connector.connected is False

    connector.connect()

    assert connector.connected is True


# ---------------------------------------------------------


@patch(
    "connectors.databases.postgresql.connector.psycopg2.connect"
)
def test_repr(mock_connect):

    mock_connection = MagicMock()

    mock_connection.closed = False

    mock_connect.return_value = mock_connection

    connector = PostgreSQLConnector(make_config())

    connector.connect()

    representation = repr(connector)

    assert "PostgreSQLConnector" in representation

    assert "dataforge" in representation

    assert "localhost" in representation


# ---------------------------------------------------------


def test_configuration_is_retained():

    config = make_config()

    connector = PostgreSQLConnector(config)

    assert connector.config is config
