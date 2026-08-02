"""
DataForge Module Registry

Responsible for registering and managing DataForge modules.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer
from pipelines.modules.module import Module


class ModuleRegistry:
    """
    Registry responsible for managing DataForge modules.

    Lifecycle

        Register Modules
                ↓
        Register Services
                ↓
           Initialize
                ↓
             Runtime
                ↓
            Shutdown
    """

    def __init__(
        self,
    ) -> None:

        self._modules: dict[str, Module] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        module: Module,
    ) -> None:
        """
        Register a module.
        """

        key = module.id

        if key in self._modules:

            raise ValueError(
                f"Module '{module.name}' is already registered."
            )

        self._modules[key] = module

    # ---------------------------------------------------------

    def unregister(
        self,
        module_name: str,
    ) -> None:
        """
        Remove a module.
        """

        self._modules.pop(
            module_name.lower(),
            None,
        )

    # ---------------------------------------------------------

    def get(
        self,
        module_name: str,
    ) -> Module:
        """
        Retrieve a module.
        """

        key = module_name.lower()

        if key not in self._modules:

            raise KeyError(
                f"Module '{module_name}' is not registered."
            )

        return self._modules[key]

    # ---------------------------------------------------------

    def contains(
        self,
        module_name: str,
    ) -> bool:

        return (
            module_name.lower()
            in self._modules
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Register services for every module and then
        initialize them.
        """

        #
        # Phase 1
        # Register every service first.
        #

        for module in self._modules.values():

            module.register_services(
                container,
            )

        #
        # Phase 2
        # Initialize after every service exists.
        #

        for module in self._modules.values():

            module.initialize(
                container,
            )

    # ---------------------------------------------------------

    def shutdown(
        self,
        container: ServiceContainer,
    ) -> None:
        """
        Shutdown every module in reverse order.
        """

        for module in reversed(
            list(self._modules.values())
        ):

            module.shutdown(
                container,
            )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._modules.clear()

    # ---------------------------------------------------------

    def list(
        self,
    ) -> list[Module]:

        return list(
            self._modules.values(),
        )

    # ---------------------------------------------------------

    def list_names(
        self,
    ) -> list[str]:

        return sorted(
            module.name
            for module in self._modules.values()
        )

    # ---------------------------------------------------------

    @property
    def module_count(
        self,
    ) -> int:

        return len(
            self._modules,
        )

    # ---------------------------------------------------------

    @property
    def is_empty(
        self,
    ) -> bool:

        return self.module_count == 0

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.module_count

    # ---------------------------------------------------------

    def __contains__(
        self,
        module_name: str,
    ) -> bool:

        return self.contains(
            module_name,
        )

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._modules.values(),
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"ModuleRegistry("
            f"modules={self.module_count})"
        )
