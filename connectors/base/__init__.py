"""
DataForge Connector Framework

Core framework for building DataForge connectors.
"""

from .base_connector import BaseConnector
from .exceptions import (APIRequestError, AuthenticationError,
                         ConfigurationError, ConnectionFailedError,
                         ConnectionTimeoutError, ConnectorError,
                         ConnectorNotConnectedError, ConnectorNotFoundError,
                         ConnectorRegistrationError, DataExtractionError,
                         DataLoadError, DataValidationError, FileFormatError,
                         IncrementalLoadError, QueryExecutionError,
                         RateLimitExceededError, SchemaMismatchError)
from .factory import ConnectorFactory
from .manager import ConnectorManager
from .registry import ConnectorRegistry
from .types import (AuthenticationType, ConnectionResult, ConnectionStatus,
                    ConnectorConfig, ConnectorMetadata, ConnectorType,
                    DatasetInfo, ExtractionResult, PipelineMode)

__all__ = [
    "BaseConnector",
    "ConnectorRegistry",
    "ConnectorFactory",
    "ConnectorManager",
    "AuthenticationType",
    "ConnectionResult",
    "ConnectionStatus",
    "ConnectorConfig",
    "ConnectorMetadata",
    "ConnectorType",
    "DatasetInfo",
    "ExtractionResult",
    "PipelineMode",
    "ConnectorError",
    "ConfigurationError",
    "ConnectionFailedError",
    "AuthenticationError",
    "ConnectionTimeoutError",
    "ConnectorNotConnectedError",
    "QueryExecutionError",
    "DataExtractionError",
    "DataLoadError",
    "DataValidationError",
    "SchemaMismatchError",
    "IncrementalLoadError",
    "ConnectorRegistrationError",
    "ConnectorNotFoundError",
    "FileFormatError",
    "APIRequestError",
    "RateLimitExceededError",
]
