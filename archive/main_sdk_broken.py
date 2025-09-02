#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - SDK-aligned implementation using FastMCP.
Supports profile-based tool loading with clean SDK category separation.
"""

import os
from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message
from server.profiles import should_load_module, get_modules_from_env, print_profile_info

# Get profile configuration from environment
MCP_PROFILE = os.getenv('MCP_PROFILE', 'FULL')
MCP_MODULES = os.getenv('MCP_MODULES', '')  # Custom module list
MCP_EXCLUDE = os.getenv('MCP_EXCLUDE', '')  # Modules to exclude

# Parse custom configurations
custom_modules = get_modules_from_env(MCP_MODULES) if MCP_MODULES else None
excluded_modules = [m.strip() for m in MCP_EXCLUDE.split(',')] if MCP_EXCLUDE else None

# Print profile information
print_profile_info(MCP_PROFILE)

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# =====================================================================
# SDK CATEGORY IMPORTS - Matches official Meraki SDK exactly
# =====================================================================

def load_sdk_module(module_name, register_function_name):
    """Dynamically load SDK modules based on profile."""
    if should_load_module(module_name, MCP_PROFILE, custom_modules, excluded_modules):
        try:
            module = __import__(f'server.tools_{module_name}', fromlist=[register_function_name])
            register_func = getattr(module, register_function_name)
            register_func(app, meraki)
            print(f"✅ Loaded SDK module: {module_name}")
        except (ImportError, AttributeError) as e:
            print(f"⚠️  Failed to load SDK module {module_name}: {e}")

def load_custom_module(module_name, register_function_name):
    """Dynamically load custom modules based on profile."""
    if should_load_module(module_name, MCP_PROFILE, custom_modules, excluded_modules):
        try:
            module = __import__(f'server.tools_{module_name}', fromlist=[register_function_name])
            register_func = getattr(module, register_function_name)
            register_func(app, meraki)
            print(f"✅ Loaded custom module: {module_name}")
        except (ImportError, AttributeError) as e:
            print(f"⚠️  Failed to load custom module {module_name}: {e}")

# Always load resources first
if should_load_module('resources', MCP_PROFILE, custom_modules, excluded_modules):
    from server.resources import register_resources
    register_resources(app, meraki)
    print("✅ Loaded resources")

# =====================================================================
# LOAD SDK CATEGORIES (matches official SDK structure)
# =====================================================================

# Load SDK modules in alphabetical order (matches `dir(dashboard)`)
load_sdk_module('administered', 'register_administered_tools')
load_sdk_module('appliance', 'register_appliance_tools')
load_sdk_module('batch', 'register_batch_tools')
load_sdk_module('camera', 'register_camera_tools')
load_sdk_module('cellularGateway', 'register_cellular_gateway_tools')
load_sdk_module('devices', 'register_device_tools')
load_sdk_module('insight', 'register_insight_tools')
load_sdk_module('licensing', 'register_licensing_tools')
load_sdk_module('networks', 'register_network_tools')
load_sdk_module('organizations', 'register_organizations_tools')
load_sdk_module('sensor', 'register_sensor_tools')
load_sdk_module('sm', 'register_sm_tools')
load_sdk_module('switch', 'register_switch_tools')
load_sdk_module('wireless', 'register_wireless_tools')

# =====================================================================
# LOAD CUSTOM/EXTENSION MODULES
# =====================================================================

# Load custom modules (non-SDK functionality)
load_custom_module('custom_helpers', 'register_helper_tools')
load_custom_module('custom_search', 'register_search_tools')
load_custom_module('custom_alerts', 'register_alert_tools')
load_custom_module('custom_analytics', 'register_analytics_tools')
load_custom_module('custom_live', 'register_live_tools')
load_custom_module('custom_monitoring', 'register_monitoring_tools')
load_custom_module('custom_monitoring_dashboard', 'register_monitoring_dashboard_tools')
load_custom_module('custom_policy', 'register_policy_tools')
load_custom_module('custom_vpn', 'register_vpn_tools')
load_custom_module('custom_event_analysis', 'register_event_analysis_tools')
load_custom_module('custom_beta', 'register_beta_tools')

# Load special modules that don't fit standard SDK categories
load_sdk_module('adaptive_policy', 'register_adaptive_policy_tools')
load_sdk_module('networks_complete', 'register_networks_complete_tools')

print(f"\n🚀 Meraki MCP Server started with profile: {MCP_PROFILE}")

# When run directly, start the server
if __name__ == "__main__":
    app.run()