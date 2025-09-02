#!/bin/bash
# Launch Meraki MCP Server with custom module selection
# Configure using environment variables

# Example custom configurations:
# 
# Load specific modules:
#   export MCP_MODULES="wireless,wireless_advanced,organizations_core"
#
# Exclude specific modules from a profile:
#   export MCP_PROFILE=NETWORK
#   export MCP_EXCLUDE="switch,appliance_firewall"
#
# Load module groups:
#   export MCP_MODULES="core,wireless_all"

echo "Starting Meraki MCP Server - Custom Configuration"

if [ -z "$MCP_MODULES" ] && [ -z "$MCP_EXCLUDE" ] && [ -z "$MCP_PROFILE" ]; then
    echo "No custom configuration found. Set one of:"
    echo "  MCP_MODULES - comma-separated list of modules to load"
    echo "  MCP_EXCLUDE - comma-separated list of modules to exclude"
    echo "  MCP_PROFILE - profile name (WIRELESS, NETWORK, ORGANIZATIONS, etc.)"
    echo ""
    echo "Example:"
    echo "  export MCP_MODULES=\"wireless,organizations_core,helpers\""
    echo "  ./run_custom.sh"
    exit 1
fi

if [ ! -z "$MCP_MODULES" ]; then
    echo "Loading modules: $MCP_MODULES"
fi

if [ ! -z "$MCP_EXCLUDE" ]; then
    echo "Excluding modules: $MCP_EXCLUDE"
fi

if [ ! -z "$MCP_PROFILE" ]; then
    echo "Base profile: $MCP_PROFILE"
fi

echo ""

# Run the server
.venv/bin/python server/main.py