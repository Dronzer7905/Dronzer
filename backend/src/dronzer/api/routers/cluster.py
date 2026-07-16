from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/cluster",
    tags=["Cloud Infrastructure"],
    responses={404: {"description": "Not found"}},
)


class ClusterRegistration(BaseModel):
    name: str
    region: str
    provider: str
    role: str = "SECONDARY"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_cluster(req: ClusterRegistration):
    """
    Registers a newly spun-up Kubernetes cluster into the Global Mesh.
    """
    return {"id": "cluster_gcp_eu", "status": "registered", "role": req.role}


@router.get("/nodes")
async def list_nodes(cluster_id: str = None):
    """
    Lists all active compute nodes and their current CPU/Memory/GPU health.
    """
    return {
        "nodes": [
            {"id": "node_aws_1", "region": "us-east-1", "status": "ACTIVE", "leader": True},
            {"id": "node_aws_2", "region": "us-east-1", "status": "ACTIVE", "leader": False},
            {"id": "node_gcp_1", "region": "eu-west-3", "status": "DRAINING", "leader": False},
        ]
    }


@router.post("/failover/{cluster_id}")
async def trigger_manual_failover(cluster_id: str):
    """
    Manually promotes a SECONDARY cluster to PRIMARY in case of regional outages.
    """
    return {"status": "success", "message": f"Cluster {cluster_id} promoted to PRIMARY."}


@router.post("/dr/snapshot")
async def trigger_snapshot(cluster_id: str):
    """
    Triggers an immediate Disaster Recovery snapshot of the database and vector store.
    """
    return {"snapshot_id": "snap_12345", "status": "uploading_to_s3"}
