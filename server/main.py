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
from server.tools_wireless_firewall import register_wireless_firewall_tools
from server.tools_switch import register_switch_tools
from server.tools_analytics import register_analytics_tools
from server.tools_alerts import register_alert_tools
from server.tools_appliance import register_appliance_tools
from server.tools_camera import register_camera_tools
from server.tools_vpn import register_vpn_tools
from server.tools_sm import register_sm_tools
from server.tools_licensing import register_licensing_tools
from server.tools_policy import register_policy_tools
from server.tools_monitoring import register_monitoring_tools
from server.tools_beta import register_beta_tools
from server.tools_live import register_live_tools
from server.tools_helpers import register_helper_tools

# Register resources and tools
register_resources(app, meraki)
register_organization_tools(app, meraki)
register_network_tools(app, meraki)
register_device_tools(app, meraki)
register_wireless_tools(app, meraki)
register_wireless_firewall_tools(app, meraki)
register_switch_tools(app, meraki)
register_analytics_tools(app, meraki)
register_alert_tools(app, meraki)
register_appliance_tools(app, meraki)
register_camera_tools(app, meraki)
register_vpn_tools(app, meraki)
register_sm_tools(app, meraki)
register_licensing_tools(app, meraki)
register_policy_tools(app, meraki)
register_monitoring_tools(app, meraki)
register_beta_tools(app, meraki)
register_live_tools(app, meraki)
register_helper_tools(app, meraki)

# When run directly, start the server
if __name__ == "__main__":
    app.run()
