# Dronzer v2.0 Upgrade Guide (Infrastructure)

This guide is for DevOps and Platform Engineers upgrading self-hosted Dronzer clusters to v2.0.

## Prerequisites
- **Postgres**: Version 15 or higher.
- **Redis**: Version 7 or higher.
- **Kubernetes** (Optional): Version 1.28+ if using the Helm charts.

## Step 1: Backup Existing Data
Before upgrading, take a full pg_dump of your v1.x database:
```bash
pg_dump -U dronzer dronzer_db > backup_v1.sql
```

## Step 2: Apply Database Migrations
Dronzer v2.0 introduces breaking schema changes for the RBAC and PromptOps domains.
1. Scale down your Dronzer Gateway pods to 0.
2. Run the migration job:
   ```bash
   # Using Docker
   docker run --rm --env-file .env dronzer/api:v2.0.0 alembic upgrade head
   ```

## Step 3: Update Environment Variables
Several environment variables have changed in v2.0:
- `JWT_SECRET` is now `DRONZER_JWT_SECRET`.
- `REDIS_URL` is now explicitly required for the Rate Limiter.
- Added `DRONZER_CLUSTER_ID` for Multi-Cluster Discovery.

## Step 4: Deploy v2.0 Images
Update your Docker Compose or Helm configurations to pull the `v2.0.0` tags.
```yaml
image: dronzer/gateway:v2.0.0
```
Scale your pods back up and monitor the `/health/readiness` endpoints.
