# --- Stage 1: Base & Dependencies ---
FROM python:3.12-slim-bookworm AS builder
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml README.md ./
COPY ./src ./src

# Install to a virtualenv for isolation
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install .

# --- Stage 2: Production ---
FROM python:3.12-slim-bookworm AS production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Create unprivileged user for security
RUN groupadd -r dronzer && useradd -r -g dronzer dronzer

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy source code
COPY ./src ./src
COPY pyproject.toml README.md ./

# Ensure dronzer user owns the code
RUN chown -R dronzer:dronzer /app

USER dronzer

EXPOSE 8000

CMD ["uvicorn", "dronzer.presentation.api.server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
