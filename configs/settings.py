"""
DataForge Global Settings
"""

from __future__ import annotations

from dataclasses import dataclass

from configs.airflow import airflow
from configs.database import database
from configs.environment import environment
from configs.logging import logging_settings
from configs.storage import storage


@dataclass(slots=True, frozen=True)
class Settings:
    """
    Unified application configuration.

    Acts as the single entry point for all
    DataForge configuration.
    """

    environment = environment

    database = database

    storage = storage

    airflow = airflow

    logging = logging_settings

    @property
    def is_development(self) -> bool:

        return (
            self.environment.environment.lower()
            == "development"
        )

    @property
    def is_production(self) -> bool:

        return (
            self.environment.environment.lower()
            == "production"
        )

    @property
    def is_testing(self) -> bool:

        return (
            self.environment.environment.lower()
            == "testing"
        )

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"environment='{self.environment.environment}')"
        )


settings = Settings()
