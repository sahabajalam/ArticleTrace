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

# Install git — required at runtime for code_analyzer.ingest, which
# uses GitPython to `git clone --depth=1` scanned repos. GitPython
# also runs an import-time check that exit(1)s if git is missing.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY data/golden/ ./data/golden/

# Add venv to path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port (matches PORT default below; Cloud Run overrides via env)
EXPOSE 8004

# Run the application — bind to $PORT if Cloud Run injected one,
# otherwise fall back to the local convention (8004). `exec` keeps
# uvicorn as PID 1 so SIGTERM is delivered cleanly on shutdown.
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8004}"]
