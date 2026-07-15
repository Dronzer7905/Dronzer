import importlib.util
import sys
from pathlib import Path

import structlog

from dronzer.application.extensions.registry import ExtensionRegistry
from dronzer.application.extensions.sandbox import SandboxManager
from dronzer.domain.sdk.extension import ExtensionBase

logger = structlog.get_logger("dronzer.extensions.loader")

class ExtensionLoader:
    """
    Dynamically loads Python modules from the filesystem into the Extension Registry.
    Supports unpacking single Python files or full packages containing an `entrypoint.py`.
    """
    def __init__(self, registry: ExtensionRegistry, sandbox: SandboxManager, extensions_dir: str = "/opt/dronzer/extensions"):
        self.registry = registry
        self.sandbox = sandbox
        self.extensions_dir = Path(extensions_dir)

    def load_all(self):
        """Scans the extensions directory and loads discovered plugins."""
        if not self.extensions_dir.exists():
            logger.info("Extensions directory does not exist. Skipping.", path=str(self.extensions_dir))
            return

        for item in self.extensions_dir.iterdir():
            if item.is_dir() and (item / "entrypoint.py").exists():
                self.load_from_path(item / "entrypoint.py")
            elif item.is_file() and item.suffix == ".py":
                self.load_from_path(item)

    def load_from_path(self, file_path: Path) -> bool:
        """
        Dynamically imports a Python file and searches for a class inheriting from ExtensionBase.
        """
        module_name = f"dronzer_ext_{file_path.stem}"
        try:
            # 1. Dynamically import the module
            spec = importlib.util.spec_from_file_location(module_name, str(file_path))
            if spec is None or spec.loader is None:
                logger.error("Failed to create module spec", path=str(file_path))
                return False

            module = importlib.util.module_from_spec(spec)
            # Add to sys.modules so the extension can perform relative imports if it's a package
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # 2. Find the ExtensionBase subclass
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, ExtensionBase) and attr is not ExtensionBase:
                    # 3. Instantiate and register
                    logger.info("Found valid Extension Class", class_name=attr_name)

                    # For safety in v1.0, we expect the extension class to instantiate itself
                    # or provide a `create_extension()` factory. If not, we attempt to init it
                    # with a default manifest (which would usually be loaded from a plugin.json).

                    # NOTE: A robust implementation would read `manifest.json` from the directory first.
                    if hasattr(module, "manifest"):
                        ext_instance = attr(manifest=module.manifest)
                        self.registry.register(ext_instance)
                        return True
                    else:
                        logger.warning("Extension missing `manifest` variable in module", module=module_name)

            logger.warning("No ExtensionBase subclass found in module", module=module_name)
            return False

        except Exception as e:
            logger.exception("Failed to load extension module", path=str(file_path), error=str(e))
            return False
