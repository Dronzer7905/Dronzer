# Dronzer AI Gateway - Extension SDK Guide

Welcome to the Dronzer Extension Platform! This guide will teach you how to write, package, and deploy dynamic extensions to intercept requests, register new AI Providers, or mount UI dashboards without modifying the core gateway codebase.

## Overview
An Extension is a Python package (or single file) that inherits from `ExtensionBase`. Dronzer loads these dynamically at startup and enforces capabilities via a strict OS-level Sandbox.

## Building Your First Extension

1. **Create an entrypoint**: Name your file `entrypoint.py`.
2. **Define the Manifest**:
   ```python
   from dronzer.domain.sdk.extension import ExtensionManifest
   
   manifest = ExtensionManifest(
       id="com.yourdomain.helloworld",
       name="Hello World Logger",
       version="1.0.0",
       author="Your Name",
       description="A sample extension.",
       dronzer_version="^1.0.0",
       allow_network=False,
       allow_filesystem=False
   )
   ```

3. **Subclass ExtensionBase**:
   ```python
   from dronzer.domain.sdk.extension import ExtensionBase, ExtensionContext
   
   class HelloWorldExtension(ExtensionBase):
       async def on_activate(self, context: ExtensionContext) -> None:
           context.api.logger.info("Hello from the custom extension!")
           
       async def on_deactivate(self) -> None:
           pass
   ```

4. **Deploy**: Drop `entrypoint.py` into the `/opt/dronzer/extensions/` directory on your Gateway server. Dronzer will dynamically load it on the next boot.

## Sandboxing

Dronzer takes security seriously. By default, extensions are **denied** access to the network and filesystem. If your extension requires network access (e.g. to reach a custom AI model API), you must set `allow_network=True` in your manifest. The server administrator must explicitly approve these permissions when installing your extension via the Dashboard.

## Interacting with the Gateway
Upon activation, your extension receives an `ExtensionContext`. This context provides safe, isolated facades to core systems:
- `context.api.logger`: Structured logging isolated by your extension ID.
- `context.api.cache`: Distributed Redis cache access isolated by your extension ID.
