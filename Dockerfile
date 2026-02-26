# LifeGrid API Server
# Runs the FastAPI/uvicorn REST + WebSocket server (headless, no GUI)

FROM python:3.13-slim

# Metadata
LABEL org.opencontainers.image.title="LifeGrid"
LABEL org.opencontainers.image.description="Extensible cellular automaton simulator — REST API server"
LABEL org.opencontainers.image.source="https://github.com/James-HoneyBadger/LifeGrid"
LABEL org.opencontainers.image.licenses="MIT"

# Keeps Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install only the runtime dependencies (no GUI/test/dev extras)
COPY requirements.txt .
RUN pip install --no-cache-dir \
        numpy \
        scipy \
        "fastapi>=0.100.0" \
        "uvicorn[standard]>=0.24.0" \
        "httpx>=0.25.0"

# Copy source
COPY src/ ./src/

# Non-root user for security
RUN useradd --create-home --shell /bin/bash lifegrid
USER lifegrid

EXPOSE 8000

# Run the FastAPI server
CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
