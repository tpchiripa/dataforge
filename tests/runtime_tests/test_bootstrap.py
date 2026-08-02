"""
DataForge Bootstrap Tests
"""

from __future__ import annotations

import pytest

from pipelines.bootstrap.bootstrap import Bootstrap

from pipelines.container.service_container import ServiceContainer
from pipelines.container.service_provider import ServiceProvider

from pipelines.discovery.module_discovery import ModuleDiscovery
from pipelines.modules.module_registry import ModuleRegistry


# ---------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------


def test_bootstrap_initialization():

    bootstrap = Bootstrap()

    assert bootstrap is not None


# ---------------------------------------------------------
# Properties
# ---------------------------------------------------------


def test_container_property():

    bootstrap = Bootstrap()

    assert isinstance(
        bootstrap.container,
        ServiceContainer,
    )


def test_modules_property():

    bootstrap = Bootstrap()

    assert isinstance(
        bootstrap.modules,
        ModuleRegistry,
    )


def test_discovery_property():

    bootstrap = Bootstrap()

    assert isinstance(
        bootstrap.discovery,
        ModuleDiscovery,
    )


# ---------------------------------------------------------
# Discovery
# ---------------------------------------------------------


def test_module_discovery():

    bootstrap = Bootstrap()

    bootstrap.discover_modules()

    assert (
        bootstrap.modules.module_count
        > 0
    )


def test_discovered_modules_are_unique():

    bootstrap = Bootstrap()

    bootstrap.discover_modules()

    names = bootstrap.modules.list_names()

    assert len(names) == len(set(names))


# ---------------------------------------------------------
# Runtime Build
# ---------------------------------------------------------


def test_build_returns_service_provider():

    bootstrap = Bootstrap()

    provider = bootstrap.build()

    assert isinstance(
        provider,
        ServiceProvider,
    )


def test_build_initializes_modules():

    bootstrap = Bootstrap()

    bootstrap.build()

    assert (
        bootstrap.modules.module_count
        > 0
    )


# ---------------------------------------------------------
# Shutdown
# ---------------------------------------------------------


def test_shutdown():

    bootstrap = Bootstrap()

    bootstrap.build()

    bootstrap.shutdown()


# ---------------------------------------------------------
# Representation
# ---------------------------------------------------------


def test_repr():

    bootstrap = Bootstrap()

    representation = repr(
        bootstrap,
    )

    assert (
        "Bootstrap("
        in representation
    )


# ---------------------------------------------------------
# Multiple Builds
# ---------------------------------------------------------


def test_multiple_bootstrap_instances():

    first = Bootstrap()

    second = Bootstrap()

    assert first is not second


def test_build_multiple_times():

    bootstrap = Bootstrap()

    provider1 = bootstrap.build()

    bootstrap.shutdown()

    provider2 = bootstrap.build()

    assert isinstance(
        provider1,
        ServiceProvider,
    )

    assert isinstance(
        provider2,
        ServiceProvider,
    )
