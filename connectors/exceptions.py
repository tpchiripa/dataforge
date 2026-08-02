"""
DataForge Connector Exceptions

Custom exceptions used by the DataForge Connector Framework.
"""

from __future__ import annotations


class ConnectorError(Exception):
    """
    Base exception for all connector-related errors.
    """

    pass


# ---------------------------------------------------------
# Registration
# ---------------------------------------------------------


class ConnectorAlreadyRegisteredError(ConnectorError):
    """
    Raised when attempting to register a connector that
    already exists in the ConnectorRegistry.
    """

    pass


class ConnectorNotFoundError(ConnectorError):
    """
    Raised when a requested connector cannot be found.
    """

    pass


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


class InvalidConnectorConfigurationError(ConnectorError):
    """
    Raised when connector configuration is invalid.
    """

    pass


# ---------------------------------------------------------
# Connection
# ---------------------------------------------------------


class ConnectorConnectionError(ConnectorError):
    """
    Raised when a connector cannot establish a connection.
    """

    pass


class ConnectorAuthenticationError(ConnectorConnectionError):
    """
    Raised when connector authentication fails.
    """

    pass


class ConnectorTimeoutError(ConnectorConnectionError):
    """
    Raised when a connector operation times out.
    """

    pass


# ---------------------------------------------------------
# Operations
# ---------------------------------------------------------


class ConnectorReadError(ConnectorError):
    """
    Raised when reading data fails.
    """

    pass


class ConnectorWriteError(ConnectorError):
    """
    Raised when writing data fails.
    """

    pass


class ConnectorValidationError(ConnectorError):
    """
    Raised when connector validation fails.
    """

    pass
