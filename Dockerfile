# Stage 1: Build Frontend (Next.js)
FROM node:22-alpine AS frontend-builder
RUN apk add --no-cache libc6-compat
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
# Inject relative paths at build time
ENV NEXT_PUBLIC_API_BASE_URL=""
ENV NEXT_PUBLIC_ADMIN_API_URL="/admin"
ENV NEXT_PUBLIC_GATEWAY_API_URL="/v1"
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 2: Build Backend (FastAPI)
FROM python:3.12-slim-bookworm AS backend-builder
WORKDIR /app/backend
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY backend/pyproject.toml backend/README.md ./
COPY backend/src ./src
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install .

# Stage 3: Monolith Production Runner
FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# Install Node.js, Caddy, Supervisor, and runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl debian-keyring debian-archive-keyring apt-transport-https \
    supervisor libpq5 \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python Environment and Source
COPY --from=backend-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY backend/ /app/backend/

# Copy Next.js Standalone
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/.next/standalone /app/frontend/
COPY --from=frontend-builder /app/frontend/.next/static /app/frontend/.next/static

# Configuration Files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY Caddyfile /app/Caddyfile

# Create Unprivileged User
RUN groupadd -r dronzer && useradd -r -g dronzer dronzer
RUN chown -R dronzer:dronzer /app

# Configure permissions for Caddy and Supervisor
ENV XDG_CONFIG_HOME=/app/.config
ENV XDG_DATA_HOME=/app/.data
RUN mkdir -p /app/.config/caddy /app/.data/caddy && chown -R dronzer:dronzer /app/.config /app/.data
RUN mkdir -p /var/log/supervisor && chown -R dronzer:dronzer /var/log/supervisor /run

USER dronzer

EXPOSE 8080
ENV PORT=8080

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
