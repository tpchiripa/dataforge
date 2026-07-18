"""
DataForge Quality Report Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.models import RuleResult
from quality.reports.quality_report import QualityReport


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

    report = QualityReport()

    assert report is not None


# ==========================================================
# Generate Report
# ==========================================================


def test_generate_report(sample_dataframe):

    report = QualityReport()

    validation_results = [
        RuleResult(
            rule_name="Null Rule",
            passed=True,
            total_records=3,
            failed_records=0,
            message="Validation passed.",
        )
    ]

    profile = {
        "rows": 3,
        "columns": 3,
    }

    statistics = {
        "age": {
            "mean": 30,
        }
    }

    result = report.generate(
        dataframe=sample_dataframe,
        validation_results=validation_results,
        profile=profile,
        statistics=statistics,
    )

    assert result["rows"] == 3
    assert result["columns"] == 3
    assert len(result["validation_results"]) == 1


# ==========================================================
# Timestamp
# ==========================================================


def test_timestamp(sample_dataframe):

    report = QualityReport()

    result = report.generate(
        dataframe=sample_dataframe,
        validation_results=[],
        profile={},
        statistics={},
    )

    assert "generated_at" in result


# ==========================================================
# Empty Validation Results
# ==========================================================


def test_empty_validation_results(sample_dataframe):

    report = QualityReport()

    result = report.generate(
        dataframe=sample_dataframe,
        validation_results=[],
        profile={},
        statistics={},
    )

    assert result["validation_results"] == []


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    report = QualityReport()

    assert "QualityReport" in repr(report)

