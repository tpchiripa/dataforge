"""
DataForge Environment Configuration
"""

from __future__ import annotations

from dataclasses import dataclass

from configs.loader import loader


@dataclass(slots=True, frozen=True)
class EnvironmentSettings:
    """
    Environment configuration.
    """

    project_name: str

    environment: str

    timezone: str

    compose_project_name: str

    pythonpath: str

    # -----------------------------------------------------

    @property
    def is_development(self) -> bool:

        return self.environment == "development"

    # -----------------------------------------------------

    @property
    def is_testing(self) -> bool:

        return self.environment == "testing"

    # -----------------------------------------------------

    @property
    def is_staging(self) -> bool:

        return self.environment == "staging"

    # -----------------------------------------------------

    @property
    def is_production(self) -> bool:

        return self.environment == "production"

    # -----------------------------------------------------

    @classmethod
    def from_env(cls) -> "EnvironmentSettings":

        return cls(
            project_name=loader.require(
                "PROJECT_NAME",
            ),
            environment=loader.require(
                "ENVIRONMENT",
            ),
            timezone=loader.require(
                "TIMEZONE",
            ),
            compose_project_name=loader.require(
                "COMPOSE_PROJECT_NAME",
            ),
            pythonpath=loader.require(
                "PYTHONPATH",
            ),
        )

    # -----------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"environment='{self.environment}', "
            f"project='{self.project_name}')"
        )


environment = EnvironmentSettings.from_env()
