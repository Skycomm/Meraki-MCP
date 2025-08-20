# Cisco Meraki MCP Server - Directory Contents

## Core Files
- `meraki_server.py` - Main server entry point
- `meraki_client.py` - Meraki API client wrapper
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `run_meraki_server.sh` - Server startup script

## Server Directory
Contains all the MCP tools organized by category:
- `server/main.py` - Server initialization
- `server/resources.py` - MCP resources
- `server/tools_*.py` - Tool implementations by category

## Python Directory
Contains the hybrid/SSE server implementation:
- `python/src/hybrid_server.py` - Network-accessible MCP server
- `python/src/meraki_tools_simple.py` - SSE version tools

## Documentation
- `README.md` - Main documentation
- `FEATURES_IMPLEMENTED_2025.md` - Complete feature list
- `DHCP_TOOLS_GUIDE.md` - DHCP tools usage guide
- `SETUP_CLAUDE_DESKTOP.md` - Claude Desktop configuration

## Utility Scripts
- `setup_mcp_server.sh` - Server setup script
- `setup_server.py` - Python setup helper

## Total: 41 files (cleaned from ~60+ files)