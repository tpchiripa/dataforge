"""
DataForge Service Container

Enterprise dependency injection container supporting

- Singleton services
- Transient services
- Existing instances
- Constructor injection
- Optional dependencies
"""

from __future__ import annotations

import inspect
import types
from typing import Any
from typing import get_args
from typing import get_origin

from pipelines.container.service_descriptor import ServiceDescriptor
from pipelines.container.service_lifetime import ServiceLifetime


class ServiceContainer:
    """
    Enterprise dependency injection container.
    """

    def __init__(self) -> None:

        self._services: dict[type, ServiceDescriptor] = {}

    # =========================================================
    # Registration
    # =========================================================

    def register_singleton(
        self,
        service_type: type,
        implementation: type | None = None,
    ) -> None:

        self._services[service_type] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation or service_type,
            lifetime=ServiceLifetime.SINGLETON,
        )

    # ---------------------------------------------------------

    def register_transient(
        self,
        service_type: type,
        implementation: type | None = None,
    ) -> None:

        self._services[service_type] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation or service_type,
            lifetime=ServiceLifetime.TRANSIENT,
        )

    # ---------------------------------------------------------

    def register_instance(
        self,
        service_type: type,
        instance: object,
    ) -> None:

        descriptor = ServiceDescriptor(
            service_type=service_type,
            implementation=service_type,
            lifetime=ServiceLifetime.SINGLETON,
        )

        descriptor.instance = instance

        self._services[service_type] = descriptor

    # =========================================================
    # Resolution
    # =========================================================

    def resolve(
        self,
        service_type: type,
    ) -> Any:

        descriptor = self._services.get(service_type)

        if descriptor is None:

            raise KeyError(
                f"Service '{service_type.__name__}' is not registered."
            )

        if descriptor.lifetime is ServiceLifetime.SINGLETON:

            if descriptor.instance is None:

                descriptor.instance = self._create_instance(
                    descriptor.implementation,
                )

            return descriptor.instance

        return self._create_instance(
            descriptor.implementation,
        )

    # =========================================================
    # Object Creation
    # =========================================================

    def _create_instance(
        self,
        implementation: type,
    ) -> Any:

        constructor = implementation.__init__

        signature = inspect.signature(
            constructor,
        )

        annotations = inspect.get_annotations(
            constructor,
            eval_str=True,
        )

        kwargs: dict[str, Any] = {}

        for parameter in list(signature.parameters.values())[1:]:

            annotation = annotations.get(
                parameter.name,
            )

            if annotation is None:

                continue

            #
            # Handle Optional[T]
            # Handle T | None
            #

            origin = get_origin(annotation)

            if origin in (types.UnionType,):

                args = [
                    arg
                    for arg in get_args(annotation)
                    if arg is not type(None)
                ]

                if args:

                    annotation = args[0]

            elif origin is not None:

                args = [
                    arg
                    for arg in get_args(annotation)
                    if arg is not type(None)
                ]

                if len(args) == 1:

                    annotation = args[0]

            if self.contains(annotation):

                kwargs[parameter.name] = self.resolve(
                    annotation,
                )

        return implementation(
            **kwargs,
        )

    # =========================================================
    # Utilities
    # =========================================================

    def contains(
        self,
        service_type: type,
    ) -> bool:

        return service_type in self._services

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._services.clear()

    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:

        return len(
            self._services,
        )

    # ---------------------------------------------------------

    @property
    def registered_services(
        self,
    ) -> list[type]:

        return list(
            self._services.keys(),
        )

    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.count

    # ---------------------------------------------------------

    def __contains__(
        self,
        service_type: type,
    ) -> bool:

        return self.contains(
            service_type,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"ServiceContainer("
            f"services={self.count})"
        )
