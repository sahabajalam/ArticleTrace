# Build stage
FROM python:3.11-slim as builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --no-dev

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/

# Copy parsed data (source JSON used by the load scripts). Vectors live
# in Neo4j as :Entity.embedding properties — not baked into the image.
COPY parsed_data/ ./parsed_data/

# Add venv to path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port (matches PORT default below; Cloud Run overrides via env)
EXPOSE 8001

# Run the application — bind to $PORT if Cloud Run injected one,
# otherwise fall back to the local convention (8001). `exec` keeps
# uvicorn as PID 1 so SIGTERM is delivered cleanly on shutdown.
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
