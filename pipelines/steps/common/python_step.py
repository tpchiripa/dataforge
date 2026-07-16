"""
DataForge Python Step

Execute arbitrary Python functions within a pipeline.
"""

from __future__ import annotations

from typing import Any, Callable

from pipelines.core.pipeline_context import PipelineContext
from pipelines.steps.base.base_step import BaseStep


class PythonStep(BaseStep):
    """
    Execute a custom Python function.

    The supplied function receives the PipelineContext and may
    modify it as required.
    """

    def __init__(
        self,
        name: str,
        function: Callable[[PipelineContext], Any],
        description: str = "",
    ):

        super().__init__(
            name=name,
            description=description or "Execute custom Python logic.",
        )

        self.function = function

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute the supplied Python function.
        """

        result = self.function(context)

        context.add_metadata(
            "python_step",
            self.name,
        )

        context.add_metadata(
            "python_function",
            self.function.__name__,
        )

        if result is not None:

            context.add_metadata(
                "python_result",
                str(result),
            )
