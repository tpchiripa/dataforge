"""
DataForge Pipeline Event

Represents an event emitted during pipeline execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .event_type import EventType


@dataclass(slots=True)
class PipelineEvent:
    """
    Represents a runtime pipeline event.
    """

    event_type: EventType

    pipeline_name: str

    timestamp: datetime = field(default_factory=datetime.utcnow)

    step_name: str = ""

    execution_id: str = ""

    message: str = ""

    payload: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------

    def add_payload(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add payload data.
        """

        self.payload[key] = value

    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve payload data.
        """

        return self.payload.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    @property
    def has_payload(
        self,
    ) -> bool:
        """
        Returns True if payload exists.
        """

        return bool(
            self.payload,
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"PipelineEvent("
            f"type={self.event_type.value}, "
            f"pipeline='{self.pipeline_name}', "
            f"step='{self.step_name}')"
        )
