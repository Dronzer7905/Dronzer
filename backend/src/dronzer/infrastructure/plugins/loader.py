import importlib
import pkgutil

import structlog

from dronzer.application.registry.provider import ProviderRegistry
from dronzer.domain.sdk.plugin import IPlugin

logger = structlog.get_logger("dronzer.plugins.loader")


class PluginLoader:
    """
    Discovers, loads, and initializes external Python plugins dynamically.
    """

    def __init__(self, provider_registry: ProviderRegistry, plugin_dir_module: str = "dronzer.infrastructure.plugins"):
        self.provider_registry = provider_registry
        self.plugin_dir_module = plugin_dir_module
        self._loaded_plugins: dict[str, IPlugin] = {}

    async def discover_and_load(self) -> None:
        """Scans the plugin directory and loads all valid plugins."""
        try:
            module = importlib.import_module(self.plugin_dir_module)
            for _, name, is_pkg in pkgutil.iter_modules(module.__path__):
                if is_pkg:
                    await self._load_plugin(f"{self.plugin_dir_module}.{name}")
        except ModuleNotFoundError:
            logger.warning("Plugin directory not found. Skipping dynamic load.")

    async def _load_plugin(self, module_name: str) -> None:
        """Dynamically imports a module and calls its register() factory."""
        try:
            plugin_module = importlib.import_module(module_name)
            if hasattr(plugin_module, "register_plugin"):
                plugin: IPlugin = plugin_module.register_plugin()

                # Execute startup hook
                await plugin.on_startup()

                # Register all providers this plugin ships
                for provider in plugin.get_providers():
                    self.provider_registry.register(provider)

                self._loaded_plugins[plugin.metadata.name] = plugin
                logger.info("Plugin loaded successfully", plugin=plugin.metadata.name, version=plugin.metadata.version)
            else:
                logger.debug("Module has no register_plugin hook", module=module_name)
        except Exception as e:
            logger.error("Failed to load plugin", module=module_name, exc_info=e)

    async def unload_all(self) -> None:
        """Triggers shutdown hooks for all loaded plugins."""
        for name, plugin in self._loaded_plugins.items():
            try:
                await plugin.on_shutdown()
                # We would also remove its providers from the registry here
            except Exception as e:
                logger.error("Error shutting down plugin", plugin=name, exc_info=e)
        self._loaded_plugins.clear()
