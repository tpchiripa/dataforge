"""
DataForge Event Bus

Simple publish/subscribe event system for the DataForge platform.

Sprint 1.7
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from .event_type import EventType


EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    """
    Lightweight synchronous event bus.

    Components can subscribe to events and receive
    notifications whenever they are published.
    """

    def __init__(self) -> None:

        self._subscribers: dict[
            EventType,
            list[EventHandler],
        ] = defaultdict(list)

    # ---------------------------------------------------------
    # Subscription
    # ---------------------------------------------------------

    def subscribe(
        self,
        event: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Register an event handler.
        """

        if handler not in self._subscribers[event]:

            self._subscribers[event].append(handler)

    # ---------------------------------------------------------

    def unsubscribe(
        self,
        event: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Remove an event handler.
        """

        if handler in self._subscribers[event]:

            self._subscribers[event].remove(handler)

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    def publish(
        self,
        event: EventType,
        **payload: Any,
    ) -> None:
        """
        Publish an event to every subscriber.
        """

        message = {
            "event": event,
            **payload,
        }

        for handler in self._subscribers[event]:

            handler(message)

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def subscriber_count(
        self,
        event: EventType,
    ) -> int:
        """
        Return the number of subscribers.
        """

        return len(self._subscribers[event])

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all subscriptions.
        """

        self._subscribers.clear()

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        total = sum(
            len(handlers)
            for handlers in self._subscribers.values()
        )

        return (
            f"EventBus("
            f"events={len(self._subscribers)}, "
            f"subscribers={total})"
        )
