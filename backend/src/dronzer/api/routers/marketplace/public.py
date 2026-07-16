from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/marketplace",
    tags=["Marketplace Public"],
)


@router.get("/search")
async def search_packages(q: str = "", category: str = None):
    """
    Public search endpoint for discovering AI Plugins, Prompts, and Connectors.
    """
    return {
        "results": [
            {
                "name": "@google/gemini-pro",
                "type": "PROVIDER",
                "version": "2.0.1",
                "rating": 4.9,
                "verified": True,
            },
            {
                "name": "@community/github-tools",
                "type": "PLUGIN",
                "version": "1.1.0",
                "rating": 4.2,
                "verified": False,
            },
        ]
    }


@router.get("/packages/{namespace}/{package_name}")
async def get_package_details(namespace: str, package_name: str):
    """
    Fetches detailed metadata, README, and version history for a specific package.
    """
    return {
        "id": f"{namespace}/{package_name}",
        "description": "Integration tools for GitHub repositories.",
        "latest_version": "1.1.0",
        "dependencies": {"@core/http": ">=1.0.0"},
        "capabilities": ["network_access"],
    }


class InstallRequest(BaseModel):
    package_id: str
    version: str = "latest"


@router.post("/install", status_code=status.HTTP_202_ACCEPTED)
async def install_package(req: InstallRequest):
    """
    Initiates an asynchronous installation of a package into the Dronzer Environment.
    Triggers the Dependency Resolver (DAG) and Sandbox capabilities check.
    """
    return {"status": "installing", "job_id": "job_install_123"}
