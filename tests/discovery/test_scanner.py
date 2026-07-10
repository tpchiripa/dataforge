"""
DataForge Scanner Tests
"""

from pathlib import Path

from connectors.discovery.scanner import ConnectorScanner


def test_scanner_finds_postgresql_connector():

    scanner = ConnectorScanner("connectors")

    files = scanner.scan()

    assert len(files) > 0

    paths = [str(file).replace("\\", "/") for file in files]

    assert any(
        path.endswith("connectors/databases/postgresql/connector.py")
        for path in paths
    )


def test_scanner_returns_path_objects():

    scanner = ConnectorScanner("connectors")

    files = scanner.scan()

    assert all(isinstance(file, Path) for file in files)


def test_scanner_returns_non_empty_list():

    scanner = ConnectorScanner("connectors")

    files = scanner.scan()

    assert isinstance(files, list)

    assert len(files) >= 1
