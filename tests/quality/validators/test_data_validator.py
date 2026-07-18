"""
DataForge Data Validator Tests
"""

from __future__ import annotations

import pandas as pd

from quality.rules.null_rule import NullRule
from quality.rules.duplicate_rule import DuplicateRule
from quality.rules.range_rule import RangeRule
from quality.rules.regex_rule import RegexRule
from quality.validators.data_validator import DataValidator


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    validator = DataValidator()

    assert validator.rules == []


# ==========================================================
# Add Rule
# ==========================================================


def test_add_rule():

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    assert len(validator.rules) == 1


# ==========================================================
# Multiple Rules
# ==========================================================


def test_add_multiple_rules():

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    validator.add_rule(
        DuplicateRule(["id"]),
    )

    validator.add_rule(
        RangeRule(
            "age",
            18,
            65,
        )
    )

    assert len(validator.rules) == 3


# ==========================================================
# Successful Validation
# ==========================================================


def test_validate_success():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["John", "Mary"],
            "age": [25, 30],
            "email": [
                "john@test.com",
                "mary@test.com",
            ],
        }
    )

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    validator.add_rule(
        DuplicateRule(["id"]),
    )

    validator.add_rule(
        RangeRule(
            "age",
            18,
            65,
        )
    )

    validator.add_rule(
        RegexRule(
            "email",
            r"^[\w\.-]+@[\w\.-]+\.\w+$",
        )
    )

    results = validator.validate(dataframe)

    assert len(results) == 4

    assert all(result.passed for result in results)


# ==========================================================
# Failed Validation
# ==========================================================


def test_validate_failure():

    dataframe = pd.DataFrame(
        {
            "id": [1, 1],
            "name": ["John", None],
            "age": [17, 80],
            "email": [
                "invalid",
                "mary@test.com",
            ],
        }
    )

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    validator.add_rule(
        DuplicateRule(["id"]),
    )

    validator.add_rule(
        RangeRule(
            "age",
            18,
            65,
        )
    )

    validator.add_rule(
        RegexRule(
            "email",
            r"^[\w\.-]+@[\w\.-]+\.\w+$",
        )
    )

    results = validator.validate(dataframe)

    assert len(results) == 4

    assert any(not result.passed for result in results)


# ==========================================================
# Clear Rules
# ==========================================================


def test_clear_rules():

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    validator.clear()

    assert validator.rules == []


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    representation = repr(validator)

    assert "DataValidator" in representation
