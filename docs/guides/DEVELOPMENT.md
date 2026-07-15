# Development Guide

Welcome to the Dronzer development guide!

## Setup
1. `cd backend && pip install -e ".[dev]"`
2. `cd frontend && npm install`
3. Run `docker-compose up -d` to start Redis and PostgreSQL.

## Quality Gates
Always run `ruff check .` and `mypy .` before committing.
