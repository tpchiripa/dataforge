"""
DataForge Quality Manager
"""

from __future__ import annotations

import pandas as pd

from quality.profiling.data_profiler import DataProfiler
from quality.analyzers.statistics import StatisticsAnalyzer
from quality.reports.quality_report import QualityReport
from quality.validators.data_validator import DataValidator


class QualityManager:
    """
    Enterprise orchestrator for the DataForge Quality subsystem.

    Coordinates:

    - Data profiling
    - Statistical analysis
    - Data validation
    - Report generation
    """

    def __init__(self) -> None:

        self.profiler = DataProfiler()
        self.statistics = StatisticsAnalyzer()
        self.report_builder = QualityReport()

    # ---------------------------------------------------------
    # Run Complete Quality Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        dataframe: pd.DataFrame,
        validator: DataValidator,
    ) -> dict:

        profile = self.profiler.profile(dataframe)

        statistics = self.statistics.analyze(dataframe)

        validation_results = validator.validate(dataframe)

        return self.report_builder.generate(
            dataframe=dataframe,
            validation_results=validation_results,
            profile=profile,
            statistics=statistics,
        )

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}()"
