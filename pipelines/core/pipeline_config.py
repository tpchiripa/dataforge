"""
DataForge Pipeline Configuration
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineConfig:
    """
    Configuration for a DataForge pipeline.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    name: str

    description: str = ""

    version: str = "1.0.0"

    enabled: bool = True

    owner: str = ""

    # ---------------------------------------------------------
    # Source & Destination
    # ---------------------------------------------------------

    source_connector: str = ""

    destination_connector: str = ""

    source_dataset: str = ""

    destination_dataset: str = ""

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    batch_size: int = 10_000

    max_retries: int = 3

    retry_delay_seconds: int = 5

    timeout_seconds: int = 3600

    schedule: str = ""

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validate_before_run: bool = True

    stop_on_error: bool = True

    # ---------------------------------------------------------
    # Notifications
    # ---------------------------------------------------------

    notify_on_success: bool = False

    notify_on_failure: bool = True

    notification_email: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    tags: list[str] = field(default_factory=list)

    parameters: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Parameter Helpers
    # ---------------------------------------------------------

    def set_parameter(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set or update a pipeline parameter.
        """

        self.parameters[key] = value

    def get_parameter(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a pipeline parameter.
        """

        return self.parameters.get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Metadata Helpers
    # ---------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set pipeline metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve pipeline metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Tag Helpers
    # ---------------------------------------------------------

    def add_tag(
        self,
        tag: str,
    ) -> None:
        """
        Add a tag if it does not already exist.
        """

        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(
        self,
        tag: str,
    ) -> None:
        """
        Remove a tag.
        """

        if tag in self.tags:
            self.tags.remove(tag)

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def retry_enabled(
        self,
    ) -> bool:
        """
        Returns True if retries are enabled.
        """

        return self.max_retries > 0

    @property
    def notifications_enabled(
        self,
    ) -> bool:
        """
        Returns True if any notifications are enabled.
        """

        return (
            self.notify_on_success
            or self.notify_on_failure
        )
