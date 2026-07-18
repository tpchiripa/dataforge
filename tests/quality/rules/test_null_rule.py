"""
DataForge Null Rule Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.null_rule import NullRule


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    rule = NullRule(
        column="name",
    )

    assert rule.name == "Null Rule"

    assert rule.column == "name"


# ==========================================================
# No Null Values
# ==========================================================


def test_validate_no_nulls():

    dataframe = pd.DataFrame(
        {
            "name": [
                "Alice",
                "Bob",
                "Charlie",
            ],
        }
    )

    rule = NullRule(
        column="name",
    )

    result = rule.validate(
        dataframe,
    )

    assert isinstance(
        result,
        RuleResult,
    )

    assert result.passed

    assert result.total_records == 3

    assert result.failed_records == 0


# ==========================================================
# Null Values Present
# ==========================================================


def test_validate_with_nulls():

    dataframe = pd.DataFrame(
        {
            "name": [
                "Alice",
                None,
                "Charlie",
                None,
            ],
        }
    )

    rule = NullRule(
        column="name",
    )

    result = rule.validate(
        dataframe,
    )

    assert not result.passed

    assert result.total_records == 4

    assert result.failed_records == 2


# ==========================================================
# All Values Null
# ==========================================================


def test_validate_all_nulls():

    dataframe = pd.DataFrame(
        {
            "name": [
                None,
                None,
                None,
            ],
        }
    )

    rule = NullRule(
        column="name",
    )

    result = rule.validate(
        dataframe,
    )

    assert not result.passed

    assert result.total_records == 3

    assert result.failed_records == 3


# ==========================================================
# Missing Column
# ==========================================================


def test_missing_column():

    dataframe = pd.DataFrame(
        {
            "id": [
                1,
                2,
            ],
        }
    )

    rule = NullRule(
        column="name",
    )

    with pytest.raises(
        RuleError,
    ):

        rule.validate(
            dataframe,
        )


# ==========================================================
# Callable
# ==========================================================


def test_call():

    dataframe = pd.DataFrame(
        {
            "name": [
                "Alice",
                "Bob",
            ],
        }
    )

    rule = NullRule(
        column="name",
    )

    result = rule(
        dataframe,
    )

    assert result.passed


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    rule = NullRule(
        column="email",
    )

    representation = repr(
        rule,
    )

    assert "NullRule" in representation

    assert "email" in representation
