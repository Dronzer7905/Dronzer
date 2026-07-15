#!/bin/bash
set -eo pipefail

# Dronzer Disaster Recovery: Automated Backup Script
# Creates a snapshot of the PostgreSQL database and Redis config/cache

BACKUP_DIR="/opt/dronzer/backups/$(date +%Y-%m-%d_%H-%M-%S)"
mkdir -p "$BACKUP_DIR"

echo "Starting Dronzer Enterprise Backup to $BACKUP_DIR..."

# 1. PostgreSQL Database Dump
echo "Backing up PostgreSQL database..."
docker exec -t dronzer-postgres pg_dumpall -c -U dronzer > "$BACKUP_DIR/pg_dump.sql"
echo "Database backed up successfully."

# 2. Redis RDB Backup
echo "Backing up Redis cache..."
docker exec -t dronzer-redis redis-cli SAVE
docker cp dronzer-redis:/data/dump.rdb "$BACKUP_DIR/redis_dump.rdb"
echo "Redis backed up successfully."

# 3. Zip and compress
echo "Compressing backups..."
tar -czvf "$BACKUP_DIR.tar.gz" -C "/opt/dronzer/backups" "$(basename $BACKUP_DIR)"
rm -rf "$BACKUP_DIR"

echo "Backup complete: $BACKUP_DIR.tar.gz"
