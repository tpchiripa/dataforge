"""
DataForge Pipeline Registry Tests
"""

from __future__ import annotations

import pytest

from pipelines.builder.pipeline_builder import PipelineBuilder
from pipelines.core.exceptions import (DuplicatePipelineError,
                                       PipelineNotFoundError)
from pipelines.registry.pipeline_registry import PipelineRegistry

# ---------------------------------------------------------
# Test Fixture
# ---------------------------------------------------------

@pytest.fixture(autouse=True)
def clear_registry():
    """
    Ensure every test starts with a clean registry.
    """
    PipelineRegistry.clear()
    yield
    PipelineRegistry.clear()


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def build_pipeline(name: str):

    builder = PipelineBuilder(name)

    return builder.build()


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_registry_initialization():

    registry = PipelineRegistry()

    assert registry.count == 0


def test_register_pipeline():

    registry = PipelineRegistry()

    pipeline = build_pipeline("Pipeline A")

    registry.register(pipeline)

    assert registry.count == 1

    assert registry.exists("Pipeline A")


def test_duplicate_registration():

    registry = PipelineRegistry()

    pipeline = build_pipeline("Pipeline A")

    registry.register(pipeline)

    with pytest.raises(DuplicatePipelineError):

        registry.register(pipeline)


def test_get_pipeline():

    registry = PipelineRegistry()

    pipeline = build_pipeline("Pipeline A")

    registry.register(pipeline)

    retrieved = registry.get("Pipeline A")

    assert retrieved is pipeline


def test_pipeline_not_found():

    registry = PipelineRegistry()

    with pytest.raises(PipelineNotFoundError):

        registry.get("Unknown Pipeline")


def test_remove_pipeline():

    registry = PipelineRegistry()

    pipeline = build_pipeline("Pipeline A")

    registry.register(pipeline)

    registry.unregister("Pipeline A")

    assert registry.count == 0

    assert not registry.exists("Pipeline A")


def test_clear_registry():

    registry = PipelineRegistry()

    registry.register(build_pipeline("Pipeline A"))

    registry.register(build_pipeline("Pipeline B"))

    registry.clear()

    assert registry.count == 0


def test_list_pipelines():

    registry = PipelineRegistry()

    registry.register(build_pipeline("Pipeline A"))

    registry.register(build_pipeline("Pipeline B"))

    names = registry.list_pipelines()

    assert names == [
        "pipeline a",
        "pipeline b",
    ]


def test_iteration():

    registry = PipelineRegistry()

    registry.register(build_pipeline("Pipeline A"))

    registry.register(build_pipeline("Pipeline B"))

    names = [
        pipeline.config.name
        for pipeline in registry
    ]

    assert names == [
        "Pipeline A",
        "Pipeline B",
    ]


def test_repr():

    registry = PipelineRegistry()

    registry.register(build_pipeline("Pipeline A"))

    representation = repr(registry)

    assert "PipelineRegistry" in representation

    assert "count=1" in representation

