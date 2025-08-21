# Multi-stage build for optimized image size and security
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 -s /bin/bash meraki

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/meraki/.local/bin:$PATH \
    HOST=0.0.0.0 \
    PORT=8000

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder --chown=meraki:meraki /root/.local /home/meraki/.local

# Copy application code
COPY --chown=meraki:meraki src/ ./src/
COPY --chown=meraki:meraki start_server.py .

# Switch to non-root user for security
USER meraki

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose the port
EXPOSE ${PORT}

# Labels for metadata
LABEL maintainer="Meraki MCP Team" \
      version="1.0.0" \
      description="Cisco Meraki MCP SSE/HTTP Server"

# Run the server
CMD ["python", "start_server.py"]