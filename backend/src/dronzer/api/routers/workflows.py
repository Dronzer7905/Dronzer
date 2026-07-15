from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/workflows",
    tags=["Workflows & Agents"],
    responses={404: {"description": "Not found"}},
)

class WorkflowDeployRequest(BaseModel):
    name: str
    description: str = ""
    definition: dict[str, Any] # The raw JSON DAG graph

class WorkflowTriggerRequest(BaseModel):
    template_id: str
    input_payload: dict[str, Any]

@router.post("/deploy", status_code=status.HTTP_201_CREATED)
async def deploy_workflow(req: WorkflowDeployRequest):
    """
    Saves a new Workflow DAG definition into the database.
    """
    # Logic to validate DAG and insert into `workflow_templates` table
    return {"id": "wf_tpl_001", "name": req.name, "status": "deployed"}

@router.post("/execute", status_code=status.HTTP_202_ACCEPTED)
async def execute_workflow(req: WorkflowTriggerRequest):
    """
    Triggers a workflow. Generates a new `WorkflowExecution` record
    and enqueues it to the Background Task Engine (Celery/Redis).
    """
    execution_id = "exec_abc123"
    # 1. Create DB record for Execution
    # 2. Enqueue background task
    return {"execution_id": execution_id, "status": "PENDING"}

@router.post("/executions/{execution_id}/resume")
async def resume_workflow(execution_id: str, action: str = "approve"):
    """
    Resumes a workflow that was paused by a Human-In-The-Loop Approval Node.
    """
    # Updates the Execution state and re-queues it into the background worker pool
    return {"execution_id": execution_id, "status": "RESUMED", "action": action}

@router.get("/agents")
async def list_agents():
    """
    Returns available AI Agents configured for the organization.
    """
    return {
        "agents": [
            {"id": "agent_01", "name": "Senior Python Engineer", "role": "Developer"}
        ]
    }
