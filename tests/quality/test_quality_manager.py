"""
DataForge Quality Manager Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.manager import QualityManager
from quality.rules.null_rule import NullRule
from quality.validators.data_validator import DataValidator


# ==========================================================
# Fixture
# ==========================================================


@pytest.fixture
def sample_dataframe():

    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["John", "Mary", "Peter"],
            "age": [25, 30, 35],
        }
    )


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    manager = QualityManager()

    assert manager is not None


# ==========================================================
# Run Quality Pipeline
# ==========================================================


def test_run(sample_dataframe):

    validator = DataValidator()

    validator.add_rule(
        NullRule("name"),
    )

    manager = QualityManager()

    report = manager.run(
        dataframe=sample_dataframe,
        validator=validator,
    )

    assert report["rows"] == 3
    assert report["columns"] == 3
    assert len(report["validation_results"]) == 1


# ==========================================================
# Empty Validator
# ==========================================================


def test_run_without_rules(sample_dataframe):

    validator = DataValidator()

    manager = QualityManager()

    report = manager.run(
        dataframe=sample_dataframe,
        validator=validator,
    )

    assert report["validation_results"] == []


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    manager = QualityManager()

    assert "QualityManager" in repr(manager)
