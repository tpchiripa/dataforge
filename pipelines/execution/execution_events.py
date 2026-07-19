"""
DataForge Execution Events
"""

from __future__ import annotations


class ExecutionEvents:

    def pipeline_started(self, name: str):

        pass

    def pipeline_completed(self, name: str):

        pass

    def pipeline_failed(self, name: str):

        pass

    def step_started(self, step: str):

        pass

    def step_completed(self, step: str):

        pass

    def step_failed(self, step: str):

        pass
