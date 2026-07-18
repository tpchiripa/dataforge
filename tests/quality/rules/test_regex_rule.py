"""
DataForge Regex Rule Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.regex_rule import RegexRule


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    rule = RegexRule(
        column="email",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
    )

    assert rule.name == "Regex Rule"
    assert rule.column == "email"
    assert rule.pattern == r"^[\w\.-]+@[\w\.-]+\.\w+$"


# ==========================================================
# Valid Values
# ==========================================================


def test_validate_success():

    dataframe = pd.DataFrame(
        {
            "email": [
                "john@test.com",
                "mary@test.com",
            ],
        }
    )

    rule = RegexRule(
        column="email",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
    )

    result = rule.validate(dataframe)

    assert isinstance(result, RuleResult)
    assert result.passed
    assert result.failed_records == 0


# ==========================================================
# Invalid Values
# ==========================================================


def test_validate_failure():

    dataframe = pd.DataFrame(
        {
            "email": [
                "john@test.com",
                "invalid-email",
                "mary@test.com",
                "123",
            ],
        }
    )

    rule = RegexRule(
        column="email",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
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
            "name": ["John"],
        }
    )

    rule = RegexRule(
        column="email",
        pattern=r".+",
    )

    with pytest.raises(RuleError):

        rule.validate(dataframe)


# ==========================================================
# Callable
# ==========================================================


def test_call():

    dataframe = pd.DataFrame(
        {
            "email": [
                "john@test.com",
            ],
        }
    )

    rule = RegexRule(
        column="email",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
    )

    result = rule(dataframe)

    assert result.passed


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    rule = RegexRule(
        column="email",
        pattern=r".+",
    )

    representation = repr(rule)

    assert "RegexRule" in representation
    assert "email" in representation
