"""
DataForge Lifecycle Manager

Coordinates lifecycle hooks and publishes
platform events.
"""

from __future__ import annotations

from pipelines.events.event_manager import EventManager
from pipelines.events.event_type import EventType
from pipelines.lifecycle.pipeline_hook import PipelineHook
from pipelines.core.pipeline_context import PipelineContext
from pipelines.core.pipeline_step import PipelineStep


class LifecycleManager:
    """
    Coordinates pipeline lifecycle hooks.
    """

    def __init__(self) -> None:

        self._hooks: list[PipelineHook] = []

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register_hook(
        self,
        hook: PipelineHook,
    ) -> None:

        self._hooks.append(hook)

    # ---------------------------------------------------------

    def unregister_hook(
        self,
        hook: PipelineHook,
    ) -> None:

        if hook in self._hooks:

            self._hooks.remove(hook)

    # ---------------------------------------------------------
    # Pipeline Lifecycle
    # ---------------------------------------------------------

    def before_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        EventManager.publish(
            EventType.PIPELINE_STARTED,
            pipeline=context.config.name,
        )

        for hook in self._hooks:

            hook.before_pipeline(
                context,
            )

    # ---------------------------------------------------------

    def after_pipeline(
        self,
        context: PipelineContext,
    ) -> None:

        EventManager.publish(
            EventType.PIPELINE_COMPLETED,
            pipeline=context.config.name,
        )

        for hook in self._hooks:

            hook.after_pipeline(
                context,
            )

    # ---------------------------------------------------------

    def on_pipeline_error(
        self,
        context: PipelineContext,
        exception: Exception,
    ) -> None:

        EventManager.publish(
            EventType.PIPELINE_FAILED,
            pipeline=context.config.name,
            exception=str(exception),
        )

        for hook in self._hooks:

            hook.on_pipeline_error(
                context,
                exception,
            )

    # ---------------------------------------------------------
    # Step Lifecycle
    # ---------------------------------------------------------

    def before_step(
        self,
        step: PipelineStep,
        context: PipelineContext,
    ) -> None:

        EventManager.publish(
            EventType.STEP_STARTED,
            pipeline=context.config.name,
            step=step.name,
        )

        for hook in self._hooks:

            hook.before_step(
                step,
                context,
            )

    # ---------------------------------------------------------

    def after_step(
        self,
        step: PipelineStep,
        context: PipelineContext,
    ) -> None:

        EventManager.publish(
            EventType.STEP_COMPLETED,
            pipeline=context.config.name,
            step=step.name,
        )

        for hook in self._hooks:

            hook.after_step(
                step,
                context,
            )

    # ---------------------------------------------------------

    def on_step_error(
        self,
        step: PipelineStep,
        context: PipelineContext,
        exception: Exception,
    ) -> None:

        EventManager.publish(
            EventType.STEP_FAILED,
            pipeline=context.config.name,
            step=step.name,
            exception=str(exception),
        )

        for hook in self._hooks:

            hook.on_step_error(
                step,
                context,
                exception,
            )

    # ---------------------------------------------------------

    @property
    def hook_count(
        self,
    ) -> int:

        return len(self._hooks)

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._hooks.clear()

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"LifecycleManager("
            f"hooks={self.hook_count})"
        )
