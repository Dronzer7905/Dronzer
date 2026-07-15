from dronzer.domain.sdk.extension import ExtensionBase, ExtensionManifest, ExtensionContext

# Define the Extension Manifest
manifest = ExtensionManifest(
    id="com.example.audit-logger",
    name="Sample Audit Logger Extension",
    version="1.0.0",
    author="Dronzer Team",
    description="A sample extension that logs activation and uses the Cache API.",
    dronzer_version="^1.0.0",
    allow_network=False,
    allow_filesystem=False
)

class AuditLoggerExtension(ExtensionBase):
    """
    A simple example demonstrating the Extension Lifecycle and SDK API access.
    """
    async def on_activate(self, context: ExtensionContext) -> None:
        context.api.logger.info("AuditLoggerExtension has been ACTIVATED!")
        
        # Safely access the isolated Redis cache namespace for this extension
        await context.api.cache.set("activation_time", "2026-07-09T00:00:00Z")
        val = await context.api.cache.get("activation_time")
        
        context.api.logger.debug(f"Successfully wrote and read from Cache: {val}")

    async def on_deactivate(self) -> None:
        print("AuditLoggerExtension DEACTIVATED. Cleaning up...")
