"""
DataForge Loader Tests
"""

from connectors.base import BaseConnector
from connectors.discovery.loader import ConnectorLoader


def test_loader_loads_postgresql_connector():

    loader = ConnectorLoader()

    connector_class = loader.load(
        "connectors/databases/postgresql/connector.py"
    )

    assert connector_class.__name__ == "PostgreSQLConnector"


def test_loader_returns_connector_class():

    loader = ConnectorLoader()

    connector_class = loader.load(
        "connectors/databases/postgresql/connector.py"
    )

    assert isinstance(connector_class, type)


def test_loader_returns_baseconnector_subclass():

    loader = ConnectorLoader()

    connector_class = loader.load(
        "connectors/databases/postgresql/connector.py"
    )

    assert issubclass(
        connector_class,
        BaseConnector,
    )
