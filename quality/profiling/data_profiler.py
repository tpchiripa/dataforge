"""
DataForge Data Profiler
"""

from __future__ import annotations

import pandas as pd


class DataProfiler:
    """
    Profiles a pandas DataFrame.
    """

    def profile(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        report = {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": list(dataframe.columns),
            "duplicates": int(dataframe.duplicated().sum()),
            "missing_values": dataframe.isna().sum().to_dict(),
            "dtypes": {
                column: str(dtype)
                for column, dtype in dataframe.dtypes.items()
            },
            "memory_usage": int(
                dataframe.memory_usage(deep=True).sum()
            ),
            "numeric": {},
        }

        numeric_columns = dataframe.select_dtypes(
            include="number",
        ).columns

        for column in numeric_columns:

            series = dataframe[column]

            report["numeric"][column] = {
                "min": series.min(),
                "max": series.max(),
                "mean": float(series.mean()),
                "std": float(series.std())
                if len(series) > 1
                else 0.0,
            }

        return report

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}()"
