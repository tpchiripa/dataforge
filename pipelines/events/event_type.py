"""
DataForge Event Types

Defines all events that can occur during
pipeline execution.
"""

from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    """
    Supported DataForge event types.
    """

    # ---------------------------------------------------------
    # Pipeline Events
    # ---------------------------------------------------------

    PIPELINE_STARTED = "pipeline.started"

    PIPELINE_COMPLETED = "pipeline.completed"

    PIPELINE_FAILED = "pipeline.failed"

    # ---------------------------------------------------------
    # Step Events
    # ---------------------------------------------------------

    STEP_STARTED = "step.started"

    STEP_COMPLETED = "step.completed"

    STEP_FAILED = "step.failed"

    # ---------------------------------------------------------
    # Validation Events
    # ---------------------------------------------------------

    VALIDATION_STARTED = "validation.started"

    VALIDATION_COMPLETED = "validation.completed"

    VALIDATION_FAILED = "validation.failed"

    # ---------------------------------------------------------
    # Extraction Events
    # ---------------------------------------------------------

    EXTRACTION_STARTED = "extraction.started"

    EXTRACTION_COMPLETED = "extraction.completed"

    EXTRACTION_FAILED = "extraction.failed"

    # ---------------------------------------------------------
    # Transformation Events
    # ---------------------------------------------------------

    TRANSFORMATION_STARTED = "transformation.started"

    TRANSFORMATION_COMPLETED = "transformation.completed"

    TRANSFORMATION_FAILED = "transformation.failed"

    # ---------------------------------------------------------
    # Load Events
    # ---------------------------------------------------------

    LOAD_STARTED = "load.started"

    LOAD_COMPLETED = "load.completed"

    LOAD_FAILED = "load.failed"

    # ---------------------------------------------------------
    # Monitoring Events
    # ---------------------------------------------------------

    METRICS_UPDATED = "metrics.updated"

    LOG_CREATED = "log.created"

    ALERT_TRIGGERED = "alert.triggered"

    # ---------------------------------------------------------
    # Registry Events
    # ---------------------------------------------------------

    PIPELINE_REGISTERED = "pipeline.registered"

    PIPELINE_UNREGISTERED = "pipeline.unregistered"

    # ---------------------------------------------------------
    # Connector Events
    # ---------------------------------------------------------

    CONNECTOR_CONNECTED = "connector.connected"

    CONNECTOR_DISCONNECTED = "connector.disconnected"

    CONNECTOR_FAILED = "connector.failed"

    # ---------------------------------------------------------

    def __str__(self) -> str:
        """
        Return the event value.
        """

        return self.value
