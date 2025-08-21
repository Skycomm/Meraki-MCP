# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Get Your API Key
1. Log into [Meraki Dashboard](https://dashboard.meraki.com)
2. Go to **Organization > Settings > Dashboard API access**
3. Enable API access and generate your API key

### 2. Install with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/cisco-meraki-mcp-server.git
cd cisco-meraki-mcp-server

# Build Docker image
docker build -t meraki-mcp-server .

# Test the server
docker run -e MERAKI_API_KEY="your-api-key" meraki-mcp-server
```

### 3. Add to Claude Desktop

Edit Claude Desktop settings:
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "meraki": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "MERAKI_API_KEY=your-actual-api-key",
        "meraki-mcp-server"
      ],
      "transport": "stdio",
      "env": {}
    }
  }
}
```

### 4. Restart Claude Desktop

Quit and restart Claude Desktop to load the MCP server.

## ✅ Verify Installation

In Claude, try these commands:

```
"Show me all organizations"
"What's my API usage today?"
"List all networks"
```

If you see your Meraki data, you're all set!

## 🎯 Common First Tasks

### Check Network Status
```
"Show network health status"
"Are any devices offline?"
"What's the bandwidth usage?"
```

### View Inventory
```
"Show all devices"
"List wireless access points"
"Show switch inventory"
```

### Security Check
```
"Show recent security alerts"
"Check firewall rules"
"Show VPN status"
```

## 🆘 Troubleshooting

### "No organizations found"
- Verify your API key is correct
- Check API access is enabled in Dashboard
- Ensure your account has admin privileges

### "Connection timeout"
- Check internet connectivity
- Verify Docker is running
- Check firewall allows HTTPS (port 443)

### "Rate limit exceeded"
- Wait 1 minute and try again
- The server handles rate limiting automatically

## 📚 Next Steps

1. Read [FEATURES.md](FEATURES.md) for full capabilities
2. Try natural language queries
3. Set up alerts and monitoring
4. Explore batch operations for bulk changes

## 💡 Pro Tips

- Use specific location names for better results
- Ask for help: "How do I configure VPN?"
- Request examples: "Show me firewall rule examples"
- Generate reports: "Create executive summary"

---

**Need help?** Ask Claude: "Show Meraki helper tools"