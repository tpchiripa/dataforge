"""
DataForge Database Configuration
"""

from __future__ import annotations

from dataclasses import dataclass

from configs.loader import loader


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    """
    PostgreSQL configuration.
    """

    host: str

    port: int

    database: str

    username: str

    password: str

    sqlalchemy_uri: str

    # ---------------------------------------------------------

    @property
    def url(self) -> str:
        """
        Standard PostgreSQL connection string.
        """

        return (
            f"postgresql://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/"
            f"{self.database}"
        )

    # ---------------------------------------------------------

    @property
    def psycopg_uri(self) -> str:
        """
        psycopg2 connection URI.
        """

        return (
            f"postgresql+psycopg2://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/"
            f"{self.database}"
        )

    # ---------------------------------------------------------

    @classmethod
    def from_env(cls) -> "DatabaseSettings":

        sqlalchemy_uri = loader.get(
            "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN",
        )

        return cls(
            host=loader.require(
                "POSTGRES_HOST",
            ),
            port=int(
                loader.require(
                    "POSTGRES_PORT",
                )
            ),
            database=loader.require(
                "POSTGRES_DB",
            ),
            username=loader.require(
                "POSTGRES_USER",
            ),
            password=loader.require(
                "POSTGRES_PASSWORD",
            ),
            sqlalchemy_uri=(
                sqlalchemy_uri
                if sqlalchemy_uri
                else (
                    f"postgresql+psycopg2://"
                    f"{loader.require('POSTGRES_USER')}:"
                    f"{loader.require('POSTGRES_PASSWORD')}"
                    f"@{loader.require('POSTGRES_HOST')}:"
                    f"{loader.require('POSTGRES_PORT')}/"
                    f"{loader.require('POSTGRES_DB')}"
                )
            ),
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"host='{self.host}', "
            f"port={self.port}, "
            f"database='{self.database}')"
        )


database = DatabaseSettings.from_env()
