# Requires: pip install kopf kubernetes
import kopf
import structlog

logger = structlog.get_logger("dronzer.k8s.operator")


@kopf.on.create("dronzer.ai", "v1", "dronzerclusters")
def create_fn(spec, name, namespace, logger, **kwargs):
    """
    Called when a new `DronzerCluster` Custom Resource is deployed to the K8s cluster.
    Spins up the necessary Deployments, Services, and Horizontal Pod Autoscalers.
    """
    logger.info(f"Creating DronzerCluster: {name} in {namespace}")

    # Example logic to create the Deployment
    replicas = spec.get("replicas", 3)
    version = spec.get("version", "latest")

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": f"{name}-deployment", "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {
                            "name": "dronzer-gateway",
                            "image": f"dronzer/gateway:{version}",
                            "ports": [{"containerPort": 8000}],
                        }
                    ]
                },
            },
        },
    }

    # In a real environment, we'd inject this via the kubernetes python client:
    # api = client.AppsV1Api()
    # obj = api.create_namespaced_deployment(namespace=namespace, body=deployment)

    return {"deployment_name": deployment["metadata"]["name"]}


@kopf.on.update("dronzer.ai", "v1", "dronzerclusters")
def update_fn(spec, name, namespace, logger, **kwargs):
    """
    Handles rolling upgrades when the CRD version or replica count changes.
    """
    logger.info(f"Updating DronzerCluster: {name}")
    # Patch deployment with new spec...
    pass


@kopf.on.delete("dronzer.ai", "v1", "dronzerclusters")
def delete_fn(name, namespace, logger, **kwargs):
    """
    Cleans up resources when the cluster is destroyed.
    """
    logger.warning(f"Deleting DronzerCluster: {name}")
    pass
