#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Modern implementation using FastMCP.
"""

from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Import all resources and tools modules - they will register with the app
from server.resources import register_resources
from server.tools_organizations import register_organization_tools
from server.tools_networks import register_network_tools
from server.tools_devices import register_device_tools
from server.tools_wireless import register_wireless_tools
from server.tools_switch import register_switch_tools

# Register resources and tools
register_resources(app, meraki)
register_organization_tools(app, meraki)
register_network_tools(app, meraki)
register_device_tools(app, meraki)
register_wireless_tools(app, meraki)
register_switch_tools(app, meraki)

# When run directly, start the server
if __name__ == "__main__":
    app.run()
