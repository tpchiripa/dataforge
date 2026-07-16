"""
DataForge Storage Configuration
"""

from __future__ import annotations

from dataclasses import dataclass

from configs.loader import loader


@dataclass(slots=True, frozen=True)
class StorageSettings:
    """
    Storage subsystem configuration.
    """

    # ---------------------------------------------------------
    # MinIO
    # ---------------------------------------------------------

    endpoint: str

    access_key: str

    secret_key: str

    secure: bool

    api_port: int

    console_port: int

    default_bucket: str = "bronze"

    # ---------------------------------------------------------

    @property
    def url(self) -> str:
        """
        Returns the MinIO endpoint URL.
        """

        protocol = "https" if self.secure else "http"

        return f"{protocol}://{self.endpoint}"

    # ---------------------------------------------------------

    @classmethod
    def from_env(cls) -> "StorageSettings":

        endpoint = loader.get("MINIO_ENDPOINT")

        if endpoint is None:

            host = loader.get(
                "MINIO_HOST",
                default="localhost",
            )

            port = loader.get(
                "MINIO_API_PORT",
                default="9000",
            )

            endpoint = f"{host}:{port}"

        secure = (
            loader.get(
                "MINIO_SECURE",
                default="false",
            ).lower()
            == "true"
        )

        return cls(
            endpoint=endpoint,
            access_key=loader.require(
                "MINIO_ROOT_USER",
            ),
            secret_key=loader.require(
                "MINIO_ROOT_PASSWORD",
            ),
            secure=secure,
            api_port=int(
                loader.require(
                    "MINIO_API_PORT",
                )
            ),
            console_port=int(
                loader.require(
                    "MINIO_CONSOLE_PORT",
                )
            ),
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"endpoint='{self.endpoint}', "
            f"secure={self.secure})"
        )


storage = StorageSettings.from_env()
