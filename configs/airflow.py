"""
DataForge Airflow Configuration
"""

from __future__ import annotations

from dataclasses import dataclass

from configs.loader import loader


@dataclass(slots=True, frozen=True)
class AirflowSettings:
    """
    Apache Airflow configuration.
    """

    home: str

    uid: int

    admin_username: str

    admin_password: str

    executor: str

    webserver_base_url: str

    @classmethod
    def from_env(cls) -> "AirflowSettings":

        return cls(
            home=loader.require("AIRFLOW_HOME"),
            uid=int(loader.require("AIRFLOW_UID")),
            admin_username=loader.require("AIRFLOW_ADMIN_USERNAME"),
            admin_password=loader.require("AIRFLOW_ADMIN_PASSWORD"),
            executor=loader.get("AIRFLOW__CORE__EXECUTOR", default="LocalExecutor"),
            webserver_base_url=loader.get(
                "AIRFLOW__WEBSERVER__BASE_URL",
                default="http://localhost:8080",
            ),
        )

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"home='{self.home}', "
            f"executor='{self.executor}')"
        )


airflow = AirflowSettings.from_env()