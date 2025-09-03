#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Clean SDK Implementation
100% SDK Coverage with consolidated modules.
"""

from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Import resources
from server.resources import register_resources

# Import ALL SDK modules (complete coverage)
from server.tools_SDK_administered import register_administered_tools      # 4 methods
from server.tools_SDK_appliance import register_appliance_tools            # 130 methods  
# from server.tools_SDK_batch import register_batch_tools                    # 12 methods (may duplicate SDK)
from server.tools_SDK_camera import register_camera_tools                  # 45 methods
from server.tools_SDK_cellularGateway import register_cellular_gateway_tools  # 24 methods
from server.tools_SDK_devices import register_devices_tools               # 27 methods
from server.tools_SDK_insight import register_insight_tools                # 7 methods
from server.tools_SDK_licensing import register_licensing_tools            # 8 methods
from server.tools_SDK_networks import register_networks_tools              # 114 methods
from server.tools_SDK_organizations import register_organizations_tools    # 173 methods
from server.tools_SDK_sensor import register_sensor_tools                  # 18 methods
from server.tools_SDK_sm import register_sm_tools                          # 49 methods
from server.tools_SDK_switch import register_switch_tools                  # 101 methods
from server.tools_SDK_wireless import register_wireless_tools              # 116 methods

# Import custom tools (non-SDK extensions) 
from server.tools_Custom_alerts_filtered import register_alerts_tools_filtered    # 7 unique webhook tools
from server.tools_Custom_batch import register_custom_batch_tools
from server.tools_Custom_monitoring_filtered import register_monitoring_tools_filtered  # 6 unique analytics tools
# Note: Some custom modules may not exist in this version
# from server.tools_Custom_analytics import register_analytics_tools
# from server.tools_Custom_beta import register_beta_tools
# from server.tools_Custom_helpers import register_helper_tools
# from server.tools_Custom_search import register_search_tools

# Register resources first
register_resources(app, meraki)

# Register ALL SDK modules (complete coverage)
print("🎯 Registering ALL SDK Modules (complete coverage)...")
register_administered_tools(app, meraki)      # 4 methods
register_appliance_tools(app, meraki)         # 130 methods
# register_batch_tools(app, meraki)             # 12 methods (may duplicate SDK tools)
register_camera_tools(app, meraki)            # 45 methods
register_cellular_gateway_tools(app, meraki)  # 24 methods
register_devices_tools(app, meraki)           # 27 methods
register_insight_tools(app, meraki)           # 7 methods
register_licensing_tools(app, meraki)         # 8 methods
register_networks_tools(app, meraki)          # 114 methods
register_organizations_tools(app, meraki)     # 173 methods
register_sensor_tools(app, meraki)            # 18 methods
register_sm_tools(app, meraki)                # 49 methods
register_switch_tools(app, meraki)            # 101 methods
register_wireless_tools(app, meraki)          # 116 methods

# Register custom tools (non-SDK extensions)
print("🔧 Registering Custom Tools...")
register_alerts_tools_filtered(app, meraki)        # 7 unique webhook tools
register_custom_batch_tools(app, meraki)
register_monitoring_tools_filtered(app, meraki)    # 6 unique analytics tools
# Commented out missing modules
# register_analytics_tools(app, meraki)
# register_beta_tools(app, meraki)
# register_helper_tools(app, meraki)
# register_search_tools(app, meraki)

print("✅ Cisco Meraki MCP Server initialized with clean SDK structure")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)