"""
DataForge Duplicate Rule Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.exceptions import RuleError
from quality.models import RuleResult
from quality.rules.duplicate_rule import DuplicateRule


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    rule = DuplicateRule(
        columns=["id"],
    )

    assert rule.name == "Duplicate Rule"

    assert rule.columns == ["id"]


# ==========================================================
# No Duplicates
# ==========================================================


def test_validate_no_duplicates():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
        }
    )

    rule = DuplicateRule(
        columns=["id"],
    )

    result = rule.validate(dataframe)

    assert isinstance(result, RuleResult)

    assert result.passed

    assert result.total_records == 3

    assert result.failed_records == 0


# ==========================================================
# Duplicate Records
# ==========================================================


def test_validate_duplicates():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 2, 3, 3],
        }
    )

    rule = DuplicateRule(
        columns=["id"],
    )

    result = rule.validate(dataframe)

    assert not result.passed

    assert result.failed_records == 2


# ==========================================================
# Multiple Columns
# ==========================================================


def test_multiple_columns():

    dataframe = pd.DataFrame(
        {
            "first": ["A", "A", "B"],
            "last": ["X", "X", "Y"],
        }
    )

    rule = DuplicateRule(
        columns=["first", "last"],
    )

    result = rule.validate(dataframe)

    assert not result.passed

    assert result.failed_records == 1


# ==========================================================
# Missing Column
# ==========================================================


def test_missing_column():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
        }
    )

    rule = DuplicateRule(
        columns=["name"],
    )

    with pytest.raises(RuleError):

        rule.validate(dataframe)


# ==========================================================
# Callable
# ==========================================================


def test_call():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
        }
    )

    rule = DuplicateRule(
        columns=["id"],
    )

    result = rule(dataframe)

    assert result.passed


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    rule = DuplicateRule(
        columns=["id"],
    )

    representation = repr(rule)

    assert "DuplicateRule" in representation

    assert "id" in representation
