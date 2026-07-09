"""
DataForge Connector Framework

Core SDK for building DataForge connectors.
"""

from .connector import BaseConnector

from .factory import ConnectorFactory
from .registry import ConnectorRegistry

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
    "ConnectorFactory",
    "ConnectorRegistry",

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
