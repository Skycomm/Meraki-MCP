#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Official API tools only (no custom tools).
"""

from mcp.server import FastMCP
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Track if tools have been registered to prevent duplicate registration
_tools_registered = False

def register_all_tools():
    """Register all tools once and only once."""
    global _tools_registered
    
    if _tools_registered:
        print("[INFO] Tools already registered, skipping...")
        return
    
    print("[INFO] Registering official Meraki API tools only...")
    
    # Import ONLY official Meraki API tool modules (no custom helpers or dashboards)
    from server.resources import register_resources
    from server.tools_organizations import register_organization_tools
    from server.tools_networks import register_network_tools
    from server.tools_devices import register_device_tools
    from server.tools_wireless import register_wireless_tools
    from server.tools_switch import register_switch_tools
    from server.tools_appliance import register_appliance_tools
    from server.tools_camera import register_camera_tools
    from server.tools_sm import register_sm_tools
    from server.tools_licensing import register_licensing_tools
    from server.tools_sensor import register_sensor_tools
    from server.tools_insight import register_insight_tools
    from server.tools_cellular_gateway import register_cellular_gateway_tools
    from server.tools_administered import register_administered_tools
    from server.tools_batch import register_batch_tools
    from server.tools_webhooks import register_webhooks_tools
    from server.tools_mqtt import register_mqtt_tools
    from server.tools_syslog import register_syslog_tools
    from server.tools_snmp import register_snmp_tools
    from server.tools_saml import register_saml_tools
    from server.tools_branding import register_branding_tools
    from server.tools_oauth import register_oauth_tools
    from server.tools_config_templates import register_config_template_tools
    from server.tools_group_policies import register_group_policies_tools
    from server.tools_floor_plans import register_floor_plans_tools
    from server.tools_meraki_auth_users import register_meraki_auth_users_tools
    from server.tools_traffic_analysis import register_traffic_analysis_tools
    from server.tools_netflow import register_netflow_tools
    from server.tools_pii import register_pii_tools
    from server.tools_bluetooth_clients import register_bluetooth_clients_tools
    from server.tools_org_admins import register_org_admins_tools
    from server.tools_login_security import register_login_security_tools
    from server.tools_early_access import register_early_access_tools
    from server.tools_switch_dhcp_policy import register_switch_dhcp_policy_tools
    from server.tools_alternate_management import register_alternate_management_tools

    # Additional modules for 100% API coverage
    from server.tools_organizations_additional import register_organizations_additional_tools
    from server.tools_networks_additional import register_networks_additional_tools
    from server.tools_devices_additional import register_devices_additional_tools
    from server.tools_wireless_additional import register_wireless_additional_tools
    from server.tools_switch_additional import register_switch_additional_tools
    from server.tools_appliance_additional import register_appliance_additional_tools
    from server.tools_sm_additional import register_sm_additional_tools
    from server.tools_camera_additional import register_camera_additional_tools
    from server.tools_sensor_additional import register_sensor_additional_tools
    from server.tools_cellularGateway_additional import register_cellularGateway_additional_tools
    from server.tools_insight_additional import register_insight_additional_tools
    from server.tools_licensing_additional import register_licensing_additional_tools
    from server.tools_administered_additional import register_administered_additional_tools
    from server.tools_batch_additional import register_batch_additional_tools

    # Register resources and official API tools only
    register_resources(app, meraki)
    register_organization_tools(app, meraki)
    register_network_tools(app, meraki)
    register_device_tools(app, meraki)
    register_wireless_tools(app, meraki)
    register_switch_tools(app, meraki)
    register_appliance_tools(app, meraki)
    register_camera_tools(app, meraki)
    register_sm_tools(app, meraki)
    register_licensing_tools(app, meraki)
    register_sensor_tools(app, meraki)
    register_insight_tools(app, meraki)
    register_cellular_gateway_tools(app, meraki)
    register_administered_tools(app, meraki)
    register_batch_tools(app, meraki)
    register_webhooks_tools(app, meraki)
    register_mqtt_tools(app, meraki)
    register_syslog_tools(app, meraki)
    register_snmp_tools(app, meraki)
    register_saml_tools(app, meraki)
    register_branding_tools(app, meraki)
    register_oauth_tools(app, meraki)
    register_config_template_tools(app, meraki)
    register_group_policies_tools(app, meraki)
    register_floor_plans_tools(app, meraki)
    register_meraki_auth_users_tools(app, meraki)
    register_traffic_analysis_tools(app, meraki)
    register_netflow_tools(app, meraki)
    register_pii_tools(app, meraki)
    register_bluetooth_clients_tools(app, meraki)
    register_org_admins_tools(app, meraki)
    register_login_security_tools(app, meraki)
    register_early_access_tools(app, meraki)
    register_switch_dhcp_policy_tools(app, meraki)
    register_alternate_management_tools(app, meraki)
    
    # Additional modules for 100% coverage
    register_organizations_additional_tools(app, meraki)
    register_networks_additional_tools(app, meraki)
    register_devices_additional_tools(app, meraki)
    register_wireless_additional_tools(app, meraki)
    register_switch_additional_tools(app, meraki)
    register_appliance_additional_tools(app, meraki)
    register_sm_additional_tools(app, meraki)
    register_camera_additional_tools(app, meraki)
    register_sensor_additional_tools(app, meraki)
    register_cellularGateway_additional_tools(app, meraki)
    register_insight_additional_tools(app, meraki)
    register_licensing_additional_tools(app, meraki)
    register_administered_additional_tools(app, meraki)
    register_batch_additional_tools(app, meraki)
    
    _tools_registered = True
    print("[INFO] Official Meraki API tool registration complete")

# Register tools on import
register_all_tools()

# Export the app
__all__ = ['app']