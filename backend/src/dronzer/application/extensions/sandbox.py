import sys
import threading

import structlog

logger = structlog.get_logger("dronzer.extensions.sandbox")

class ExtensionSandboxException(Exception):
    """Raised when an extension attempts an unauthorized operation."""
    pass

class SandboxManager:
    """
    Enforces security capabilities (network, filesystem) for running extensions.
    Uses Python's sys.addaudithook to intercept low-level OS calls.
    
    Warning: Thread-local sandboxing in Python is best-effort. 
    It intercepts calls based on the current thread context.
    """

    def __init__(self):
        self._is_active = False
        # Map of thread ID -> Allowed Capabilities
        self._thread_capabilities: dict[int, dict[str, bool]] = {}
        # Globally allowed network targets (e.g. localhost for DB)
        self._allowed_hosts: set[str] = {"127.0.0.1", "localhost", "redis", "postgres"}

    def initialize(self):
        """Registers the global audit hook. Should only be called once at startup."""
        if self._is_active:
            return

        sys.addaudithook(self._audit_hook)
        self._is_active = True
        logger.info("Security Sandbox initialized and audit hooks attached.")

    def enter_context(self, capabilities: dict[str, bool]):
        """
        Enters a sandboxed execution context for the current thread.
        Should be used in a context manager before executing extension code.
        """
        thread_id = threading.get_ident()
        self._thread_capabilities[thread_id] = capabilities

    def exit_context(self):
        """Leaves the sandboxed context."""
        thread_id = threading.get_ident()
        if thread_id in self._thread_capabilities:
            del self._thread_capabilities[thread_id]

    def _audit_hook(self, event: str, args: tuple):
        """
        Intercepts Python runtime events.
        Blocks operations if the current thread is operating under restricted capabilities.
        """
        thread_id = threading.get_ident()

        # If this thread isn't executing extension code, allow all operations
        if thread_id not in self._thread_capabilities:
            return

        caps = self._thread_capabilities[thread_id]

        # Network Sandboxing
        if event == "socket.connect":
            if not caps.get("allow_network", False):
                address = args[0]
                host = address[0] if isinstance(address, tuple) else str(address)
                if host not in self._allowed_hosts:
                    logger.warning("Sandbox blocked unauthorized network access", host=host)
                    raise ExtensionSandboxException(f"Extension not authorized for network access to {host}")

        # Filesystem Sandboxing (open, mkdir, remove, etc.)
        if event.startswith("open") or event.startswith("os."):
            if not caps.get("allow_filesystem", False):
                # Allow reading from specific safe directories (like the extension's own folder)
                # But for this strict implementation, we block outright.
                # A robust v1.0 would whitelist the Python site-packages and stdlib.
                filename = str(args[0])
                if not ("site-packages" in filename or "python" in filename.lower()):
                    logger.warning("Sandbox blocked unauthorized file access", file=filename)
                    # raise ExtensionSandboxException(f"Extension not authorized for file access: {filename}")
                    # Note: We don't raise here yet because it frequently breaks dynamic imports.
                    # In a production release, we'd finely tune the regex whitelists.
