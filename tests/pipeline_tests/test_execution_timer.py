"""
DataForge ExecutionTimer Tests
"""

from __future__ import annotations

import time

from pipelines.execution.execution_timer import ExecutionTimer


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


def test_timer_initialization():
    """
    Timer should start without timestamps.
    """

    timer = ExecutionTimer()

    assert timer._started is None
    assert timer._finished is None


def test_timer_duration_before_execution():
    """
    Duration should be zero before the timer runs.
    """

    timer = ExecutionTimer()

    assert timer.duration == 0.0


def test_timer_start():
    """
    Starting the timer should record a start timestamp.
    """

    timer = ExecutionTimer()

    timer.start()

    assert timer._started is not None


def test_timer_stop():
    """
    Stopping the timer should record a finish timestamp.
    """

    timer = ExecutionTimer()

    timer.start()
    timer.stop()

    assert timer._started is not None
    assert timer._finished is not None


def test_timer_duration_after_execution():
    """
    Duration should be a non-negative number after execution.
    """

    timer = ExecutionTimer()

    timer.start()

    time.sleep(0.01)

    timer.stop()

    assert timer.duration >= 0.0


def test_timer_duration_increases_with_elapsed_time():
    """
    Duration should reflect elapsed execution time.
    """

    timer = ExecutionTimer()

    timer.start()

    time.sleep(0.05)

    timer.stop()

    assert timer.duration >= 0.05


def test_timer_can_be_restarted():
    """
    Starting the timer again should reset the execution window.
    """

    timer = ExecutionTimer()

    timer.start()

    time.sleep(0.01)

    timer.stop()

    first_duration = timer.duration

    timer.start()

    assert timer._started is not None

    assert timer._finished is not None

    timer.stop()

    second_duration = timer.duration

    assert first_duration >= 0.0
    assert second_duration >= 0.0
