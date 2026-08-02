"""
DataForge Event Manager

Provides global access to the DataForge EventBus.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .event_bus import EventBus
from .event_type import EventType


EventHandler = Callable[[dict[str, Any]], None]


class EventManager:
    """
    Singleton-style manager around the DataForge EventBus.

    This provides a single shared event bus for the
    entire DataForge runtime.
    """

    _bus = EventBus()

    # ---------------------------------------------------------
    # Subscription
    # ---------------------------------------------------------

    @classmethod
    def subscribe(
        cls,
        event: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Subscribe to an event.
        """

        cls._bus.subscribe(
            event,
            handler,
        )

    # ---------------------------------------------------------

    @classmethod
    def unsubscribe(
        cls,
        event: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Remove an event subscription.
        """

        cls._bus.unsubscribe(
            event,
            handler,
        )

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    @classmethod
    def publish(
        cls,
        event: EventType,
        **payload: Any,
    ) -> None:
        """
        Publish an event.
        """

        cls._bus.publish(
            event,
            **payload,
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    @classmethod
    def subscriber_count(
        cls,
        event: EventType,
    ) -> int:
        """
        Return the number of subscribers for an event.
        """

        return cls._bus.subscriber_count(
            event,
        )

    # ---------------------------------------------------------

    @classmethod
    def clear(cls) -> None:
        """
        Remove all event subscriptions.

        Primarily useful for testing.
        """

        cls._bus.clear()

    # ---------------------------------------------------------

    @classmethod
    def bus(cls) -> EventBus:
        """
        Return the underlying EventBus.
        """

        return cls._bus

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"EventManager({self._bus})"
