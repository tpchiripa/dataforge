"""
DataForge Regex Rule
"""

from __future__ import annotations

import re

import pandas as pd

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


class RegexRule(BaseRule):
    """
    Validates values against a regular expression.
    """

    def __init__(
        self,
        column: str,
        pattern: str,
    ) -> None:

        super().__init__(
            name="Regex Rule",
        )

        self.column = column
        self.pattern = pattern
        self._regex = re.compile(pattern)

    # ---------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        if self.column not in dataframe.columns:

            raise RuleError(
                f"Column '{self.column}' does not exist."
            )

        values = dataframe[self.column].fillna("").astype(str)

        invalid = ~values.str.fullmatch(self._regex)

        failed_records = int(invalid.sum())

        return RuleResult(
            rule_name=self.name,
            passed=failed_records == 0,
            total_records=len(dataframe),
            failed_records=failed_records,
            message=(
                "Validation passed."
                if failed_records == 0
                else f"{failed_records} value(s) failed regex validation."
            ),
            details={
                "column": self.column,
                "pattern": self.pattern,
            },
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(column='{self.column}', "
            f"pattern='{self.pattern}')"
        )
