# Dronzer Community Onboarding Guide

Welcome to the Dronzer Core Team! We are thrilled to have you contribute to the Universal AI Integration Platform.

## 1. Local Environment Setup
The easiest way to get started is using the Local Dev Toolkit:
```bash
cd tools/docker
docker-compose -f docker-compose.dev.yml up -d
```
This spins up Postgres, Redis, and the Dronzer Gateway API on `http://localhost:8000`.

## 2. Running the Test Suite
We require 100% passing tests for any PR.
```bash
cd backend
pytest tests/
```

## 3. Submitting a Pull Request
- Create a branch: `git checkout -b feature/my-awesome-feature`
- Ensure your code passes all linters (`ruff`, `mypy`).
- Submit the PR using our GitHub Pull Request Template. A Core Maintainer will review it within 48 hours.
