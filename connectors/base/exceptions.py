"""
DataForge Connector Exceptions

Defines the exception hierarchy used throughout the
DataForge Connector Framework (DCF).
"""

from __future__ import annotations

from typing import Any


class ConnectorError(Exception):
    """
    Base exception for all DataForge connector errors.
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


# ==========================================================
# Configuration Errors
# ==========================================================

class ConfigurationError(ConnectorError):
    """
    Raised when connector configuration is invalid.
    """
    pass


# ==========================================================
# Connection Errors
# ==========================================================

class ConnectionFailedError(ConnectorError):
    """
    Raised when a connection cannot be established.
    """
    pass


class AuthenticationError(ConnectionFailedError):
    """
    Raised when authentication fails.
    """
    pass


class ConnectionTimeoutError(ConnectionFailedError):
    """
    Raised when a connection attempt times out.
    """
    pass


class ConnectorNotConnectedError(ConnectionFailedError):
    """
    Raised when an operation requires an active connection.
    """
    pass


# ==========================================================
# Query Errors
# ==========================================================

class QueryExecutionError(ConnectorError):
    """
    Raised when query execution fails.
    """
    pass


# ==========================================================
# Data Errors
# ==========================================================

class DataExtractionError(ConnectorError):
    """
    Raised when data extraction fails.
    """
    pass


class DataLoadError(ConnectorError):
    """
    Raised when loading data fails.
    """
    pass


class DataValidationError(ConnectorError):
    """
    Raised when extracted data fails validation.
    """
    pass


class SchemaMismatchError(DataValidationError):
    """
    Raised when the source schema differs from the expected schema.
    """
    pass


class IncrementalLoadError(DataExtractionError):
    """
    Raised when an incremental extraction fails.
    """
    pass


# ==========================================================
# Connector Registry Errors
# ==========================================================

class ConnectorRegistrationError(ConnectorError):
    """
    Raised when connector registration fails.
    """
    pass


class ConnectorNotFoundError(ConnectorError):
    """
    Raised when a requested connector is not registered.
    """
    pass


# ==========================================================
# File Connector Errors
# ==========================================================

class FileFormatError(ConnectorError):
    """
    Raised when an unsupported or invalid file format is encountered.
    """
    pass


# ==========================================================
# API Errors
# ==========================================================

class APIRequestError(ConnectorError):
    """
    Raised when an API request fails.
    """
    pass


class RateLimitExceededError(APIRequestError):
    """
    Raised when an API rate limit has been exceeded.
    """
    pass

