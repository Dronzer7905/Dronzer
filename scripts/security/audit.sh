#!/bin/bash
set -eo pipefail

echo "============================================="
echo " Dronzer Security Audit & Vulnerability Scan "
echo "============================================="

# 1. Backend Dependency Audit
echo -e "\n---> Running Python Dependency Audit (backend)..."
if command -v pip-audit &> /dev/null; then
    cd /opt/dronzer/backend && pip-audit -r requirements.txt
else
    echo "pip-audit not installed. Skipping..."
fi

# 2. Frontend Dependency Audit
echo -e "\n---> Running Node.js Dependency Audit (frontend)..."
if command -v npm &> /dev/null; then
    cd /opt/dronzer/frontend && npm audit --audit-level=high
else
    echo "npm not installed. Skipping..."
fi

# 3. Docker Container Scan using Trivy
echo -e "\n---> Running Trivy Container Scan (ghcr.io/dronzer-api)..."
if command -v trivy &> /dev/null; then
    trivy image --severity HIGH,CRITICAL ghcr.io/dronzer/dronzer-api:latest
    trivy image --severity HIGH,CRITICAL ghcr.io/dronzer/dronzer-dashboard:latest
else
    echo "Trivy not installed. Skipping container scan..."
fi

echo -e "\n[SUCCESS] Security Audit Completed."
