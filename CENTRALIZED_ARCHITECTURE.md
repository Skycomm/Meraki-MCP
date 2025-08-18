# Centralized Meraki MCP Server Architecture

## Overview

This document outlines a hybrid architecture that enables multiple clients and n8n to use the Meraki MCP server centrally while maintaining security and isolation.

## Architecture Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Claude/AI     │     │      n8n        │     │   REST API      │
│   Assistants    │     │   Workflows     │     │   Clients       │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                         │
         │ MCP-over-HTTP         │ REST API               │ REST API
         │                       │                         │
┌────────▼───────────────────────▼─────────────────────────▼────────┐
│                         API Gateway (Traefik)                      │
│                    - Authentication & Rate Limiting                │
│                    - Request Routing                               │
│                    - SSL Termination                               │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌────────▼────────┐     ┌────────▼────────┐    ┌────────▼────────┐
│  MCP-HTTP       │     │   REST API      │    │  WebSocket      │
│  Adapter        │     │   Service       │    │  Service        │
│  (Port 8001)    │     │  (Port 8002)    │    │  (Port 8003)    │
└────────┬────────┘     └────────┬────────┘    └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                      ┌──────────▼──────────┐
                      │   Shared Backend    │
                      │   - Meraki Client   │
                      │   - Tool Logic      │
                      │   - Rate Limiting   │
                      └─────────────────────┘
```

## Implementation Plan

### 1. Core Services

#### A. REST API Service (for n8n and simple integrations)
```python
# rest_api_service.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import asyncio
from typing import Optional

app = FastAPI(title="Meraki MCP REST API")

class MerakiRequest(BaseModel):
    tool: str
    params: dict
    api_key: Optional[str] = None

@app.post("/api/v1/execute")
async def execute_tool(
    request: MerakiRequest,
    x_api_key: Optional[str] = Header(None)
):
    # Use provided API key or header
    api_key = request.api_key or x_api_key
    if not api_key:
        raise HTTPException(401, "API key required")
    
    # Initialize client with request-specific API key
    client = MerakiClient(api_key)
    
    # Execute tool
    tool_func = TOOL_REGISTRY.get(request.tool)
    if not tool_func:
        raise HTTPException(404, f"Tool {request.tool} not found")
    
    try:
        result = await tool_func(client, **request.params)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Tool-specific endpoints for n8n
@app.get("/api/v1/organizations")
async def list_organizations(x_api_key: str = Header()):
    client = MerakiClient(x_api_key)
    return await client.get_organizations()

@app.get("/api/v1/organizations/{org_id}/networks")
async def get_networks(org_id: str, x_api_key: str = Header()):
    client = MerakiClient(x_api_key)
    return await client.get_organization_networks(org_id)
```

#### B. MCP-over-HTTP Adapter (for AI assistants)
```python
# mcp_http_adapter.py
from fastapi import FastAPI, WebSocket
import json
import asyncio

app = FastAPI(title="MCP HTTP Adapter")

@app.websocket("/mcp")
async def mcp_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Get API key from initial auth message
    auth_msg = await websocket.receive_json()
    api_key = auth_msg.get("api_key")
    
    # Create dedicated MCP server instance
    mcp_instance = create_mcp_server(api_key)
    
    # Bridge WebSocket to MCP stdio
    async def handle_messages():
        while True:
            msg = await websocket.receive_json()
            response = await mcp_instance.handle_message(msg)
            await websocket.send_json(response)
    
    await handle_messages()
```

### 2. Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./traefik.yml:/etc/traefik/traefik.yml
      - ./letsencrypt:/letsencrypt
      - /var/run/docker.sock:/var/run/docker.sock
    labels:
      - "traefik.enable=true"

  rest-api:
    build:
      context: .
      dockerfile: Dockerfile.rest
    environment:
      - REDIS_URL=redis://redis:6379
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.rest-api.rule=Host(`api.meraki-mcp.yourdomain.com`)"
      - "traefik.http.routers.rest-api.tls=true"
      - "traefik.http.services.rest-api.loadbalancer.server.port=8002"
    depends_on:
      - redis

  mcp-adapter:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    environment:
      - REDIS_URL=redis://redis:6379
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.mcp.rule=Host(`mcp.meraki-mcp.yourdomain.com`)"
      - "traefik.http.routers.mcp.tls=true"
      - "traefik.http.services.mcp.loadbalancer.server.port=8001"
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

### 3. n8n Integration

#### A. Custom n8n Node
```typescript
// n8n-nodes-meraki-mcp/nodes/MerakiMcp/MerakiMcp.node.ts
import { INodeType, INodeTypeDescription } from 'n8n-workflow';

export class MerakiMcp implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Meraki MCP',
        name: 'merakiMcp',
        group: ['transform'],
        version: 1,
        description: 'Access Meraki via MCP Server',
        defaults: {
            name: 'Meraki MCP',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'merakiMcpApi',
                required: true,
            },
        ],
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                options: [
                    {
                        name: 'List Organizations',
                        value: 'listOrganizations',
                    },
                    {
                        name: 'Get Networks',
                        value: 'getNetworks',
                    },
                    {
                        name: 'Get Devices',
                        value: 'getDevices',
                    },
                    {
                        name: 'Reboot Device',
                        value: 'rebootDevice',
                    },
                ],
                default: 'listOrganizations',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const operation = this.getNodeParameter('operation', 0) as string;
        const credentials = await this.getCredentials('merakiMcpApi');
        
        const response = await this.helpers.request({
            method: 'POST',
            uri: `${credentials.baseUrl}/api/v1/execute`,
            headers: {
                'X-API-Key': credentials.apiKey,
            },
            body: {
                tool: operation,
                params: this.getNodeParameter('params', 0, {}),
            },
            json: true,
        });

        return [this.helpers.returnJsonArray(response)];
    }
}
```

### 4. Security & Multi-tenancy

#### A. API Key Management
```python
# auth_middleware.py
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import hashlib
import redis

