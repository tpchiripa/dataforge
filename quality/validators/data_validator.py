"""
DataForge Data Validator
"""

from __future__ import annotations

import pandas as pd

from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


class DataValidator:
    """
    Executes a collection of validation rules.
    """

    def __init__(self) -> None:

        self._rules: list[BaseRule] = []

    # ---------------------------------------------------------

    @property
    def rules(self) -> list[BaseRule]:

        return self._rules

    # ---------------------------------------------------------

    def add_rule(
        self,
        rule: BaseRule,
    ) -> None:

        self._rules.append(rule)

    # ---------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> list[RuleResult]:

        return [
            rule.validate(dataframe)
            for rule in self._rules
        ]

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._rules.clear()

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(rules={len(self._rules)})"
        )
