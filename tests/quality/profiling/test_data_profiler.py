"""
DataForge Data Profiler Tests
"""

from __future__ import annotations

import pandas as pd
import pytest

from quality.profiling.data_profiler import DataProfiler


# ==========================================================
# Fixture
# ==========================================================


@pytest.fixture
def sample_dataframe():

    return pd.DataFrame(
        {
            "id": [1, 2, 2],
            "name": ["John", "Mary", None],
            "age": [25, 30, 30],
            "salary": [1000.0, 2000.0, 2000.0],
        }
    )


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    profiler = DataProfiler()

    assert profiler is not None


# ==========================================================
# Profile Dataset
# ==========================================================


def test_profile(sample_dataframe):

    profiler = DataProfiler()

    report = profiler.profile(sample_dataframe)

    assert report["rows"] == 3
    assert report["columns"] == 4

    # Duplicate ROWS (not duplicate IDs)
    assert report["duplicates"] == 0


# ==========================================================
# Missing Values
# ==========================================================


def test_missing_values(sample_dataframe):

    profiler = DataProfiler()

    report = profiler.profile(sample_dataframe)

    assert report["missing_values"]["name"] == 1


# ==========================================================
# Column Types
# ==========================================================


def test_column_types(sample_dataframe):

    profiler = DataProfiler()

    report = profiler.profile(sample_dataframe)

    assert report["dtypes"]["id"] == "int64"

    # Compatible with multiple pandas versions
    assert report["dtypes"]["name"] in (
        "object",
        "str",
        "string",
    )

    assert report["dtypes"]["age"] == "int64"
    assert report["dtypes"]["salary"] == "float64"


# ==========================================================
# Numeric Statistics
# ==========================================================


def test_numeric_statistics(sample_dataframe):

    profiler = DataProfiler()

    report = profiler.profile(sample_dataframe)

    assert report["numeric"]["age"]["min"] == 25
    assert report["numeric"]["age"]["max"] == 30

    assert report["numeric"]["salary"]["min"] == 1000.0
    assert report["numeric"]["salary"]["max"] == 2000.0


# ==========================================================
# Memory Usage
# ==========================================================


def test_memory_usage(sample_dataframe):

    profiler = DataProfiler()

    report = profiler.profile(sample_dataframe)

    assert report["memory_usage"] > 0


# ==========================================================
# Empty DataFrame
# ==========================================================


def test_empty_dataframe():

    profiler = DataProfiler()

    report = profiler.profile(pd.DataFrame())

    assert report["rows"] == 0
    assert report["columns"] == 0
    assert report["duplicates"] == 0
    assert report["missing_values"] == {}
    assert report["numeric"] == {}


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    profiler = DataProfiler()

    assert "DataProfiler" in repr(profiler)
