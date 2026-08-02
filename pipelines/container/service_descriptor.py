"""
DataForge Service Descriptor
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from pipelines.container.service_lifetime import ServiceLifetime


@dataclass(slots=True)
class ServiceDescriptor:
    """
    Describes a registered service.
    """

    service_type: type

    implementation: Callable[..., Any] | type

    lifetime: ServiceLifetime

    instance: Any = None
