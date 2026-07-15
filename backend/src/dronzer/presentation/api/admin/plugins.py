from typing import Any

import structlog
from fastapi import APIRouter, HTTPException, Request

logger = structlog.get_logger("dronzer.api.admin.plugins")
router = APIRouter(prefix="/plugins", tags=["Admin Plugins"])

@router.get("")
async def list_plugins(request: Request) -> list[dict[str, Any]]:
    """
    Lists all dynamically loaded plugins.
    """
    # Assuming loader is on state
    loader = getattr(request.app.state, "plugin_loader", None)
    if not loader:
        return []

    results = []
    for name, plugin in loader._loaded_plugins.items():
        meta = plugin.metadata
        results.append({
            "name": meta.name,
            "version": meta.version,
            "author": meta.author,
            "description": meta.description
        })
    return results

@router.post("/reload")
async def reload_plugins(request: Request):
    """
    Hot-reloads the plugin directory.
    """
    loader = getattr(request.app.state, "plugin_loader", None)
    if not loader:
        raise HTTPException(status_code=500, detail="Plugin loader not initialized")

    logger.info("Admin initiated plugin hot-reload")
    await loader.unload_all()
    await loader.discover_and_load()
    return {"status": "success", "message": "Plugins reloaded successfully"}
