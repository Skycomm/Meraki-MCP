#!/bin/bash
# Launch Meraki MCP Server with Wireless profile (179 tools)
# Focused on wireless, RF profiles, and SSID management

export MCP_PROFILE=WIRELESS
echo "Starting Meraki MCP Server - Wireless Profile"
echo "Tool count: ~179 tools"
echo ""

# Run the server
.venv/bin/python server/main.py