"""
DataForge Base Quality Rule
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from quality.models import RuleResult


class BaseRule(ABC):
    """
    Base class for all data quality rules.

    Every quality rule in DataForge inherits from this class
    and implements the validate() method.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:

        self._name = name
        self._description = description

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:

        return self._name

    # ---------------------------------------------------------

    @property
    def description(
        self,
    ) -> str:

        return self._description

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:
        """
        Execute the rule against a DataFrame.

        Parameters
        ----------
        dataframe:
            DataFrame to validate.

        Returns
        -------
        RuleResult
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    def __call__(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        return self.validate(dataframe)

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )
