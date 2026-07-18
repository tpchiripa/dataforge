"""
DataForge Statistics Analyzer Tests
"""

from __future__ import annotations

import pandas as pd

from quality.analyzers.statistics import StatisticsAnalyzer


# ==========================================================
# Fixture
# ==========================================================


def dataframe():

    return pd.DataFrame(
        {
            "age": [25, 30, 35, 40],
            "salary": [1000, 2000, 3000, 4000],
        }
    )


# ==========================================================
# Initialization
# ==========================================================


def test_initialization():

    analyzer = StatisticsAnalyzer()

    assert analyzer is not None


# ==========================================================
# Analyze
# ==========================================================


def test_analyze():

    analyzer = StatisticsAnalyzer()

    report = analyzer.analyze(dataframe())

    assert "age" in report
    assert "salary" in report


# ==========================================================
# Mean
# ==========================================================


def test_mean():

    analyzer = StatisticsAnalyzer()

    report = analyzer.analyze(dataframe())

    assert report["age"]["mean"] == 32.5


# ==========================================================
# Min / Max
# ==========================================================


def test_min_max():

    analyzer = StatisticsAnalyzer()

    report = analyzer.analyze(dataframe())

    assert report["salary"]["min"] == 1000
    assert report["salary"]["max"] == 4000


# ==========================================================
# Empty DataFrame
# ==========================================================


def test_empty_dataframe():

    analyzer = StatisticsAnalyzer()

    report = analyzer.analyze(pd.DataFrame())

    assert report == {}


# ==========================================================
# Representation
# ==========================================================


def test_repr():

    analyzer = StatisticsAnalyzer()

    assert "StatisticsAnalyzer" in repr(analyzer)
