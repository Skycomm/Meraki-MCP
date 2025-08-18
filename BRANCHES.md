# Meraki MCP Server - Branch Structure

This repository contains three deployment options for the Meraki MCP Server:

## 🏠 `main` branch (Local Deployment)

The default branch for local/single-user deployment.

**Use this when:**
- Running MCP server locally on your machine
- Using with Claude Desktop on the same computer
- Each user has their own Meraki API key
- You want direct stdio communication

**Features:**
- Standard MCP server implementation
- Direct Meraki API integration
- All tools and resources available
- Docker support for local containerization

**Setup:**
```bash
git checkout main
uv run meraki_server.py
```

## 🌐 `network` branch (Remote/Centralized Deployment)

For centralized, multi-user deployment using Cloudflare Workers.

**Use this when:**
- Multiple staff need access to the same MCP server
- You want centralized API key management
- Integration with n8n workflows is needed
- Remote access from anywhere is required

**Features:**
- Cloudflare Workers serverless deployment
- GitHub OAuth authentication
- Single Meraki API key stored server-side
- Role-based access control
- Support for Claude Desktop, n8n, and REST clients

**Setup:**
```bash
git checkout network
cd remote-meraki-mcp
wrangler deploy
```

## 🐍 `improved-python` branch (Enhanced Python Implementation)

Modern Python implementation with advanced features and best practices.

**Use this when:**
- You prefer Python over TypeScript
- Need advanced features like caching and rate limiting
- Want comprehensive testing and monitoring
- Require both CLI and MCP server modes

**Features:**
- Async/await for better performance
- Built-in rate limiting and caching
- Comprehensive test suite
- CLI for direct command-line usage
- Structured logging and optional Sentry monitoring
- Docker and docker-compose support

**Setup:**
```bash
git checkout improved-python
cd python
pip install -r requirements.txt
python -m meraki_mcp.server  # For MCP mode
# OR
python -m meraki_mcp.cli list-orgs  # For CLI mode
```

## Choosing Between Branches

| Feature | Local (`main`) | Network (`network`) |
|---------|---------------|-------------------|
| Deployment | Local machine | Cloudflare (global) |
| Authentication | API key per user | GitHub OAuth + tokens |
| Multi-user | No | Yes |
| n8n Integration | Difficult | Native REST API |
| Infrastructure | Your computer | Serverless |
| Cost | Free | Free tier available |
| Setup Complexity | Simple | Moderate |

## Switching Between Branches

```bash
# Switch to local deployment
git checkout main

# Switch to network deployment  
git checkout network
```

Both branches are maintained and can be used based on your deployment needs.