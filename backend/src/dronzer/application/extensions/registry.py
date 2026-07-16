import structlog

from dronzer.domain.sdk.extension import ExtensionBase

logger = structlog.get_logger("dronzer.extensions.registry")


class ExtensionRegistry:
    """
    Central repository tracking all loaded and active extensions.
    Manages dependency resolution and semantic versioning constraints.
    """

    def __init__(self):
        # extension_id -> ExtensionBase instance
        self._extensions: dict[str, ExtensionBase] = {}
        # extension_id -> is_active boolean
        self._active_status: dict[str, bool] = {}

    def register(self, extension: ExtensionBase) -> bool:
        """Registers a loaded extension instance into the registry."""
        ext_id = extension.manifest.id
        if ext_id in self._extensions:
            logger.warning(f"Extension {ext_id} is already registered. Overwriting.")

        self._extensions[ext_id] = extension
        self._active_status[ext_id] = False
        logger.info(f"Registered extension {ext_id} (v{extension.manifest.version})")
        return True

    def get_extension(self, extension_id: str) -> ExtensionBase | None:
        return self._extensions.get(extension_id)

    def is_active(self, extension_id: str) -> bool:
        return self._active_status.get(extension_id, False)

    def check_dependencies(self, extension_id: str) -> bool:
        """
        Validates that all required dependencies for an extension are present and active.
        """
        ext = self.get_extension(extension_id)
        if not ext:
            return False

        for dep in ext.manifest.dependencies:
            if dep not in self._extensions:
                logger.error(f"Dependency {dep} missing for extension {extension_id}")
                return False
            if not self.is_active(dep):
                logger.error(f"Dependency {dep} is not active for extension {extension_id}")
                return False

        return True

    def mark_active(self, extension_id: str, status: bool = True):
        """Marks an extension's runtime status."""
        if extension_id in self._extensions:
            self._active_status[extension_id] = status

    def list_extensions(self) -> list[dict]:
        """Returns a serialized list of all installed extensions and their states."""
        return [
            {
                "id": ext.manifest.id,
                "name": ext.manifest.name,
                "version": ext.manifest.version,
                "active": self.is_active(ext.manifest.id),
            }
            for ext in self._extensions.values()
        ]
