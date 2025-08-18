# Complete Setup Guide - Meraki MCP Hybrid Server

This guide will help you set up the Meraki MCP server to work with both Claude Desktop and n8n on your private network.

## Step 1: Start the Server

### Option A: Using Docker (Recommended)

```bash
cd python

# Build the Docker image
docker build -t meraki-mcp-hybrid .

# Run the server
docker run -d \
  --name meraki-mcp \
  -p 8000:8000 \
  -e MERAKI_API_KEY="your-meraki-api-key" \
  -e PRIVILEGED_USERS="admin@company.com,you@company.com" \
  -e HOST=0.0.0.0 \
  meraki-mcp-hybrid \
  python -m hybrid_server
```

### Option B: Direct Python

```bash
cd python

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MERAKI_API_KEY="your-meraki-api-key"
export PRIVILEGED_USERS="admin@company.com,you@company.com"

# Run the server
python src/hybrid_server.py
```

## Step 2: Get Your Server IP

Find your server's IP address on the network:

```bash
# Linux/Mac
ip addr show | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4
```

Example: `192.168.1.100`

## Step 3: Get Authentication Token

From any machine on your network:

```bash
curl -X POST http://192.168.1.100:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "your-email@company.com"}'
```

Response:
```json
{
  "token": "Dkj3lK2mNb4pQr5sT6uV7wX8yZ9aB0cD",
  "username": "your-email@company.com",
  "is_privileged": true
}
```

**Save this token! You'll need it for both Claude and n8n.**

## Step 4: Setup Claude Desktop

### 4.1 Install MCP SSE Client

First, create the MCP SSE client on your local machine:

```bash
# Create a directory for MCP tools
mkdir -p ~/mcp-tools
cd ~/mcp-tools

# Install required packages
npm init -y
npm install node-fetch eventsource
```

### 4.2 Create the Client Script

Create `~/mcp-tools/meraki-mcp-client.js`:

```javascript
#!/usr/bin/env node

const EventSource = require('eventsource');
const fetch = require('node-fetch');
const readline = require('readline');

// Configuration from environment
const SERVER_URL = process.env.MCP_SERVER_URL || 'http://192.168.1.100:8000';
const AUTH_TOKEN = process.env.MCP_AUTH_TOKEN;

if (!AUTH_TOKEN) {
    console.error('Error: MCP_AUTH_TOKEN environment variable is required');
    process.exit(1);
}

// Create SSE connection
const sseUrl = `${SERVER_URL}/sse?token=${AUTH_TOKEN}`;
const eventSource = new EventSource(sseUrl);

// Connection established
eventSource.onopen = () => {
    console.error('Connected to Meraki MCP server');
};

// Handle messages from server
eventSource.onmessage = (event) => {
    process.stdout.write(event.data + '\n');
};

// Handle errors
eventSource.onerror = (error) => {
    console.error('SSE Error:', error.message);
    if (error.status === 401) {
        console.error('Authentication failed. Check your token.');
    }
    process.exit(1);
};

// Read from stdin and forward to server
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', async (line) => {
    try {
        // Parse the incoming message
        const message = JSON.parse(line);
        
        // Forward to server via POST
        const response = await fetch(`${SERVER_URL}/sse`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${AUTH_TOKEN}`
            },
            body: JSON.stringify(message)
        });
        
        if (!response.ok) {
            console.error('Failed to send message:', response.statusText);
        }
    } catch (error) {
        console.error('Error processing message:', error.message);
    }
});

// Handle shutdown
process.on('SIGINT', () => {
    eventSource.close();
    process.exit(0);
});
```

Make it executable:
```bash
chmod +x ~/mcp-tools/meraki-mcp-client.js
```

### 4.3 Configure Claude Desktop

Add this to your Claude Desktop configuration file:

**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "meraki": {
      "command": "node",
      "args": ["/Users/YOUR_USERNAME/mcp-tools/meraki-mcp-client.js"],
      "env": {
        "MCP_SERVER_URL": "http://192.168.1.100:8000",
        "MCP_AUTH_TOKEN": "Dkj3lK2mNb4pQr5sT6uV7wX8yZ9aB0cD"
      }
    }
  }
}
```

**Important**: Replace:
- `/Users/YOUR_USERNAME` with your actual home directory path
- `192.168.1.100` with your server's IP address
- The token with your actual token from Step 3

### 4.4 Restart Claude Desktop

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. You should see "meraki" in the MCP tools list

## Step 5: Setup n8n

### 5.1 Create HTTP Request Credentials

In n8n:
1. Go to Credentials
2. Create new "Header Auth" credential:
   - Name: `Meraki MCP`
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_TOKEN_HERE`

### 5.2 Example Workflow: Monitor Uplinks

Create a new workflow with these nodes:

1. **Schedule Trigger**
   - Interval: Every 5 minutes

2. **HTTP Request**
   - Method: `POST`
   - URL: `http://192.168.1.100:8000/api/v1/execute`
   - Authentication: Use "Meraki MCP" credentials
   - Send Headers: Yes
   - Send Body: Yes
   - Body Type: JSON
   - Body:
     ```json
     {
       "tool": "check_uplinks",
       "arguments": {
         "org_id": "YOUR_ORG_ID",
         "timespan": 300
       }
     }
     ```

3. **IF Node**
   - Condition: `{{ $json.result.includes("⚠️") }}`

4. **Send Email/Slack**
   - Send alert if packet loss detected

## Step 6: Test Everything

### Test with Claude Desktop

In Claude, you should be able to say:
- "List all Meraki organizations"
- "Check uplink status for organization 123456"
- "Show me networks in organization 123456"

### Test with n8n

Manually execute your workflow and verify it returns data.

### Test with curl

```bash
# List organizations
curl -X POST http://192.168.1.100:8000/api/v1/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_organizations", "arguments": {}}'

# Check uplinks
curl -X POST http://192.168.1.100:8000/api/v1/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "check_uplinks", "arguments": {"org_id": "123456"}}'
```

## Troubleshooting

### Claude Desktop Issues

1. **"meraki" not showing in tools**
   - Check the config file path is correct
   - Verify the JSON syntax is valid
   - Make sure the client script path is absolute

2. **Connection errors**
   - Verify the server is running: `curl http://192.168.1.100:8000/health`
   - Check the token is correct
   - Ensure firewall allows port 8000

3. **Check Claude logs**
   - Mac: `~/Library/Logs/Claude/mcp.log`
   - Windows: `%APPDATA%\Claude\logs\mcp.log`

### n8n Issues

1. **401 Unauthorized**
   - Regenerate token and update credentials
   - Check "Bearer " prefix in header value

2. **Connection timeout**
   - Verify server IP is correct
   - Check network connectivity
   - Ensure n8n can reach the server

## Available Tools Reference

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_organizations` | List all Meraki organizations | None |
| `get_networks` | Get networks in an organization | `org_id` (required) |
| `check_uplinks` | Check uplink packet loss/latency | `org_id` (required), `timespan` (optional, max 300) |
| `ping_device` | Run ping test from a device | `serial` (required), `target` (required), `count` (optional) |
| `reboot_device` | Reboot a device (privileged only) | `serial` (required), `confirmation` (required) |

## Security Notes

1. **Tokens are stored in memory** - They're lost when server restarts
2. **Use HTTPS in production** - Add nginx reverse proxy with SSL
3. **Restrict network access** - Use firewall rules to limit who can connect
4. **Monitor usage** - Check server logs regularly

## Next Steps

1. Set up monitoring dashboard in n8n
2. Create more complex workflows
3. Add custom tools for your specific needs
4. Set up persistent token storage (Redis)