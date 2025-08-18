# Remote Meraki MCP Server Deployment Guide

This guide shows you how to deploy your Meraki MCP server as a centralized, authenticated service using Cloudflare Workers.

## Architecture Overview

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Claude Desktop  │      │      n8n        │      │  Staff Users    │
│   (via SSE)     │      │  (via REST)     │      │  (via API)      │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         │                        │                         │
         └────────────────────────┼─────────────────────────┘
                                  │
                           ┌──────▼──────┐
                           │ Cloudflare  │
                           │   Worker    │
                           │  (Global)   │
                           └──────┬──────┘
                                  │
                           ┌──────▼──────┐
                           │GitHub OAuth │
                           │    Auth     │
                           └──────┬──────┘
                                  │
                           ┌──────▼──────┐
                           │ Meraki API  │
                           │(Single Key) │
                           └─────────────┘
```

## Benefits of This Approach

1. **Centralized API Key**: Store your Meraki API key once on the server
2. **GitHub Authentication**: Staff authenticate with their GitHub accounts
3. **Role-Based Access**: Control who can perform privileged operations
4. **Global Deployment**: Cloudflare Workers run globally with low latency
5. **No Infrastructure**: Serverless - no servers to manage
6. **Easy Integration**: Works with Claude, n8n, and custom applications

## Setup Steps

### 1. Create GitHub OAuth App

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Meraki MCP Server`
   - **Homepage URL**: `https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev`
   - **Authorization callback URL**: `https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev/oauth/callback`
4. Save your Client ID and Client Secret

### 2. Setup Cloudflare Account

1. Sign up for a free Cloudflare account at https://cloudflare.com
2. Install Wrangler CLI:
   ```bash
   npm install -g wrangler
   ```
3. Authenticate:
   ```bash
   wrangler login
   ```

### 3. Create KV Namespace

```bash
# Create KV namespace for storing auth tokens
wrangler kv:namespace create "auth_tokens"

# Note the ID that's returned, you'll need it for wrangler.toml
```

### 4. Configure the Project

1. Update `wrangler.toml`:
   ```toml
   name = "remote-meraki-mcp"
   main = "src/index.ts"
   compatibility_date = "2024-11-16"

   [vars]
   GITHUB_CLIENT_ID = "your-github-client-id"
   GITHUB_CLIENT_SECRET = "your-github-client-secret"
   MERAKI_API_KEY = "your-meraki-api-key"
   # Add your staff GitHub usernames
   PRIVILEGED_USERS = "daviduser,tomuser,sarahuser"

   [[kv_namespaces]]
   binding = "KV"
   id = "your-kv-namespace-id-from-step-3"
   ```

### 5. Install Dependencies and Deploy

```bash
cd remote-meraki-mcp
npm install
wrangler deploy
```

Your server will be available at:
`https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev`

## Usage Instructions

### For Claude Desktop Users

1. **Get Authentication Token**:
   - Visit `https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev/auth`
   - Authorize with GitHub
   - Copy your token from the callback page

2. **Configure Claude Desktop**:
   ```json
   {
     "mcpServers": {
       "meraki-remote": {
         "url": "https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev/",
         "transport": "sse",
         "headers": {
           "Authorization": "Bearer YOUR_TOKEN_HERE"
         }
       }
     }
   }
   ```

### For n8n Integration

1. **Create HTTP Request Node** with:
   - **Method**: POST
   - **URL**: `https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev/api/v1/execute`
   - **Headers**:
     ```json
     {
       "Authorization": "Bearer YOUR_TOKEN",
       "Content-Type": "application/json"
     }
     ```
   - **Body**:
     ```json
     {
       "tool": "list_organizations",
       "params": {}
     }
     ```

2. **Example n8n Workflow**:
   ```json
   {
     "nodes": [
       {
         "name": "List Meraki Orgs",
         "type": "n8n-nodes-base.httpRequest",
         "parameters": {
           "method": "POST",
           "url": "https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev/api/v1/execute",
           "headerParametersUi": {
             "parameter": [
               {
                 "name": "Authorization",
                 "value": "Bearer YOUR_TOKEN"
               }
             ]
           },
           "jsonParameters": true,
           "bodyParametersJson": {
             "tool": "list_organizations",
             "params": {}
           }
         }
       }
     ]
   }
   ```

### For Custom Applications

```python
# Python example
import requests

class MerakiMCPClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def execute_tool(self, tool_name, **params):
        response = requests.post(
            f"{self.base_url}/api/v1/execute",
            json={"tool": tool_name, "params": params},
            headers=self.headers
        )
        return response.json()

# Usage
client = MerakiMCPClient(
    "https://remote-meraki-mcp.YOUR-SUBDOMAIN.workers.dev",
    "your-auth-token"
)

# List organizations
orgs = client.execute_tool("list_organizations")

# Get uplink stats
stats = client.execute_tool(
    "get_uplink_loss_latency",
    org_id="12345",
    timespan=300
)
```

## Managing Access

### Adding/Removing Privileged Users

1. Update the `PRIVILEGED_USERS` variable in `wrangler.toml`
2. Redeploy:
   ```bash
   wrangler deploy
   ```

### Revoking Tokens

```bash
# List all tokens
wrangler kv:key list --binding=KV --prefix="token:"

# Delete a specific token
wrangler kv:key delete --binding=KV "token:TOKEN_TO_REVOKE"
```

## Monitoring and Logs

```bash
# View real-time logs
wrangler tail

# View metrics in Cloudflare dashboard
# Go to Workers > your-worker > Analytics
```

## Security Considerations

1. **API Key Protection**: Your Meraki API key is stored only on the server
2. **Token Expiration**: Tokens expire after 30 days
3. **Rate Limiting**: Built into Cloudflare Workers
4. **HTTPS Only**: All communication is encrypted
5. **Audit Trail**: All operations include the user who performed them

## Troubleshooting

### "Unauthorized" Error
- Check that your token is included in the Authorization header
- Verify the token hasn't expired
- Ensure you've authenticated via GitHub

### "Permission Denied" for Reboot
- Verify your GitHub username is in the PRIVILEGED_USERS list
- Check the exact spelling/case of your username

### Tool Not Found
- Ensure the tool name matches exactly
- Check that the tool is implemented in the corresponding file

## Cost Estimation

Cloudflare Workers Free Tier includes:
- 100,000 requests/day
- 10ms CPU time per request

For typical usage with 10 staff members:
- ~1,000 requests/day = **FREE**
- No infrastructure costs
- No maintenance required

## Next Steps

1. **Implement All Tools**: Port all your existing MCP tools to the new format
2. **Add Logging**: Send logs to a centralized service
3. **Create Dashboard**: Build a web UI for token management
4. **Add Webhooks**: Notify on critical operations like reboots
5. **Implement Caching**: Cache frequently accessed data in KV