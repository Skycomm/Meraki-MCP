# Network Deployment Guide - Private Network

This guide shows you how to deploy the Meraki MCP server on your private network so multiple clients (Claude Desktop, n8n, etc.) can access it.

## Quick Start

### 1. Find Your Server's IP Address

```bash
# On the server machine, find your IP
# Linux/Mac:
ip addr show | grep inet
# or
ifconfig | grep inet

# Windows:
ipconfig

# Look for your network IP (e.g., 192.168.1.100, 10.0.0.50, etc.)
```

### 2. Setup the Server

```bash
# Clone the repository
git clone https://github.com/Skycomm/Meraki-MCP.git
cd Meraki-MCP
git checkout improved-python
cd python

# Copy and configure environment
cp .env.example .env
# Edit .env and add your MERAKI_API_KEY
```

### 3. Start the Network Server

**Option A: Using Docker (Recommended)**
```bash
# Start the server accessible on your network
docker-compose -f docker-compose.network.yml up -d

# Check it's running
docker-compose -f docker-compose.network.yml logs
```

**Option B: Direct Python**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the network server
HOST=0.0.0.0 PORT=8000 python -m meraki_mcp.remote_server
```

### 4. Test the Server

From any machine on your network:
```bash
# Replace 192.168.1.100 with your server's IP
curl http://192.168.1.100:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00",
  "meraki_connected": true
}
```

## Client Configuration

### For Claude Desktop (on any network machine)

1. First, get an auth token:
```bash
curl -X POST http://YOUR_SERVER_IP:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "your-name"}'

# Response:
# {"token": "your-auth-token", "username": "your-name", "is_privileged": false}
```

2. Configure Claude Desktop:
```json
{
  "mcpServers": {
    "meraki-network": {
      "command": "node",
      "args": [
        "/path/to/mcp-client-http.js",
        "http://192.168.1.100:8000/sse"
      ],
      "env": {
        "AUTH_TOKEN": "your-auth-token"
      }
    }
  }
}
```

### For n8n (on any network machine)

1. Add HTTP Request node with:
   - **Method**: POST
   - **URL**: `http://192.168.1.100:8000/api/v1/execute`
   - **Headers**:
     ```json
     {
       "Authorization": "Bearer your-auth-token",
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

### For Python Scripts

```python
import requests

# Server configuration
SERVER_URL = "http://192.168.1.100:8000"
TOKEN = "your-auth-token"

# Execute a tool
response = requests.post(
    f"{SERVER_URL}/api/v1/execute",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={
        "tool": "get_uplink_loss_latency",
        "params": {
            "org_id": "123456",
            "timespan": 300
        }
    }
)

result = response.json()
print(result["result"])
```

## Security Considerations

### 1. Network Access
- The server listens on `0.0.0.0:8000` (all interfaces)
- Make sure port 8000 is only accessible from your private network
- Use firewall rules to restrict access:

```bash
# Example: Allow only from local network
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

### 2. Authentication
- Every user needs an auth token
- Tokens are stored in memory (restart clears them)
- For production, consider adding a database

### 3. Privileged Users
Set privileged users in `.env`:
```
PRIVILEGED_USERS=admin@company.com,manager@company.com
```

Only these users can:
- Reboot devices
- Perform other dangerous operations

## Monitoring

### View Logs
```bash
# Docker logs
docker-compose -f docker-compose.network.yml logs -f

# Or direct Python
# Logs are printed to console
```

### Check Server Status
```bash
# From any network machine
curl http://YOUR_SERVER_IP:8000/health
```

### List Active Tokens (coming soon)
```bash
curl http://YOUR_SERVER_IP:8000/admin/tokens \
  -H "Authorization: Bearer admin-token"
```

## Troubleshooting

### "Connection Refused"
1. Check server is running: `docker ps` or `ps aux | grep python`
2. Check firewall: `sudo ufw status`
3. Verify IP address: Make sure you're using the correct server IP

### "Unauthorized"
1. Check your auth token is correct
2. Token may have expired (restart server clears tokens)
3. Get a new token using `/auth` endpoint

### "Rate Limit Exceeded"
- Wait 60 seconds
- Or increase limits in `.env`:
  ```
  RATE_LIMIT_REQUESTS=200
  RATE_LIMIT_WINDOW=60
  ```

### Can't Access from Other Machines
1. Check server is bound to `0.0.0.0` not `127.0.0.1`
2. Check no firewall blocking port 8000
3. Verify you're on the same network

## Example Use Cases

### 1. Network Monitoring Dashboard
Set up n8n to check uplinks every 5 minutes and alert on packet loss.

### 2. Multi-User Access
Multiple team members can use Claude Desktop with their own auth tokens.

### 3. Automation Scripts
Python scripts can monitor and manage the network programmatically.

## Advanced Configuration

### Use a Different Port
```bash
# In .env or docker-compose.network.yml
PORT=9000

# Update client configurations to use :9000
```

### Add SSL/TLS (Recommended for Production)
Use a reverse proxy like nginx:

```nginx
server {
    listen 443 ssl;
    server_name meraki.internal.company.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then update clients to use `https://meraki.internal.company.com`