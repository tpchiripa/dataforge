"""
DataForge Quality Exceptions
"""

from __future__ import annotations


class QualityError(Exception):
    """
    Base exception for all quality-related errors.
    """


class ValidationError(QualityError):
    """
    Raised when data validation fails.
    """


class RuleError(QualityError):
    """
    Raised when a quality rule cannot be executed.
    """


class ProfilingError(QualityError):
    """
    Raised when profiling fails.
    """


class ReportError(QualityError):
    """
    Raised when generating a quality report fails.
    """

