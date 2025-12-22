# Multi-stage build for optimized image size
# Stage 1: Base image with dependencies
FROM pytorch/pytorch:latest AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime image
FROM pytorch/pytorch:latest

WORKDIR /app

# Copy installed packages from base stage
COPY --from=base /opt/conda /opt/conda

# Copy application code
COPY app/ app/
COPY models/ models/
COPY examples/ examples/

# Create output directory
RUN mkdir -p output

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DEVICE=auto

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# Use gunicorn for production with multiple workers
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "300", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
