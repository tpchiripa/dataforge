"""
DataForge Plugin Discovery

Automatically discovers and loads DataForge plugins.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

from pipelines.plugins.plugin import Plugin
from pipelines.plugins.plugin_manager import PluginManager


class PluginDiscovery:
    """
    Discovers every Plugin subclass inside the
    DataForge plugins package.
    """

    def __init__(
        self,
        package: str = "pipelines.plugins",
    ) -> None:

        self.package = package

    # ---------------------------------------------------------

    def discover(
        self,
        manager: PluginManager,
    ) -> None:
        """
        Discover and load plugins.
        """

        package = importlib.import_module(
            self.package,
        )

        for _, module_name, is_pkg in pkgutil.iter_modules(
            package.__path__,
        ):

            #
            # Skip private modules.
            #

            if module_name.startswith("_"):

                continue

            #
            # Support plugin packages.
            #

            if is_pkg:

                try:

                    module = importlib.import_module(
                        f"{self.package}.{module_name}.{module_name}_plugin",
                    )

                except ModuleNotFoundError:

                    continue

            else:

                module = importlib.import_module(
                    f"{self.package}.{module_name}",
                )

            #
            # Find every Plugin subclass.
            #

            for _, cls in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    issubclass(
                        cls,
                        Plugin,
                    )
                    and cls is not Plugin
                ):

                    manager.load(
                        cls(),
                    )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PluginDiscovery("
            f"package='{self.package}')"
        )
