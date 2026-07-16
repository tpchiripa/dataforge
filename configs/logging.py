"""
DataForge Logging Configuration
"""

from __future__ import annotations

import logging
from pathlib import Path

from configs.loader import loader


class LoggingSettings:
    """
    Logging configuration.
    """

    def __init__(self) -> None:

        self.level = loader.get(
            "LOG_LEVEL",
            default="INFO",
        ).upper()

        self.log_directory = Path(
            loader.get(
                "LOG_DIRECTORY",
                default="logs",
            )
        )

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_file = self.log_directory / "dataforge.log"

    # ---------------------------------------------------------

    def configure(self) -> None:
        """
        Configure the root logger.
        """

        logging.basicConfig(
            level=getattr(logging, self.level),
            format=(
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s | "
                "%(message)s"
            ),
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(),
            ],
        )

    # ---------------------------------------------------------

    def get_logger(
        self,
        name: str,
    ) -> logging.Logger:

        return logging.getLogger(name)

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"level='{self.level}', "
            f"log_file='{self.log_file}')"
        )


logging_settings = LoggingSettings()
