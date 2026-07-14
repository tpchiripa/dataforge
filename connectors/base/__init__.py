"""
DataForge Connector Framework

Core framework for building DataForge connectors.
"""

from .base_connector import BaseConnector

from .registry import ConnectorRegistry
from .factory import ConnectorFactory
from .manager import ConnectorManager

from .types import (
    AuthenticationType,
    ConnectionResult,
    ConnectionStatus,
    ConnectorConfig,
    ConnectorMetadata,
    ConnectorType,
    DatasetInfo,
    ExtractionResult,
    PipelineMode,
)

from .exceptions import (
    ConnectorError,
    ConfigurationError,
    ConnectionFailedError,
    AuthenticationError,
    ConnectionTimeoutError,
    ConnectorNotConnectedError,
    QueryExecutionError,
    DataExtractionError,
    DataLoadError,
    DataValidationError,
    SchemaMismatchError,
    IncrementalLoadError,
    ConnectorRegistrationError,
    ConnectorNotFoundError,
    FileFormatError,
    APIRequestError,
    RateLimitExceededError,
)

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
