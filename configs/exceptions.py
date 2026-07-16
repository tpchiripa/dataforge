"""
DataForge Configuration Exceptions
"""

from __future__ import annotations


class ConfigurationError(Exception):
    """
    Base exception for all configuration-related errors.
    """


class EnvironmentVariableError(ConfigurationError):
    """
    Raised when a required environment variable is missing.
    """


class InvalidConfigurationError(ConfigurationError):
    """
    Raised when a configuration value is invalid.
    """


class ConfigurationValidationError(ConfigurationError):
    """
    Raised when configuration validation fails.
    """


class EnvironmentFileNotFoundError(ConfigurationError):
    """
    Raised when the .env file cannot be located.
    """


class EnvironmentFileLoadError(ConfigurationError):
    """
    Raised when the .env file cannot be loaded.
    """
