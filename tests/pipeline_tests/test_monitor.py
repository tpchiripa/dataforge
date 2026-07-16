"""
DataForge Pipeline Monitor Tests
"""

from __future__ import annotations

from datetime import datetime

from pipelines.core.pipeline_result import PipelineResult
from pipelines.core.pipeline_status import PipelineStatus
from pipelines.monitoring.pipeline_monitor import PipelineMonitor

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def make_result(
    *,
    success: bool = True,
    duration: float = 5.0,
    name: str = "Test Pipeline",
) -> PipelineResult:

    now = datetime.utcnow()

    return PipelineResult(
        success=success,
        status=(
            PipelineStatus.COMPLETED
            if success
            else PipelineStatus.FAILED
        ),
        pipeline_name=name,
        message="Completed" if success else "Failed",
        started_at=now,
        finished_at=now,
        duration_seconds=duration,
        metadata={},
        errors=[] if success else ["Failure"],
        warnings=[],
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_monitor_initialization():

    monitor = PipelineMonitor()

    assert monitor.execution_count == 0

    assert monitor.success_count == 0

    assert monitor.failure_count == 0


def test_record_execution():

    monitor = PipelineMonitor()

    monitor.record(make_result())

    assert monitor.execution_count == 1


def test_history():

    monitor = PipelineMonitor()

    first = make_result(name="Pipeline A")

    second = make_result(name="Pipeline B")

    monitor.record(first)

    monitor.record(second)

    history = monitor.history

    assert len(history) == 2

    assert history[0] is first

    assert history[1] is second


def test_last_execution():

    monitor = PipelineMonitor()

    first = make_result(name="Pipeline A")

    second = make_result(name="Pipeline B")

    monitor.record(first)

    monitor.record(second)

    assert monitor.last_execution is second


def test_successful_runs():

    monitor = PipelineMonitor()

    monitor.record(make_result(success=True))

    monitor.record(make_result(success=False))

    assert len(monitor.successful_runs) == 1


def test_failed_runs():

    monitor = PipelineMonitor()

    monitor.record(make_result(success=True))

    monitor.record(make_result(success=False))

    assert len(monitor.failed_runs) == 1


def test_success_rate():

    monitor = PipelineMonitor()

    monitor.record(make_result(success=True))

    monitor.record(make_result(success=True))

    monitor.record(make_result(success=False))

    assert monitor.success_rate == (2 / 3) * 100


def test_average_duration():

    monitor = PipelineMonitor()

    monitor.record(make_result(duration=5))

    monitor.record(make_result(duration=15))

    assert monitor.average_duration == 10


def test_summary():

    monitor = PipelineMonitor()

    monitor.record(make_result(success=True, duration=4))

    monitor.record(make_result(success=False, duration=6))

    summary = monitor.summary

    assert summary["executions"] == 2

    assert summary["successful"] == 1

    assert summary["failed"] == 1

    assert summary["average_duration"] == 5


def test_clear():

    monitor = PipelineMonitor()

    monitor.record(make_result())

    monitor.record(make_result())

    monitor.clear()

    assert monitor.execution_count == 0


def test_len():

    monitor = PipelineMonitor()

    monitor.record(make_result())

    monitor.record(make_result())

    assert len(monitor) == 2


def test_repr():

    monitor = PipelineMonitor()

    monitor.record(make_result())

    representation = repr(monitor)

    assert "PipelineMonitor" in representation

    assert "1" in representation