api_key_header = APIKeyHeader(name="X-API-Key")
redis_client = redis.Redis()

class AuthManager:
    @staticmethod
    async def validate_api_key(api_key: str = Security(api_key_header)):
        # Hash API key for storage
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Check rate limits
        rate_key = f"rate:{key_hash}"
        current = redis_client.incr(rate_key)
        if current == 1:
            redis_client.expire(rate_key, 60)  # 1 minute window
        
        if current > 100:  # 100 requests per minute
            raise HTTPException(429, "Rate limit exceeded")
        
        # Validate key exists and is active
        key_data = redis_client.hgetall(f"apikey:{key_hash}")
        if not key_data or key_data.get(b'active') != b'1':
            raise HTTPException(401, "Invalid API key")
        
        return {
            'key_hash': key_hash,
            'meraki_key': key_data.get(b'meraki_key').decode(),
            'tenant_id': key_data.get(b'tenant_id').decode()
        }
```

#### B. Tenant Isolation
```python
# tenant_manager.py
class TenantManager:
    @staticmethod
    async def get_tenant_context(auth_info: dict):
        return {
            'tenant_id': auth_info['tenant_id'],
            'meraki_api_key': auth_info['meraki_key'],
            'allowed_orgs': await get_allowed_orgs(auth_info['tenant_id']),
            'rate_limits': await get_tenant_limits(auth_info['tenant_id'])
        }
    
    @staticmethod
    async def validate_access(tenant_context: dict, resource: str):
        # Check if tenant has access to requested resource
        if resource.startswith('org:'):
            org_id = resource.split(':')[1]
            if org_id not in tenant_context['allowed_orgs']:
                raise HTTPException(403, "Access denied to organization")
```

### 5. Deployment Steps

1. **Setup Infrastructure**
   ```bash
   # Create deployment directory
   mkdir meraki-mcp-central
   cd meraki-mcp-central
   
   # Clone and prepare code
   git clone https://github.com/Skycomm/Meraki-MCP.git
   cp -r Meraki-MCP/* .
   ```

2. **Configure Environment**
   ```bash
   # .env.production
   REDIS_URL=redis://redis:6379
   API_BASE_URL=https://api.meraki-mcp.yourdomain.com
   MCP_BASE_URL=https://mcp.meraki-mcp.yourdomain.com
   ENABLE_METRICS=true
   LOG_LEVEL=info
   ```

3. **Deploy Services**
   ```bash
   # Build and start services
   docker-compose -f docker-compose.prod.yml up -d
   
   # Initialize database
   docker-compose exec rest-api python init_db.py
   
   # Create first API key
   docker-compose exec rest-api python manage.py create-key \
     --tenant-id default \
     --meraki-key $MERAKI_API_KEY
   ```

### 6. Client Configuration Examples

#### A. Claude Desktop (using MCP-over-HTTP)
```json
{
  "mcpServers": {
    "meraki-central": {
      "command": "npx",
      "args": ["@modelcontextprotocol/mcp-client-http", 
               "https://mcp.meraki-mcp.yourdomain.com/mcp"],
      "env": {
        "MCP_API_KEY": "your-mcp-api-key"
      }
    }
  }
}
```

#### B. n8n Workflow
```yaml
# Import this as n8n workflow
{
  "name": "Meraki Device Monitor",
  "nodes": [
    {
      "name": "Meraki MCP",
      "type": "merakiMcp",
      "parameters": {
        "operation": "getDevices",
        "networkId": "{{ $json.network_id }}"
      },
      "credentials": {
        "merakiMcpApi": {
          "id": "1",
          "name": "Meraki MCP Central"
        }
      }
    }
  ]
}
```

#### C. Python Client
```python
# python_client.py
import requests

class MerakiMCPClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def execute_tool(self, tool, **params):
        response = requests.post(
            f"{self.base_url}/api/v1/execute",
            json={"tool": tool, "params": params},
            headers=self.headers
        )
        return response.json()

# Usage
client = MerakiMCPClient(
    "https://api.meraki-mcp.yourdomain.com",
    "your-api-key"
)
orgs = client.execute_tool("list_organizations")
```

### 7. Monitoring & Observability

```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    ports:
      - "3000:3000"
```

### 8. Benefits of This Architecture

1. **Multi-tenant Support**: Each client uses their own API key
2. **n8n Integration**: Native REST API for easy workflow integration  
3. **AI Assistant Support**: MCP protocol preserved via WebSocket adapter
4. **Scalability**: Services can be scaled independently
5. **Security**: API key validation, rate limiting, tenant isolation
6. **Monitoring**: Full observability with Prometheus/Grafana
7. **High Availability**: Can run multiple instances behind load balancer

### 9. Next Steps

1. Implement the REST API service with all Meraki tools
2. Create WebSocket adapter for MCP protocol
3. Build n8n custom node package
4. Setup monitoring and alerting
5. Create admin UI for API key management
6. Document API endpoints
7. Setup CI/CD pipeline