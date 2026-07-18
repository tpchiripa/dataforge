"""
DataForge Statistics Analyzer
"""

from __future__ import annotations

import pandas as pd


class StatisticsAnalyzer:
    """
    Computes descriptive statistics for numeric columns.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        if dataframe.empty:
            return {}

        report = {}

        numeric = dataframe.select_dtypes(include="number")

        for column in numeric.columns:

            series = numeric[column]

            report[column] = {
                "count": int(series.count()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "min": series.min(),
                "max": series.max(),
                "sum": float(series.sum()),
            }

        return report

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}()"
