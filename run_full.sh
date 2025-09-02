#!/bin/bash
# Launch Meraki MCP Server with FULL profile (833 tools)
# Complete Meraki API coverage - all tools enabled

export MCP_PROFILE=FULL
echo "Starting Meraki MCP Server - Full Profile"
echo "Tool count: 833 tools (ALL TOOLS)"
echo "WARNING: This may exceed Claude Desktop's tool limit"
echo ""

# Run the server
.venv/bin/python server/main.py