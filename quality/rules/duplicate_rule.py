"""
DataForge Duplicate Rule
"""

from __future__ import annotations

import pandas as pd

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


class DuplicateRule(BaseRule):
    """
    Validates duplicate records using one or more columns.
    """

    def __init__(
        self,
        columns: list[str],
    ) -> None:

        super().__init__(
            name="Duplicate Rule",
        )

        self.columns = columns

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        missing = [
            column
            for column in self.columns
            if column not in dataframe.columns
        ]

        if missing:

            raise RuleError(
                f"Missing column(s): {', '.join(missing)}"
            )

        total_records = len(dataframe)

        failed_records = int(
            dataframe.duplicated(
                subset=self.columns,
            ).sum()
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
                else f"{failed_records} duplicate record(s) found."
            ),
            details={
                "columns": self.columns,
            },
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(columns={self.columns})"
        )
