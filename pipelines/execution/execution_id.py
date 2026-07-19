"""
DataForge Execution ID Generator
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4


class ExecutionID:

    @staticmethod
    def generate() -> str:
        """
        Generate a unique pipeline execution ID.
        """

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        identifier = uuid4().hex[:8]

        return f"run_{timestamp}_{identifier}"
