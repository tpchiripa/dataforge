"""
DataForge Range Rule
"""

from __future__ import annotations

import pandas as pd

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


class RangeRule(BaseRule):
    """
    Validates that numeric values fall within a specified range.
    """

    def __init__(
        self,
        column: str,
        minimum: float | int,
        maximum: float | int,
    ) -> None:

        super().__init__(
            name="Range Rule",
        )

        self.column = column
        self.minimum = minimum
        self.maximum = maximum

    # ---------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        if self.column not in dataframe.columns:

            raise RuleError(
                f"Column '{self.column}' does not exist."
            )

        invalid = (
            (dataframe[self.column] < self.minimum)
            | (dataframe[self.column] > self.maximum)
        )

        failed_records = int(invalid.sum())

        return RuleResult(
            rule_name=self.name,
            passed=failed_records == 0,
            total_records=len(dataframe),
            failed_records=failed_records,
            message=(
                "Validation passed."
                if failed_records == 0
                else f"{failed_records} value(s) outside allowed range."
            ),
            details={
                "column": self.column,
                "minimum": self.minimum,
                "maximum": self.maximum,
            },
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(column='{self.column}', "
            f"minimum={self.minimum}, "
            f"maximum={self.maximum})"
        )
