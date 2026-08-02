"""
DataForge Pipeline Hooks

Registry responsible for managing lifecycle hooks.
"""

from __future__ import annotations

from .pipeline_hook import PipelineHook


class PipelineHooks:
    """
    Registry of pipeline lifecycle hooks.

    Hooks are executed in the order they are registered.
    """

    _hooks: list[PipelineHook] = []

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        hook: PipelineHook,
    ) -> None:
        """
        Register a lifecycle hook.
        """

        if hook not in cls._hooks:

            cls._hooks.append(hook)

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        hook: PipelineHook,
    ) -> None:
        """
        Remove a lifecycle hook.
        """

        if hook in cls._hooks:

            cls._hooks.remove(hook)

    # ---------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Remove all registered hooks.
        """

        cls._hooks.clear()

    # ---------------------------------------------------------

    @classmethod
    def list(
        cls,
    ) -> list[PipelineHook]:
        """
        Return all registered hooks.
        """

        return list(cls._hooks)

    # ---------------------------------------------------------

    @classmethod
    def exists(
        cls,
        hook_name: str,
    ) -> bool:
        """
        Check whether a hook is registered.
        """

        return any(
            hook.name.lower() == hook_name.lower()
            for hook in cls._hooks
        )

    # ---------------------------------------------------------
    # Pipeline Events
    # ---------------------------------------------------------

    @classmethod
    def before_pipeline(
        cls,
        context,
    ) -> None:

        for hook in cls._hooks:

            hook.before_pipeline(context)

    # ---------------------------------------------------------

    @classmethod
    def after_pipeline(
        cls,
        context,
    ) -> None:

        for hook in cls._hooks:

            hook.after_pipeline(context)

    # ---------------------------------------------------------

    @classmethod
    def on_pipeline_error(
        cls,
        context,
        exception: Exception,
    ) -> None:

        for hook in cls._hooks:

            hook.on_pipeline_error(
                context,
                exception,
            )

    # ---------------------------------------------------------
    # Step Events
    # ---------------------------------------------------------

    @classmethod
    def before_step(
        cls,
        step,
        context,
    ) -> None:

        for hook in cls._hooks:

            hook.before_step(
                step,
                context,
            )

    # ---------------------------------------------------------

    @classmethod
    def after_step(
        cls,
        step,
        context,
    ) -> None:

        for hook in cls._hooks:

            hook.after_step(
                step,
                context,
            )

    # ---------------------------------------------------------

    @classmethod
    def on_step_error(
        cls,
        step,
        context,
        exception: Exception,
    ) -> None:

        for hook in cls._hooks:

            hook.on_step_error(
                step,
                context,
                exception,
            )

    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:
        """
        Number of registered hooks.
        """

        return len(self._hooks)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._hooks)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(self._hooks)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineHooks("
            f"count={len(self._hooks)})"
        )
