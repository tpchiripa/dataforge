"""
DataForge Metadata Exceptions
"""

from __future__ import annotations


class MetadataError(Exception):
    """
    Base exception for all metadata-related errors.
    """


class DatasetNotFoundError(MetadataError):
    """
    Raised when a requested dataset cannot be found.
    """


class PipelineRunNotFoundError(MetadataError):
    """
    Raised when a requested pipeline run cannot be found.
    """


class MetadataPersistenceError(MetadataError):
    """
    Raised when a metadata write fails.

    Callers (e.g. MetadataHook) are expected to catch this and
    log rather than propagate it, per the subsystem's failure
    policy: metadata persistence failure must never fail a
    pipeline.
    """