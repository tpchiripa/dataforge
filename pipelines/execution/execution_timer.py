"""
DataForge Execution Timer
"""

from __future__ import annotations

from datetime import datetime


class ExecutionTimer:

    def __init__(self):

        self._started = None

        self._finished = None

    def start(self):

        self._started = datetime.utcnow()

    def stop(self):

        self._finished = datetime.utcnow()

    @property
    def duration(self):

        if self._started is None or self._finished is None:

            return 0.0

        return (self._finished - self._started).total_seconds()
