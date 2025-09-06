#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Clean SDK Implementation
100% SDK Coverage with consolidated modules and profile support.
"""

import os
from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message
from server.profiles import should_load_module, print_profile_info

# Get profile from environment
profile_name = os.getenv('MCP_PROFILE', 'FULL').upper()

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Import resources (always loaded)
from server.resources import register_resources

# Print profile information
print_profile_info(profile_name)

# Import ALL SDK modules (conditionally based on profile)
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
from server.tools_Custom_analytics import register_analytics_tools
from server.tools_Custom_batch import register_custom_batch_tools
from server.tools_Custom_beta import register_beta_tools
# from server.tools_Custom_helpers import register_helper_tools  # Disabled due to syntax errors
from server.tools_Custom_monitoring_filtered import register_monitoring_tools_filtered  # 6 unique analytics tools
from server.tools_Custom_search import register_search_tools
from server.tools_IP_lookup import register_ip_lookup_tools

# Import N8N essentials module
from server.tools_N8N_essentials import register_n8n_essentials_tools

# Register resources first (always loaded)
register_resources(app, meraki)

# Register SDK modules based on profile
if should_load_module('SDK_administered', profile_name):
    register_administered_tools(app, meraki)
if should_load_module('SDK_appliance', profile_name):
    register_appliance_tools(app, meraki)
if should_load_module('SDK_camera', profile_name):
    register_camera_tools(app, meraki)
if should_load_module('SDK_cellularGateway', profile_name):
    register_cellular_gateway_tools(app, meraki)
if should_load_module('SDK_devices', profile_name):
    register_devices_tools(app, meraki)
if should_load_module('SDK_insight', profile_name):
    register_insight_tools(app, meraki)
if should_load_module('SDK_licensing', profile_name):
    register_licensing_tools(app, meraki)
if should_load_module('SDK_networks', profile_name):
    register_networks_tools(app, meraki)
if should_load_module('SDK_organizations', profile_name):
    register_organizations_tools(app, meraki)
if should_load_module('SDK_sensor', profile_name):
    register_sensor_tools(app, meraki)
if should_load_module('SDK_sm', profile_name):
    register_sm_tools(app, meraki)
if should_load_module('SDK_switch', profile_name):
    register_switch_tools(app, meraki)
if should_load_module('SDK_wireless', profile_name):
    register_wireless_tools(app, meraki)

# Register custom tools based on profile
if should_load_module('Custom_alerts_filtered', profile_name):
    register_alerts_tools_filtered(app, meraki)
if should_load_module('Custom_analytics', profile_name):
    register_analytics_tools(app, meraki)
if should_load_module('Custom_batch', profile_name):
    register_custom_batch_tools(app, meraki)
if should_load_module('Custom_beta', profile_name):
    register_beta_tools(app, meraki)
# Custom_helpers temporarily disabled due to syntax errors
# if should_load_module('Custom_helpers', profile_name):
#     register_helper_tools(app, meraki)
if should_load_module('Custom_monitoring_filtered', profile_name):
    register_monitoring_tools_filtered(app, meraki)
if should_load_module('Custom_search', profile_name):
    register_search_tools(app, meraki)

# Always register IP lookup tools (critical for device finding)
register_ip_lookup_tools(app, meraki)

# Register N8N essentials module
if should_load_module('N8N_essentials', profile_name):
    register_n8n_essentials_tools(app, meraki)

print(f"✅ Cisco Meraki MCP Server initialized with {profile_name} profile")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)