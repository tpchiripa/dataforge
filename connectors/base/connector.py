"""
DataForge Base Connector

Abstract base class that defines the interface for all
DataForge connectors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from .types import (
    ConnectorConfig,
    ConnectorMetadata,
    ConnectionResult,
    DatasetInfo,
    ExtractionResult,
)


class BaseConnector(ABC):
    """
    Abstract base class for all DataForge connectors.

    Every connector implementation must inherit from this class
    and implement the required methods.
    """

    def __init__(self, config: ConnectorConfig):
        self.config = config
        self.connection = None
        self.connected = False

    # ==========================================================
    # Connection Management
    # ==========================================================

    @abstractmethod
    def connect(self) -> ConnectionResult:
        """
        Establish a connection to the data source.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the connection.
        """
        raise NotImplementedError

    @abstractmethod
    def test_connection(self) -> ConnectionResult:
        """
        Test connectivity without performing extraction.
        """
        raise NotImplementedError

    # ==========================================================
    # Metadata
    # ==========================================================

    @abstractmethod
    def get_metadata(self) -> ConnectorMetadata:
        """
        Return connector metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def list_datasets(self) -> list[DatasetInfo]:
        """
        List available datasets.
        """
        raise NotImplementedError

    # ==========================================================
    # Data Extraction
    # ==========================================================

    @abstractmethod
    def extract(self, *args, **kwargs) -> ExtractionResult:
        """
        Extract data from the source.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_dataframe(self, *args, **kwargs) -> pd.DataFrame:
        """
        Return extracted data as a pandas DataFrame.
        """
        raise NotImplementedError

    # ==========================================================
    # Validation
    # ==========================================================

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate connector configuration.
        """
        raise NotImplementedError

    # ==========================================================
    # Utility
    # ==========================================================

    @property
    def is_connected(self) -> bool:
        """
        Indicates whether the connector is connected.
        """
        return self.connected

    def __enter__(self):
        """
        Enable context manager support.

        Example:
            with PostgreSQLConnector(config) as connector:
                ...
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically disconnect when leaving the context.
        """
        self.disconnect()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.config.name}', "
            f"type='{self.config.connector_type.value}')"
        )
