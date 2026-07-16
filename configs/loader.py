"""
DataForge Configuration Loader
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from configs.constants import ENV_FILE
from configs.exceptions import (EnvironmentFileLoadError,
                                EnvironmentFileNotFoundError,
                                EnvironmentVariableError)


class ConfigLoader:
    """
    Loads and accesses DataForge configuration.

    Examples
    --------
    >>> loader = ConfigLoader()
    >>> loader.load()
    >>> loader.get("POSTGRES_HOST")
    """

    def __init__(
        self,
        env_file: str | Path | None = None,
    ) -> None:

        self._env_file = Path(env_file) if env_file else ENV_FILE

        self._loaded = False

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def env_file(self) -> Path:

        return self._env_file

    @property
    def loaded(self) -> bool:

        return self._loaded

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Load the .env file.
        """

        if not self._env_file.exists():

            raise EnvironmentFileNotFoundError(
                f"Environment file not found: {self._env_file}"
            )

        success = load_dotenv(
            dotenv_path=self._env_file,
            override=False,
        )

        if not success:

            raise EnvironmentFileLoadError(
                f"Failed to load environment file: {self._env_file}"
            )

        self._loaded = True

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        """
        Returns an environment variable.
        """

        return os.getenv(
            key,
            default,
        )

    # ---------------------------------------------------------

    def require(
        self,
        key: str,
    ) -> str:
        """
        Returns a required environment variable.
        """

        value = os.getenv(key)

        if value is None or value.strip() == "":

            raise EnvironmentVariableError(
                f"Required environment variable '{key}' is missing."
            )

        return value

    # ---------------------------------------------------------

    def has(
        self,
        key: str,
    ) -> bool:
        """
        Returns True if the variable exists.
        """

        value = os.getenv(key)

        return value is not None

    # ---------------------------------------------------------

    def reload(self) -> None:
        """
        Reload the environment file.
        """

        load_dotenv(
            dotenv_path=self._env_file,
            override=True,
        )

        self._loaded = True

    # ---------------------------------------------------------

    def as_dict(self) -> dict[str, str]:
        """
        Returns all environment variables.
        """

        return dict(os.environ)

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"env_file='{self._env_file}', "
            f"loaded={self._loaded})"
        )


# ==========================================================
# Global Loader
# ==========================================================

loader = ConfigLoader()

