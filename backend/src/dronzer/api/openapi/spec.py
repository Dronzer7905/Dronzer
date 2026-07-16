from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """
    Overrides the default FastAPI OpenAPI generation to inject
    OpenAPI 3.1 specific metadata needed for rigorous SDK and CLI generation.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Dronzer Enterprise API",
        version="1.0.0",
        description="""
        Welcome to the official Dronzer Platform API.
        
        This API allows developers to automate AI Workflows, manage Prompts, 
        trigger LLMOps Evaluations, and integrate Dronzer into their CI/CD pipelines.
        """,
        routes=app.routes,
    )

    # 1. OpenAPI 3.1 Specific Overrides
    openapi_schema["openapi"] = "3.1.0"

    # 2. Rich Server Definitions (for SDKs)
    openapi_schema["servers"] = [
        {"url": "https://api.dronzer.io", "description": "Production Cloud"},
        {"url": "https://sandbox.api.dronzer.io", "description": "Sandbox / Testing"},
        {"url": "http://localhost:8000", "description": "Local Development"},
    ]

    # 3. Standardized Error Components
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}

    openapi_schema["components"]["schemas"]["DronzerError"] = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "example": "rate_limit_exceeded"},
            "message": {"type": "string"},
            "request_id": {"type": "string"},
        },
        "required": ["code", "message"],
    }

    # 4. Webhook Definitions
    openapi_schema["webhooks"] = {
        "workflow.completed": {
            "post": {
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/WorkflowResult"}
                        }
                    }
                },
                "responses": {"200": {"description": "Webhook received successfully"}},
            }
        }
    }

    # Add Vendor Extensions for SDK Generator
    openapi_schema["x-sdk-package-name"] = "dronzer"
    openapi_schema["x-sdk-languages"] = ["python", "typescript", "go", "java"]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
