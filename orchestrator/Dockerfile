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

# Copy application code. src/ carries the YAML rule corpus at
# src/code_analyzer/rules/ — the image is unusable without it (DL-035).
#
# There was a `COPY data/golden/` here until 2026-08-31. That directory was
# removed in an earlier restructure and is gitignored; the golden tests live in
# knowledge_engine/golden_tests/ and run from the CI checkout, never from this
# image. The stale line broke every orchestrator build after the removal, which
# is why the deployed image sat at 2026-04-29 for four months.
COPY src/ ./src/

# Add venv to path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port (matches PORT default below; Cloud Run overrides via env)
EXPOSE 8004

# Run the application — bind to $PORT if Cloud Run injected one,
# otherwise fall back to the local convention (8004). `exec` keeps
# uvicorn as PID 1 so SIGTERM is delivered cleanly on shutdown.
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8004}"]
