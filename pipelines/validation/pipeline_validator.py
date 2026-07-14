"""
DataForge Pipeline Validator

Responsible for validating pipelines before execution.
"""

from __future__ import annotations

from pipelines.core.exceptions import PipelineValidationError
from pipelines.core.pipeline import Pipeline
from pipelines.steps.base.base_step import BaseStep


class PipelineValidator:
    """
    Validates DataForge pipelines before execution.

    The validator ensures that a pipeline is structurally valid
    before it is executed by the PipelineExecutor.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def validate(
        self,
        pipeline: Pipeline,
    ) -> bool:
        """
        Validate a pipeline.

        Parameters
        ----------
        pipeline
            Pipeline to validate.

        Raises
        ------
        PipelineValidationError
            If the pipeline is invalid.
        """

        if pipeline is None:
            raise PipelineValidationError(
                "Pipeline cannot be None."
            )

        self._validate_configuration(
            pipeline,
        )

        self._validate_steps(
            pipeline,
        )

        return True

    # ---------------------------------------------------------
    # Configuration Validation
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
    # Step Validation
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

        names: set[str] = set()

        for step in pipeline.steps:

            if not isinstance(
                step,
                BaseStep,
            ):
                raise PipelineValidationError(
                    "Pipeline contains an invalid step."
                )

            if not step.enabled:
                raise PipelineValidationError(
                    f"Pipeline step '{step.name}' is disabled."
                )

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
    # Convenience API
    # ---------------------------------------------------------

    def is_valid(
        self,
        pipeline: Pipeline,
    ) -> bool:
        """
        Return True if the pipeline is valid.
        """

        try:

            self.validate(
                pipeline,
            )

            return True

        except PipelineValidationError:

            return False

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        String representation.
        """

        return "PipelineValidator()"
