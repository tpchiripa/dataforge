"""
DataForge Bootstrap

Bootstraps the DataForge runtime by configuring the
dependency injection container and automatically
discovering DataForge modules.
"""

from __future__ import annotations

from pipelines.container.service_container import ServiceContainer
from pipelines.container.service_provider import ServiceProvider

from pipelines.discovery.module_discovery import ModuleDiscovery
from pipelines.modules.module_registry import ModuleRegistry

from pipelines.executor.pipeline_executor import PipelineExecutor
from pipelines.lifecycle.lifecycle_manager import LifecycleManager
from pipelines.plugins.plugin_manager import PluginManager


class Bootstrap:
    """
    DataForge application bootstrap.

    Responsible for:

    - Creating the dependency injection container
    - Registering core runtime services
    - Discovering DataForge modules
    - Initializing all modules
    - Producing the ServiceProvider
    """

    def __init__(
        self,
    ) -> None:

        #
        # Create dependency injection container
        #

        self._container = ServiceContainer()

        self._container.register_instance(
            ServiceContainer,
            self._container,
        )

        #
        # Runtime infrastructure
        #

        self._modules = ModuleRegistry()

        self._discovery = ModuleDiscovery()

        self._container.register_instance(
            ModuleRegistry,
            self._modules,
        )

        self._container.register_instance(
            ModuleDiscovery,
            self._discovery,
        )

        #
        # Core services
        #

        self._lifecycle = LifecycleManager()

        self._plugins = PluginManager(
            container=self._container,
        )

        self._executor = PipelineExecutor(
            lifecycle=self._lifecycle,
            plugins=self._plugins,
        )

        self._container.register_instance(
            LifecycleManager,
            self._lifecycle,
        )

        self._container.register_instance(
            PluginManager,
            self._plugins,
        )

        self._container.register_instance(
            PipelineExecutor,
            self._executor,
        )

    # ---------------------------------------------------------
    # Module Discovery
    # ---------------------------------------------------------

    def discover_modules(
        self,
    ) -> None:
        """
        Automatically discover every DataForge module.
        """

        self._discovery.discover(
            self._modules,
        )

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def build(
        self,
    ) -> ServiceProvider:
        """
        Build the DataForge runtime.
        """

        self.discover_modules()

        self._modules.initialize(
            self._container,
        )

        return ServiceProvider(
            self._container,
        )

    # ---------------------------------------------------------

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the runtime.
        """

        self._modules.shutdown(
            self._container,
        )

        self._plugins.shutdown_all()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def container(
        self,
    ) -> ServiceContainer:

        return self._container

    # ---------------------------------------------------------

    @property
    def modules(
        self,
    ) -> ModuleRegistry:

        return self._modules

    # ---------------------------------------------------------

    @property
    def discovery(
        self,
    ) -> ModuleDiscovery:

        return self._discovery

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "Bootstrap("
            f"modules={self._modules.module_count})"
        )
