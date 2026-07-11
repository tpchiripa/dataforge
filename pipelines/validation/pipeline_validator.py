"""
DataForge Pipeline Validator

Responsible for validating pipelines before execution.
"""

from __future__ import annotations

from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline import Pipeline


class PipelineValidator:
    """
    Validates DataForge pipelines.
    """

    def validate(
        self,
        pipeline: Pipeline,
    ) -> bool:
        """
        Validate a pipeline.

        Raises
        ------
        PipelineValidationError
            If the pipeline is invalid.
        """

        self._validate_configuration(pipeline)

        self._validate_steps(pipeline)

        return True

    # ---------------------------------------------------------

    def _validate_configuration(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Validate pipeline configuration.
        """

        config = pipeline.config

        if not config.enabled:
            raise PipelineValidationError(
                "Pipeline is disabled."
            )

        if not config.name.strip():
            raise PipelineValidationError(
                "Pipeline name cannot be empty."
            )

    # ---------------------------------------------------------

    def _validate_steps(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Validate pipeline steps.
        """

        if len(pipeline.steps) == 0:
            raise PipelineValidationError(
                "Pipeline contains no steps."
            )

        names = set()

        for step in pipeline.steps:

            if not step.name.strip():

                raise PipelineValidationError(
                    "Pipeline step name cannot be empty."
                )

            key = step.name.lower()

            if key in names:

                raise PipelineValidationError(
                    f"Duplicate pipeline step '{step.name}'."
                )

            names.add(key)

    # ---------------------------------------------------------

    def is_valid(
        self,
        pipeline: Pipeline,
    ) -> bool:
        """
        Return True if the pipeline is valid.
        """

        try:

            self.validate(pipeline)

            return True

        except PipelineValidationError:

            return False
