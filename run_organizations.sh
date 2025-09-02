#!/bin/bash
# Launch Meraki MCP Server with Organizations profile (126 tools)
# Focused on organization-level management and configuration

export MCP_PROFILE=ORGANIZATIONS
echo "Starting Meraki MCP Server - Organizations Admin Profile"
echo "Tool count: ~126 tools"
echo ""

# Run the server
.venv/bin/python server/main.py