"""
DataForge Configuration Validation
"""

from __future__ import annotations

from configs.constants import (SUPPORTED_ENVIRONMENTS, SUPPORTED_LOG_LEVELS,
                               SUPPORTED_STORAGE_BACKENDS)
from configs.exceptions import ConfigurationValidationError
from configs.loader import ConfigLoader


class ConfigValidator:
    """
    Validates the DataForge configuration.

    Examples
    --------
    >>> loader.load()
    >>> validator = ConfigValidator(loader)
    >>> validator.validate()
    """

    def __init__(
        self,
        loader: ConfigLoader,
    ) -> None:

        self._loader = loader

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Runs all configuration validation.
        """

        self._validate_environment()

        self._validate_database()

        self._validate_storage()

        self._validate_airflow()

        self._validate_redis()

        self._validate_logging()

    # ---------------------------------------------------------
    # Environment
    # ---------------------------------------------------------

    def _validate_environment(self) -> None:

        environment = self._loader.require(
            "ENVIRONMENT",
        )

        if environment not in SUPPORTED_ENVIRONMENTS:

            raise ConfigurationValidationError(
                f"Unsupported environment '{environment}'. "
                f"Supported values are: "
                f"{', '.join(SUPPORTED_ENVIRONMENTS)}"
            )

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------

    def _validate_database(self) -> None:

        self._loader.require("POSTGRES_HOST")

        self._loader.require("POSTGRES_PORT")

        self._loader.require("POSTGRES_DB")

        self._loader.require("POSTGRES_USER")

        self._loader.require("POSTGRES_PASSWORD")

    # ---------------------------------------------------------
    # Storage
    # ---------------------------------------------------------

    def _validate_storage(self) -> None:

        backend = self._loader.get(
            "DATAFORGE_STORAGE_BACKEND",
            "filesystem",
        )

        if backend not in SUPPORTED_STORAGE_BACKENDS:

            raise ConfigurationValidationError(
                f"Unsupported storage backend '{backend}'. "
                f"Supported values are: "
                f"{', '.join(SUPPORTED_STORAGE_BACKENDS)}"
            )

    # ---------------------------------------------------------
    # Airflow
    # ---------------------------------------------------------

    def _validate_airflow(self) -> None:

        self._loader.require("AIRFLOW_HOME")

        self._loader.require("AIRFLOW_UID")

        self._loader.require("AIRFLOW_ADMIN_USERNAME")

        self._loader.require("AIRFLOW_ADMIN_PASSWORD")

    # ---------------------------------------------------------
    # Redis
    # ---------------------------------------------------------

    def _validate_redis(self) -> None:

        self._loader.require("REDIS_HOST")

        self._loader.require("REDIS_PORT")

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def _validate_logging(self) -> None:

        level = self._loader.get(
            "DATAFORGE_LOG_LEVEL",
            "INFO",
        )

        if level not in SUPPORTED_LOG_LEVELS:

            raise ConfigurationValidationError(
                f"Unsupported log level '{level}'. "
                f"Supported values are: "
                f"{', '.join(SUPPORTED_LOG_LEVELS)}"
            )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"loader={self._loader!r})"
        )


# ==========================================================
# Global Validator
# ==========================================================

validator = ConfigValidator(
    ConfigLoader(),
)
