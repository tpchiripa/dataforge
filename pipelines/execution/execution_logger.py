"""
DataForge Execution Logger
"""

from __future__ import annotations

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class ExecutionLogger:

    def __init__(self):

        self.logger = logging.getLogger("DataForge")

    def info(self, message: str):

        self.logger.info(message)

    def warning(self, message: str):

        self.logger.warning(message)

    def error(self, message: str):

        self.logger.error(message)
