"""
DataForge Null Rule
"""

from __future__ import annotations

import pandas as pd

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


class NullRule(BaseRule):
    """
    Validates that a column does not contain null values.
    """

    def __init__(
        self,
        column: str,
    ) -> None:

        super().__init__(
            name="Null Rule",
        )

        self.column = column

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        if self.column not in dataframe.columns:

            raise RuleError(
                f"Column '{self.column}' does not exist."
            )

        total_records = len(dataframe)

        failed_records = int(
            dataframe[self.column].isna().sum()
        )

        passed = failed_records == 0

        return RuleResult(
            rule_name=self.name,
            passed=passed,
            total_records=total_records,
            failed_records=failed_records,
            message=(
                "Validation passed."
                if passed
                else f"{failed_records} null value(s) found."
            ),
            details={
                "column": self.column,
            },
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(column='{self.column}')"
        )
