# n8n Native MCP Integration with Meraki MCP Server

Since n8n now has native MCP support, you can connect directly to your Meraki MCP server!

## Server Setup

### 1. Start the MCP Server

```bash
cd /Users/david/docker/cisco-meraki-mcp-server-tvi/python

# Update .env with your API key
echo "MERAKI_API_KEY=1ac5962056ad56da8cea908864f136adc5878a43" > .env
echo "PRIVILEGED_USERS=david@skycomm.com" >> .env

# Start the server
python src/hybrid_server.py
```

The server will run on `http://localhost:8000` with SSE endpoint at `http://localhost:8000/sse`

### 2. Get Authentication Token

```bash
curl -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "david@skycomm.com"}'
```

Save the token from the response.

## n8n Configuration

### Using MCP Client Tool Node

1. **Add MCP Client Tool node** to your workflow

2. **Configure the node**:
   - **SSE Endpoint**: `http://localhost:8000/sse`
   - **Authentication**: Bearer Token
   - **Token**: Your token from step 2
   - **Tools to Include**: All (or select specific tools)

3. **Connect to AI Agent**:
   - Add an AI Agent node
   - Connect the MCP Client Tool as a tool
   - The agent can now use all Meraki tools!

### Available Tools in n8n

- `list_organizations` - List all Meraki organizations
- `get_networks` - Get networks in an organization
- `check_uplinks` - Monitor packet loss and latency
- `ping_device` - Run ping tests from devices
- `reboot_device` - Reboot devices (privileged users only)

## Example n8n Workflow

### Network Health Monitor

1. **Schedule Trigger** (every 5 minutes)
2. **MCP Client Tool** connected to AI Agent
3. **AI Agent** with prompt:
   ```
   Check the uplink status for organization 686470.
   If any uplinks have packet loss > 1%, create an alert.
   ```
4. **IF** node to check for alerts
5. **Send Email/Slack** notification

### Interactive Meraki Assistant

1. **Webhook Trigger** (for Slack/Teams)
2. **MCP Client Tool** connected to AI Agent
3. **AI Agent** processes natural language requests:
   - "Show me all networks"
   - "Check if Suite 36 Hollywood has packet loss"
   - "Run a ping test from device Q2XX-XXXX to 8.8.8.8"
4. **Reply** with results

## Benefits of Native MCP in n8n

1. **No REST API needed** - Direct MCP protocol communication
2. **AI Agent Integration** - Natural language processing of requests
3. **Streaming Support** - Real-time updates via SSE
4. **Tool Discovery** - n8n automatically discovers available tools
5. **Type Safety** - n8n validates tool parameters

## Testing Your Setup

In n8n:
1. Create a simple workflow with MCP Client Tool
2. Connect it to a Basic LLM Chain or AI Agent
3. Test with: "List all Meraki organizations"

The AI agent will automatically use the MCP tools to fulfill the request!

## Advanced: n8n as MCP Server

You can also use n8n's **MCP Server Trigger** to expose n8n workflows as MCP tools that Claude can use! This creates bidirectional integration:

- **n8n → Meraki**: Using MCP Client Tool to access Meraki
- **Claude → n8n**: Using MCP Server Trigger to access n8n workflows