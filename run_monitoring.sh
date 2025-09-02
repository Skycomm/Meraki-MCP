#!/bin/bash
# Launch Meraki MCP Server with Monitoring profile (141 tools)
# Focused on devices, cameras, sensors, and analytics

export MCP_PROFILE=MONITORING
echo "Starting Meraki MCP Server - Monitoring & Analytics Profile"
echo "Tool count: ~141 tools"
echo ""

# Run the server
.venv/bin/python server/main.py