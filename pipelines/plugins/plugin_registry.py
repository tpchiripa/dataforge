"""
DataForge Plugin Registry

Stores every registered plugin.
"""

from __future__ import annotations

from pipelines.plugins.plugin import Plugin


class PluginRegistry:
    """
    Registry of DataForge plugins.
    """

    _plugins: dict[str, Plugin] = {}

    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        plugin: Plugin,
    ) -> None:

        cls._plugins[
            plugin.name.lower()
        ] = plugin

    # ---------------------------------------------------------

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:

        cls._plugins.pop(
            name.lower(),
            None,
        )

    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Plugin | None:

        return cls._plugins.get(
            name.lower(),
        )

    # ---------------------------------------------------------

    @classmethod
    def plugins(
        cls,
    ) -> list[Plugin]:

        return list(
            cls._plugins.values(),
        )

    # ---------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._plugins.clear()

    # ---------------------------------------------------------

    @classmethod
    def count(
        cls,
    ) -> int:

        return len(
            cls._plugins,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"PluginRegistry("
            f"plugins={len(self._plugins)})"
        )
