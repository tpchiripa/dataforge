"""
DataForge Quality Models
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any


# ==========================================================
# Rule Result
# ==========================================================


@dataclass(slots=True)
class RuleResult:
    """
    Result returned by a quality rule.
    """

    rule_name: str
    passed: bool

    total_records: int = 0
    failed_records: int = 0

    message: str = ""

    details: dict[str, Any] = field(
        default_factory=dict,
    )


# ==========================================================
# Validation Result
# ==========================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Aggregated validation outcome.
    """

    dataset_name: str

    passed: bool

    rule_results: list[RuleResult] = field(
        default_factory=list,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def total_rules(
        self,
    ) -> int:

        return len(self.rule_results)

    @property
    def passed_rules(
        self,
    ) -> int:

        return sum(
            1
            for result in self.rule_results
            if result.passed
        )

    @property
    def failed_rules(
        self,
    ) -> int:

        return sum(
            1
            for result in self.rule_results
            if not result.passed
        )


# ==========================================================
# Profile Result
# ==========================================================


@dataclass(slots=True)
class ProfileResult:
    """
    Dataset profiling output.
    """

    dataset_name: str

    row_count: int = 0

    column_count: int = 0

    columns: dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )


# ==========================================================
# Quality Report
# ==========================================================


@dataclass(slots=True)
class QualityReport:
    """
    Final quality report object.
    """

    validation_result: ValidationResult

    profile_result: ProfileResult | None = None

    generated_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def success(
        self,
    ) -> bool:

        return self.validation_result.passed
