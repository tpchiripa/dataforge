"""
DataForge Service Provider
"""

from __future__ import annotations

from typing import Any

from pipelines.container.service_container import ServiceContainer


class ServiceProvider:
    """
    Provides access to registered services.
    """

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self._container = container

    # ---------------------------------------------------------

    def get(
        self,
        service_type: type,
    ) -> Any:
        """
        Resolve a service.
        """

        return self._container.resolve(
            service_type,
        )

    # ---------------------------------------------------------

    @property
    def container(
        self,
    ) -> ServiceContainer:

        return self._container

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"ServiceProvider("
            f"services={self._container.count})"
        )
