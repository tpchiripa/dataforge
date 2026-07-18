"""
DataForge Base Rule Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.models import RuleResult
from quality.rules.base_rule import BaseRule


# ==========================================================
# Dummy Rule
# ==========================================================


class DummyRule(BaseRule):
    """
    Concrete implementation used for testing.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Dummy Rule",
            description="Test rule",
        )

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:

        return RuleResult(
            rule_name=self.name,
            passed=True,
            total_records=len(dataframe),
            failed_records=0,
            message="Validation successful.",
        )


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    rule = DummyRule()

    assert rule.name == "Dummy Rule"

    assert rule.description == "Test rule"


# ==========================================================
# Validate
# ==========================================================


def test_validate():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
        }
    )

    rule = DummyRule()

    result = rule.validate(dataframe)

    assert isinstance(
        result,
        RuleResult,
    )

    assert result.passed

    assert result.total_records == 3

    assert result.failed_records == 0


# ==========================================================
# Callable
# ==========================================================


def test_call():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
        }
    )

    rule = DummyRule()

    result = rule(dataframe)

    assert result.passed

    assert result.total_records == 2


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    rule = DummyRule()

    representation = repr(rule)

    assert "DummyRule" in representation

    assert "Dummy Rule" in representation


# ==========================================================
# Abstract Base Class
# ==========================================================


def test_base_rule_cannot_be_instantiated():

    with pytest.raises(TypeError):

        BaseRule(
            name="Base",
            description="Abstract",
        )
