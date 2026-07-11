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

    batch_size: int = 10000

    max_retries: int = 3

    retry_delay_seconds: int = 5

    timeout_seconds: int = 3600

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validate_before_run: bool = True

    stop_on_error: bool = True

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    tags: list[str] = field(default_factory=list)

    parameters: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------

    def add_parameter(self, key: str, value: Any) -> None:
        """
        Add or update a pipeline parameter.
        """
        self.parameters[key] = value

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add or update pipeline metadata.
        """
        self.metadata[key] = value

    def add_tag(self, tag: str) -> None:
        """
        Add a tag if it does not already exist.
        """
        if tag not in self.tags:
            self.tags.append(tag)
