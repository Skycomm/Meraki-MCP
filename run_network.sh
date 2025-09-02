#!/bin/bash
# Launch Meraki MCP Server with Network Infrastructure profile (402 tools)
# Focused on switch, appliance, networks, and VPN management

export MCP_PROFILE=NETWORK
echo "Starting Meraki MCP Server - Network Infrastructure Profile"
echo "Tool count: ~402 tools"
echo ""

# Run the server
.venv/bin/python server/main.py