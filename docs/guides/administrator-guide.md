# Dronzer AI Gateway - Administrator Guide

Welcome to the Dronzer Administrator Guide! This document covers the operational management of the Dronzer Gateway, including deployment, scaling, and observability.

## Deployment Options

Dronzer is packaged as a set of Docker containers. We support two primary deployment topologies:

### 1. Docker Compose (Single Node)
For small to medium workloads, you can deploy Dronzer on a single virtual machine using Docker Compose.
```bash
git clone https://github.com/dronzer/gateway.git
cd gateway
docker-compose -f docker-compose.prod.yml up -d
```
This will spin up the PostgreSQL database, Redis cache, Python API Gateway, Next.js Dashboard, and the Prometheus observability stack.

### 2. Kubernetes Helm Chart (High Availability)
For enterprise workloads requiring auto-scaling and zero-downtime deployments, deploy Dronzer via our official Helm Chart.
```bash
helm install my-dronzer-gateway ./helm/dronzer -f ./helm/dronzer/values.yaml
```

## Admin Dashboard

The primary way to administer the gateway is via the **Enterprise Dashboard**.
Navigate to `https://dashboard.yourdomain.com` (or `http://localhost:3000` locally).

From the dashboard, you can:
- **Manage API Keys**: Issue secure API keys to your developers and set strict budget and token quotas per key.
- **Configure Routing Policies**: Set up failover rules. For example, "If OpenAI fails, automatically route to Anthropic".
- **Monitor Costs**: View live dashboards of token consumption and estimated USD spend across all configured AI providers.

## System Observability

Dronzer exports highly detailed Prometheus metrics on port `8000` at the `/metrics` endpoint. 
If you deployed using the `docker-compose.prod.yml` stack, you can access the pre-configured **Grafana** dashboard on port `3001` to view live traffic, latency percentiles, and error rates.
