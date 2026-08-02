"""
DataForge Module Discovery

Automatically discovers and registers DataForge modules.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

from pipelines.modules.module import Module
from pipelines.modules.module_registry import ModuleRegistry


class ModuleDiscovery:
    """
    Automatically discovers every DataForge module.

    Every concrete subclass of Module located inside
    the configured package is instantiated and
    registered with the ModuleRegistry.
    """

    #
    # Desired initialization order.
    #

    MODULE_PRIORITY = {

        "Runtime": 0,
        "Events": 1,
        "Plugins": 2,
        "Monitoring": 3,
        "Pipeline": 4,

    }

    def __init__(
        self,
        package: str = "pipelines.modules",
    ) -> None:

        self.package = package

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        registry: ModuleRegistry,
    ) -> None:
        """
        Discover and register every module.
        """

        package = importlib.import_module(
            self.package,
        )

        discovered: list[Module] = []

        #
        # Scan package.
        #

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__,
        ):

            #
            # Ignore private modules.
            #

            if module_name.startswith("_"):

                continue

            module = importlib.import_module(
                f"{self.package}.{module_name}",
            )

            for _, cls in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                #
                # Ignore imported classes.
                #

                if cls.__module__ != module.__name__:

                    continue

                #
                # Ignore abstract base class.
                #

                if cls is Module:

                    continue

                #
                # Ignore abstract subclasses.
                #

                if inspect.isabstract(
                    cls,
                ):

                    continue

                if issubclass(
                    cls,
                    Module,
                ):

                    discovered.append(
                        cls(),
                    )

        #
        # Sort by startup priority.
        #

        discovered.sort(

            key=lambda module: (
                self.MODULE_PRIORITY.get(
                    module.name,
                    999,
                ),
                module.name,
            )

        )

        #
        # Register modules.
        #

        for module in discovered:

            if not registry.contains(
                module.name,
            ):

                registry.register(
                    module,
                )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"package='{self.package}')"
        )
