"""
DataForge Range Rule Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.range_rule import RangeRule


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    assert rule.name == "Range Rule"
    assert rule.column == "age"
    assert rule.minimum == 18
    assert rule.maximum == 65


# ==========================================================
# Valid Data
# ==========================================================


def test_validate_success():

    dataframe = pd.DataFrame(
        {
            "age": [20, 30, 45, 60],
        }
    )

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    result = rule.validate(dataframe)

    assert isinstance(result, RuleResult)
    assert result.passed
    assert result.failed_records == 0


# ==========================================================
# Values Outside Range
# ==========================================================


def test_validate_failure():

    dataframe = pd.DataFrame(
        {
            "age": [15, 20, 70],
        }
    )

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    result = rule.validate(dataframe)

    assert not result.passed
    assert result.failed_records == 2


# ==========================================================
# Missing Column
# ==========================================================


def test_missing_column():

    dataframe = pd.DataFrame(
        {
            "salary": [1000, 2000],
        }
    )

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    with pytest.raises(RuleError):

        rule.validate(dataframe)


# ==========================================================
# Callable
# ==========================================================


def test_call():

    dataframe = pd.DataFrame(
        {
            "age": [30],
        }
    )

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    result = rule(dataframe)

    assert result.passed


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    rule = RangeRule(
        column="age",
        minimum=18,
        maximum=65,
    )

    representation = repr(rule)

    assert "RangeRule" in representation
    assert "age" in representation
