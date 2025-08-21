# Docker Deployment Guide - Meraki MCP SSE Server

## Quick Start

1. **Clone the repository** (if not already done):
```bash
git clone https://github.com/skycomm/meraki-mcp.git
cd meraki-mcp/python_sse
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your Meraki API key
nano .env
```

3. **Build and run with Docker Compose**:
```bash
# Basic deployment
docker-compose up -d

# Or build fresh
docker-compose up --build -d
```

4. **Verify deployment**:
```bash
# Check if container is running
docker ps

# Check logs
docker-compose logs -f meraki-mcp-sse

# Test health endpoint
curl http://localhost:8000/health
```

## Deployment Options

### 1. Basic Deployment
```bash
docker-compose up -d
```
- Runs the SSE server on port 8000
- Uses environment variables from .env file
- Includes health checks and auto-restart

### 2. With SSL/TLS (Nginx)
```bash
# Add SSL certificates to nginx/certs/
mkdir -p nginx/certs
cp /path/to/cert.pem nginx/certs/
cp /path/to/key.pem nginx/certs/

# Run with SSL profile
docker-compose --profile with-ssl up -d
```

### 3. With Traefik (Auto SSL)
```bash
# Run with Traefik for automatic SSL via Let's Encrypt
docker-compose --profile with-traefik up -d
```

### 4. With OpenWebUI Integration
```bash
# Run with mcpo proxy for OpenWebUI
docker-compose --profile openwebui up -d
```

### 5. With Monitoring Stack
```bash
# Run with Prometheus and Grafana
docker-compose --profile monitoring up -d
```

### 6. With Everything
```bash
# Run all optional services
docker-compose \
  --profile with-ssl \
  --profile with-cache \
  --profile with-db \
  --profile monitoring \
  up -d
```

## Docker Commands

### Build the image
```bash
# Build with default settings
docker build -t meraki-mcp-sse:latest .

# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.12 -t meraki-mcp-sse:3.12 .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t meraki-mcp-sse:latest .
```

### Run standalone container
```bash
# Run with environment file
docker run -d \
  --name meraki-mcp-sse \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  meraki-mcp-sse:latest

# Run with inline environment variables
docker run -d \
  --name meraki-mcp-sse \
  -p 8000:8000 \
  -e MERAKI_API_KEY=your-api-key \
  -e PRIVILEGED_USERS=admin@example.com \
  --restart unless-stopped \
  meraki-mcp-sse:latest
```

### Container Management
```bash
# View logs
docker logs -f meraki-mcp-sse

# Access container shell
docker exec -it meraki-mcp-sse /bin/bash

# Stop container
docker stop meraki-mcp-sse

# Remove container
docker rm meraki-mcp-sse

# Clean up everything
docker-compose down -v
```

## Production Deployment

### 1. Security Hardening
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  meraki-mcp-sse:
    image: meraki-mcp-sse:latest
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 2. Using Docker Secrets
```bash
# Create secrets
echo "your-api-key" | docker secret create meraki_api_key -
echo "your-secret" | docker secret create auth_secret -

# Use in docker-compose
version: '3.8'
services:
  meraki-mcp-sse:
    secrets:
      - meraki_api_key
      - auth_secret
    environment:
      - MERAKI_API_KEY_FILE=/run/secrets/meraki_api_key
      - AUTH_SECRET_FILE=/run/secrets/auth_secret

secrets:
  meraki_api_key:
    external: true
  auth_secret:
    external: true
```

### 3. Kubernetes Deployment
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meraki-mcp-sse
spec:
  replicas: 3
  selector:
    matchLabels:
      app: meraki-mcp-sse
  template:
    metadata:
      labels:
        app: meraki-mcp-sse
    spec:
      containers:
      - name: meraki-mcp-sse
        image: meraki-mcp-sse:latest
        ports:
        - containerPort: 8000
        env:
        - name: MERAKI_API_KEY
          valueFrom:
            secretKeyRef:
              name: meraki-secrets
              key: api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          limits:
            memory: "1Gi"
            cpu: "1000m"
          requests:
            memory: "256Mi"
            cpu: "250m"
```

## Environment Variables

### Required
- `MERAKI_API_KEY`: Your Meraki Dashboard API key

### Optional
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `PRIVILEGED_USERS`: Comma-separated list of admin users
- `RATE_LIMIT_REQUESTS`: Max requests per window (default: 100)
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 60)
- `LOG_LEVEL`: Logging level (default: INFO)
- `CORS_ENABLED`: Enable CORS (default: true)
- `CORS_ORIGINS`: Allowed origins (default: *)

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics (with Prometheus)
```bash
curl http://localhost:8000/metrics
```

### Logs
```bash
# JSON formatted logs
docker-compose logs --tail=100 -f meraki-mcp-sse | jq '.'

# Filter by level
docker-compose logs meraki-mcp-sse | grep ERROR
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs meraki-mcp-sse

# Check configuration
docker-compose config

# Validate environment
docker-compose run --rm meraki-mcp-sse env
```

### Connection refused
```bash
# Check if port is exposed
docker port meraki-mcp-sse

# Check firewall
sudo ufw status

# Test from inside container
docker exec meraki-mcp-sse curl http://localhost:8000/health
```

### Permission denied
```bash
# Fix volume permissions
sudo chown -R 1000:1000 ./logs

# Or run as root (not recommended)
docker-compose run --user root meraki-mcp-sse
```

### Out of memory
```bash
# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

## Performance Tuning

### 1. Use Redis for caching
```bash
docker-compose --profile with-cache up -d
```

### 2. Scale horizontally
```bash
docker-compose up -d --scale meraki-mcp-sse=3
```

### 3. Use production WSGI server
```dockerfile
# In Dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "start_server:app"]
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Docker Build and Push

on:
  push:
    branches: [main, sse]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: ./python_sse
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/meraki-mcp-sse:latest
          ${{ secrets.DOCKER_USERNAME }}/meraki-mcp-sse:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## Security Best Practices

1. **Never commit .env files** with real API keys
2. **Use secrets management** (Docker secrets, Kubernetes secrets, Vault)
3. **Run as non-root user** (already configured)
4. **Enable TLS/SSL** in production
5. **Set resource limits** to prevent DoS
6. **Use read-only filesystem** where possible
7. **Regularly update base images**
8. **Scan images for vulnerabilities**:
```bash
docker scan meraki-mcp-sse:latest
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/skycomm/meraki-mcp/issues
- Documentation: https://github.com/skycomm/meraki-mcp/wiki